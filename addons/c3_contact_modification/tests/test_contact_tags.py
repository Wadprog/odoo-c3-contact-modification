"""Tests for required contact tag setup."""

from odoo import Command
from odoo.tests import TransactionCase, tagged

from odoo.addons.c3_contact_modification.models.res_partner_category import (
    C3_CONTACT_TAGS,
    MODULE,
)


@tagged("post_install", "-at_install")
class TestContactTags(TransactionCase):
    def test_required_contact_tags_exist(self):
        categories = self.env["res.partner.category"]

        for _xmlid_name, tag_name in C3_CONTACT_TAGS:
            with self.subTest(tag_name=tag_name):
                self.assertTrue(categories.search([("name", "=", tag_name)], limit=1))

    def test_contact_tag_setup_is_idempotent(self):
        categories = self.env["res.partner.category"]
        before_counts = {
            tag_name: categories.search_count([("name", "=", tag_name)])
            for _xmlid_name, tag_name in C3_CONTACT_TAGS
        }

        categories._ensure_c3_contact_tags()

        after_counts = {
            tag_name: categories.search_count([("name", "=", tag_name)])
            for _xmlid_name, tag_name in C3_CONTACT_TAGS
        }
        self.assertEqual(after_counts, before_counts)

    def test_required_contact_tags_have_stable_external_ids(self):
        model_data = self.env["ir.model.data"]

        for xmlid_name, tag_name in C3_CONTACT_TAGS:
            with self.subTest(tag_name=tag_name):
                external_id = model_data.search(
                    [
                        ("module", "=", MODULE),
                        ("name", "=", xmlid_name),
                    ],
                    limit=1,
                )
                self.assertTrue(external_id)
                self.assertEqual(external_id.model, "res.partner.category")
                self.assertEqual(external_id.res_id, self.env.ref(f"{MODULE}.{xmlid_name}").id)

    def test_required_contact_tags_can_be_assigned_to_people_and_companies(self):
        tag = self.env.ref(f"{MODULE}.{C3_CONTACT_TAGS[0][0]}")
        partners = self.env["res.partner"]

        person = partners.create(
            {
                "name": "Doe John",
                "is_company": False,
                "gender": "male",
                "category_id": [Command.link(tag.id)],
            }
        )
        company = partners.create(
            {
                "name": "C3 Test Company",
                "is_company": True,
                "category_id": [Command.link(tag.id)],
            }
        )

        self.assertIn(tag, person.category_id)
        self.assertIn(tag, company.category_id)
