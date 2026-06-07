"""Tests for the contact date of birth field view integration."""

from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerDateOfBirthView(TransactionCase):
    def _get_partner_form_arch(self):
        view = self.env["res.partner"].get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )
        return etree.fromstring(view["arch"].encode())

    def test_date_of_birth_field_is_present_on_main_contact_form(self):
        arch = self._get_partner_form_arch()

        dob_fields = arch.xpath("//field[@name='date_of_birth']")

        self.assertEqual(len(dob_fields), 1)
        self.assertEqual(dob_fields[0].get("invisible"), "is_company")
