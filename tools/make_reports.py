#!/usr/bin/env python3
"""Rebuild output/phase1 and output/final, then write the memo replies and changes_report.md.

usage: make_reports.py [input_dir]   (default: the repository root)

Intermediate states after each memo are built in a temporary folder so every memo
reply reports the real differences that memo caused.
"""
import csv
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_filing  # noqa: E402
import diff_filing  # noqa: E402

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
OUT = os.path.join(ROOT, "output")

REPLIES = {
    1: dict(to="Carla Ruiz (office manager)", re="New matter opened - Delgado (memo of 2026-09-28)", body="""\
Thank you for confirming that conflicts cleared and 1002-003 is open. I checked everything waiting in `box/_Needs_Review/`. Two emails belong to the new matter, both from Maria Delgado to Ravi Iyer about her daughter's bakery LLC:

- **AAMk8dff666589.eml** (2026-08-19 13:30, "New question"): the original request to form the LLC.
- **AAMk68f6cdb2f8.eml** (2026-09-21 10:30, "Bakery LLC - name ideas"): the follow-up about the name "Delgado Bakery LLC".

What I changed:

- Created `box/Clients/1002 Delgado Maria/1002-003 Delgado Bakery LLC Formation/Correspondence/` and moved both emails there under their unchanged file names.
- Category changed from needs_review to matter, primary matter 1002-003, privilege AC (client to her attorney about the matter).
- Removed the new-matter-request flag from both, as you asked. Neither email has any other flag.
- Neither email has an attachment, so nothing was added to Documents/.
- needs_review.md: both entries removed (5 → 3 emails). The two "new-matter request" items for Ravi Iyer were removed from attorney_actions.md.
- No effect on wall incidents or the privilege log. The other Delgado emails stay where they were: estate 1002-001, and the closed purchase 1002-002 with its post-closing and potential-conflict flags.
- Counts: matter 51 → 53, needs_review 5 → 3, 1002-003 now holds 2 emails; Ravi Iyer's matter count goes from 9 to 11. Files in box/ stay at 91 (two files moved).

Please note one point for Ravi Iyer: the emails say the LLC is for Maria's daughter, but the matter is opened under client 1002 (Maria Delgado), as your memo specifies. He may want to confirm who the engagement letter names."""),
    2: dict(to="Carla Ruiz (office manager)", re="Intake decisions (memo of 2026-09-29)", body="""\
Both decisions are applied.

**1. Kestrel Packaging: declined**

- **AAMkc707b37e14.eml** (2026-08-13 14:15, "Request for representation", Robert Baines to Jonah Hartwell) moved from `box/_Needs_Review/` to `box/Firm_Admin/Declined_Intake/2026-08-13_1415_baines_request-for-representation.eml`.
- Category changed from needs_review to firm_admin; privilege stays n/a.
- Flags changed from `potential-conflict;new-matter-request` to `declined-intake;new-matter-request`. declined-intake takes potential-conflict's place in the flag order. I kept new-matter-request because your memo replaces only potential-conflict and no matter was opened for this request. Tell me if you want it dropped as well.
- needs_review.md: entry removed. attorney_actions.md: Mira Osei's FYI item was removed, and Jonah Hartwell's conflict-check item was replaced by a close-out note: keep the decline letter with the intake record, and have no contact with Kestrel about the 1001-001 litigation.

**2. Blue Heron Marina: new matter 1007-002**

- **AAMk1b66809a11.eml** (2026-08-25 09:20, "Heron fuel dock incident", Sam Pryce to Jonah Hartwell) is the only email waiting for this matter. It moved to `box/Clients/1007 Blue Heron Marina/1007-002 Fuel Dock Damage Claim/Correspondence/2026-08-25_0920_pryce_heron-fuel-dock-incident.eml`.
- Category changed from needs_review to matter, primary matter 1007-002, privilege AC. I removed the new-matter-request flag because the request now belongs to an existing matter, the same treatment memo 01 gave the bakery emails. It has no attachment.
- The other marina emails (sig page, insurance certificate, rent receipt) stay in 1007-001 Slip C Lease. Paul Ostrander's email asking whether his brother can get help with a slip contract at the marina stays in 1005-001 with its potential-conflict flag; this memo does not resolve it.
- needs_review.md: entry removed. attorney_actions.md: Jonah Hartwell's new-matter item for the fuel dock was removed.

Totals: needs_review 3 → 1 (only the misdirected Carter Whitfield email is left), firm_admin 2 → 3, matter 53 → 54, and 1007-002 now holds 1 email. No change to wall incidents or the privilege log. Files in box/ stay at 91. I also updated the checker (tools/check_filing.py) to accept the Declined_Intake folder and flag."""),
    3: dict(to="Jonah Hartwell (ethics partner)", re="Tran ethical wall - expanded (memo of 2026-09-30)", body="""\
I applied Tom Weller's screen from 1003-001 back to 2026-08-15 and re-checked every email he sent, received or was copied on:

| email | date | matter | result |
|---|---|---|---|
| AAMkcd2f45e678.eml "Tran deposition outline?" (Tom cc) | 2026-08-05 | 1003-001 | before 2026-08-15: no incident for Tom (Anika Brandt's incident stands) |
| AAMk65fb710734.eml "Litigation hold notice - Kestrel dispute" (Tom cc) | 2026-08-10 | 1001-001 | not 1003-001 |
| AAMkbda7677796.eml "Kestrel production - Bates ranges" (Tom sender) | 2026-08-11 | 1001-001 | not 1003-001 |
| AAMk017ff12229.eml "Sato - draft demand letter" (Tom to) | 2026-08-18 | 1008-001 | not 1003-001 |
| **AAMk04f542441d.eml "Tran mediation - authority" (Tom cc)** | **2026-08-26** | **1003-001** | **new incident** |

I also checked the one email cross-referenced to 1003-001 (AAMka775139237.eml, Dock 7 / Tran's counsel). Tom is not on it.

What I changed:

- **AAMk04f542441d.eml** (Hank Moreau to Mira Osei, cc Tom Weller, "Tran mediation - authority"): flags '' → `ethical-wall`. Its path is unchanged: `box/Clients/1003 Northpoint Logistics/1003-001 Tran Employment Claim/Correspondence/2026-08-26_0945_moreau_tran-mediation-authority.eml`.
- wall_incidents.csv: added one row (AAMk04f542441d.eml, 2026-08-26 09:45, Tom Weller, cc, 1003-001), so there are now 4 incidents (3 Anika Brandt, 1 Tom Weller).
- attorney_actions.md: added an item for you (document the incident, confirm Tom keeps no 1003-001 material) and an item for Mira Osei (ask Northpoint to stop copying Tom, and keep him off 1003-001 distribution).
- matters_effective.csv now records both screens on 1003-001. The checker reads it, so it recomputes Tom's incidents independently.
- No change to categories, paths, privilege, the privilege log or needs_review."""),
    4: dict(to="Carla Ruiz (office manager)", re="Client name change (memo of 2026-10-01)", body="""\
The client folder is renamed from `1001 Brightwater Foods` to `1001 Brightwater Brands` (client name Brightwater Brands Inc. in matters_effective.csv). Matter numbers and matter folder names are unchanged.

What moved (25 files, all byte-identical after the move; nothing deleted, which matters for the 1001-001 hold):

- 17 email copies: 13 in 1001-001 Kestrel Supply Dispute (including the hold duplicate `2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml`), 3 in 1001-002 SunHarvest Trademark, and 1 in 1001-003 General Corporate. The box_path of each changes only in the client folder segment; they are listed below.
- 7 extracted attachments in the three Documents/ folders.
- 1 cross-reference stub: `1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt`. I rewrote its line to `Filed at: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml`.

Everything else that pointed to the old path was updated: filing_log.csv box_path for the 17 emails, the triage notes, and the box paths in needs_review / attorney_actions. A search of output/final/ for "1001 Brightwater Foods" returns nothing.

Unchanged: categories, matters, flags (the hold, attorney-action and duplicate-retained flags stay), privilege values, the privilege log (it has no paths; I did not rewrite client or document text inside the original emails and attachments), wall incidents, needs_review, and all counts (files in box/ stay at 91)."""),
}


