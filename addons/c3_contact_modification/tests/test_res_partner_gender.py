"""Tests for the contact gender field."""

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerGender(TransactionCase):
    def test_gender_field_is_registered(self):
        field = self.env["res.partner"]._fields["gender"]

        self.assertEqual(field.type, "selection")
        self.assertEqual(
            field.selection,
            [
                ("male", "Male"),
                ("female", "Female"),
            ],
        )

    def test_gender_value_can_be_stored_on_contact(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe John",
                "gender": "male",
            }
        )

        self.assertEqual(partner.gender, "male")
