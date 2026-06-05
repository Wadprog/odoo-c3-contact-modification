"""Tests for contact ID document attachment validation."""

import base64

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged

from .test_contact_id_document_storage import VALID_PNG_DATA


@tagged("post_install", "-at_install")
class TestContactIdDocumentValidation(TransactionCase):
    def _create_partner(self):
        return self.env["res.partner"].create(
            {
                "name": "Doe Alice",
                "is_company": False,
                "type": "contact",
                "gender": "female",
            }
        )

    def _create_attachment(self, partner, name, mimetype, datas=VALID_PNG_DATA):
        return self.env["ir.attachment"].create(
            {
                "name": name,
                "datas": datas,
                "mimetype": mimetype,
                "res_model": "res.partner",
                "res_id": partner.id,
            }
        )

    def test_jpg_upload_is_accepted(self):
        partner = self._create_partner()
        attachment = self._create_attachment(partner, "id-document.jpg", "image/jpeg")

        partner.c3_id_document_attachment_id = attachment

        self.assertEqual(partner.c3_id_document_attachment_id, attachment)

    def test_jpeg_upload_is_accepted(self):
        partner = self._create_partner()
        attachment = self._create_attachment(partner, "id-document.jpeg", "image/jpeg")

        partner.c3_id_document_attachment_id = attachment

        self.assertEqual(partner.c3_id_document_attachment_id, attachment)

    def test_png_upload_is_accepted(self):
        partner = self._create_partner()
        attachment = self._create_attachment(partner, "id-document.png", "image/png")

        partner.c3_id_document_attachment_id = attachment

        self.assertEqual(partner.c3_id_document_attachment_id, attachment)

    def test_unsupported_file_type_is_rejected(self):
        partner = self._create_partner()
        attachment = self._create_attachment(partner, "id-document.gif", "image/gif")

        with self.assertRaisesRegex(
            ValidationError,
            "Only JPG and PNG identity document images are allowed.",
        ):
            partner.c3_id_document_attachment_id = attachment

    def test_non_image_file_type_is_rejected(self):
        partner = self._create_partner()
        attachment = self._create_attachment(
            partner,
            "id-document.txt",
            "text/plain",
            base64.b64encode(b"not an image").decode(),
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Only JPG and PNG identity document images are allowed.",
        ):
            partner.c3_id_document_attachment_id = attachment

    def test_files_larger_than_5_mb_are_rejected(self):
        partner = self._create_partner()
        oversized_data = base64.b64encode(b"x" * ((5 * 1024 * 1024) + 1)).decode()
        attachment = self._create_attachment(
            partner,
            "id-document.png",
            "image/png",
            oversized_data,
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Identity document images must be 5 MB or smaller.",
        ):
            partner.c3_id_document_attachment_id = attachment
