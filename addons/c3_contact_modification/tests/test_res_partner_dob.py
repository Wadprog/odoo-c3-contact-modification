"""Tests for the contact date of birth field."""

from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerDateOfBirth(TransactionCase):
    def test_date_of_birth_field_is_registered(self):
        field = self.env["res.partner"]._fields["date_of_birth"]

        self.assertEqual(field.type, "date")

    def test_date_of_birth_value_can_be_stored_on_contact(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe John",
                "gender": "male",
                "date_of_birth": date(1990, 1, 2),
            }
        )

        self.assertEqual(partner.date_of_birth, date(1990, 1, 2))

    def test_individual_contact_requires_date_of_birth_on_create(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Date of birth is required for individual contacts.",
        ):
            self.env["res.partner"].create(
                {
                    "name": "Doe Jane",
                    "is_company": False,
                    "type": "contact",
                }
            )

    def test_individual_contact_requires_date_of_birth_on_write(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe Jane",
                "is_company": False,
                "type": "contact",
                "gender": "female",
                "date_of_birth": date(1991, 4, 5),
            }
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Date of birth is required for individual contacts.",
        ):
            partner.write({"date_of_birth": False})

    def test_company_contact_does_not_require_date_of_birth(self):
        partner = self.env["res.partner"].create(
            {
                "name": "C3 Test Company",
                "is_company": True,
                "type": "contact",
            }
        )

        self.assertFalse(partner.date_of_birth)

    def test_non_contact_address_does_not_require_date_of_birth(self):
        partner = self.env["res.partner"].create(
            {
                "name": "C3 Test Invoice Address",
                "is_company": False,
                "type": "invoice",
            }
        )

        self.assertFalse(partner.date_of_birth)

    def test_future_date_of_birth_is_rejected_on_create(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Date of birth cannot be in the future.",
        ):
            self.env["res.partner"].create(
                {
                    "name": "Doe Jane",
                    "is_company": False,
                    "type": "contact",
                    "date_of_birth": date.today() + timedelta(days=1),
                }
            )

    def test_future_date_of_birth_is_rejected_on_write(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe Jane",
                "is_company": False,
                "type": "contact",
                "date_of_birth": date(1992, 6, 7),
                "gender": "female",
            }
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Date of birth cannot be in the future.",
        ):
            partner.write({"date_of_birth": date.today() + timedelta(days=1)})
