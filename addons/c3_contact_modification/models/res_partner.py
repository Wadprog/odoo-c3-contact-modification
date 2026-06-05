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

    @api.model_create_multi
    def create(self, vals_list):
        self._c3_normalize_company_type(vals_list)
        self._c3_normalize_id_document_deletion(vals_list)
        partners = super().create(vals_list)
        partners._c3_log_id_document_uploads_from_create(vals_list)
        return partners

    def write(self, vals):
        self._c3_normalize_company_type([vals])
        self._c3_normalize_id_document_deletion([vals])
        previous_documents = {}
        if "c3_id_document" in vals:
            previous_documents = {partner.id: partner.c3_id_document for partner in self}
        result = super().write(vals)
        if "c3_id_document" in vals:
            self._c3_log_id_document_changes_from_write(vals, previous_documents)
        return result

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

    @api.model
    def _c3_normalize_company_type(self, vals_list):
        for vals in vals_list:
            if "company_type" in vals:
                vals["is_company"] = vals["company_type"] == "company"

    @api.model
    def _c3_normalize_id_document_deletion(self, vals_list):
        for vals in vals_list:
            if "c3_id_document" in vals and vals["c3_id_document"] is False:
                vals["c3_id_document_filename"] = False

    def _c3_log_id_document_uploads_from_create(self, vals_list):
        for partner, vals in zip(self, vals_list):
            if partner.is_company or not vals.get("c3_id_document"):
                continue
            partner._c3_post_id_document_log("upload")

    def _c3_log_id_document_changes_from_write(self, vals, previous_documents):
        new_document = vals.get("c3_id_document")
        for partner in self:
            if partner.is_company:
                continue
            previous_document = previous_documents.get(partner.id)
            if new_document is False:
                if previous_document:
                    partner._c3_post_id_document_log("delete")
            elif new_document:
                if not previous_document:
                    partner._c3_post_id_document_log("upload")
                elif new_document != previous_document:
                    partner._c3_post_id_document_log("replace")

    def _c3_post_id_document_log(self, action):
        self.ensure_one()
        if not hasattr(self, "message_post"):
            return

        user_name = self.env.user.display_name
        messages = {
            "upload": _("%(user)s uploaded an ID document.", user=user_name),
            "replace": _("%(user)s replaced the ID document.", user=user_name),
            "delete": _("%(user)s deleted the ID document.", user=user_name),
        }
        self.message_post(
            body=messages[action],
            message_type="notification",
            subtype_xmlid="mail.mt_note",
        )
