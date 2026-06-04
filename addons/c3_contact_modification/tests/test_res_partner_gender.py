"""Tests for the contact gender field."""

from odoo.exceptions import ValidationError
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

    def test_individual_contact_requires_gender_on_create(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Gender is required for individual contacts.",
        ):
            self.env["res.partner"].create(
                {
                    "name": "Doe Jane",
                    "is_company": False,
                    "type": "contact",
                }
            )

    def test_individual_contact_requires_gender_on_write(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe Jane",
                "is_company": False,
                "type": "contact",
                "gender": "female",
            }
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Gender is required for individual contacts.",
        ):
            partner.write({"gender": False})

    def test_company_contact_does_not_require_gender(self):
        partner = self.env["res.partner"].create(
            {
                "name": "C3 Test Company",
                "is_company": True,
                "type": "contact",
            }
        )

        self.assertFalse(partner.gender)

    def test_non_contact_address_does_not_require_gender(self):
        partner = self.env["res.partner"].create(
            {
                "name": "C3 Test Invoice Address",
                "is_company": False,
                "type": "invoice",
            }
        )

        self.assertFalse(partner.gender)
