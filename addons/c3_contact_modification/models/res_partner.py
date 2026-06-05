"""Contact model extensions."""

import base64
import binascii
import os

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


ID_DOCUMENT_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ID_DOCUMENT_ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}
ID_DOCUMENT_MAX_SIZE = 5 * 1024 * 1024


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

    @api.constrains("c3_id_document_attachment_id")
    def _check_c3_id_document_attachment(self):
        for partner in self:
            attachment = partner.c3_id_document_attachment_id
            if attachment:
                partner._validate_c3_id_document_attachment(attachment)

    def unlink(self):
        id_documents = self.mapped("c3_id_document_attachment_id")
        result = super().unlink()
        id_documents.exists().unlink()
        return result

    def _is_c3_individual_contact_without_gender(self):
        self.ensure_one()
        return not self.is_company and self.type == "contact" and not self.gender

    def _validate_c3_id_document_attachment(self, attachment):
        self.ensure_one()
        if not self._is_c3_supported_id_document_type(attachment):
            raise ValidationError(_("Only JPG and PNG identity document images are allowed."))

        if self._get_c3_attachment_size(attachment) > ID_DOCUMENT_MAX_SIZE:
            raise ValidationError(_("Identity document images must be 5 MB or smaller."))

    def _is_c3_supported_id_document_type(self, attachment):
        mimetype = (attachment.mimetype or "").lower()
        if mimetype:
            return mimetype in ID_DOCUMENT_ALLOWED_MIMETYPES

        _root, extension = os.path.splitext(attachment.name or "")
        return extension.lower() in ID_DOCUMENT_ALLOWED_EXTENSIONS

    def _get_c3_attachment_size(self, attachment):
        if attachment.file_size:
            return attachment.file_size

        try:
            return len(base64.b64decode(attachment.datas or b"", validate=True))
        except (binascii.Error, TypeError):
            return 0