def build_all():
    with tempfile.TemporaryDirectory() as tmp:
        stages = []
        for n in range(5):
            d = os.path.join(tmp, f"stage{n}")
            build_filing.build(ROOT, d, n)
            stages.append(d)
        for d, name in ((stages[0], "phase1"), (stages[4], "final")):
            dst = os.path.join(OUT, name)
            if name == "final" and os.path.exists(dst):
                keep = {f: open(os.path.join(dst, f), encoding="utf-8").read() for f in os.listdir(dst)
                        if f.startswith("verification") and os.path.isfile(os.path.join(dst, f))}
            else:
                keep = {}
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(d, dst)
            for f, t in keep.items():
                open(os.path.join(dst, f), "w", encoding="utf-8").write(t)
        final = os.path.join(OUT, "final")
        for n in range(1, 5):
            r = REPLIES[n]
            text = [f"# Reply to memo {n:02d}", "", f"To: {r['to']}", "From: Legal operations (Box migration)",
                    f"Re: {r['re']}", "", r["body"], "",
                    "## Exact differences (filing state before vs after this memo)", "",
                    diff_filing.diff(stages[n - 1], stages[n]), ""]
            open(os.path.join(final, f"memo_reply_{n:02d}.md"), "w", encoding="utf-8").write("\n".join(text))
        write_changes_report(stages, final)


