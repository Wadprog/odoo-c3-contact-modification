"""Tests for contact visit reasons."""

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerVisitReason(TransactionCase):
    def test_visit_reason_model_is_registered(self):
        field = self.env["c3.contact.visit.reason"]._fields["name"]

        self.assertEqual(field.type, "char")
        self.assertTrue(field.required)

    def test_visit_reason_can_be_created(self):
        reason = self.env["c3.contact.visit.reason"].create({"name": "Buy a book"})

        self.assertEqual(reason.name, "Buy a book")

    def test_visit_reason_can_be_edited_and_deleted_normally(self):
        reason = self.env["c3.contact.visit.reason"].create({"name": "Visit"})

        reason.write({"name": "Customer visit"})
        self.assertEqual(reason.name, "Customer visit")

        reason.unlink()
        self.assertFalse(reason.exists())
