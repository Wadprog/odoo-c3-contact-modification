# Odoo 19 List View Note

## Note

In this Odoo 19 environment, standard list views should use the `list` view type and `list,form` in `view_mode`.

Using the older `tree` syntax can fail module installation with:

- `Invalid view type: 'tree'`

This repository should use `list` for new configuration and administrative views that display records in tabular form.
