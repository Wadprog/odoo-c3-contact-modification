"""Migrate explicit ID document attachments to the attachment-backed binary field."""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE ir_attachment AS attachment
           SET res_model = 'res.partner',
               res_id = partner.id,
               res_field = 'c3_id_document'
          FROM res_partner AS partner
         WHERE partner.c3_id_document_attachment_id = attachment.id
           AND partner.c3_id_document_attachment_id IS NOT NULL
        """
    )
