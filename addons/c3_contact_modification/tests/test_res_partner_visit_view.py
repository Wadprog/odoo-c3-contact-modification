"""Tests for the contact visit form tab."""

from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerVisitView(TransactionCase):
    def _get_partner_form_arch(self):
        view = self.env["res.partner"].get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )
        return etree.fromstring(view["arch"].encode())

    def test_visit_tab_is_after_id_document_and_hidden_for_companies(self):
        arch = self._get_partner_form_arch()

        id_document_page = arch.xpath("//page[@name='c3_id_document']")[0]
        visit_page = arch.xpath("//page[@name='c3_contact_visits']")[0]

        self.assertEqual(visit_page.get("string"), "Visits")
        self.assertEqual(visit_page.get("invisible"), "is_company")
        self.assertIs(id_document_page.getnext(), visit_page)

    def test_visit_tab_contains_a_simple_list(self):
        arch = self._get_partner_form_arch()

        visit_list = arch.xpath("//page[@name='c3_contact_visits']//field[@name='visit_ids']/list")[0]
        field_names = [field.get("name") for field in visit_list.xpath("./field")]

        self.assertEqual(field_names, ["create_date", "visit_reason_id", "note"])
