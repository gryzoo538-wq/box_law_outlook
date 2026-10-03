# Verification log

Date: 2026-10-03. Folders verified: `output/phase1/` (first pass) and `output/final/` (after memos 01-04).
Everything is reproducible with `python3 tools/make_reports.py` followed by `python3 tools/check_filing.py output/phase1` and `python3 tools/check_filing.py output/final`.

Input layout note: the 64 .eml files sit at the repository root, not in a `mailbox/` folder, and the memos are `memo_01.md` to `memo_04.md` at the root, not in `memos/`. The tools use `mailbox/` when it exists and the root otherwise. The memos were not opened until Part 1 and Part 2 were finished and committed (commit ec2abe7, "Phase 1 filing pass").

## 1. Scanned attachments re-opened as images

All 15 image-only PDFs were re-rendered from the copies **extracted into `output/final/box/`**, not the originals, so the check also confirms the extracted files. Each was viewed again and compared with the matter whose Documents/ folder holds it.

| extracted file | what the image shows | folder / matter | result |
|---|---|---|---|
| 2026-08-04_scan_0812.pdf (rotated 90°) | Appraisal report, 88 Alder Street, Estate of Ricardo Delgado | 1002-001 Estate | confirmed |
| 2026-08-05_landlord_letter.pdf (upside down) | Harborview Properties, Dock 7 lease renewal counter, tenant Northpoint | 1003-002 Dock 7 | confirmed |
| 2026-08-06_ledger.pdf | Fenwick Lane HOA owner ledger, unit 22 (K. Albright), $1,860 | 1006-001 Collections | confirmed |
| 2026-08-06_sigpage.pdf | Blue Heron Marina LLC, Slip C lease signature page | 1007-001 Slip C | confirmed |
| 2026-08-07_hoa_letter.pdf | Fenwick Lane HOA to Maria Delgado, 14 Fenwick Lane, $750 transfer fee, June 2026 conveyance | 1002-002 Purchase (post-closing, potential-conflict) | confirmed |
| 2026-08-11_personnel_excerpt.pdf | Northpoint personnel file, employee Jessica Tran | 1003-001 Tran | confirmed |
| 2026-08-18_coi.pdf (rotated 90°) | Certificate of liability insurance, holder Blue Heron Marina LLC, re Slip C lease | 1007-001 Slip C | confirmed |
| 2026-08-21_parenting_plan.pdf | Proposed parenting plan, In re the Marriage of Ostrander, by Respondent | 1005-001 Divorce | confirmed |
| 2026-08-27_scan0047.pdf | Letters testamentary, Estate of Ricardo Delgado, executor Maria Delgado | 1002-001 Estate | confirmed |
| 2026-08-27_scan0103.pdf (rotated 90°) | Lease amendment no. 3, Dock 7, Harborview / Northpoint, executed | 1003-002 Dock 7 | confirmed |
| 2026-08-28_IMG_2211.pdf | Specimen of use, mark SUNHARVEST, packaging label | 1001-002 SunHarvest | confirmed |
| 2026-08-28_doc_0828.pdf (upside down) | CONFIDENTIAL, Calloway risk assessment, July access incident | 1004-001 Privacy (Restricted) | confirmed |
| 2026-08-31_scan_lien.pdf | Notice of mechanic's lien, Rivera & Sons Roofing, 210 Mill Street | 1008-001 Rivera | confirmed |
| 2026-09-01_statement_jul.pdf | First Harbor Bank statement, Paul Ostrander, July 2026 | 1005-001 Divorce | confirmed |
| 2026-09-02_receipt.pdf | Blue Heron Marina, Slip C first month's rent receipt 0091 | 1007-001 Slip C | confirmed |

Observation: the brief said one scan is rotated. The images show five pages printed sideways or upside down (scan_0812, coi and scan0103 at 90°; landlord_letter and doc_0828 at 180°), although the PDF rotation flag is 0 on all of them. hoa_letter and statement_jul are only slightly skewed. All were readable, and the triage notes record each orientation.