def write_changes_report(stages, final):
    logs = [diff_filing.log(s) for s in stages]
    fields = ["category", "primary_matter", "xref_matters", "privilege", "flags", "box_path"]
    memo_name = {1: "memo 01 (new matter 1002-003)", 2: "memo 02 (intake decisions)",
                 3: "memo 03 (Tom Weller wall)", 4: "memo 04 (client rename)"}
    L = ["# Changes report: phase 1 → final", "",
         "Compares `output/phase1/` with `output/final/`. Each change is attributed to the memo that caused it, "
         "found by rebuilding the filing after each memo in turn (memo 01 → 04, date order).", ""]
    changed = []
    for k in logs[0]:
        diffs = [(f, logs[0][k][f], logs[4][k][f]) for f in fields if logs[0][k][f] != logs[4][k][f]]
        if not diffs:
            continue
        memos = []
        for n in range(1, 5):
            if any(logs[n - 1][k][f] != logs[n][k][f] for f in fields):
                memos.append(n)
        changed.append((k, diffs, memos))
    L += [f"## Emails whose category, matter, flags, privilege or path changed ({len(changed)})", "",
          "| email | subject | field | phase 1 | final | memo |", "|---|---|---|---|---|---|"]
    for k, diffs, memos in changed:
        for f, a, b in diffs:
            who = [n for n in memos if logs[n - 1][k][f] != logs[n][k][f]]
            L.append(f"| {k} | {logs[0][k]['subject']} | {f} | `{a or '-'}` | `{b or '-'}` | {', '.join(memo_name[n] for n in who)} |")
    by_memo = {n: sum(1 for _, _, m in changed if n in m) for n in range(1, 5)}
    L += ["", "Emails changed per memo: " + "; ".join(f"{memo_name[n]}: {by_memo[n]}" for n in range(1, 5)) + ".",
          "attachments_saved is unchanged for every email: the file names keep the email date and the original name, "
          "and only their folder moved under memo 04.", ""]
    L += ["## Other files", ""]
    for n in range(1, 5):
        d = diff_filing.diff(stages[n - 1], stages[n])
        section = []
        for title in ("Wall incidents", "Privilege log", "needs_review", "Attorney actions", "Counts"):
            part = d.split(f"### {title}")[1].split("\n### ")[0]
            section.append(f"**{title}{part.splitlines()[0]}**")
            section += [ln for ln in part.splitlines()[1:] if ln.strip()]
            section.append("")
        L += [f"### {memo_name[n][0].upper() + memo_name[n][1:]}", ""] + section
    # overall
    a, b = diff_filing.summary_counts(stages[0]), diff_filing.summary_counts(stages[4])
    L += ["## Net count changes (phase 1 → final)", "", "| measure | phase 1 | final |", "|---|---|---|"]
    for c in ["matter", "needs_review", "firm_admin", "non_matter", "duplicate"]:
        L.append(f"| category {c} | {a['category'][c]} | {b['category'][c]} |")
    for m in sorted(set(a["matter"]) | set(b["matter"])):
        if a["matter"][m] != b["matter"][m]:
            L.append(f"| matter {m} | {a['matter'][m]} | {b['matter'][m]} |")
    wa = sum(1 for _ in csv.DictReader(open(os.path.join(stages[0], "wall_incidents.csv"))))
    wb = sum(1 for _ in csv.DictReader(open(os.path.join(stages[4], "wall_incidents.csv"))))
    pa = sum(1 for _ in csv.DictReader(open(os.path.join(stages[0], "privilege_log.csv"))))
    pb = sum(1 for _ in csv.DictReader(open(os.path.join(stages[4], "privilege_log.csv"))))
    L += [f"| wall incidents | {wa} | {wb} |", f"| privilege log entries | {pa} | {pb} |",
          f"| needs_review emails | {len(diff_filing.needs_review(stages[0]))} | {len(diff_filing.needs_review(stages[4]))} |",
          f"| attorney-action items (person/email) | {len(diff_filing.actions(stages[0]))} | {len(diff_filing.actions(stages[4]))} |",
          f"| files in box/ | {a['files']} | {b['files']} |", ""]
    open(os.path.join(final, "changes_report.md"), "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    build_all()
    print("rebuilt output/phase1 and output/final; wrote memo_reply_01-04.md and changes_report.md")
