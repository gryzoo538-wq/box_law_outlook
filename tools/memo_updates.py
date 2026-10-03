"""Fact changes from the four memos, applied in date order on top of tools/decisions.py.

Each function edits the decision table (dec) and the matter facts (matters) in place
and returns a short description. build_filing.py --memos N applies the first N.
"""


def _matter(matters, **kw):
    row = dict(notes="", closed_date="", status="open", hold_start=None, walls=[], restricted=False)
    row.update(kw)
    matters[row["matter_no"]] = row


def memo_01(dec, matters):
    """2026-09-28 Carla Ruiz: new matter 1002-003 Delgado Bakery LLC Formation."""
    _matter(matters, matter_no="1002-003", client_no="1002", client_name="Maria Delgado",
            client_folder="1002 Delgado Maria", matter_name="Formation of Delgado Bakery LLC",
            matter_folder="1002-003 Delgado Bakery LLC Formation", responsible_attorney="Ravi Iyer")
    for k in ("AAMk8dff666589", "AAMk68f6cdb2f8"):
        d = dec[k]
        d.update(cat="matter", m="1002-003", priv="AC", flags=[], actions=[])
        d.pop("review", None)
        d.setdefault("memo_notes", []).append(
            "Memo 01 (2026-09-28): conflicts cleared and matter 1002-003 (Delgado Bakery LLC Formation, Ravi Iyer) opened. "
            "Moved from _Needs_Review into 1002-003 Correspondence; category matter, privilege AC (client to her attorney about the matter); "
            "new-matter-request removed as the memo directs.")
    return "1002-003 opened; bakery emails filed there"


def memo_02(dec, matters):
    """2026-09-29 Carla Ruiz: Kestrel engagement declined; new matter 1007-002 Fuel Dock Damage Claim."""
    d = dec["AAMkc707b37e14"]
    d.update(cat="firm_admin", subdir="Declined_Intake", priv="n/a",
             actions=[("Jonah Hartwell (ethics partner)", "Closed out (memo 02): Kestrel's engagement request was declined and the decline letter sent. "
                       "Keep the decline letter with this intake record; no further contact with Kestrel about the 1001-001 litigation.")],
             flags=["declined-intake" if f == "potential-conflict" else f for f in d.get("flags", [])])
    d.pop("review", None)
    d.setdefault("memo_notes", []).append(
        "Memo 02 (2026-09-29): engagement DECLINED (decline letter sent). Moved to box/Firm_Admin/Declined_Intake/, category firm_admin, "
        "privilege n/a; flag declined-intake replaces potential-conflict. new-matter-request is kept because the memo replaces only "
        "potential-conflict and no matter was opened for this request.")
    _matter(matters, matter_no="1007-002", client_no="1007", client_name="Blue Heron Marina LLC",
            client_folder="1007 Blue Heron Marina", matter_name="Fuel dock damage claim",
            matter_folder="1007-002 Fuel Dock Damage Claim", responsible_attorney="Jonah Hartwell")
    d = dec["AAMk1b66809a11"]
    d.update(cat="matter", m="1007-002", priv="AC", flags=[], actions=[])
    d.pop("review", None)
    d.setdefault("memo_notes", []).append(
        "Memo 02 (2026-09-29): matter 1007-002 (Fuel Dock Damage Claim, Jonah Hartwell) opened. Moved from _Needs_Review into "
        "1007-002 Correspondence; category matter, privilege AC; new-matter-request removed because the request now belongs to an "
        "existing matter (same treatment memo 01 gives the bakery emails).")
    return "Kestrel declined; 1007-002 opened; fuel-dock email filed there"


def memo_03(dec, matters):
    """2026-09-30 Jonah Hartwell: Tom Weller also screened from 1003-001 from 2026-08-15."""
    m = matters["1003-001"]
    m["notes"] += " ETHICAL WALL: Tom Weller is screened from this matter (since 2026-08-15)."
    m["walls"] = list(m["walls"]) + [("Tom Weller", "2026-08-15")]
    d = dec["AAMk04f542441d"]
    d.setdefault("actions", []).extend([
        ("Jonah Hartwell (ethics partner)", "Wall incident (memo 03, screen effective 2026-08-15): paralegal Tom Weller was copied on Northpoint's "
         "settlement-authority email for the Tran mediation (2026-08-26). Document it and confirm he keeps no 1003-001 material."),
        ("Mira Osei", "Tom Weller is screened from 1003-001 from 2026-08-15 but was copied on Hank Moreau's settlement-authority email (2026-08-26). "
         "Ask Northpoint to stop copying him on Tran correspondence and keep him off 1003-001 distribution.")])
    d.setdefault("memo_notes", []).append(
        "Memo 03 (2026-09-30): Tom Weller is screened from 1003-001 from 2026-08-15. He is copied on this 2026-08-26 email about 1003-001, "
        "so it gets the ethical-wall flag and a wall incident (role cc).")
    d = dec["AAMkcd2f45e678"]
    d.setdefault("memo_notes", []).append(
        "Memo 03 (2026-09-30): Tom Weller is copied here, but on 2026-08-05, before his screen took effect (2026-08-15), so no incident "
        "for him (memo: nothing before 2026-08-15 counts). The Anika Brandt incident stands.")
    return "Tom Weller screened from 1003-001 since 2026-08-15"


def memo_04(dec, matters):
    """2026-10-01 Carla Ruiz: Brightwater Foods Inc. renamed Brightwater Brands Inc.; client folder renamed."""
    for m in matters.values():
        if m["client_no"] == "1001":
            m["client_name"] = "Brightwater Brands Inc."
            m["client_folder"] = "1001 Brightwater Brands"
    for d in dec.values():
        if d.get("m", "").startswith("1001-") or d is dec["AAMk9770c6a5b8"] or any(x.startswith("1001-") for x in d.get("x", [])):
            d.setdefault("memo_notes", []).append(
                "Memo 04 (2026-10-01): client renamed Brightwater Brands Inc.; the copy, its attachments and any stub now sit under "
                "box/Clients/1001 Brightwater Brands/ (matter folder unchanged).")
    return "client folder renamed to 1001 Brightwater Brands"


MEMOS = [memo_01, memo_02, memo_03, memo_04]
