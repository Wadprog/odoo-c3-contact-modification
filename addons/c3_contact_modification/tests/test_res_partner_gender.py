"""Tests for the contact gender field."""

from datetime import date

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
                "date_of_birth": date(1990, 1, 2),
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
                "date_of_birth": date(1991, 4, 5),
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
                "date_of_birth": date(1992, 6, 7),
            }
        )

        self.assertFalse(partner.gender)

    def test_child_contact_does_not_require_gender(self):
        parent = self.env["res.partner"].create(
            {
                "name": "C3 Test Parent Company",
                "is_company": True,
                "type": "contact",
            }
        )
        partner = self.env["res.partner"].create(
            {
                "name": "C3 Test Child Contact",
                "parent_id": parent.id,
                "is_company": False,
                "type": "contact",
            }
        )

        self.assertFalse(partner.gender)
