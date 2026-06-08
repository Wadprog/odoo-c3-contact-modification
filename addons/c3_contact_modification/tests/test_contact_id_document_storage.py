"""Tests for attachment-backed contact ID document storage."""

from datetime import date

from odoo.tests import TransactionCase, new_test_user, tagged


VALID_PNG_DATA = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMB/"
    "axzZ3cAAAAASUVORK5CYII="
)
VALID_JPEG_DATA = (
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRof"
    "Hh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwh"
    "MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAAR"
    "CAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAg"
    "EDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcY"
    "GRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJip"
    "KTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6er"
    "x8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDB"
    "AcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRom"
    "JygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZa"
    "XmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+"
    "Pn6/9oADAMBAAIRAxEAPwD3+iiigD//2Q=="
)


@tagged("post_install", "-at_install")
class TestContactIdDocumentStorage(TransactionCase):
    def _create_partner(self):
        return self.env["res.partner"].create(
            {
                "name": "Doe Alice",
                "is_company": False,
                "type": "contact",
                "gender": "female",
                "date_of_birth": date(1990, 1, 2),
            }
        )

    def _id_document_attachments(self, partner):
        return self.env["ir.attachment"].search(
            [
                ("res_model", "=", "res.partner"),
                ("res_id", "=", partner.id),
                ("res_field", "=", "c3_id_document"),
            ]
        )

    def test_id_document_binary_field_is_attachment_backed(self):
        field = self.env["res.partner"]._fields["c3_id_document"]

        self.assertEqual(field.type, "binary")
        self.assertTrue(field.attachment)
        self.assertFalse(field.copy)

    def test_individual_contact_can_store_one_id_document(self):
        partner = self._create_partner()

        partner.write(
            {
                "c3_id_document": VALID_PNG_DATA,
                "c3_id_document_filename": "id-document.png",
            }
        )

        self.assertTrue(partner.c3_id_document)
        self.assertEqual(partner.c3_id_document_filename, "id-document.png")
        self.assertEqual(len(self._id_document_attachments(partner)), 1)

    def test_id_document_attachment_is_distinct_from_general_attachments(self):
        partner = self._create_partner()
        general_attachment = self.env["ir.attachment"].create(
            {
                "name": "general-note.png",
                "datas": VALID_PNG_DATA,
                "res_model": "res.partner",
                "res_id": partner.id,
            }
        )

        partner.c3_id_document = VALID_PNG_DATA

        id_document_attachment = self._id_document_attachments(partner)
        self.assertEqual(len(id_document_attachment), 1)
        self.assertNotEqual(id_document_attachment, general_attachment)

    def test_replacing_id_document_keeps_one_backing_attachment(self):
        partner = self._create_partner()
        partner.c3_id_document = VALID_PNG_DATA

        partner.c3_id_document = VALID_JPEG_DATA

        self.assertEqual(len(self._id_document_attachments(partner)), 1)

    def test_normal_contact_user_can_delete_id_document_and_backing_attachment(self):
        partner = self._create_partner()
        partner.write(
            {
                "c3_id_document": VALID_PNG_DATA,
                "c3_id_document_filename": "id-document.png",
            }
        )
        attachment = self._id_document_attachments(partner)
        contact_user = new_test_user(
            self.env,
            login="contact_document_editor",
            groups="base.group_user,base.group_partner_manager",
            gender="female",
        )

        partner.with_user(contact_user).write({"c3_id_document": False})

        self.assertFalse(attachment.exists())
        self.assertFalse(partner.c3_id_document)
        self.assertFalse(partner.c3_id_document_filename)
        self.assertFalse(self._id_document_attachments(partner))

    def test_company_contacts_start_without_id_document(self):
        company = self.env["res.partner"].create(
            {
                "name": "C3 Test Company",
                "is_company": True,
                "type": "contact",
            }
        )

        self.assertFalse(company.c3_id_document)
