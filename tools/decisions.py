"""Phase-1 filing decisions for the Hartwell & Osei mailbox (one entry per email).

Each entry records what a human reviewer decided after reading the email and every
attachment (scans were inspected as images). Derived flags (hold, post-closing,
ethical-wall, restricted, duplicate-retained) are NOT listed here: the build script
computes them from matters.csv facts so they stay consistent with the rules.

Keys
  cat      category (matter / needs_review / firm_admin / non_matter / duplicate)
  m        primary matter (matter emails only)
  x        cross-referenced matters (same client only)
  priv     AC / WP / none for matter emails (others are n/a)
  flags    manual flags (potential-conflict, new-matter-request, misdirected,
           phishing, delivery-failure, attorney-action)
  summary  one-line summary of the body
  att      {attachment filename: what it shows}
  why      reasoning for the category / matter
  notes    judgment calls
  actions  [(person, action)] for attorney_actions.md
  review   (reason, decision needed, who decides) for needs_review emails
  privdesc privilege-log description (must not reveal privileged content)
"""

T = "Text PDF"  # attachment has a text layer
S = "SCAN (image-only, read from rendered image)"

E = {
    "AAMkdd73cf256d": dict(
        cat="matter", m="1001-001", priv="AC",
        summary="Client sends the March-May Kestrel delivery logs Mira requested; short shipments highlighted.",
        att={"delivery_logs_mar-may.pdf": f"{T}: Brightwater Foods inbound delivery log, supplier Kestrel Packaging Ltd, Mar-May 2026, 14 of 61 deliveries short."},
        why="Client (brightwaterfoods.test) to Mira Osei about Kestrel short shipments, the subject of the Kestrel supply dispute.",
        notes="Dated 2026-08-03, before the hold start (2026-08-10), so no hold flag. Listed in the privilege log because the matter is under hold and the log covers every AC/WP email in 1001-001.",
        privdesc="Email from client representative to litigation counsel transmitting business records requested by counsel."),
    "AAMkdb8f4d3e27": dict(
        cat="matter", m="1001-002", priv="AC",
        summary="Leah Park tells the client the USPTO issued an office action on the SunHarvest application.",
        why="SunHarvest trademark application is matter 1001-002; Leah Park is its responsible attorney.",
        notes=""),
    "AAMkc7ec99108d": dict(
        cat="matter", m="1001-001", priv="none",
        summary="Opposing counsel (Tolland Law, for Kestrel) sends a proposed stipulated protective order for edits.",
        att={"proposed_protective_order.pdf": f"{T}: [Proposed] Stipulated Protective Order, Brightwater Foods Inc. v. Kestrel Packaging Ltd (US District Court)."},
        why="Opposing counsel named in matters.csv for 1001-001; caption names the case.",
        notes="Pre-hold (2026-08-04); privilege none because opposing counsel is a party to the email."),
    "AAMk737734d7c1": dict(
        cat="matter", m="1002-001", priv="AC",
        summary="Maria Delgado sends the scanned appraiser's report on her late father's house.",
        att={"scan_0812.pdf": f"{S}, page rotated 90°: APPRAISAL REPORT, Property: 88 Alder Street, Prepared for: Estate of Ricardo Delgado, Purpose: date-of-death valuation, Opinion of value: $412,000."},
        why="The scan identifies 88 Alder Street, the estate property listed for 1002-001.",
        notes="Overlap: Maria Delgado has two matters (estate 1002-001 and the closed 14 Fenwick Lane purchase 1002-002). The body says only 'Dad's house'; the scan settles it as the estate property."),
    "AAMkda8201e2bd": dict(
        cat="matter", m="1005-001", priv="AC",
        summary="Ravi Iyer reminds Paul Ostrander that his financial disclosure is due August 28 and asks for bank statements.",
        why="Divorce matter 1005-001 (financial disclosure to the court).",
        notes="This message later bounced (see AAMkeefee5a5b2)."),
    "AAMk30965eda32": dict(
        cat="matter", m="1003-002", priv="AC",
        summary="Northpoint sends the landlord's counter-proposal on the Dock 7 renewal (4% annual escalator).",
        att={"landlord_letter.pdf": f"{S}, page upside down (180°): HARBORVIEW PROPERTIES, Re: Dock 7 - lease renewal, Counter-proposal: 5-year term, 4% annual escalator, Tenant: Northpoint Logistics LLC."},
        why="Client Northpoint (northpointlogistics.test), Dock 7 lease renewal = 1003-002.",
        notes=""),
    "AAMkcd2f45e678": dict(
        cat="matter", m="1003-001", priv="WP",
        summary="Anika Brandt offers Mira help with the Tran deposition outline, saying she worked on Ms. Tran's side at her old firm.",
        why="About the Tran deposition, matter 1003-001; internal firm staff only, so WP.",
        notes="ETHICAL WALL: Anika Brandt is screened from 1003-001 since 2026-07-01 and is the sender. She also reveals she worked for the adverse party (Ms. Tran) at her prior firm, which is the reason for the screen. The ethics partner must be told; she must not receive the deposition work.",
        actions=[("Jonah Hartwell (ethics partner)", "Wall incident: screened associate Anika Brandt emailed Mira Osei and Tom Weller about the Tran deposition and offered to use knowledge from her prior representation of Ms. Tran. Document the incident, remind her of the screen in writing, and confirm she receives no 1003-001 work."),
                 ("Mira Osei", "Decline Anika Brandt's offer and do not share the deposition outline; she is screened from 1003-001. Confirm Tom Weller does not forward 1003-001 material to her.")],
        privdesc="Internal email among firm staff concerning deposition preparation."),
    "AAMk79830c71c2": dict(
        cat="non_matter",
        summary="Marketing for a paid ethics CLE webinar.",
        why="Unsolicited marketing.", notes=""),
    "AAMk9da13ffe79": dict(
        cat="matter", m="1004-001", priv="AC",
        summary="Calloway sends its IT vendor's draft timeline of the July access incident; asks to keep circulation tight.",
        att={"incident_timeline_draft.pdf": f"{T}: Calloway Medical Group PC access incident timeline (DRAFT): Jul 14 unusual login detected, Jul 15 account disabled."},
        why="Calloway (callowaymed.test) privacy/data access incident = 1004-001, a RESTRICTED matter, so filed under box/Restricted/.",
        notes="Restricted matter: path under box/Restricted/ and flag restricted."),
    "AAMk2fcb008853": dict(
        cat="matter", m="1004-002", priv="AC",
        summary="Calloway sends Riverside's responses to the Heron diligence request list.",
        att={"diligence_responses.pdf": f"{T}: Riverside Imaging LLC responses to due diligence request list, prepared for Calloway Medical Group PC."},
        why="'Heron' here is Project Heron (Calloway's acquisition of Riverside Imaging), confirmed by the sender domain and the attachment.",
        notes="Name overlap: 'Heron' also appears in Blue Heron Marina (client 1007). Sender and attachment show this is Project Heron 1004-002."),
    "AAMk7218187993": dict(
        cat="matter", m="1007-001", priv="AC",
        summary="Blue Heron Marina sends the signed signature page.",
        att={"sigpage.pdf": f"{S}: BLUE HERON MARINA LLC, Slip C Lease Agreement - signature page, Signed: S. Pryce, Manager."},
        why="Sender is Blue Heron Marina (blueheronmarina.test); scan is the Slip C lease signature page = 1007-001.",
        notes="Name overlap: the subject says 'Heron slip agreement', but this is Blue Heron Marina, not Calloway's Project Heron."),
    "AAMk244dabb481": dict(
        cat="matter", m="1008-001", priv="AC",
        summary="Kenji Sato asks how to respond to Rivera & Sons billing for incomplete roof work at 210 Mill Street.",
        why="Sato Architecture fee dispute with Rivera & Sons Roofing (210 Mill Street) = 1008-001.",
        notes=""),
    "AAMk8917362f25": dict(
        cat="matter", m="1006-001", priv="AC",
        summary="HOA board reports the unit 22 owner is four months behind on dues; ledger attached.",
        att={"ledger.pdf": f"{S}: FENWICK LANE HOMEOWNERS ASSOCIATION, Owner ledger - Unit 22 (owner: K. Albright), Balance due: $1,860.00."},
        why="Client Fenwick Lane HOA, dues arrears = Assessment Collections 1006-001.",
        notes="Name overlap: 'Fenwick Lane' is also in Delgado's closed purchase matter (1002-002). This is the HOA client and an unrelated owner (unit 22)."),
    "AAMke3cf44dd3f": dict(
        cat="matter", m="1002-002", priv="AC", flags=["potential-conflict"],
        summary="Maria Delgado forwards an HOA letter demanding a transfer fee for her June purchase and asks whether she owes it.",
        att={"hoa_letter.pdf": f"{S}, slightly skewed: FENWICK LANE HOMEOWNERS ASSOCIATION, To: Maria Delgado, 14 Fenwick Lane, Transfer fee due on June 2026 conveyance: $750.00."},
        why="About the June purchase of 14 Fenwick Lane = 1002-002 (closed 2026-06-30).",
        notes="POST-CLOSING: matter closed 2026-06-30; email dated 2026-08-07. POTENTIAL CONFLICT: the HOA demanding the fee is itself a current client (1006 Fenwick Lane HOA), so two current clients are adverse on the transfer fee. Nothing is placed in the HOA's folders (rule 2); flagged instead.",
        actions=[("Ravi Iyer", "Post-closing item on closed matter 1002-002: Maria Delgado asks whether she owes the $750 HOA transfer fee. Decide whether to reopen the matter or send a scope letter; hold off substantive advice until the conflict is cleared."),
                 ("Jonah Hartwell (ethics partner)", "Potential conflict: current client Maria Delgado (1002) disputes a transfer fee claimed by current client Fenwick Lane HOA (1006). Run a conflict review before either Ravi Iyer or Leah Park acts.")]),
    "AAMk980ab8ab67": dict(
        cat="matter", m="1001-001", priv="none",
        summary="Opposing counsel accepts Mira's edits to paragraphs 4 and 9 of the protective order; clean version to follow.",
        why="Thread on the 1001-001 protective order with opposing counsel.",
        notes="Two byte-identical copies share this Message-ID (AAMk980ab8ab67 and AAMka2b1852f27, same Date). The copy whose mailbox file name sorts first is treated as the original. Pre-hold (2026-08-07), so the other copy goes to _Duplicates."),
    "AAMka2b1852f27": dict(
        cat="duplicate", priv="n/a",
        summary="Identical copy of opposing counsel's protective-order acceptance (same Message-ID as AAMk980ab8ab67).",
        why="Same Message-ID as AAMk980ab8ab67; dated 2026-08-07, before the 1001-001 hold start, so the rule 6 exception does not apply.",
        notes="Moved to box/_Duplicates/ (not retained, because it is pre-hold)."),
    "AAMk65fb710734": dict(
        cat="matter", m="1001-001", priv="AC",
        summary="Mira sends the client the litigation hold notice: nothing related to Kestrel may be deleted.",
        att={"litigation_hold_notice.pdf": f"{T}: LITIGATION HOLD NOTICE, Matter: Brightwater v. Kestrel Packaging, Effective: 2026-08-10."},
        why="Hold notice for the Kestrel dispute = 1001-001.",
        notes="Dated on the hold start date, so the hold flag applies.",
        privdesc="Email from litigation counsel to client representative (copying firm paralegal) transmitting a legal notice concerning document preservation."),
    "AAMk73f6fa5db8": dict(
        cat="matter", m="1001-001", x=["1001-002"], priv="AC",
        summary="Client tells Mira more April Kestrel emails were found, then asks Leah whether the SunHarvest launch delay affects trademark timing.",
        why="Two matters of the same client: Kestrel (addressed first) is primary; SunHarvest gets a cross-reference stub.",
        notes="Two-matter email, same client (Brightwater 1001): primary 1001-001 (first in the body), xref stub in 1001-002 Correspondence. Hold applies (2026-08-10 is the hold start).",
        privdesc="Email from client representative to counsel concerning document collection, with a question for counsel on a separate matter of the same client."),
    "AAMkbda7677796": dict(
        cat="matter", m="1001-001", priv="WP",
        summary="Tom Weller proposes Bates ranges for the first Kestrel production and notes draft privilege calls.",
        why="Internal work on the Kestrel production = 1001-001.",
        notes="Internal staff only: WP. Hold applies.",
        privdesc="Internal email between firm paralegal and attorney concerning document production logistics."),
    "AAMka69d95847e": dict(
        cat="matter", m="1003-001", priv="none",
        summary="Tran's counsel (Cole Labor Law) offers mediation dates of Sept 15 or 22.",
        why="Opposing counsel named in matters.csv for 1003-001.",
        notes="ETHICAL WALL: Anika Brandt (screened from 1003-001 since 2026-07-01) is copied. Opposing counsel copied her, perhaps because of her former firm.",
        actions=[("Jonah Hartwell (ethics partner)", "Wall incident: opposing counsel copied screened associate Anika Brandt on Tran mediation dates. Confirm she does not act on it or reply, and consider asking Cole Labor Law to stop copying her."),
                 ("Mira Osei", "When replying to Cole Labor Law on mediation dates, remove Anika Brandt from the thread.")]),
    "AAMk9f28518867": dict(
        cat="matter", m="1003-001", priv="AC",
        summary="Northpoint sends the personnel-file excerpt Mira requested.",
        att={"personnel_excerpt.pdf": f"{S}: NORTHPOINT LOGISTICS LLC - PERSONNEL FILE, Employee: Jessica Tran, Performance reviews 2024-2026 (excerpt)."},
        why="Scan shows Jessica Tran's personnel file = Tran employment claim 1003-001.",
        notes="Brandt is not on this email, so there is no wall incident."),
    "AAMkd403d71684": dict(
        cat="matter", m="1008-001", priv="none",
        summary="Rivera & Sons Roofing sends counsel a notice that invoice 4471 (210 Mill Street) is 60 days overdue.",
        why="Adverse party in the Sato fee dispute (Rivera & Sons, 210 Mill Street) = 1008-001.",
        notes="Sent to the front desk. Privilege none (third party/adverse party)."),
    "AAMk108743feb6": dict(
        cat="firm_admin",
        summary="Automated notice that the firm's storage is 91% full.",
        why="The firm's own IT/storage business.",
        notes="Freeing space must not touch material under the 1001-001 hold.",
        actions=[("IT", "Storage 91% full (Box sync notice). Add capacity; do not delete or archive anything in 1001-001 (litigation hold) to free space.")]),
    "AAMk090f3ebdd3": dict(
        cat="matter", m="1005-001", priv="AC", flags=["potential-conflict", "new-matter-request"],
        summary="Paul Ostrander approves the kids' holiday schedule, then asks whether Ravi can help his brother with a slip contract at Blue Heron Marina.",
        why="Mainly the divorce (parenting schedule) = 1005-001; the brother's request is new work, so the email stays in the existing matter with new-matter-request (rule 2).",
        notes="NEW MATTER REQUEST for a non-client (the brother). POTENTIAL CONFLICT: the counterparty to the brother's slip contract would be Blue Heron Marina LLC, a current client (1007) whose slip leases the firm handles. Nothing is filed in 1007's folders. 'Heron' overlap noted; this is the marina, not Project Heron.",
        actions=[("Ravi Iyer", "New-matter request: Paul Ostrander's brother wants help with a slip contract at Blue Heron Marina. Do not take the call until conflicts clears; the marina is a current client."),
                 ("Jonah Hartwell (ethics partner)", "Potential conflict: a prospective client (Paul Ostrander's brother) wants representation on a slip contract with current client Blue Heron Marina LLC (1007, your matter). Decide whether the firm can accept it.")]),
    "AAMke130b17d0b": dict(
        cat="matter", m="1004-001", priv="AC",
        summary="Leah sends Calloway draft v2 of the regulator notification letter (privileged).",
        why="Privacy investigation regulator notification = 1004-001 (RESTRICTED).",
        notes="Restricted: filed under box/Restricted/."),
    "AAMk993deffa38": dict(
        cat="non_matter", flags=["phishing"],
        summary="'IT Support' from the look-alike domain hartwe11-osei.test (digit 1s) asks three lawyers to verify their password via a link.",
        why="Impersonates the firm's IT and asks for credentials: suspected phishing.",
        notes="Look-alike domain: hartwe11 (two digit ones) instead of hartwell.",
        actions=[("IT", "Phishing: 'IT Support' <it-support@hartwe11-osei.test> (look-alike domain) asked Mira Osei, Leah Park and Ravi Iyer to verify passwords via a link. Block the domain, purge the message, check whether anyone clicked, and reset credentials if so."),
                 ("Mira Osei", "Phishing email received 2026-08-13 ('Password expiry - verify now'). Do not click; confirm to IT whether the link was opened."),
                 ("Leah Park", "Phishing email received 2026-08-13 ('Password expiry - verify now'). Do not click; confirm to IT whether the link was opened."),
                 ("Ravi Iyer", "Phishing email received 2026-08-13 ('Password expiry - verify now'). Do not click; confirm to IT whether the link was opened.")]),
    "AAMkc707b37e14": dict(
        cat="needs_review", flags=["potential-conflict", "new-matter-request"],
        summary="Kestrel Packaging's CEO asks to engage the firm for a new distribution agreement.",
        why="A request to represent Kestrel Packaging, the adverse party in 1001-001 (Brightwater v. Kestrel). This is a conflict check and possible new matter, so it cannot be filed in any client folder.",
        notes="POTENTIAL CONFLICT: adverse party in an open, held litigation wants to hire the firm. Nothing goes in Brightwater's folders.",
        review=("Request for representation from Kestrel Packaging Ltd, the adverse party in open matter 1001-001 (Brightwater v. Kestrel, under litigation hold).",
                "Whether the firm may accept or must decline the engagement (direct adversity to current client Brightwater), and how to respond to Kestrel without discussing the litigation.",
                "Jonah Hartwell (ethics partner, who also received the email), in consultation with Mira Osei (responsible attorney for 1001-001)."),
        actions=[("Jonah Hartwell (ethics partner)", "Conflict check: Kestrel Packaging (adverse party in 1001-001) asked you to represent it on a new distribution agreement. Decline, or clear the conflict, and reply without discussing the litigation."),
                 ("Mira Osei", "FYI conflict: Kestrel Packaging, adverse in 1001-001, has approached the firm for a new engagement (sent to Jonah Hartwell).")]),
    "AAMk5376c468ae": dict(
        cat="matter", m="1001-003", priv="AC",
        summary="Client sends the Q2 board minutes for the minute book.",
        att={"q2_minutes.pdf": f"{T}: Brightwater Foods Inc. Minutes of the Board of Directors - Q2 2026."},
        why="Board/minute book = General corporate and board matters 1001-003 (Jonah Hartwell).",
        notes="Same client as the Kestrel dispute but a different matter; 1001-003 is not under hold."),
    "AAMk32d7a94ded": dict(
        cat="matter", m="1001-001", priv="none",
        summary="Opposing counsel intends to depose Dana Whitcomb in late September and asks for dates.",
        why="Deposition notice from opposing counsel in 1001-001.",
        notes="Two byte-identical copies share this Message-ID (AAMk32d7a94ded and AAMk9770c6a5b8). The copy whose mailbox file name sorts first is the original; the other is retained under hold (rule 6)."),
    "AAMk9770c6a5b8": dict(
        cat="duplicate", priv="none",
        summary="Identical copy of the Whitcomb deposition email (same Message-ID as AAMk32d7a94ded).",
        why="Duplicate of an email filed in 1001-001 (under hold) and dated after the hold start, so it is kept in the matter's Correspondence folder with '_dup' (rule 6).",
        notes="HOLD DUPLICATE RETAINED: flags hold;duplicate-retained. Privilege is recorded as 'none' (as for its original) because it sits in the matter folder; it is not AC/WP, so it is not on the privilege log."),
    "AAMk3b84e55160": dict(
        cat="matter", m="1004-001", x=["1004-002"], priv="AC",
        summary="Calloway tells Leah the notification letter went out Friday, and tells Jonah the Heron board vote is set for September 2.",
        why="Two matters of the same client (Calloway 1004): the privacy notification letter (1004-001, addressed first) is primary; Project Heron 1004-002 gets a stub.",
        notes="Primary is RESTRICTED 1004-001, so the copy is under box/Restricted/. The stub in 1004-002 (same client) points to the Restricted path; the rules allow same-client stubs. 'Heron' = Project Heron (Calloway)."),
    "AAMk4ba3ea284d": dict(
        cat="needs_review", flags=["misdirected"],
        summary="Lucy Carter (Carter Whitfield LLP) sends 'Martinez closing docs' per a call; no Martinez client or matter exists at the firm.",
        why="Clearly meant for another firm or person: no Martinez matter, and the sender refers to a call that did not happen with this firm. Not read further.",
        notes="MISDIRECTED. The email says documents are attached, but the message has no attachment.",
        review=("Misdirected: Carter Whitfield LLP sent 'Martinez closing docs' to Mira Osei; the firm has no Martinez client or matter. The body mentions attachments but none arrived.",
                "Notify the sender that the email reached the wrong recipient, and decide whether to delete it or keep a record of the misdirection (no client file).",
                "Mira Osei (recipient)."),
        actions=[("Mira Osei", "Misdirected email from Lucy Carter (Carter Whitfield LLP), 'Martinez closing docs'. Tell the sender it was misdirected; do not use the contents.")]),
    "AAMk017ff12229": dict(
        cat="matter", m="1008-001", priv="WP",
        summary="Mira asks Tom Weller to draft the demand letter to Rivera & Sons (no payment for work not performed).",
        why="Internal work on the Sato/Rivera dispute = 1008-001.", notes=""),
    "AAMk15a9964aef": dict(
        cat="matter", m="1007-001", priv="AC",
        summary="Blue Heron Marina sends the requested insurance certificate.",
        att={"coi.pdf": f"{S}, page rotated 90°: CERTIFICATE OF LIABILITY INSURANCE, Certificate holder: Blue Heron Marina LLC, Re: Slip C lease."},
        why="Scan references the Slip C lease = 1007-001.",
        notes="Rotated scan; read after mentally rotating. Not Project Heron."),
    "AAMka775139237": dict(
        cat="matter", m="1003-002", x=["1003-001"], priv="AC",
        summary="Northpoint says the landlord accepted the Dock 7 counter, then reports that Ms. Tran's lawyer called him directly again and asks if that is allowed.",
        why="Two matters of the same client (Northpoint 1003): Dock 7 (1003-002, addressed first) is primary; the Tran claim (1003-001) gets a stub.",
        notes="ETHICAL WALL: Anika Brandt is copied, and the email (through its cross-reference) is about 1003-001, from which she is screened. One incident row (matter 1003-001). Also, opposing counsel contacting a represented party directly is an ethics issue for Mira Osei.",
        actions=[("Jonah Hartwell (ethics partner)", "Wall incident: screened associate Anika Brandt was copied on Hank Moreau's email about Tran's lawyer contacting him directly (1003-001, cross-referenced). Remove her from the thread when replying."),
                 ("Jonah Hartwell", "Reply to Hank Moreau on Dock 7, and route his question about Tran's counsel to Mira Osei without copying Anika Brandt."),
                 ("Mira Osei", "Hank Moreau reports Ms. Tran's lawyer (Cole Labor Law) again contacted him directly, although Northpoint is represented. Advise the client and raise the contact with opposing counsel.")]),
    "AAMk684735af1c": dict(
        cat="matter", m="1002-001", priv="AC",
        summary="Maria Delgado reports the estate inventory hearing is set for October 6.",
        why="Probate of Ricardo Delgado's estate = 1002-001.", notes=""),
    "AAMk8dff666589": dict(
        cat="needs_review", flags=["new-matter-request"],
        summary="Maria Delgado, saying it is unrelated to the estate, asks whether Ravi can help her daughter form a bakery LLC.",
        why="A request for legal services outside every existing matter (and for a non-client, the daughter). Possible new matter.",
        notes="Existing client, but the request is expressly 'unrelated to Dad's estate'.",
        review=("New-matter request: an LLC formation for Maria Delgado's daughter (not a client); no existing matter covers it.",
                "Whether to open a new matter (who the client is, conflict check, engagement letter) or decline.",
                "Ravi Iyer (relationship attorney), with conflict clearance by Jonah Hartwell (ethics partner)."),
        actions=[("Ravi Iyer", "New-matter request: bakery LLC for Maria Delgado's daughter. Run conflicts and intake, then accept or decline in writing.")]),
    "AAMkeefee5a5b2": dict(
        cat="matter", m="1005-001", priv="none", flags=["delivery-failure"],
        summary="Non-delivery notice: Ravi's 'Financial disclosure deadline' email to paul.ostrander@mailbox.test failed.",
        why="Bounce of AAMkda8201e2bd, filed in that email's matter (1005-001) per the delivery-failure rule.",
        notes="DELIVERY FAILURE. Privilege none (automated sender). Paul Ostrander later wrote from the same address, but the court deadline reminder may never have reached him.",
        actions=[("Ravi Iyer", "Delivery failure: the 2026-08-04 reminder that Paul Ostrander's financial disclosure is due August 28 bounced (notice 2026-08-20). Confirm by phone that he received the deadline and has a working address.")]),
    "AAMk15d7185dda": dict(
        cat="matter", m="1001-001", priv="AC",
        summary="Client sends the April Kestrel emails as one PDF.",
        att={"april_emails.pdf": f"{T}: Export of Brightwater purchasing mailbox, correspondence with Kestrel Packaging Ltd, April 2026."},
        why="Documents collected for the Kestrel dispute = 1001-001.", notes="Hold applies.",
        privdesc="Email from client representative to litigation counsel transmitting collected documents."),
    "AAMk41b53302fc": dict(
        cat="matter", m="1001-002", priv="AC",
        summary="Leah tells the client the office action response was filed.",
        why="SunHarvest trademark = 1001-002.", notes=""),
    "AAMkc250b601fc": dict(
        cat="matter", m="1005-001", priv="none",
        summary="Joan Kline (Kline Family Law) sends 'our proposed parenting plan' to Ravi.",
        att={"parenting_plan.pdf": f"{S}: PROPOSED PARENTING PLAN, In re the Marriage of Ostrander, Submitted by Respondent."},
        why="The scan identifies the Ostrander marriage case, so Joan Kline is opposing counsel in 1005-001.",
        notes="Identifiable only from the attachment. Privilege none (opposing counsel)."),
    "AAMk833acb6266": dict(
        cat="matter", m="1006-001", priv="AC", flags=["potential-conflict"],
        summary="HOA board says the new owner of 14 Fenwick Lane, Maria Delgado, disputes the transfer fee and asks Leah to send a demand letter.",
        why="HOA collections work = Assessment Collections 1006-001.",
        notes="POTENTIAL CONFLICT: the demand would be against Maria Delgado, a current client (1002). Nothing is filed in Delgado's folders (rule 2). Leah must not send the demand until the conflict is resolved.",
        actions=[("Leah Park", "The HOA asks for a demand letter to Maria Delgado over the 14 Fenwick Lane transfer fee. She is a current firm client (Ravi Iyer). Hold the demand until the ethics partner clears the conflict."),
                 ("Jonah Hartwell (ethics partner)", "Potential conflict: Fenwick Lane HOA (1006) asks the firm to send a demand letter to current client Maria Delgado (1002). Decide whether the firm can act or must decline/refer.")]),
    "AAMk0749fe85b0": dict(
        cat="matter", m="1008-001", priv="AC",
        summary="Kenji Sato asks whether mediation with Rivera makes sense.",
        why="Sato/Rivera dispute = 1008-001.", notes=""),
    "AAMk9011fa2ac0": dict(
        cat="firm_admin",
        summary="Office manager asks all lawyers to submit Q3 time entries by September 5.",
        why="Firm billing business.",
        notes="Anika Brandt is a recipient, but the email concerns no matter, so there is no wall issue."),
    "AAMk1bc42b7170": dict(
        cat="matter", m="1004-002", priv="AC",
        summary="Calloway sends draft escrow instructions for Heron.",
        att={"escrow_instructions.pdf": f"{T}: ESCROW INSTRUCTIONS - DRAFT, Buyer: Calloway Medical Group PC, Seller: Riverside Imaging LLC."},
        why="Project Heron acquisition = 1004-002.", notes="'Heron' = Project Heron (attachment names Riverside Imaging)."),
    "AAMk1b66809a11": dict(
        cat="needs_review", flags=["new-matter-request"],
        summary="Blue Heron Marina asks for advice on a damage claim after a visiting boat struck its fuel dock.",
        why="Existing client, but a new legal service (property damage/insurance claim) outside the only marina matter (Slip C lease). Possible new matter.",
        notes="'Heron' overlap: this is Blue Heron Marina, not Project Heron. Not filed in 1007-001, because the Slip C lease does not cover a fuel-dock damage claim.",
        review=("New-matter request from existing client Blue Heron Marina LLC: a damage claim after a boat struck its fuel dock. Not part of the Slip C lease matter (1007-001).",
                "Whether to open a new matter for Blue Heron Marina (conflict check on the boat owner and the insurer, engagement terms).",
                "Jonah Hartwell (responsible attorney for Blue Heron Marina)."),
        actions=[("Jonah Hartwell", "New-matter request: Blue Heron Marina's fuel-dock damage claim. Run conflicts on the boat owner and the insurer, then open a matter or decline.")]),
    "AAMk4ad8b9b45c": dict(
        cat="matter", m="1001-001", priv="none",
        summary="Opposing counsel asks, for settlement purposes only, whether the client would consider a structured credit on future orders.",
        why="Settlement communication from Kestrel's counsel in 1001-001.", notes="FRE 408 communication; hold applies; privilege none (opposing counsel)."),
    "AAMk1162f28d1a": dict(
        cat="matter", m="1001-001", priv="AC",
        summary="Mira sends the client (copying Jonah) her recommendation on Kestrel's settlement feeler (privileged).",
        why="Settlement strategy in the Kestrel dispute = 1001-001.", notes="Hold applies.",
        privdesc="Email from litigation counsel to client representative (copying a firm partner) providing legal advice regarding settlement."),
    "AAMk04f542441d": dict(
        cat="matter", m="1003-001", priv="AC",
        summary="Northpoint confirms management approved settlement authority for the Tran mediation.",
        why="Tran employment claim = 1003-001.",
        notes="Recipients are Mira Osei and Tom Weller; Brandt is not on it, so there is no incident."),
    "AAMkafd8e94b15": dict(
        cat="non_matter",
        summary="Employment-law newsletter.", why="Newsletter.", notes=""),
    "AAMk360023b682": dict(
        cat="matter", m="1002-001", priv="AC",
        summary="Maria Delgado sends a scan with no body text.",
        att={"scan0047.pdf": f"{S}: LETTERS TESTAMENTARY, Estate of Ricardo Delgado, deceased, Executor: Maria Delgado."},
        why="Identifiable only from the attachment: letters testamentary for the Ricardo Delgado estate = 1002-001.",
        notes="Delgado has two matters; the scan settles it as the estate."),
    "AAMked35b00a54": dict(
        cat="matter", m="1003-002", priv="AC",
        summary="Northpoint forwards a scan with no body text (subject 'fwd').",
        att={"scan0103.pdf": f"{S}, page rotated 90°: LEASE AMENDMENT NO. 3, Premises: Dock 7, Landlord: Harborview Properties, Tenant: Northpoint Logistics LLC, EXECUTED."},
        why="Identifiable only from the attachment: the executed Dock 7 lease amendment = 1003-002.",
        notes="Northpoint has two matters; the scan settles it as Dock 7."),
    "AAMk0de90794df": dict(
        cat="matter", m="1001-002", priv="AC",
        summary="Client sends 'photos' ('As discussed.') to Leah Park.",
        att={"IMG_2211.pdf": f"{S}: Specimen of use, Mark: SUNHARVEST, Retail packaging label - front panel."},
        why="Identifiable only from the attachment: a trademark specimen for SUNHARVEST = 1001-002 (Leah Park).",
        notes="Brightwater has three matters; the scan shows the trademark matter, not the Kestrel dispute, so there is no hold flag."),
    "AAMk6078511608": dict(
        cat="matter", m="1004-001", priv="AC",
        summary="Calloway sends a scanned document with no body text (subject 'doc').",
        att={"doc_0828.pdf": f"{S}, page upside down (180°): CONFIDENTIAL, Calloway Medical Group PC, Risk assessment - July access incident."},
        why="Identifiable only from the attachment: a risk assessment of the July access incident = 1004-001 (RESTRICTED).",
        notes="Calloway has two matters; the scan shows the privacy incident, not Project Heron. Filed under box/Restricted/."),
    "AAMkb5faf8cda9": dict(
        cat="matter", m="1008-001", priv="AC",
        summary="Kenji Sato sends a scan with no body text.",
        att={"scan_lien.pdf": f"{S}: NOTICE OF MECHANIC'S LIEN, Claimant: Rivera & Sons Roofing, Property: 210 Mill Street."},
        why="Identifiable only from the attachment: Rivera's lien on 210 Mill Street = 1008-001.", notes=""),
    "AAMk6b65bd9acb": dict(
        cat="matter", m="1005-001", priv="AC",
        summary="Paul Ostrander sends a scan with no body text.",
        att={"statement_jul.pdf": f"{S}: FIRST HARBOR BANK, Account holder: Paul Ostrander, Statement period: July 2026."},
        why="A bank statement for the financial disclosure Ravi requested = divorce 1005-001.",
        notes="Identifiable from the attachment together with the earlier disclosure request."),
    "AAMk9012b2a414": dict(
        cat="matter", m="1007-001", priv="AC",
        summary="Blue Heron Marina sends a receipt (subject 'Re: Heron').",
        att={"receipt.pdf": f"{S}: BLUE HERON MARINA LLC, Slip C - first month's rent received, Receipt no. 0091."},
        why="Attachment is a Slip C rent receipt = 1007-001.",
        notes="Name overlap: the subject 'Re: Heron' could suggest Project Heron (1004-002), but the sender and scan show Blue Heron Marina's Slip C lease."),
    "AAMk32a123f501": dict(
        cat="matter", m="1004-002", priv="AC",
        summary="Jonah congratulates Calloway on the board approval and sends the Heron closing checklist.",
        why="Project Heron acquisition = 1004-002.", notes=""),
    "AAMkacc74c7ccf": dict(
        cat="matter", m="1003-002", priv="none",
        summary="Northstar Insurance says the Dock 7 landlord needs an updated additional-insured certificate and asks for the tenant's broker.",
        why="Dock 7 lease renewal for Northpoint = 1003-002.", notes="Third-party insurer: privilege none."),
    "AAMk5645100358": dict(
        cat="matter", m="1003-002", priv="AC",
        summary="Anika Brandt asks Northpoint to confirm the signatory for the Dock 7 renewal.",
        why="Dock 7 lease renewal = 1003-002.",
        notes="Anika Brandt is screened only from 1003-001 (Tran), not from Dock 7, so this is not a wall incident."),
    "AAMk4f164f1513": dict(
        cat="non_matter",
        summary="Personal message to Ravi Iyer about Friday dinner.", why="Personal message.", notes="Shares a surname with Ravi Iyer; personal, not firm business."),
    "AAMk03552454f1": dict(
        cat="matter", m="1001-001", priv="none",
        summary="Opposing counsel sends Kestrel's second production volume.",
        att={"production_vol2_index.pdf": f"{T}: Kestrel Packaging Ltd - Document Production Volume 2 Index: KPL004001-KPL006250."},
        why="Production in the Kestrel dispute = 1001-001.", notes="Hold applies."),
    "AAMk68f6cdb2f8": dict(
        cat="needs_review", flags=["new-matter-request"],
        summary="Maria Delgado asks whether 'Delgado Bakery LLC' is available as a name.",
        why="A follow-up on the bakery LLC request, which still has no matter. Possible new matter.",
        notes="Same request as AAMk8dff666589.",
        review=("Follow-up on the bakery LLC new-matter request (name availability for 'Delgado Bakery LLC'). Still no matter exists.",
                "Same decision as AAMk8dff666589: open a new matter for the daughter's LLC, or decline.",
                "Ravi Iyer, with conflict clearance by Jonah Hartwell."),
        actions=[("Ravi Iyer", "Follow-up on the bakery LLC request (name check). Respond once intake is decided.")]),
    "AAMkecc20ef164": dict(
        cat="matter", m="1001-001", priv="AC", flags=["attorney-action"],
        summary="Client asks whether its IT team may purge the April purchasing mailbox to save space.",
        why="The April purchasing mailbox holds the Kestrel correspondence collected for 1001-001.",
        notes="ATTORNEY ACTION: the client asks to delete data the hold (from 2026-08-10) forbids deleting. Mira must say no.",
        actions=[("Mira Osei", "URGENT (hold): Brightwater asks to purge its April purchasing mailbox, which holds Kestrel correspondence. The litigation hold forbids deletion. Instruct the client in writing not to purge, and confirm IT preservation steps.")],
        privdesc="Email from client representative to litigation counsel requesting legal advice regarding document preservation."),
}
