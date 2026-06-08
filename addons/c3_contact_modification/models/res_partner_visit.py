"""Visit records for C3 contact modification."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartnerVisit(models.Model):
    _name = "c3.contact.visit"
    _description = "Contact Visit"
    _order = "create_date desc, id desc"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact",
        required=True,
        ondelete="cascade",
        index=True,
    )
    visit_reason_id = fields.Many2one(
        comodel_name="c3.contact.visit.reason",
        string="Visit Reason",
        required=True,
        ondelete="restrict",
        index=True,
    )
    note = fields.Text(
        string="Note",
    )

    @api.model_create_multi
    def create(self, vals_list):
        visits = super().create(vals_list)
        return visits

    def write(self, vals):
        raise UserError(_("Visit records cannot be edited after creation."))

    def unlink(self):
        raise UserError(_("Visit records cannot be deleted after creation."))