## 2. Emails re-read against the rules

Re-read: every email that is flagged or was ever in needs_review, and every email that mentions Heron, Fenwick, Kestrel, Tran, Anika Brandt or Tom Weller (43 emails). Conclusions:

- **Heron (name overlap).** 2fcb008853, 1bc42b7170 and 32a123f501 are Calloway's Project Heron (Calloway sender or recipient; the attachments name Riverside Imaging), so 1004-002. 3b84e55160 is primary in Restricted 1004-001 with a same-client stub in 1004-002. 7218187993, 15a9964aef and 9012b2a414 come from blueheronmarina.test, and their scans show Slip C, so 1007-001. 1b66809a11 (fuel dock) was needs_review in phase 1 and 1007-002 after memo 02. 090f3ebdd3 (brother's slip contract at Blue Heron Marina) stays in 1005-001 with potential-conflict and new-matter-request. Nothing is filed by keyword.
- **Fenwick.** 8917362f25 is HOA collections for unit 22, so plain 1006-001. e3cf44dd3f is Delgado's closed purchase: post-closing (2026-08-07 > closed 2026-06-30) and potential-conflict (the HOA is a current client). 833acb6266 is the HOA asking for a demand letter against Delgado: 1006-001 with potential-conflict. No stub or copy crosses between clients 1002 and 1006.
- **Kestrel / hold.** Every 1001-001 email dated 2026-08-10 or later carries hold (10 in total, including the retained duplicate). dd73cf256d, c7ec99108d and 980ab8ab67 are pre-hold, so they have no hold flag, and the pre-hold duplicate a2b1852f27 is correctly in _Duplicates. ecc20ef164 (purge request) has hold;attorney-action. 0de90794df ("photos") is the SunHarvest specimen, not Kestrel, so it has no hold. c707b37e14 (Kestrel wants to hire the firm) was needs_review + potential-conflict in phase 1 and firm_admin/Declined_Intake after memo 02.
- **Tran / walls.** Anika Brandt incidents: cd2f45e678 (sender), a69d95847e (cc) and a775139237 (cc, through the 1003-001 cross-reference). Non-incidents: 5645100358 (Dock 7 only), 9011fa2ac0 (billing, no matter) and 9f28518867 (Brandt not on it). Tom Weller (memo 03, from 2026-08-15): one incident, 04f542441d (cc, 2026-08-26). His cc on cd2f45e678 (2026-08-05) is before the effective date, and his other emails (65fb710734, bda7677796, 017ff12229) are not about 1003-001.
- **Other flags.** 993deffa38: phishing (hartwe11 look-alike domain). eefee5a5b2: delivery failure, filed in the bounced email's matter 1005-001. 4ba3ea284d: misdirected (no Martinez matter), still needs_review in final.

**Result:** no decision needed changing.

## 3. Cross-file consistency (each folder)

A separate script parsed triage_notes.md (decision and Filed-at lines), needs_review.md (flags and paths), attorney_actions.md (category, matter and flags quoted in each item), wall_incidents.csv and the summary totals, and compared them with filing_log.csv:

- `output/phase1`: 0 inconsistencies; 64 triage entries; 26 attorney-action items.
- `output/final`: 0 inconsistencies; 64 triage entries; 24 attorney-action items.

`check_filing.py` also compares box/ with the log in both directions: every logged file exists, every .eml in box/ is logged and byte-identical to its mailbox original, every stub is backed by xref_matters, nothing extra or misnamed sits in Documents/, and "Files in box/" in the summary matches the real count (91 in both folders). Other checks:

- `output/phase1` is byte-identical to the stage-0 rebuild (`diff -r` clean).
- `output/final` contains no remaining reference to "1001 Brightwater Foods" (grep).
- The emails changed per memo match the stage-by-stage rebuilds (2 / 2 / 1 / 17).

## 4. Mistakes found and fixed

