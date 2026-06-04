"""Tests for the contact gender field view integration."""

from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerGenderView(TransactionCase):
    def test_gender_field_is_present_on_main_contact_form(self):
        view = self.env["res.partner"].get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"].encode())

        gender_fields = arch.xpath("//field[@name='gender']")

        self.assertEqual(len(gender_fields), 1)
        self.assertEqual(gender_fields[0].get("invisible"), "is_company")
