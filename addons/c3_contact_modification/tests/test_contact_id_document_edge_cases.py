"""Tests for contact ID document lifecycle edge cases."""

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged

from .test_contact_id_document_storage import VALID_PNG_DATA


@tagged("post_install", "-at_install")
class TestContactIdDocumentEdgeCases(TransactionCase):
    def _create_partner(self):
        return self.env["res.partner"].create(
            {
                "name": "Doe Alice",
                "is_company": False,
                "type": "contact",
                "gender": "female",
            }
        )

    def _create_partner_with_id_document(self):
        partner = self._create_partner()
        partner.write(
            {
                "c3_id_document": VALID_PNG_DATA,
                "c3_id_document_filename": "id-document.png",
            }
        )
        return partner

    def _id_document_attachments(self, partner):
        return self.env["ir.attachment"].search(
            [
                ("res_model", "=", "res.partner"),
                ("res_id", "=", partner.id),
                ("res_field", "=", "c3_id_document"),
            ]
        )

    def test_duplicating_contact_does_not_copy_id_document(self):
        partner = self._create_partner_with_id_document()

        duplicate = partner.copy({"name": "Doe Alice Copy"})

        self.assertFalse(duplicate.c3_id_document)
        self.assertFalse(duplicate.c3_id_document_filename)

    def test_deleting_contact_deletes_id_document_attachment(self):
        partner = self._create_partner_with_id_document()
        attachment = self._id_document_attachments(partner)

        partner.unlink()

        self.assertFalse(attachment.exists())

    def test_changing_individual_with_id_document_to_company_is_blocked(self):
        partner = self._create_partner_with_id_document()

        with self.assertRaisesRegex(
            ValidationError,
            "ID documents are only available for individual contacts.",
        ):
            partner.is_company = True

    def test_changing_individual_to_company_succeeds_after_id_document_is_removed(self):
        partner = self._create_partner_with_id_document()

        partner.write(
            {
                "c3_id_document": False,
                "c3_id_document_filename": False,
                "is_company": True,
            }
        )

        self.assertTrue(partner.is_company)
        self.assertFalse(partner.c3_id_document)

    def test_company_contact_cannot_keep_id_document(self):
        company = self.env["res.partner"].create(
            {
                "name": "C3 Test Company",
                "is_company": True,
                "type": "contact",
            }
        )

        with self.assertRaisesRegex(
            ValidationError,
            "ID documents are only available for individual contacts.",
        ):
            company.c3_id_document = VALID_PNG_DATA