| # | found by | mistake | fix | rebuilt / re-checked |
|---|---|---|---|---|
| 1 | review of privilege_log.csv | The description for "Two things" (2026-08-10) disclosed the second topic ("an unrelated trademark timing question"), which says too much. | Reworded to "...document collection, with a question for counsel on a separate matter of the same client." | phase1 and final rebuilt; checker passes |
| 2 | deliberate-break testing | Deleting the retained hold duplicate was caught only as a generic missing box_path. | Checker now reports "hold duplicate not retained ... nothing may be deleted under hold". | extra break test confirmed |
| 3 | checker on the memo 02 stage | AAMkc707b37e14 kept new-matter-request (memo 02 replaces only potential-conflict), but no attorney action referred to it, so the checker failed. | Added a close-out item for the ethics partner (keep the decline letter; no contact about 1001-001). | stages 2-4 and final pass 13/13 |
| 4 | reading memo diffs | The diff tool printed "no change" twice for wall incidents. | Fixed. | memo replies regenerated |
| 5 | reading changes_report.md | The memo 03 heading was lower-cased ("tom weller wall"). | Fixed capitalisation. | changes_report regenerated |
| 6 | reading changes_report.md | The count changes did not show per-attorney counts. | Added (Ravi Iyer 9→11 via memo 01; Jonah Hartwell 12→13 via memo 02). | regenerated |

No unresolved mistakes remain.

## 5. Judgment calls the firm may want to revisit (not errors)

- **Privilege log scope:** it lists every AC/WP email filed in 1001-001 (7), including dd73cf256d from 2026-08-03, before the hold start. Restricting it to emails dated on or after the hold would give 6.
- **Byte-identical duplicates:** for each pair, the copy whose mailbox file name sorts first is treated as the original. The pairs are AAMk980ab8ab67/AAMka2b1852f27 and AAMk32d7a94ded/AAMk9770c6a5b8.
- **Retained hold duplicate:** category duplicate, privilege recorded as "none" (as its original) because it sits in the matter folder.
- **090f3ebdd3:** the brother's slip-contract request is flagged potential-conflict because his counterparty would be current client Blue Heron Marina.
- **Kestrel after memo 02:** flags are `declined-intake;new-matter-request`, with declined-intake in potential-conflict's slot in the flag order.

## 6. Final checker output: output/phase1

```
Matter facts: matters_effective.csv (identical to matters.csv)

PASS  filing_log.csv: one row per mailbox email, fields match headers
PASS  every mailbox email appears exactly once as a primary copy; every box_path exists
PASS  file names follow rule 4
PASS  duplicates (rule 6): hold duplicates retained with _dup, others in _Duplicates
PASS  categories map to rule 3 folders; restricted matters only under box/Restricted
PASS  cross-reference stubs: one 'Filed at:' line, target exists, same client only
PASS  attachments of matter emails extracted to Documents/ as <date>_<original name>
PASS  flags: valid, ordered, and hold/post-closing/restricted/ethical-wall match the facts
PASS  privilege values follow rule 7
PASS  wall_incidents.csv matches every screened-person contact (rule 8)
PASS  privilege_log.csv lists every AC/WP email filed in 1001-001
PASS  triage_notes / needs_review / attorney_actions cover the right emails
PASS  filing_summary.md counts match the log and box/

13/13 checks passed
```

## 7. Final checker output: output/final

