#!/usr/bin/env python3
"""Compare two filing output folders (e.g. phase1 vs final) and print a markdown diff.

usage: diff_filing.py <old_dir> <new_dir>
"""
import csv
import os
import re
import sys
from collections import Counter

FIELDS = ["category", "primary_matter", "xref_matters", "privilege", "flags", "box_path", "attachments_saved"]


def log(d):
    return {r["email_file"]: r for r in csv.DictReader(open(os.path.join(d, "filing_log.csv"), newline="", encoding="utf-8"))}


def rows(d, name, key):
    return {key(r) for r in csv.DictReader(open(os.path.join(d, name), newline="", encoding="utf-8"))}


def actions(d):
    text = open(os.path.join(d, "attorney_actions.md"), encoding="utf-8").read()
    out, who = set(), None
    for line in text.splitlines():
        m = re.match(r"^## (.+?) \(\d+\)$", line)
        if m:
            who = m.group(1)
        m = re.match(r"^- \*\*(AAMk[0-9a-f]+\.eml)\*\*", line)
        if m and who:
            out.add((who, m.group(1)))
    return out


def needs_review(d):
    return set(re.findall(r"^## (AAMk[0-9a-f]+\.eml)", open(os.path.join(d, "needs_review.md"), encoding="utf-8").read(), flags=re.M))


def box_files(d):
    out = set()
    for root, _, fs in os.walk(os.path.join(d, "box")):
        for f in fs:
            out.add(os.path.relpath(os.path.join(root, f), d))
    return out


def summary_counts(d):
    L = log(d)
    resp = {r["matter_no"]: r["responsible_attorney"]
            for r in csv.DictReader(open(os.path.join(d, "matters_effective.csv"), newline="", encoding="utf-8"))}
    return dict(category=Counter(r["category"] for r in L.values()),
                matter=Counter(r["primary_matter"] for r in L.values() if r["primary_matter"]),
                attorney=Counter(resp[r["primary_matter"]] for r in L.values() if r["primary_matter"]),
                files=len(box_files(d)))


def diff(old, new):
    A, B = log(old), log(new)
    out = []
    changed = []
    for k in A:
        ch = [(f, A[k][f], B[k][f]) for f in FIELDS if A[k][f] != B[k][f]]
        if ch:
            changed.append((k, B[k]["subject"], ch))
    out.append(f"### Emails changed ({len(changed)})\n")
    for k, subj, ch in changed:
        out.append(f"- **{k}** \"{subj}\"")
        for f, a, b in ch:
            if f in ("box_path",):
                out.append(f"  - {f}: `{a}` -> `{b}`")
            else:
                out.append(f"  - {f}: '{a}' -> '{b}'")
    key_w = lambda r: (r["email_file"], r["screened_person"], r["role"], r["matter"])
    wa, wb = rows(old, "wall_incidents.csv", key_w), rows(new, "wall_incidents.csv", key_w)
    out.append(f"\n### Wall incidents ({len(wa)} -> {len(wb)})\n")
    out += [f"- added: {x}" for x in sorted(wb - wa)] + [f"- removed: {x}" for x in sorted(wa - wb)]
    if wa == wb:
        out.append("- no change")
    key_p = lambda r: (r["date"], r["subject"], r["privilege"])
    pa, pb = rows(old, "privilege_log.csv", key_p), rows(new, "privilege_log.csv", key_p)
    out.append(f"\n### Privilege log ({len(pa)} -> {len(pb)})\n")
    out += [f"- added: {x}" for x in sorted(pb - pa)] + [f"- removed: {x}" for x in sorted(pa - pb)]
    if pa == pb:
        out.append("- no change")
    na, nb = needs_review(old), needs_review(new)
    out.append(f"\n### needs_review ({len(na)} -> {len(nb)})\n")
    out += [f"- added: {x}" for x in sorted(nb - na)] + [f"- removed: {x}" for x in sorted(na - nb)]
    if na == nb:
        out.append("- no change")
    aa, ab = actions(old), actions(new)
    out.append(f"\n### Attorney actions ({len(aa)} -> {len(ab)} person/email items)\n")
    out += [f"- added: {w} / {e}" for w, e in sorted(ab - aa)] + [f"- removed: {w} / {e}" for w, e in sorted(aa - ab)]
    if aa == ab:
        out.append("- no change")
    sa, sb = summary_counts(old), summary_counts(new)
    out.append("\n### Counts\n")
    for c in sorted(set(sa["category"]) | set(sb["category"])):
        if sa["category"][c] != sb["category"][c]:
            out.append(f"- category {c}: {sa['category'][c]} -> {sb['category'][c]}")
    for m in sorted(set(sa["matter"]) | set(sb["matter"])):
        if sa["matter"][m] != sb["matter"][m]:
            out.append(f"- matter {m}: {sa['matter'][m]} -> {sb['matter'][m]}")
    for m in sorted(set(sa["attorney"]) | set(sb["attorney"])):
        if sa["attorney"][m] != sb["attorney"][m]:
            out.append(f"- attorney {m}: {sa['attorney'][m]} -> {sb['attorney'][m]}")
    out.append(f"- files in box/: {sa['files']} -> {sb['files']}")
    fa, fb = box_files(old), box_files(new)
    out.append(f"\n### box/ files ({len(fa - fb)} removed, {len(fb - fa)} added)\n")
    out += [f"- removed `{x}`" for x in sorted(fa - fb)] + [f"- added `{x}`" for x in sorted(fb - fa)]
    return "\n".join(out)


if __name__ == "__main__":
    print(diff(sys.argv[1], sys.argv[2]))
