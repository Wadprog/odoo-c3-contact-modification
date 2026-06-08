"""Tests for contact ID document chatter audit logging."""

from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, new_test_user, tagged
from odoo.tools import html2plaintext

from .test_contact_id_document_storage import VALID_JPEG_DATA, VALID_PNG_DATA


@tagged("post_install", "-at_install")
class TestContactIdDocumentAuditLog(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.lang"]._activate_lang("fr_FR")

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

    def _message_bodies(self, partner):
        return [html2plaintext(message.body or "") for message in partner.message_ids]

    def _id_document_log_messages(self, partner):
        markers = (
            "uploaded an ID document",
            "replaced the ID document",
            "deleted the ID document",
            "a téléversé une pièce d'identité",
            "a remplacé la pièce d'identité",
            "a supprimé la pièce d'identité",
        )
        return [
            message
            for message in partner.message_ids
            if any(marker in html2plaintext(message.body or "") for marker in markers)
        ]

    def _latest_id_document_log_body(self, partner):
        logs = self._id_document_log_messages(partner)
        self.assertTrue(logs)
        return html2plaintext(logs[0].body or "")

    def _latest_message_body(self, partner):
        self.assertTrue(partner.message_ids)
        return html2plaintext(partner.message_ids[0].body or "")

    def _assert_latest_id_document_log_contains(self, partner, text):
        self.assertIn(text, self._latest_id_document_log_body(partner))

    def _assert_latest_log_contains(self, partner, text):
        self.assertIn(text, self._latest_message_body(partner))

    def test_uploading_id_document_creates_chatter_log(self):
        partner = self._create_partner()
        initial_log_count = len(self._id_document_log_messages(partner))

        partner.write(
            {
                "c3_id_document": VALID_PNG_DATA,
                "c3_id_document_filename": "id-document.png",
            }
        )

        self.assertEqual(len(self._id_document_log_messages(partner)), initial_log_count + 1)
        self._assert_latest_id_document_log_contains(partner, "uploaded an ID document")
        self._assert_latest_id_document_log_contains(partner, self.env.user.display_name)

    def test_creating_contact_with_id_document_creates_upload_log(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe Alice",
                "is_company": False,
                "type": "contact",
                "gender": "female",
                "date_of_birth": date(1990, 1, 2),
                "c3_id_document": VALID_PNG_DATA,
                "c3_id_document_filename": "id-document.png",
            }
        )

        self.assertEqual(len(self._id_document_log_messages(partner)), 1)
        self._assert_latest_id_document_log_contains(partner, "uploaded an ID document")

    def test_replacing_id_document_creates_replacement_log(self):
        partner = self._create_partner()
        partner.c3_id_document = VALID_PNG_DATA
        initial_log_count = len(self._id_document_log_messages(partner))

        partner.c3_id_document = VALID_JPEG_DATA

        self.assertEqual(len(self._id_document_log_messages(partner)), initial_log_count + 1)
        self._assert_latest_id_document_log_contains(partner, "replaced the ID document")
        self.assertNotIn(
            "uploaded an ID document",
            self._latest_id_document_log_body(partner),
        )

    def test_deleting_id_document_creates_deletion_log(self):
        partner = self._create_partner()
        partner.write(
            {
                "c3_id_document": VALID_PNG_DATA,
                "c3_id_document_filename": "id-document.png",
            }
        )
        initial_log_count = len(self._id_document_log_messages(partner))

        partner.write({"c3_id_document": False})

        self.assertEqual(len(self._id_document_log_messages(partner)), initial_log_count + 1)
        self._assert_latest_id_document_log_contains(partner, "deleted the ID document")

    def test_unchanged_id_document_write_does_not_create_log(self):
        partner = self._create_partner()
        partner.c3_id_document = VALID_PNG_DATA
        initial_log_count = len(self._id_document_log_messages(partner))

        partner.write({"c3_id_document": VALID_PNG_DATA})

        self.assertEqual(len(self._id_document_log_messages(partner)), initial_log_count)

    def test_unrelated_write_does_not_create_id_document_log(self):
        partner = self._create_partner()
        partner.c3_id_document = VALID_PNG_DATA
        initial_log_count = len(self._id_document_log_messages(partner))

        partner.write({"name": "Doe Alice Updated"})

        self.assertEqual(len(self._id_document_log_messages(partner)), initial_log_count)

    def test_company_contact_id_document_change_does_not_create_log(self):
        company = self.env["res.partner"].create(
            {
                "name": "C3 Test Company",
                "is_company": True,
                "type": "contact",
            }
        )

        company.write({"c3_id_document": False})
        self.assertFalse(self._id_document_log_messages(company))

        with self.assertRaises(ValidationError):
            company.write({"c3_id_document": VALID_PNG_DATA})

        self.assertFalse(self._id_document_log_messages(company))

    def test_normal_contact_user_can_create_id_document_log(self):
        partner = self._create_partner()
        contact_user = new_test_user(
            self.env,
            login="contact_document_logger",
            groups="base.group_user,base.group_partner_manager",
            gender="female",
        )

        partner.with_user(contact_user).write({"c3_id_document": VALID_PNG_DATA})

        self._assert_latest_id_document_log_contains(partner, contact_user.display_name)
        self._assert_latest_id_document_log_contains(partner, "uploaded an ID document")

    def test_french_id_document_log_messages(self):
        partner = self._create_partner().with_context(lang="fr_FR")

        partner.write({"c3_id_document": VALID_PNG_DATA})
        self._assert_latest_id_document_log_contains(partner, "a téléversé une pièce d'identité.")

        partner.write({"c3_id_document": VALID_JPEG_DATA})
        self._assert_latest_id_document_log_contains(partner, "a remplacé la pièce d'identité.")

        partner.write({"c3_id_document": False})
        self._assert_latest_id_document_log_contains(partner, "a supprimé la pièce d'identité.")
