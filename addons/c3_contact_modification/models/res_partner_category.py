"""Contact tag setup for C3 contact modification."""

from odoo import api, models


MODULE = "c3_contact_modification"

C3_CONTACT_TAGS = [
    ("contact_tag_acheteur", "Acheteur"),
    ("contact_tag_demarcheur", "Démarcheur"),
    ("contact_tag_professeur", "Professeur"),
    ("contact_tag_auteur", "Auteur"),
    ("contact_tag_fournisseur", "Fournisseur"),
    ("contact_tag_employe", "Employé"),
    ("contact_tag_contractuel", "Contractuel"),
    ("contact_tag_librairie", "Librairie"),
    ("contact_tag_ecole", "Ecole"),
    ("contact_tag_administration_publique", "Administration publique"),
    ("contact_tag_ong", "ONG"),
    ("contact_tag_institution_privee", "Institution privée"),
]


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    @api.model
    def _ensure_c3_contact_tags(self):
        model_data = self.env["ir.model.data"].sudo()

        for xmlid_name, tag_name in C3_CONTACT_TAGS:
            tag = self.search([("name", "=", tag_name)], limit=1)
            if not tag:
                tag = self.create({"name": tag_name})

            external_id = model_data.search(
                [
                    ("module", "=", MODULE),
                    ("name", "=", xmlid_name),
                ],
                limit=1,
            )
            values = {
                "module": MODULE,
                "name": xmlid_name,
                "model": self._name,
                "res_id": tag.id,
                "noupdate": True,
            }
            if external_id:
                external_id.write(values)
            else:
                model_data.create(values)

        return True
