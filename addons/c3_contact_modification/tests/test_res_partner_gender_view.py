"""Tests for the contact gender field view integration."""

from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerGenderView(TransactionCase):
    def _get_partner_form_arch(self):
        view = self.env["res.partner"].get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )
        return etree.fromstring(view["arch"].encode())

    def test_gender_field_is_present_on_main_contact_form(self):
        arch = self._get_partner_form_arch()

        gender_fields = arch.xpath("//field[@name='gender']")

        self.assertEqual(len(gender_fields), 1)
        self.assertEqual(gender_fields[0].get("invisible"), "is_company")

    def test_individual_name_field_shows_name_order_placeholder(self):
        arch = self._get_partner_form_arch()

        individual_name_fields = arch.xpath("//field[@name='name' and @invisible='is_company']")

        self.assertEqual(len(individual_name_fields), 1)
        self.assertEqual(
            individual_name_fields[0].get("placeholder"),
            "Last name first, then first name",
        )
