#!/usr/bin/env python3
"""Build the Box filing (box/ tree + reports) from the mailbox and the decision table.

usage: build_filing.py <input_dir> <output_dir> [--memos N]

  input_dir   folder holding the .eml files (in mailbox/ or at its root), matters.csv,
              staff.csv and filing_rules.md
  --memos N   apply the first N memo updates (tools/memo_updates.py); 0 = phase 1
"""
import argparse
import copy
import csv
import email
import os
import re
import shutil
import sys
from collections import Counter, OrderedDict, defaultdict
from email import policy
from email.utils import getaddresses, parseaddr, parsedate_to_datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decisions  # noqa: E402

FLAG_ORDER = ["hold", "post-closing", "ethical-wall", "declined-intake", "potential-conflict",
              "new-matter-request", "misdirected", "phishing", "delivery-failure",
              "restricted", "duplicate-retained", "attorney-action"]
CAT_DIR = {"needs_review": "_Needs_Review", "firm_admin": "Firm_Admin",
           "non_matter": "_Non_Matter", "duplicate": "_Duplicates"}
FIRM_DOMAIN = "@hartwell-osei.test"


# ---------------------------------------------------------------- inputs
def mailbox_dir(inp):
    mb = os.path.join(inp, "mailbox")
    return mb if os.path.isdir(mb) else inp


def load_matters(path):
    """Read matters.csv and parse hold / wall / restricted facts from the notes."""
    out = OrderedDict()
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            notes = r["notes"]
            r["hold_start"] = None
            m = re.search(r"Litigation hold from (\d{4}-\d{2}-\d{2})", notes)
            if m:
                r["hold_start"] = m.group(1)
            r["walls"] = [(n.strip(), d) for n, d in re.findall(
                r"ETHICAL WALL: ([A-Za-z .'-]+?) is screened from this matter \(since (\d{4}-\d{2}-\d{2})\)", notes)]
            r["restricted"] = "RESTRICTED" in notes
            out[r["matter_no"]] = r
    return out