```
Matter facts: matters_effective.csv (amended vs matters.csv):
    1001-001.client_folder: '1001 Brightwater Foods' -> '1001 Brightwater Brands'
    1001-002.client_folder: '1001 Brightwater Foods' -> '1001 Brightwater Brands'
    1001-003.client_folder: '1001 Brightwater Foods' -> '1001 Brightwater Brands'
    1002-003: added
    1003-001.notes: 'ETHICAL WALL: Anika Brandt is screened from this matter (since 2026-07-01). Adverse: Jessica Tran (counsel: Cole Labor Law).' -> 'ETHICAL WALL: Anika Brandt is screened from this matter (since 2026-07-01). Adverse: Jessica Tran (counsel: Cole Labor Law). ETHICAL WALL: Tom Weller is screened from this matter (since 2026-08-15).'
    1007-002: added

PASS  filing_log.csv: one row per mailbox email, fields match headers
PASS  every mailbox email appears exactly once as a primary copy; every box_path exists
PASS  file names follow rule 4
PASS  duplicates (rule 6): hold duplicates retained with _dup, others in _Duplicates
PASS  categories map to rule 3 folders; restricted matters only under box/Restricted
PASS  cross-reference stubs: one 'Filed at:' line, target exists, same client only
PASS  attachments of matter emails extracted to Documents/ as <date>_<original name>
PASS  flags: valid, ordered, and hold/post-closing/restricted/ethical-wall match the facts
PASS  privilege values follow rule 7
PASS  wall_incidents.csv matches every screened-person contact (rule 8)
PASS  privilege_log.csv lists every AC/WP email filed in 1001-001
PASS  triage_notes / needs_review / attorney_actions cover the right emails
PASS  filing_summary.md counts match the log and box/

13/13 checks passed
```

## 8. Deliberate-break test

`output/phase1/` was copied to a scratch folder and broken three ways:

1. **Moved a file:** `2026-08-26_0945_moreau_tran-mediation-authority.eml` moved from 1003-001 to 1003-002 Correspondence.
2. **Corrupted a stub:** the 1001-002 stub for "Two things" was rewritten to point at a non-existent file (`...two-thing.eml`).
3. **Renamed an attachment:** `2026-08-18_coi.pdf` renamed to `coi.pdf`.

Checker output on the broken copy (exit code 1; all three caught):

```
Matter facts: matters_effective.csv (identical to matters.csv)

PASS  filing_log.csv: one row per mailbox email, fields match headers
FAIL  every mailbox email appears exactly once as a primary copy; every box_path exists (2)
        - AAMk04f542441d.eml: box_path does not exist: box/Clients/1003 Northpoint Logistics/1003-001 Tran Employment Claim/Correspondence/2026-08-26_0945_moreau_tran-mediation-authority.eml
        - unlogged .eml in box: box/Clients/1003 Northpoint Logistics/1003-002 Dock 7 Lease Renewal/Correspondence/2026-08-26_0945_moreau_tran-mediation-authority.eml
PASS  file names follow rule 4
PASS  duplicates (rule 6): hold duplicates retained with _dup, others in _Duplicates
PASS  categories map to rule 3 folders; restricted matters only under box/Restricted
FAIL  cross-reference stubs: one 'Filed at:' line, target exists, same client only (3)
        - stub target does not exist: box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt -> box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-thing.eml
        - stub name does not match its target: box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt -> box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-thing.eml
        - stub points to box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-thing.eml, primary copy is box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml
FAIL  attachments of matter emails extracted to Documents/ as <date>_<original name> (2)
        - AAMk15a9964aef.eml: attachment not extracted: box/Clients/1007 Blue Heron Marina/1007-001 Slip C Lease/Documents/2026-08-18_coi.pdf
        - unexpected or misnamed file in Documents/: box/Clients/1007 Blue Heron Marina/1007-001 Slip C Lease/Documents/coi.pdf
PASS  flags: valid, ordered, and hold/post-closing/restricted/ethical-wall match the facts
PASS  privilege values follow rule 7
PASS  wall_incidents.csv matches every screened-person contact (rule 8)
PASS  privilege_log.csv lists every AC/WP email filed in 1001-001
PASS  triage_notes / needs_review / attorney_actions cover the right emails
PASS  filing_summary.md counts match the log and box/

10/13 checks passed
```

The same three breaks applied to a copy of `output/final/` were also all caught (exit code 1, 10/13 checks passed).

An extra test on another copy also failed as expected: deleting the hold duplicate, moving a Restricted email under Clients, adding a cross-client stub (1006 → 1002) and editing a summary count.
