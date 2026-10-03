#!/usr/bin/env python3
"""Validate a Box filing output folder against filing_rules.md and the inputs.

usage: check_filing.py <output_dir> [--input <dir with mailbox, matters.csv, staff.csv>]

Every rule is recomputed from the raw .eml files and the matter facts; nothing in
filing_log.csv is trusted. Matter facts come from <output_dir>/matters_effective.csv
when present (matters.csv as amended by later memos); every difference from the
input matters.csv is printed so it can be reviewed.

Exit status 0 = all checks pass, 1 = at least one failure.
"""
import argparse
import csv
import email
import hashlib
import os
import re
import sys
from collections import Counter, defaultdict
from email import policy
from email.utils import getaddresses, parseaddr, parsedate_to_datetime

FLAG_ORDER = ["hold", "post-closing", "ethical-wall", "potential-conflict",
              "new-matter-request", "misdirected", "phishing", "delivery-failure",
              "restricted", "duplicate-retained", "attorney-action"]
CATS = {"matter", "needs_review", "firm_admin", "non_matter", "duplicate"}
CAT_DIR = {"needs_review": "box/_Needs_Review", "firm_admin": "box/Firm_Admin",
           "non_matter": "box/_Non_Matter", "duplicate": "box/_Duplicates"}
LOG_COLS = ["email_file", "received", "sender", "subject", "category", "primary_matter", "xref_matters",
            "privilege", "flags", "box_path", "attachments_saved"]
FIRM = "@hartwell-osei.test"
ACTION_FLAGS = {"post-closing", "potential-conflict", "new-matter-request", "ethical-wall",
                "delivery-failure", "phishing", "attorney-action", "misdirected"}


class Report:
    def __init__(self):
        self.results = []

    def check(self, name, errors):
        self.results.append((name, errors))

    def show(self):
        bad = 0
        for name, errs in self.results:
            if errs:
                bad += 1
                print(f"FAIL  {name} ({len(errs)})")
                for e in errs[:25]:
                    print(f"        - {e}")
                if len(errs) > 25:
                    print(f"        ... {len(errs) - 25} more")
            else:
                print(f"PASS  {name}")
        print(f"\n{len(self.results) - bad}/{len(self.results)} checks passed")
        return bad == 0


# ---------------------------------------------------------------- helpers (independent of the builder)
def slug(subject):
    s = subject.strip()
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"^\s*(re|fw|fwd)\s*:\s*", "", s, flags=re.I)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40].rstrip("-")
    return s or "no-subject"


def expected_name(msg, date):
    name, addr = parseaddr(msg["From"] or "")
    last = name.split()[-1] if name.strip() else addr.split("@")[0]
    last = re.sub(r"[^a-z0-9]", "", last.lower())
    return f"{date:%Y-%m-%d}_{date:%H%M}_{last}_{slug(msg['Subject'] or '')}.eml"