def load_staff(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {r["email"].lower(): r for r in csv.DictReader(fh)}


def parse_mail(path):
    raw = open(path, "rb").read()
    m = email.message_from_bytes(raw, policy=policy.default)
    d = parsedate_to_datetime(m["Date"])
    atts, body = [], ""
    for part in m.walk():
        if part.is_multipart():
            continue
        fn = part.get_filename()
        if fn:
            atts.append((fn, part.get_payload(decode=True)))
        elif part.get_content_type() == "text/plain":
            body += part.get_content()
    return dict(raw=raw, msg=m, date=d, frm=m["From"] or "", to=m["To"] or "", cc=m["Cc"] or "",
                subject=m["Subject"] or "", msgid=(m["Message-ID"] or "").strip(), atts=atts, body=body)


# ---------------------------------------------------------------- naming
def slug(subject):
    s = subject.strip()
    while True:
        n = re.sub(r"^\s*(re|fw|fwd)\s*:\s*", "", s, flags=re.I)
        if n == s:
            break
        s = n
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    s = s[:40].rstrip("-")
    return s or "no-subject"


def sender_last(frm):
    name, addr = parseaddr(frm)
    if name.strip():
        last = name.split()[-1]
    else:
        last = addr.split("@")[0]
    return re.sub(r"[^a-z0-9]", "", last.lower())


def file_name(e):
    d = e["date"]
    return f"{d:%Y-%m-%d}_{d:%H%M}_{sender_last(e['frm'])}_{slug(e['subject'])}.eml"


def people(e, field):
    return [(n, a.lower()) for n, a in getaddresses([e[field]]) if a]


def fmt_people(e, field):
    return "; ".join(f"{n} <{a}>" if n else a for n, a in getaddresses([e[field]]) if a)


# ---------------------------------------------------------------- build
def matter_dir(matters, mno):
    r = matters[mno]
    top = "Restricted" if r["restricted"] else "Clients"
    return f"box/{top}/{r['client_folder']}/{r['matter_folder']}"


def build(inp, out, n_memos=0):
    mb = mailbox_dir(inp)
    matters = load_matters(os.path.join(inp, "matters.csv"))
    staff = load_staff(os.path.join(inp, "staff.csv"))
    dec = copy.deepcopy(decisions.E)
    memo_log = []
    if n_memos:
        import memo_updates
        for i in range(n_memos):
            memo_log.append(memo_updates.MEMOS[i](dec, matters))

    files = sorted(f for f in os.listdir(mb) if f.endswith(".eml"))
    mails = OrderedDict()
    for f in files:
        mails[f[:-4]] = parse_mail(os.path.join(mb, f))
    missing = set(mails) ^ set(dec)
    if missing:
        sys.exit(f"decision table / mailbox mismatch: {sorted(missing)}")

    order = sorted(mails, key=lambda k: (mails[k]["date"].replace(tzinfo=None), k))

    # duplicates: same Message-ID as an earlier email (ties broken by mailbox file name)
    first_by_id, dup_of = {}, {}
    for k in order:
        mid = mails[k]["msgid"]
        if mid in first_by_id:
            dup_of[k] = first_by_id[mid]
        else:
            first_by_id[mid] = k

    rows = OrderedDict()
    for k in order:
        e, d = mails[k], dec[k]
        cat = d["cat"]
        if k in dup_of and cat != "duplicate":
            sys.exit(f"{k}: duplicate Message-ID but category {cat}")
        if cat == "duplicate" and k not in dup_of:
            sys.exit(f"{k}: category duplicate but Message-ID is unique")
        rows[k] = dict(key=k, e=e, d=d, cat=cat, name=file_name(e),
                       m=d.get("m", ""), x=list(d.get("x", [])), flags=set(d.get("flags", [])),
                       priv=d.get("priv", "n/a"))

    for k, r in rows.items():
        e, date = r["e"], r["e"]["date"]
        day = f"{date:%Y-%m-%d}"
        if r["cat"] == "duplicate":
            orig = rows[dup_of[k]]
            om = orig["m"]
            hs = matters[om]["hold_start"] if om else None
            if om and hs and day >= hs:
                r["m"] = om
                r["flags"] |= {"hold", "duplicate-retained"}
                r["priv"] = orig["priv"]
                r["path"] = f"{matter_dir(matters, om)}/Correspondence/{r['name'][:-4]}_dup.eml"
            else:
                r["m"] = ""
                r["priv"] = "n/a"
                r["path"] = f"box/{CAT_DIR['duplicate']}/{r['name']}"
            r["x"] = []
            continue
        if r["cat"] == "matter":
            mr = matters[r["m"]]
            r["path"] = f"{matter_dir(matters, r['m'])}/Correspondence/{r['name']}"
            if mr["hold_start"] and day >= mr["hold_start"]:
                r["flags"].add("hold")
            if mr["status"] == "closed" and mr["closed_date"] and day > mr["closed_date"]:
                r["flags"].add("post-closing")
            if mr["restricted"]:
                r["flags"].add("restricted")
            for xm in r["x"]:
                if matters[xm]["client_no"] != mr["client_no"]:
                    sys.exit(f"{k}: cross-client xref {r['m']} -> {xm}")
        else:
            sub = f"/{r['d']['subdir']}" if r["d"].get("subdir") else ""
            r["path"] = f"box/{CAT_DIR[r['cat']]}{sub}/{r['name']}"
            r["priv"] = "n/a"

    # ethical walls: screened person on an email about the matter (primary or xref)
    staff_by_name = {v["name"].lower(): k for k, v in staff.items()}
    incidents = []
    for k, r in rows.items():
        e = r["e"]
        day = f"{e['date']:%Y-%m-%d}"
        about = ([r["m"]] if r["m"] else []) + r["x"]
        for mno in about:
            for person, since in matters[mno]["walls"]:
                addr = staff_by_name.get(person.lower())
                if day < since:
                    continue
                for role, field in (("sender", "frm"), ("to", "to"), ("cc", "cc")):
                    if any(a == addr for _, a in people(e, field)):
                        r["flags"].add("ethical-wall")
                        incidents.append(dict(email_file=k + ".eml", received=f"{e['date']:%Y-%m-%d %H:%M}",
                                              screened_person=person, role=role, matter=mno,
                                              action=r["d"].get("wall_action", default_wall_action(person, role, mno, matters, r))))

    for r in rows.values():
        r["flag_str"] = ";".join(f for f in FLAG_ORDER if f in r["flags"])
        unknown = r["flags"] - set(FLAG_ORDER)
        if unknown:
            sys.exit(f"{r['key']}: unknown flags {unknown}")

    # ------------------------------------------------------------ write box/
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    for r in rows.values():
        dst = os.path.join(out, r["path"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(r["e"]["raw"])
        r["saved"] = []
        if r["cat"] == "matter":
            docdir = os.path.join(out, matter_dir(matters, r["m"]), "Documents")
            for fn, data in r["e"]["atts"]:
                aname = f"{r['e']['date']:%Y-%m-%d}_{fn}"
                os.makedirs(docdir, exist_ok=True)
                ap = os.path.join(docdir, aname)
                if os.path.exists(ap):
                    sys.exit(f"attachment name collision: {ap}")
                with open(ap, "wb") as fh:
                    fh.write(data)
                r["saved"].append(f"{matter_dir(matters, r['m'])}/Documents/{aname}")
        r["stubs"] = []
        for xm in r["x"]:
            sp = f"{matter_dir(matters, xm)}/Correspondence/{r['name']}.xref.txt"
            os.makedirs(os.path.dirname(os.path.join(out, sp)), exist_ok=True)
            with open(os.path.join(out, sp), "w", encoding="utf-8") as fh:
                fh.write(f"Filed at: {r['path']}\n")
            r["stubs"].append(sp)

    ctx = dict(rows=rows, matters=matters, staff=staff, incidents=incidents, dup_of=dup_of,
               out=out, memo_log=memo_log, n_memos=n_memos)
    write_filing_log(ctx)
    write_wall_incidents(ctx)
    write_privilege_log(ctx)
    write_needs_review(ctx)
    write_attorney_actions(ctx)
    write_summary(ctx)
    write_triage(ctx)
    write_effective_matters(ctx)
    return ctx


def default_wall_action(person, role, mno, matters, r):
    verb = {"sender": "sent", "to": "received", "cc": "was copied on"}[role]
    via = "" if r["m"] == mno else f" (cross-referenced from primary matter {r['m']})"
    return (f"{person} {verb} an email about {mno}{via} despite the screen. Notify ethics partner Jonah Hartwell; "
            f"remove {person.split()[0]} from the thread and any {mno} distribution; confirm no matter material was used or forwarded; "
            f"document the incident.")


# ---------------------------------------------------------------- reports
def write_filing_log(ctx):
    cols = ["email_file", "received", "sender", "subject", "category", "primary_matter", "xref_matters",
            "privilege", "flags", "box_path", "attachments_saved"]
    with open(os.path.join(ctx["out"], "filing_log.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in ctx["rows"].values():
            e = r["e"]
            name, addr = parseaddr(e["frm"])
            w.writerow([r["key"] + ".eml", f"{e['date']:%Y-%m-%d %H:%M}", f"{name} <{addr}>" if name else addr,
                        e["subject"], r["cat"], r["m"], ";".join(r["x"]), r["priv"], r["flag_str"], r["path"],
                        ";".join(os.path.basename(p) for p in r["saved"])])


def write_wall_incidents(ctx):
    cols = ["email_file", "received", "screened_person", "role", "matter", "action"]
    with open(os.path.join(ctx["out"], "wall_incidents.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for i in ctx["incidents"]:
            w.writerow(i)


def privilege_rows(ctx):
    return [r for r in ctx["rows"].values() if r["m"] == "1001-001" and r["priv"] in ("AC", "WP")]


def write_privilege_log(ctx):
    cols = ["date", "from", "to", "cc", "subject", "privilege", "description"]
    with open(os.path.join(ctx["out"], "privilege_log.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in privilege_rows(ctx):
            e = r["e"]
            desc = r["d"].get("privdesc")
            if not desc:
                sys.exit(f"{r['key']}: privilege-log row without a description")
            w.writerow([f"{e['date']:%Y-%m-%d}", fmt_people(e, "frm"), fmt_people(e, "to"), fmt_people(e, "cc"),
                        e["subject"], r["priv"], desc])


def write_needs_review(ctx):
    rs = [r for r in ctx["rows"].values() if r["cat"] == "needs_review"]
    L = [f"# Needs review ({len(rs)} emails)", "",
         "Emails filed in `box/_Needs_Review/` because they cannot go into a client folder yet. "
         "Attachments of these emails are not extracted.", ""]
    for r in rs:
        reason, decide, who = r["d"]["review"]
        e = r["e"]
        L += [f"## {r['key']}.eml: {e['subject']}", "",
              f"- Received: {e['date']:%Y-%m-%d %H:%M} from {fmt_people(e, 'frm')} to {fmt_people(e, 'to')}",
              f"- Flags: {r['flag_str'] or '(none)'}",
              f"- Filed at: `{r['path']}`",
              f"- Reason: {reason}",
              f"- Decision needed: {decide}",
              f"- Who decides: {who}", ""]
    open(os.path.join(ctx["out"], "needs_review.md"), "w", encoding="utf-8").write("\n".join(L))


ACTION_ORDER = ["Mira Osei", "Leah Park", "Jonah Hartwell", "Ravi Iyer", "Jonah Hartwell (ethics partner)", "IT"]


def write_attorney_actions(ctx):
    by = defaultdict(list)
    for r in ctx["rows"].values():
        for who, what in r["d"].get("actions", []):
            by[who].append((r, what))
    L = ["# Attorney actions", "",
         "Emails needing action, grouped by the person who must act. Each entry gives the email, its filing location and the reason.",
         "Jonah Hartwell appears twice: once as responsible attorney for his own matters and once as ethics partner "
         "(every wall incident and conflict question goes to him in that role).", ""]
    for who in ACTION_ORDER + sorted(set(by) - set(ACTION_ORDER)):
        if who not in by:
            continue
        L += [f"## {who} ({len(by[who])})", ""]
        for r, what in by[who]:
            e = r["e"]
            L.append(f"- **{r['key']}.eml** ({e['date']:%Y-%m-%d %H:%M}, \"{e['subject']}\"; "
                     f"{r['cat']}{' ' + r['m'] if r['m'] else ''}{'; flags ' + r['flag_str'] if r['flag_str'] else ''}): {what}")
        L.append("")
    open(os.path.join(ctx["out"], "attorney_actions.md"), "w", encoding="utf-8").write("\n".join(L))


def count_files(root):
    return sum(len(fs) for _, _, fs in os.walk(root))


def summary_counts(rows, matters):
    cats = Counter(r["cat"] for r in rows)
    by_matter = Counter(r["m"] for r in rows if r["m"])
    by_att = Counter(matters[r["m"]]["responsible_attorney"] for r in rows if r["m"])
    return cats, by_matter, by_att


def write_summary(ctx):
    rows, matters, out = list(ctx["rows"].values()), ctx["matters"], ctx["out"]
    cats, by_matter, by_att = summary_counts(rows, matters)
    nbox = count_files(os.path.join(out, "box"))
    stubs = sum(len(r["stubs"]) for r in rows)
    atts = sum(len(r["saved"]) for r in rows)
    L = ["# Filing summary", "",
         f"Emails in mailbox: {len(rows)}", "",
         "## By category", "", "| category | emails |", "|---|---|"]
    for c in ["matter", "needs_review", "firm_admin", "non_matter", "duplicate"]:
        L.append(f"| {c} | {cats.get(c, 0)} |")
    L += [f"| **total** | {len(rows)} |", "",
          "## By matter", "",
          "Primary copies filed in each matter's Correspondence folder (a hold duplicate kept in the matter counts there). "
          "Cross-reference stubs are not counted.", "",
          "| matter | matter folder | emails | xref stubs |", "|---|---|---|---|"]
    xcount = Counter(x for r in rows for x in r["x"])
    for mno, mr in matters.items():
        if by_matter.get(mno) or xcount.get(mno):
            L.append(f"| {mno} | {mr['matter_folder']} | {by_matter.get(mno, 0)} | {xcount.get(mno, 0)} |")
    L += [f"| **total** | | {sum(by_matter.values())} | {sum(xcount.values())} |", "",
          "## By responsible attorney", "", "Emails filed in matters, by the primary matter's responsible attorney.", "",
          "| attorney | emails |", "|---|---|"]
    for a, n in sorted(by_att.items()):
        L.append(f"| {a} | {n} |")
    L += [f"| **total** | {sum(by_att.values())} |", "",
          "## Files in box/", "",
          f"Files in box/: {nbox}", "",
          f"- email copies (.eml): {len(rows)}",
          f"- cross-reference stubs (.xref.txt): {stubs}",
          f"- extracted attachments (Documents/): {atts}", "",
          "## Flags", "", "| flag | emails |", "|---|---|"]
    fc = Counter(f for r in rows for f in r["flag_str"].split(";") if f)
    for f in FLAG_ORDER:
        if fc.get(f):
            L.append(f"| {f} | {fc[f]} |")
    L += ["", f"Wall incidents: {len(ctx['incidents'])}", f"Privilege log entries: {len(privilege_rows(ctx))}", "",
          "## Open issues", ""]
    for i, r in enumerate([r for r in rows if r["cat"] == "needs_review"], 1):
        L.append(f"{i}. Needs review: {r['key']}.eml ({r['e']['subject']}): {r['d']['review'][0]}")
    n = sum(1 for r in rows if r["cat"] == "needs_review")
    extra = []
    for r in rows:
        fl = r["flag_str"].split(";")
        if "attorney-action" in fl:
            extra.append(f"Hold conflict: {r['key']}.eml asks to delete data under the 1001-001 hold; Mira Osei must refuse in writing.")
        if "potential-conflict" in fl and r["cat"] == "matter":
            extra.append(f"Potential conflict: {r['key']}.eml ({r['e']['subject']}) filed in {r['m']}; ethics partner review pending.")
        if "post-closing" in fl:
            extra.append(f"Post-closing: {r['key']}.eml in closed matter {r['m']}; {matters[r['m']]['responsible_attorney']} to decide whether to reopen.")
        if "delivery-failure" in fl:
            extra.append(f"Delivery failure: {r['key']}.eml; the client may not have received a court deadline.")
        if "phishing" in fl:
            extra.append(f"Phishing: {r['key']}.eml; IT to block and check for clicks.")
    if ctx["incidents"]:
        extra.append(f"Ethical wall: {len(ctx['incidents'])} incident(s) in wall_incidents.csv; ethics partner to document and remediate.")
    for j, t in enumerate(extra, n + 1):
        L.append(f"{j}. {t}")
    L += ctx.get("summary_extra", [])
    L.append("")
    open(os.path.join(out, "filing_summary.md"), "w", encoding="utf-8").write("\n".join(L))


def write_triage(ctx):
    rows = ctx["rows"]
    L = ["# Triage notes", "",
         f"One entry per email ({len(rows)}), in date order. Every attachment was extracted and opened; "
         "image-only scans were rendered and read by eye (no OCR). Mailbox file names are Outlook IDs.", ""]
    for i, r in enumerate(rows.values(), 1):
        e, d = r["e"], r["d"]
        L += [f"## {i}. {r['key']}.eml", "",
              f"- From: {fmt_people(e, 'frm')}",
              f"- To: {fmt_people(e, 'to')}" + (f"; Cc: {fmt_people(e, 'cc')}" if e["cc"] else ""),
              f"- Date: {e['msg']['Date']}",
              f"- Subject: {e['subject']}",
              f"- Message-ID: {e['msgid']}",
              f"- Summary: {d['summary']}"]
        if e["atts"]:
            for fn, _ in e["atts"]:
                L.append(f"- Attachment `{fn}`: {d.get('att', {}).get(fn, 'MISSING DESCRIPTION')}")
        else:
            L.append("- Attachments: none")
        where = r["cat"] + (f" / {r['m']}" if r["m"] else "")
        if r["x"]:
            where += f" (xref {', '.join(r['x'])})"
        L += [f"- Decision: {where}; privilege {r['priv']}; flags {r['flag_str'] or '(none)'}",
              f"- Filed at: `{r['path']}`",
              f"- Why: {d['why']}"]
        if d.get("notes"):
            L.append(f"- Judgment calls: {d['notes']}")
        for note in d.get("memo_notes", []):
            L.append(f"- Memo update: {note}")
        L.append("")
    open(os.path.join(ctx["out"], "triage_notes.md"), "w", encoding="utf-8").write("\n".join(L))


def write_effective_matters(ctx):
    """matters_effective.csv = matters.csv as amended by the memos (identical in phase 1).
    The checker validates against this so memo-changed facts are honoured."""
    rows = list(ctx["matters"].values())
    cols = ["matter_no", "client_no", "client_name", "client_folder", "matter_name", "matter_folder",
            "responsible_attorney", "status", "closed_date", "notes"]
    with open(os.path.join(ctx["out"], "matters_effective.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("output_dir")
    ap.add_argument("--memos", type=int, default=0)
    a = ap.parse_args()
    c = build(a.input_dir, a.output_dir, a.memos)
    print(f"built {a.output_dir}: {len(c['rows'])} emails, {count_files(os.path.join(a.output_dir, 'box'))} files in box/, "
          f"{len(c['incidents'])} wall incidents, {len(privilege_rows(c))} privilege-log rows")
