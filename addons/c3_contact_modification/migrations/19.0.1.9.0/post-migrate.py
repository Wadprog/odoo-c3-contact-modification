"""Preserve migrated ID document attachment filenames."""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE res_partner AS partner
           SET c3_id_document_filename = attachment.name
          FROM ir_attachment AS attachment
         WHERE attachment.res_model = 'res.partner'
           AND attachment.res_id = partner.id
           AND attachment.res_field = 'c3_id_document'
           AND partner.c3_id_document_filename IS NULL
        """
    )
