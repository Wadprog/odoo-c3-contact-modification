"""Contact model extensions."""

import base64
import binascii

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.mimetypes import guess_mimetype


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
    c3_id_document = fields.Binary(
        string="ID Document",
        attachment=True,
        copy=False,
    )
    c3_id_document_filename = fields.Char(
        string="ID Document Filename",
        copy=False,
    )

    @api.constrains("gender", "is_company", "type")
    def _check_gender_required_for_individual_contacts(self):
        for partner in self:
            if partner._is_c3_individual_contact_without_gender():
                raise ValidationError(_("Gender is required for individual contacts."))

    @api.constrains("c3_id_document", "is_company")
    def _check_c3_id_document_individual_only(self):
        for partner in self:
            if partner.is_company and partner.c3_id_document:
                raise ValidationError(
                    _(
                        "ID documents are only available for individual contacts. "
                        "Remove the ID document before changing this contact to a company."
                    )
                )

    @api.constrains("c3_id_document")
    def _check_c3_id_document(self):
        for partner in self:
            if partner.c3_id_document:
                partner._validate_c3_id_document(partner.c3_id_document)

    def _is_c3_individual_contact_without_gender(self):
        self.ensure_one()
        return not self.is_company and self.type == "contact" and not self.gender

    def _validate_c3_id_document(self, encoded_document):
        self.ensure_one()
        document = self._decode_c3_id_document(encoded_document)
        if len(document) > ID_DOCUMENT_MAX_SIZE:
            raise ValidationError(_("Identity document images must be 5 MB or smaller."))

        if guess_mimetype(document) not in ID_DOCUMENT_ALLOWED_MIMETYPES:
            raise ValidationError(_("Only JPG and PNG identity document images are allowed."))

    def _decode_c3_id_document(self, encoded_document):
        try:
            return base64.b64decode(encoded_document, validate=True)
        except (binascii.Error, TypeError):
            raise ValidationError(_("Only JPG and PNG identity document images are allowed."))
