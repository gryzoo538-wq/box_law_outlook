# Reply to memo 02

To: Carla Ruiz (office manager)
From: Legal operations (Box migration)
Re: Intake decisions (memo of 2026-09-29)

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

Totals: needs_review 3 → 1 (only the misdirected Carter Whitfield email is left), firm_admin 2 → 3, matter 53 → 54, and 1007-002 now holds 1 email. No change to wall incidents or the privilege log. Files in box/ stay at 91. I also updated the checker (tools/check_filing.py) to accept the Declined_Intake folder and flag.

## Exact differences (filing state before vs after this memo)

### Emails changed (2)

- **AAMkc707b37e14.eml** "Request for representation"
  - category: 'needs_review' -> 'firm_admin'
  - flags: 'potential-conflict;new-matter-request' -> 'declined-intake;new-matter-request'
  - box_path: `box/_Needs_Review/2026-08-13_1415_baines_request-for-representation.eml` -> `box/Firm_Admin/Declined_Intake/2026-08-13_1415_baines_request-for-representation.eml`
- **AAMk1b66809a11.eml** "Heron fuel dock incident"
  - category: 'needs_review' -> 'matter'
  - primary_matter: '' -> '1007-002'
  - privilege: 'n/a' -> 'AC'
  - flags: 'new-matter-request' -> ''
  - box_path: `box/_Needs_Review/2026-08-25_0920_pryce_heron-fuel-dock-incident.eml` -> `box/Clients/1007 Blue Heron Marina/1007-002 Fuel Dock Damage Claim/Correspondence/2026-08-25_0920_pryce_heron-fuel-dock-incident.eml`

### Wall incidents (3 -> 3)

- no change

### Privilege log (7 -> 7)

- no change

### needs_review (3 -> 1)

- removed: AAMk1b66809a11.eml
- removed: AAMkc707b37e14.eml

### Attorney actions (24 -> 22 person/email items)

- removed: Jonah Hartwell / AAMk1b66809a11.eml
- removed: Mira Osei / AAMkc707b37e14.eml

### Counts

- category firm_admin: 2 -> 3
- category matter: 53 -> 54
- category needs_review: 3 -> 1
- matter 1007-002: 0 -> 1
- attorney Jonah Hartwell: 12 -> 13
- files in box/: 91 -> 91

### box/ files (2 removed, 2 added)

- removed `box/_Needs_Review/2026-08-13_1415_baines_request-for-representation.eml`
- removed `box/_Needs_Review/2026-08-25_0920_pryce_heron-fuel-dock-incident.eml`
- added `box/Clients/1007 Blue Heron Marina/1007-002 Fuel Dock Damage Claim/Correspondence/2026-08-25_0920_pryce_heron-fuel-dock-incident.eml`
- added `box/Firm_Admin/Declined_Intake/2026-08-13_1415_baines_request-for-representation.eml`
