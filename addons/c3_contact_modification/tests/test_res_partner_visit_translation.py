"""Tests for visit translations."""

from lxml import etree

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerVisitTranslation(TransactionCase):
    def _get_partner_form_arch(self, lang=None):
        partner = self.env["res.partner"]
        if lang:
            partner = partner.with_context(lang=lang)
        view = partner.get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )
        return etree.fromstring(view["arch"].encode())

    def test_visit_labels_are_translated_in_french(self):
        arch = self._get_partner_form_arch(lang="fr_FR")

        visit_page = arch.xpath("//page[@name='c3_contact_visits']")[0]
        visit_fields = {
            field.get("name"): field.get("string")
            for field in arch.xpath("//page[@name='c3_contact_visits']//field")
        }

        self.assertEqual(visit_page.get("string"), "Visites")
        self.assertEqual(visit_fields["visit_reason_id"], "Motif de visite")
        self.assertEqual(visit_fields["site_id"], "Site")
        self.assertEqual(visit_fields["note"], "Note")

    def test_visit_validation_messages_are_translated_in_french(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Doe John",
                "is_company": False,
                "type": "contact",
            }
        )
        site = self.env["res.partner"].create(
            {
                "name": "C3 Test Site",
                "is_company": False,
                "type": "contact",
            }
        )
        reason = self.env["c3.contact.visit.reason"].create({"name": "Visit"})

        with self.assertRaisesRegex(ValidationError, "Le motif de visite est obligatoire."):
            self.env["c3.contact.visit"].with_context(lang="fr_FR").create(
                {
                    "partner_id": partner.id,
                    "site_id": site.id,
                }
            )

        with self.assertRaisesRegex(ValidationError, "Le site est obligatoire."):
            self.env["c3.contact.visit"].with_context(lang="fr_FR").create(
                {
                    "partner_id": partner.id,
                    "visit_reason_id": reason.id,
                }
            )
