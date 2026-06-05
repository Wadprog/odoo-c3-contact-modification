"""Tests for contact ID document attachment storage."""

from odoo.tests import TransactionCase, tagged


VALID_PNG_DATA = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMB/"
    "axzZ3cAAAAASUVORK5CYII="
)


@tagged("post_install", "-at_install")
class TestContactIdDocumentStorage(TransactionCase):
    def _create_attachment(self, partner, name="id-document.png"):
        return self.env["ir.attachment"].create(
            {
                "name": name,
                "datas": VALID_PNG_DATA,
                "mimetype": "image/png",
                "res_model": "res.partner",
                "res_id": partner.id,
            }
        )

    def test_id_document_attachment_field_is_registered(self):
        field = self.env["res.partner"]._fields["c3_id_document_attachment_id"]

        self.assertEqual(field.type, "many2one")
        self.assertEqual(field.comodel_name, "ir.attachment")
        self.assertFalse(field.copy)

    def test_individual_contact_can_reference_one_id_document_attachment(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe Alice",
                "is_company": False,
                "type": "contact",
                "gender": "female",
            }
        )
        attachment = self._create_attachment(partner)

        partner.c3_id_document_attachment_id = attachment

        self.assertEqual(partner.c3_id_document_attachment_id, attachment)
        self.assertEqual(partner.c3_id_document_attachment_id.res_model, "res.partner")
        self.assertEqual(partner.c3_id_document_attachment_id.res_id, partner.id)

    def test_id_document_attachment_is_distinct_from_general_contact_attachments(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe John",
                "is_company": False,
                "type": "contact",
                "gender": "male",
            }
        )
        id_attachment = self._create_attachment(partner, "id-document.png")
        general_attachment = self._create_attachment(partner, "general-note.png")

        partner.c3_id_document_attachment_id = id_attachment

        self.assertEqual(partner.c3_id_document_attachment_id, id_attachment)
        self.assertNotEqual(partner.c3_id_document_attachment_id, general_attachment)

    def test_only_one_current_id_document_attachment_is_referenced(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe Jane",
                "is_company": False,
                "type": "contact",
                "gender": "female",
            }
        )
        first_attachment = self._create_attachment(partner, "first-id.png")
        second_attachment = self._create_attachment(partner, "second-id.png")

        partner.c3_id_document_attachment_id = first_attachment
        partner.c3_id_document_attachment_id = second_attachment

        self.assertEqual(partner.c3_id_document_attachment_id, second_attachment)
        self.assertNotEqual(partner.c3_id_document_attachment_id, first_attachment)

    def test_company_contacts_start_without_id_document_attachment(self):
        company = self.env["res.partner"].create(
            {
                "name": "C3 Test Company",
                "is_company": True,
                "type": "contact",
            }
        )

        self.assertFalse(company.c3_id_document_attachment_id)
