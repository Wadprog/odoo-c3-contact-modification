"""Visit reason records for C3 contact modification."""

from odoo import fields, models


class ResPartnerVisitReason(models.Model):
    _name = "c3.contact.visit.reason"
    _description = "Contact Visit Reason"
    _order = "name"

    name = fields.Char(
        string="Visit Reason",
        required=True,
        index=True,
    )
