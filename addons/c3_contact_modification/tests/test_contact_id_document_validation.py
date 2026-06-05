"""Tests for contact ID document binary validation."""

import base64

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged

from .test_contact_id_document_storage import VALID_JPEG_DATA, VALID_PNG_DATA


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

    def test_jpg_upload_is_accepted(self):
        partner = self._create_partner()

        partner.write(
            {
                "c3_id_document": VALID_JPEG_DATA,
                "c3_id_document_filename": "id-document.jpg",
            }
        )

        self.assertTrue(partner.c3_id_document)

    def test_jpeg_upload_is_accepted(self):
        partner = self._create_partner()

        partner.write(
            {
                "c3_id_document": VALID_JPEG_DATA,
                "c3_id_document_filename": "id-document.jpeg",
            }
        )

        self.assertTrue(partner.c3_id_document)

    def test_png_upload_is_accepted(self):
        partner = self._create_partner()

        partner.c3_id_document = VALID_PNG_DATA

        self.assertTrue(partner.c3_id_document)

    def test_unsupported_image_type_is_rejected(self):
        partner = self._create_partner()
        gif_data = base64.b64encode(b"GIF89a" + (b"\0" * 20)).decode()

        with self.assertRaisesRegex(
            ValidationError,
            "Only JPG and PNG identity document images are allowed.",
        ):
            partner.c3_id_document = gif_data

    def test_non_image_file_type_is_rejected(self):
        partner = self._create_partner()
        text_data = base64.b64encode(b"not an image").decode()

        with self.assertRaisesRegex(
            ValidationError,
            "Only JPG and PNG identity document images are allowed.",
        ):
            partner.c3_id_document = text_data

    def test_files_larger_than_5_mb_are_rejected(self):
        partner = self._create_partner()
        oversized_png = base64.b64encode(
            b"\x89PNG\r\n\x1a\n" + (b"\0" * (5 * 1024 * 1024))
        ).decode()

        with self.assertRaisesRegex(
            ValidationError,
            "Identity document images must be 5 MB or smaller.",
        ):
            partner.c3_id_document = oversized_png
