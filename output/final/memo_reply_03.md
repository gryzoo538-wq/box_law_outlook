# Reply to memo 03

To: Jonah Hartwell (ethics partner)
From: Legal operations (Box migration)
Re: Tran ethical wall - expanded (memo of 2026-09-30)

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
- No change to categories, paths, privilege, the privilege log or needs_review.

## Exact differences (filing state before vs after this memo)

### Emails changed (1)

- **AAMk04f542441d.eml** "Tran mediation - authority"
  - flags: '' -> 'ethical-wall'

### Wall incidents (3 -> 4)

- added: ('AAMk04f542441d.eml', 'Tom Weller', 'cc', '1003-001')

### Privilege log (7 -> 7)

- no change

### needs_review (1 -> 1)

- no change

### Attorney actions (22 -> 24 person/email items)

- added: Jonah Hartwell (ethics partner) / AAMk04f542441d.eml
- added: Mira Osei / AAMk04f542441d.eml

### Counts

- files in box/: 91 -> 91

### box/ files (0 removed, 0 added)