def load_matters(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            n = r["notes"]
            m = re.search(r"Litigation hold from (\d{4}-\d{2}-\d{2})", n)
            r["hold_start"] = m.group(1) if m else None
            r["walls"] = re.findall(r"ETHICAL WALL: ([A-Za-z .'-]+?) is screened from this matter \(since (\d{4}-\d{2}-\d{2})\)", n)
            r["restricted"] = "RESTRICTED" in n
            r["dir"] = f"box/{'Restricted' if r['restricted'] else 'Clients'}/{r['client_folder']}/{r['matter_folder']}"
            out[r["matter_no"]] = r
    return out


def sha(b):
    return hashlib.sha256(b).hexdigest()


def addrs(msg, field):
    return [a.lower() for _, a in getaddresses([msg[field] or ""]) if a]


def md_table(text, heading):
    """Rows of the first markdown table under '## heading'."""
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if not m:
        return None
    rows = []
    for line in m.group(1).splitlines():
        if line.startswith("|") and not re.match(r"^\|[-| ]+\|$", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:] if rows else []


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output_dir")
    ap.add_argument("--input", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    out, inp = a.output_dir, a.input
    mb = os.path.join(inp, "mailbox") if os.path.isdir(os.path.join(inp, "mailbox")) else inp
    R = Report()

    # inputs
    mails = {}
    for f in sorted(os.listdir(mb)):
        if f.endswith(".eml"):
            raw = open(os.path.join(mb, f), "rb").read()
            msg = email.message_from_bytes(raw, policy=policy.default)
            date = parsedate_to_datetime(msg["Date"])
            atts = [(p.get_filename(), p.get_payload(decode=True)) for p in msg.walk()
                    if not p.is_multipart() and p.get_filename()]
            mails[f] = dict(raw=raw, msg=msg, date=date, day=f"{date:%Y-%m-%d}", atts=atts,
                            msgid=(msg["Message-ID"] or "").strip())
    staff = {r["email"].lower(): r for r in csv.DictReader(open(os.path.join(inp, "staff.csv"), encoding="utf-8"))}
    staff_by_name = {r["name"].lower(): e for e, r in staff.items()}
    base_m = load_matters(os.path.join(inp, "matters.csv"))
    eff_path = os.path.join(out, "matters_effective.csv")
    matters = load_matters(eff_path) if os.path.exists(eff_path) else base_m
    if matters is not base_m:
        diffs = []
        for k in sorted(set(base_m) | set(matters)):
            b, e = base_m.get(k), matters.get(k)
            if b is None or e is None:
                diffs.append(f"{k}: {'added' if b is None else 'removed'}")
                continue
            for c in ["client_no", "client_folder", "matter_folder", "responsible_attorney", "status", "closed_date", "notes"]:
                if b[c] != e[c]:
                    diffs.append(f"{k}.{c}: '{b[c]}' -> '{e[c]}'")
        print("Matter facts: matters_effective.csv" + (" (amended vs matters.csv):" if diffs else " (identical to matters.csv)"))
        for d in diffs:
            print(f"    {d}")
        print()

    box = os.path.join(out, "box")
    all_files = set()
    for d, _, fs in os.walk(box):
        for f in fs:
            all_files.add(os.path.relpath(os.path.join(d, f), out).replace(os.sep, "/"))

    # ---- filing_log.csv structure
    errs = []
    log_path = os.path.join(out, "filing_log.csv")
    if not os.path.exists(log_path):
        R.check("filing_log.csv exists", ["missing"])
        R.show()
        sys.exit(1)
    with open(log_path, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames != LOG_COLS:
            errs.append(f"columns {rd.fieldnames} != {LOG_COLS}")
        log = list(rd)
    files = Counter(r["email_file"] for r in log)
    for f, n in files.items():
        if n > 1:
            errs.append(f"{f} listed {n} times")
    for f in set(mails) - set(files):
        errs.append(f"{f} missing from log")
    for f in set(files) - set(mails):
        errs.append(f"{f} in log but not in mailbox")
    if len(log) != len(mails):
        errs.append(f"{len(log)} rows for {len(mails)} mailbox emails")
    for r in log:
        if r["email_file"] not in mails:
            continue
        m = mails[r["email_file"]]
        if r["received"] != f"{m['date']:%Y-%m-%d %H:%M}":
            errs.append(f"{r['email_file']}: received {r['received']} != Date header {m['date']:%Y-%m-%d %H:%M}")
        if r["subject"] != (m["msg"]["Subject"] or ""):
            errs.append(f"{r['email_file']}: subject mismatch")
        if parseaddr(r["sender"])[1].lower() != parseaddr(m["msg"]["From"])[1].lower():
            errs.append(f"{r['email_file']}: sender mismatch")
        if r["category"] not in CATS:
            errs.append(f"{r['email_file']}: bad category {r['category']}")
    R.check("filing_log.csv: one row per mailbox email, fields match headers", errs)
    log = [r for r in log if r["email_file"] in mails]
    by_file = {r["email_file"]: r for r in log}

    # ---- primary copies
    errs = []
    eml_in_box = {p for p in all_files if p.endswith(".eml")}
    logged_paths = Counter(r["box_path"] for r in log)
    for p, n in logged_paths.items():
        if n > 1:
            errs.append(f"box_path used by {n} rows: {p}")
    for r in log:
        p = r["box_path"]
        if p not in all_files:
            errs.append(f"{r['email_file']}: box_path does not exist: {p}")
        elif open(os.path.join(out, p), "rb").read() != mails[r["email_file"]]["raw"]:
            errs.append(f"{r['email_file']}: file at box_path is not a byte-identical copy")
    for p in eml_in_box - set(logged_paths):
        errs.append(f"unlogged .eml in box: {p}")
    want = Counter(sha(m["raw"]) for m in mails.values())
    have = Counter(sha(open(os.path.join(out, p), "rb").read()) for p in eml_in_box)
    for h, n in want.items():
        if have.get(h, 0) != n:
            errs.append(f"content {h[:10]} expected {n} primary copies in box, found {have.get(h, 0)}")
    R.check("every mailbox email appears exactly once as a primary copy; every box_path exists", errs)

    # ---- naming
    errs = []
    for r in log:
        m = mails[r["email_file"]]
        exp = expected_name(m["msg"], m["date"])
        if "duplicate-retained" in r["flags"].split(";"):
            exp = exp[:-4] + "_dup.eml"
        got = os.path.basename(r["box_path"])
        if got != exp:
            errs.append(f"{r['email_file']}: file name {got} != {exp}")
    R.check("file names follow rule 4", errs)

    # ---- duplicates / hold
    order = sorted(mails, key=lambda f: (mails[f]["date"].replace(tzinfo=None), f))
    first, dup_of = {}, {}
    for f in order:
        mid = mails[f]["msgid"]
        if mid in first:
            dup_of[f] = first[mid]
        else:
            first[mid] = f
    errs = []
    for f in order:
        r = by_file[f]
        fl = r["flags"].split(";") if r["flags"] else []
        if f in dup_of:
            if r["category"] != "duplicate":
                errs.append(f"{f}: same Message-ID as {dup_of[f]} but category {r['category']}")
                continue
            o = by_file[dup_of[f]]
            om = o["primary_matter"]
            hs = matters[om]["hold_start"] if om in matters else None
            if om and hs and mails[f]["day"] >= hs:
                exp_dir = f"{matters[om]['dir']}/Correspondence"
                if r["box_path"] not in all_files:
                    errs.append(f"{f}: hold duplicate not retained (no file at {r['box_path']}); nothing may be deleted under hold")
                if os.path.dirname(r["box_path"]) != exp_dir or not r["box_path"].endswith("_dup.eml"):
                    errs.append(f"{f}: hold duplicate must be retained in {exp_dir} with _dup, got {r['box_path']}")
                if "hold" not in fl or "duplicate-retained" not in fl:
                    errs.append(f"{f}: retained hold duplicate needs flags hold;duplicate-retained (has '{r['flags']}')")
                if r["primary_matter"] != om:
                    errs.append(f"{f}: retained duplicate should list primary_matter {om}")
            else:
                if os.path.dirname(r["box_path"]) != CAT_DIR["duplicate"]:
                    errs.append(f"{f}: duplicate should be in box/_Duplicates, got {r['box_path']}")
                if "duplicate-retained" in fl:
                    errs.append(f"{f}: duplicate-retained but not under a hold")
        elif r["category"] == "duplicate":
            errs.append(f"{f}: category duplicate but its Message-ID is the first occurrence")
    # nothing filed in a held matter may be missing: every email dated on/after a hold start whose
    # copy sits in that matter is present (covered above); also no held-matter file outside the log
    for mno, mr in matters.items():
        if mr["hold_start"]:
            for p in all_files:
                if p.startswith(mr["dir"] + "/Correspondence/") and p.endswith(".eml") and p not in logged_paths:
                    errs.append(f"held matter {mno} has an unlogged file {p}")
    R.check("duplicates (rule 6): hold duplicates retained with _dup, others in _Duplicates", errs)

    # ---- categories, folders, restricted
    errs = []
    restricted_dirs = {m["dir"] for m in matters.values() if m["restricted"]}
    for r in log:
        f, cat, p, mno = r["email_file"], r["category"], r["box_path"], r["primary_matter"]
        if cat == "matter" or (cat == "duplicate" and mno):
            if mno not in matters:
                errs.append(f"{f}: unknown primary_matter '{mno}'")
                continue
            if os.path.dirname(p) != f"{matters[mno]['dir']}/Correspondence":
                errs.append(f"{f}: {p} is not in {matters[mno]['dir']}/Correspondence")
        else:
            if mno or r["xref_matters"]:
                errs.append(f"{f}: {cat} email must not have a matter or xrefs")
            if os.path.dirname(p) != CAT_DIR[cat]:
                errs.append(f"{f}: {cat} email must be in {CAT_DIR[cat]}, got {p}")
    for p in all_files:
        parts = p.split("/")
        if len(parts) >= 4 and parts[1] in ("Clients", "Restricted"):
            d = "/".join(parts[:4])
            mm = [m for m in matters.values() if m["dir"] == d]
            if not mm:
                alt = [m for m in matters.values() if f"{m['client_folder']}/{m['matter_folder']}" == "/".join(parts[2:4])]
                if alt and alt[0]["restricted"]:
                    errs.append(f"restricted matter {alt[0]['matter_no']} content outside box/Restricted: {p}")
                elif alt:
                    errs.append(f"non-restricted matter {alt[0]['matter_no']} content under box/Restricted: {p}")
                else:
                    errs.append(f"file in unknown matter folder: {p}")
        elif len(parts) >= 2 and parts[1] not in ("Clients", "Restricted", "_Needs_Review", "Firm_Admin", "_Non_Matter", "_Duplicates"):
            errs.append(f"file outside the rule 3 folders: {p}")
    R.check("categories map to rule 3 folders; restricted matters only under box/Restricted", errs)

    # ---- stubs
    errs = []
    stubs = {p for p in all_files if p.endswith(".xref.txt")}
    expected_stubs = {}
    for r in log:
        xs = [x for x in r["xref_matters"].split(";") if x]
        for x in xs:
            if x not in matters:
                errs.append(f"{r['email_file']}: unknown xref matter {x}")
                continue
            pm = r["primary_matter"]
            if pm in matters and matters[x]["client_no"] != matters[pm]["client_no"]:
                errs.append(f"{r['email_file']}: xref {x} crosses clients (primary {pm})")
            if x == pm:
                errs.append(f"{r['email_file']}: xref equals primary matter")
            sp = f"{matters[x]['dir']}/Correspondence/{os.path.basename(r['box_path'])}.xref.txt"
            expected_stubs[sp] = r
    for sp, r in expected_stubs.items():
        if sp not in stubs:
            errs.append(f"{r['email_file']}: missing stub {sp}")
    for sp in sorted(stubs):
        if sp not in expected_stubs:
            errs.append(f"stub not backed by the log's xref_matters: {sp}")
        content = open(os.path.join(out, sp), encoding="utf-8").read()
        lines = content.splitlines()
        if len(lines) != 1 or not lines[0].startswith("Filed at: "):
            errs.append(f"stub must contain exactly one 'Filed at: <path>' line: {sp} -> {content!r}")
            continue
        target = lines[0][len("Filed at: "):]
        if target not in all_files:
            errs.append(f"stub target does not exist: {sp} -> {target}")
        if os.path.basename(sp) != os.path.basename(target) + ".xref.txt":
            errs.append(f"stub name does not match its target: {sp} -> {target}")
        sc = sp.split("/")[2]
        tc = target.split("/")[2] if target.count("/") >= 2 else None
        if sc != tc:
            errs.append(f"stub crosses clients: {sp} -> {target}")
        if sp in expected_stubs and target != expected_stubs[sp]["box_path"]:
            errs.append(f"stub points to {target}, primary copy is {expected_stubs[sp]['box_path']}")
    R.check("cross-reference stubs: one 'Filed at:' line, target exists, same client only", errs)

    # ---- attachments
    errs = []
    expected_docs = set()
    for r in log:
        m = mails[r["email_file"]]
        saved = [s for s in r["attachments_saved"].split(";") if s]
        if r["category"] == "matter" and r["primary_matter"] in matters:
            exp = [f"{m['day']}_{fn}" for fn, _ in m["atts"]]
            if sorted(saved) != sorted(exp):
                errs.append(f"{r['email_file']}: attachments_saved {saved} != expected {exp}")
            for fn, data in m["atts"]:
                p = f"{matters[r['primary_matter']]['dir']}/Documents/{m['day']}_{fn}"
                expected_docs.add(p)
                if p not in all_files:
                    errs.append(f"{r['email_file']}: attachment not extracted: {p}")
                elif open(os.path.join(out, p), "rb").read() != data:
                    errs.append(f"{r['email_file']}: extracted attachment differs from the original: {p}")
        elif saved:
            errs.append(f"{r['email_file']}: {r['category']} email must not have extracted attachments")
    for p in all_files:
        if "/Documents/" in p and p not in expected_docs:
            errs.append(f"unexpected or misnamed file in Documents/: {p}")
    R.check("attachments of matter emails extracted to Documents/ as <date>_<original name>", errs)

    # ---- flags (derived ones recomputed)
    errs = []
    incidents_exp = set()
    for r in log:
        f, m = r["email_file"], mails[r["email_file"]]
        fl = r["flags"].split(";") if r["flags"] else []
        bad = [x for x in fl if x not in FLAG_ORDER]
        if bad:
            errs.append(f"{f}: unknown flags {bad}")
            continue
        if fl != sorted(fl, key=FLAG_ORDER.index) or len(set(fl)) != len(fl):
            errs.append(f"{f}: flags not in rule 5 order: {r['flags']}")
        mno = r["primary_matter"]
        mr = matters.get(mno)
        exp_hold = bool(mr and mr["hold_start"] and m["day"] >= mr["hold_start"])
        if exp_hold != ("hold" in fl):
            errs.append(f"{f}: hold flag should be {exp_hold}")
        exp_pc = bool(mr and r["category"] == "matter" and mr["status"] == "closed" and mr["closed_date"] and m["day"] > mr["closed_date"])
        if exp_pc != ("post-closing" in fl):
            errs.append(f"{f}: post-closing flag should be {exp_pc}")
        exp_r = bool(mr and mr["restricted"])
        if exp_r != ("restricted" in fl):
            errs.append(f"{f}: restricted flag should be {exp_r}")
        about = ([mno] if mno else []) + [x for x in r["xref_matters"].split(";") if x]
        wall = False
        for am in about:
            for person, since in matters.get(am, {"walls": []})["walls"]:
                pa = staff_by_name.get(person.lower())
                if m["day"] < since:
                    continue
                for role, field in (("sender", "From"), ("to", "To"), ("cc", "Cc")):
                    if pa in addrs(m["msg"], field):
                        wall = True
                        incidents_exp.add((f, person, role, am))
        if wall != ("ethical-wall" in fl):
            errs.append(f"{f}: ethical-wall flag should be {wall}")
        if "delivery-failure" in fl and r["category"] != "matter":
            errs.append(f"{f}: delivery-failure must be filed in the original email's matter")
        if "phishing" in fl and r["category"] != "non_matter":
            errs.append(f"{f}: phishing belongs in non_matter")
        if "misdirected" in fl and r["category"] != "needs_review":
            errs.append(f"{f}: misdirected belongs in needs_review")
        if "attorney-action" in fl and "hold" not in fl:
            errs.append(f"{f}: attorney-action used outside a hold")
    R.check("flags: valid, ordered, and hold/post-closing/restricted/ethical-wall match the facts", errs)

    # ---- privilege
    errs = []
    for r in log:
        f, m, pv = r["email_file"], mails[r["email_file"]], r["privilege"]
        in_matter = r["category"] == "matter" or (r["category"] == "duplicate" and r["primary_matter"])
        if not in_matter:
            if pv != "n/a":
                errs.append(f"{f}: {r['category']} email must have privilege n/a")
            continue
        if pv not in ("AC", "WP", "none"):
            errs.append(f"{f}: privilege must be AC/WP/none, got {pv}")
            continue
        parts = set(addrs(m["msg"], "From") + addrs(m["msg"], "To") + addrs(m["msg"], "Cc"))
        firm = {p for p in parts if p.endswith(FIRM) and not p.split("@")[1].startswith("mx.")}
        allfirm = parts == firm
        sender = addrs(m["msg"], "From")[0]
        automated = any(t in sender for t in ("mailer-daemon", "noreply", "no-reply"))
        if allfirm and pv != "WP":
            errs.append(f"{f}: firm-staff-only email must be WP, got {pv}")
        if not allfirm and pv == "WP":
            errs.append(f"{f}: WP but non-firm participants present")
        if automated and pv != "none":
            errs.append(f"{f}: automated sender must be privilege none")
        if pv == "AC" and not firm:
            errs.append(f"{f}: AC but no firm participant")
    R.check("privilege values follow rule 7", errs)

    # ---- wall incidents file
    errs = []
    wp = os.path.join(out, "wall_incidents.csv")
    if not os.path.exists(wp):
        errs.append("wall_incidents.csv missing")
    else:
        rows = list(csv.DictReader(open(wp, newline="", encoding="utf-8")))
        got = set()
        for w in rows:
            got.add((w["email_file"], w["screened_person"], w["role"], w["matter"]))
            if not w.get("action", "").strip():
                errs.append(f"{w['email_file']}: incident without an action")
            if w["email_file"] in mails and w["received"] != f"{mails[w['email_file']]['date']:%Y-%m-%d %H:%M}":
                errs.append(f"{w['email_file']}: incident received date mismatch")
        for x in incidents_exp - got:
            errs.append(f"missing incident {x}")
        for x in got - incidents_exp:
            errs.append(f"unexpected incident {x}")
        if len(rows) != len(got):
            errs.append("duplicate incident rows")
    R.check("wall_incidents.csv matches every screened-person contact (rule 8)", errs)

    # ---- privilege log
    errs = []
    pp = os.path.join(out, "privilege_log.csv")
    if not os.path.exists(pp):
        errs.append("privilege_log.csv missing")
    else:
        rows = list(csv.DictReader(open(pp, newline="", encoding="utf-8")))
        exp = Counter((mails[r["email_file"]]["day"], r["subject"], r["privilege"]) for r in log
                      if r["primary_matter"] == "1001-001" and r["privilege"] in ("AC", "WP"))
        got = Counter((w["date"], w["subject"], w["privilege"]) for w in rows)
        for x in exp - got:
            errs.append(f"missing privilege-log entry {x}")
        for x in got - exp:
            errs.append(f"unexpected privilege-log entry {x}")
        for w in rows:
            if not w["description"].strip():
                errs.append(f"empty description for {w['subject']}")
    R.check("privilege_log.csv lists every AC/WP email filed in 1001-001", errs)

    # ---- markdown reports
    errs = []
    def read(n):
        p = os.path.join(out, n)
        return open(p, encoding="utf-8").read() if os.path.exists(p) else None
    tri, nr, aa = read("triage_notes.md"), read("needs_review.md"), read("attorney_actions.md")
    for n, t in (("triage_notes.md", tri), ("needs_review.md", nr), ("attorney_actions.md", aa)):
        if t is None:
            errs.append(f"{n} missing")
    if tri:
        for f in mails:
            if f"## " not in tri or not re.search(rf"^## \d+\. {re.escape(f)}\s*$", tri, flags=re.M):
                errs.append(f"triage_notes.md has no entry for {f}")
        if "MISSING DESCRIPTION" in tri:
            errs.append("triage_notes.md has an attachment without a description")
    if nr:
        heads = set(re.findall(r"^## (AAMk[0-9a-f]+\.eml)", nr, flags=re.M))
        exp = {r["email_file"] for r in log if r["category"] == "needs_review"}
        for f in exp - heads:
            errs.append(f"needs_review.md missing {f}")
        for f in heads - exp:
            errs.append(f"needs_review.md lists {f}, which is not needs_review in the log")
    if aa:
        for r in log:
            fl = set(r["flags"].split(";")) & ACTION_FLAGS
            if fl and r["email_file"] not in aa:
                errs.append(f"attorney_actions.md does not mention {r['email_file']} (flags {sorted(fl)})")
        if incidents_exp and "ethics partner" not in aa.lower():
            errs.append("attorney_actions.md has no ethics-partner section despite wall incidents")
    R.check("triage_notes / needs_review / attorney_actions cover the right emails", errs)

    # ---- summary counts
    errs = []
    sm = read("filing_summary.md")
    if sm is None:
        errs.append("filing_summary.md missing")
    else:
        cats = Counter(r["category"] for r in log)
        t = md_table(sm, "By category") or []
        got = {row[0]: row[1] for row in t if not row[0].startswith("**")}
        for c in CATS:
            if str(cats.get(c, 0)) != got.get(c, "0"):
                errs.append(f"category {c}: summary {got.get(c)} vs log {cats.get(c, 0)}")
        bym = Counter(r["primary_matter"] for r in log if r["primary_matter"])
        t = md_table(sm, "By matter") or []
        got = {row[0]: row[2] for row in t if not row[0].startswith("**")}
        for k in set(bym) | set(got):
            if str(bym.get(k, 0)) != got.get(k, "0"):
                errs.append(f"matter {k}: summary {got.get(k)} vs log {bym.get(k, 0)}")
        xs = Counter(x for r in log for x in r["xref_matters"].split(";") if x)
        gotx = {row[0]: row[3] for row in t if not row[0].startswith("**") and len(row) > 3}
        for k in set(xs) | set(gotx):
            if str(xs.get(k, 0)) != gotx.get(k, "0"):
                errs.append(f"xref stubs {k}: summary {gotx.get(k)} vs log {xs.get(k, 0)}")
        bya = Counter(matters[r["primary_matter"]]["responsible_attorney"] for r in log if r["primary_matter"] in matters)
        t = md_table(sm, "By responsible attorney") or []
        got = {row[0]: row[1] for row in t if not row[0].startswith("**")}
        for k in set(bya) | set(got):
            if str(bya.get(k, 0)) != got.get(k, "0"):
                errs.append(f"attorney {k}: summary {got.get(k)} vs log {bya.get(k, 0)}")
        m = re.search(r"Files in box/: (\d+)", sm)
        if not m or int(m.group(1)) != len(all_files):
            errs.append(f"Files in box/: summary {m.group(1) if m else None} vs actual {len(all_files)}")
        m = re.search(r"Emails in mailbox: (\d+)", sm)
        if not m or int(m.group(1)) != len(mails):
            errs.append("Emails in mailbox count wrong")
        m = re.search(r"Wall incidents: (\d+)", sm)
        if m and int(m.group(1)) != len(incidents_exp):
            errs.append(f"Wall incidents: summary {m.group(1)} vs {len(incidents_exp)}")
    R.check("filing_summary.md counts match the log and box/", errs)

    ok = R.show()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
