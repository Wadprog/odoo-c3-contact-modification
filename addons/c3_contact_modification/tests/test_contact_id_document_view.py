"""Tests for the contact ID document form tab."""

from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestContactIdDocumentView(TransactionCase):
    def _get_partner_form_arch(self):
        view = self.env["res.partner"].get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )
        return etree.fromstring(view["arch"].encode())

    def test_id_document_tab_is_after_notes_and_hidden_for_companies(self):
        arch = self._get_partner_form_arch()

        notes_page = arch.xpath("//page[@name='internal_notes']")[0]
        id_document_page = arch.xpath("//page[@name='c3_id_document']")[0]

        self.assertEqual(id_document_page.get("string"), "ID Document")
        self.assertEqual(id_document_page.get("invisible"), "is_company")
        self.assertIs(notes_page.getnext(), id_document_page)

    def test_id_document_field_uses_standard_binary_upload_controls(self):
        arch = self._get_partner_form_arch()

        id_document_field = arch.xpath(
            "//page[@name='c3_id_document']//field[@name='c3_id_document']"
        )[0]

        self.assertEqual(
            id_document_field.get("filename"),
            "c3_id_document_filename",
        )
        self.assertEqual(
            id_document_field.get("options"),
            "{'accepted_file_extensions': '.jpg,.jpeg,.png', "
            "'allowed_mime_type': 'image/jpeg,image/png'}",
        )

    def test_id_document_filename_field_is_hidden(self):
        arch = self._get_partner_form_arch()

        filename_field = arch.xpath(
            "//page[@name='c3_id_document']//field[@name='c3_id_document_filename']"
        )[0]

        self.assertEqual(filename_field.get("invisible"), "1")
