"""Contact model extensions."""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
        index=True,
    )

    @api.constrains("gender", "is_company", "type")
    def _check_gender_required_for_individual_contacts(self):
        for partner in self:
            if partner._is_c3_individual_contact_without_gender():
                raise ValidationError(_("Gender is required for individual contacts."))

    def _is_c3_individual_contact_without_gender(self):
        self.ensure_one()
        return not self.is_company and self.type == "contact" and not self.gender
