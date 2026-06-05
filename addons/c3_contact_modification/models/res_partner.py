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
    c3_id_document_attachment_id = fields.Many2one(
        comodel_name="ir.attachment",
        string="ID Document",
        copy=False,
        ondelete="set null",
    )

    @api.constrains("gender", "is_company", "type")
    def _check_gender_required_for_individual_contacts(self):
        for partner in self:
            if partner._is_c3_individual_contact_without_gender():
                raise ValidationError(_("Gender is required for individual contacts."))

    @api.constrains("c3_id_document_attachment_id", "is_company")
    def _check_c3_id_document_individual_only(self):
        for partner in self:
            if partner.is_company and partner.c3_id_document_attachment_id:
                raise ValidationError(
                    _(
                        "ID documents are only available for individual contacts. "
                        "Remove the ID document before changing this contact to a company."
                    )
                )

    def unlink(self):
        id_documents = self.mapped("c3_id_document_attachment_id")
        result = super().unlink()
        id_documents.exists().unlink()
        return result

    def _is_c3_individual_contact_without_gender(self):
        self.ensure_one()
        return not self.is_company and self.type == "contact" and not self.gender
