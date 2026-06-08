"""Tests for contact visit records."""

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerVisit(TransactionCase):
    def test_visit_model_is_registered(self):
        model = self.env["c3.contact.visit"]
        partner_field = model._fields["partner_id"]
        reason_field = model._fields["visit_reason_id"]

        self.assertEqual(partner_field.type, "many2one")
        self.assertEqual(partner_field.comodel_name, "res.partner")
        self.assertEqual(reason_field.type, "many2one")
        self.assertEqual(reason_field.comodel_name, "c3.contact.visit.reason")
        self.assertTrue(reason_field.required)

    def test_visit_can_be_linked_to_a_contact(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe John",
                "is_company": False,
                "type": "contact",
            }
        )
        reason = self.env["c3.contact.visit.reason"].create({"name": "Visit"})

        visit = self.env["c3.contact.visit"].create(
            {"partner_id": partner.id, "visit_reason_id": reason.id}
        )

        self.assertEqual(visit.partner_id, partner)
        self.assertEqual(visit.visit_reason_id, reason)
        self.assertTrue(visit.create_date)

    def test_visit_records_cannot_be_edited(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe John",
                "is_company": False,
                "type": "contact",
            }
        )
        reason = self.env["c3.contact.visit.reason"].create({"name": "Visit"})
        visit = self.env["c3.contact.visit"].create(
            {"partner_id": partner.id, "visit_reason_id": reason.id}
        )

        with self.assertRaisesRegex(
            UserError,
            "Visit records cannot be edited after creation.",
        ):
            visit.write({"partner_id": partner.id})

    def test_visit_records_cannot_be_deleted(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe John",
                "is_company": False,
                "type": "contact",
            }
        )
        reason = self.env["c3.contact.visit.reason"].create({"name": "Visit"})
        visit = self.env["c3.contact.visit"].create(
            {"partner_id": partner.id, "visit_reason_id": reason.id}
        )

        with self.assertRaisesRegex(
            UserError,
            "Visit records cannot be deleted after creation.",
        ):
            visit.unlink()
