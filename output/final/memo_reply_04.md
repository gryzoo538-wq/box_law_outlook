# Reply to memo 04

To: Carla Ruiz (office manager)
From: Legal operations (Box migration)
Re: Client name change (memo of 2026-10-01)

The client folder is renamed from `1001 Brightwater Foods` to `1001 Brightwater Brands` (client name Brightwater Brands Inc. in matters_effective.csv). Matter numbers and matter folder names are unchanged.

What moved (25 files, all byte-identical after the move; nothing deleted, which matters for the 1001-001 hold):

- 17 email copies: 13 in 1001-001 Kestrel Supply Dispute (including the hold duplicate `2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml`), 3 in 1001-002 SunHarvest Trademark, and 1 in 1001-003 General Corporate. The box_path of each changes only in the client folder segment; they are listed below.
- 7 extracted attachments in the three Documents/ folders.
- 1 cross-reference stub: `1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt`. I rewrote its line to `Filed at: box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml`.

Everything else that pointed to the old path was updated: filing_log.csv box_path for the 17 emails, the triage notes, and the box paths in needs_review / attorney_actions. A search of output/final/ for "1001 Brightwater Foods" returns nothing.

Unchanged: categories, matters, flags (the hold, attorney-action and duplicate-retained flags stay), privilege values, the privilege log (it has no paths; I did not rewrite client or document text inside the original emails and attachments), wall incidents, needs_review, and all counts (files in box/ stay at 91).

## Exact differences (filing state before vs after this memo)

### Emails changed (17)

- **AAMkdd73cf256d.eml** "Kestrel shipment records"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml`
- **AAMkdb8f4d3e27.eml** "SunHarvest - USPTO office action"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml`
- **AAMkc7ec99108d.eml** "Brightwater v. Kestrel - proposed protective order"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- **AAMk980ab8ab67.eml** "RE: Brightwater v. Kestrel - proposed protective order"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- **AAMk65fb710734.eml** "Litigation hold notice - Kestrel dispute"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml`
- **AAMk73f6fa5db8.eml** "Two things"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml`
- **AAMkbda7677796.eml** "Kestrel production - Bates ranges"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml`
- **AAMk5376c468ae.eml** "Board minutes Q2"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml` -> `box/Clients/1001 Brightwater Brands/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml`
- **AAMk32d7a94ded.eml** "Deposition of D. Whitcomb"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml`
- **AAMk9770c6a5b8.eml** "Deposition of D. Whitcomb"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml`
- **AAMk15d7185dda.eml** "April emails"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml`
- **AAMk41b53302fc.eml** "SunHarvest response filed"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml`
- **AAMk4ad8b9b45c.eml** "Settlement discussion (FRE 408)"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml`
- **AAMk1162f28d1a.eml** "Settlement strategy - privileged"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml`
- **AAMk0de90794df.eml** "photos"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml` -> `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml`
- **AAMk03552454f1.eml** "Kestrel - document production vol. 2"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml`
- **AAMkecc20ef164.eml** "Old April mailbox"
  - box_path: `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml` -> `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml`

### Wall incidents (4 -> 4)

- no change

### Privilege log (7 -> 7)

- no change

### needs_review (1 -> 1)

- no change

### Attorney actions (24 -> 24 person/email items)

- no change

### Counts

- files in box/: 91 -> 91

### box/ files (25 removed, 25 added)

- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-04_proposed_protective_order.pdf`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-10_litigation_hold_notice.pdf`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-08-20_april_emails.pdf`
- removed `box/Clients/1001 Brightwater Foods/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf`
- removed `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt`
- removed `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-002 SunHarvest Trademark/Documents/2026-08-28_IMG_2211.pdf`
- removed `box/Clients/1001 Brightwater Foods/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml`
- removed `box/Clients/1001 Brightwater Foods/1001-003 General Corporate/Documents/2026-08-14_q2_minutes.pdf`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-03_0912_whitcomb_kestrel-shipment-records.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-04_1005_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-07_1100_tolland_brightwater-v-kestrel-proposed-protectiv.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_0900_osei_litigation-hold-notice-kestrel-dispute.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-10_1430_whitcomb_two-things.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-11_1010_weller_kestrel-production-bates-ranges.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-14_1125_tolland_deposition-of-d-whitcomb_dup.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-20_1145_whitcomb_april-emails.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1100_tolland_settlement-discussion-fre-408.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-08-25_1530_osei_settlement-strategy-privileged.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-14_1100_tolland_kestrel-document-production-vol-2.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Correspondence/2026-09-25_1600_whitcomb_old-april-mailbox.eml`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-03_delivery_logs_mar-may.pdf`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-04_proposed_protective_order.pdf`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-10_litigation_hold_notice.pdf`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-08-20_april_emails.pdf`
- added `box/Clients/1001 Brightwater Brands/1001-001 Kestrel Supply Dispute/Documents/2026-09-14_production_vol2_index.pdf`
- added `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-03_1440_park_sunharvest-uspto-office-action.eml`
- added `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-10_1430_whitcomb_two-things.eml.xref.txt`
- added `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-20_1520_park_sunharvest-response-filed.eml`
- added `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Correspondence/2026-08-28_0900_whitcomb_photos.eml`
- added `box/Clients/1001 Brightwater Brands/1001-002 SunHarvest Trademark/Documents/2026-08-28_IMG_2211.pdf`
- added `box/Clients/1001 Brightwater Brands/1001-003 General Corporate/Correspondence/2026-08-14_0905_whitcomb_board-minutes-q2.eml`
- added `box/Clients/1001 Brightwater Brands/1001-003 General Corporate/Documents/2026-08-14_q2_minutes.pdf`
