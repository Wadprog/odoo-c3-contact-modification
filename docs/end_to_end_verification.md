# End-to-End Verification

This checklist verifies the complete `c3_contact_modification` addon in the Odoo 19 Docker environment.

## Automated Verification

Run the post-install test suite from a clean database:

```bash
docker compose run --rm web odoo -d c3_contact_modification_e2e_test -i c3_contact_modification --test-enable --test-tags /c3_contact_modification --stop-after-init --without-demo=all
```

Expected result:

- The addon installs cleanly.
- Post-install tests complete with `0 failed`.
- The suite verifies gender model behavior, contact form view inheritance, required tags, protected tag behavior, and an end-to-end contact workflow.

Run the same command again with `-u c3_contact_modification` against an existing database when verifying upgrade behavior:

```bash
docker compose run --rm web odoo -d c3_contact_modification_e2e_test -u c3_contact_modification --test-enable --test-tags /c3_contact_modification --stop-after-init --without-demo=all
```

Expected result:

- The addon updates cleanly.
- Required contact tags are not duplicated.
- Protected tags remain protected.

## GitHub Actions

The repository CI runs the same addon-scoped test gate on every push and pull request:

```bash
docker compose run --rm web odoo -d c3_contact_modification_ci_test -i c3_contact_modification --test-enable --test-tags /c3_contact_modification --stop-after-init --without-demo=all
```

The `--test-tags /c3_contact_modification` flag is required. Without it, Odoo runs unrelated core/addon tests that are not the acceptance gate for this module.

## Manual UI Verification

Use the standard Contacts app. This addon must not add a standalone app, top-level menu, or separate contact workflow.

### Individual Contacts

- Open `Contacts`.
- Create an individual contact.
- Confirm the name field shows the placeholder `Last name first, then first name`.
- Confirm the `Gender` field appears on the main contact form.
- Try saving without gender and confirm Odoo blocks the save with `Gender is required for individual contacts.`
- Select `Male` or `Female` and confirm the contact saves.

### Company Contacts

- Create a company contact.
- Confirm the `Gender` field is hidden.
- Confirm the company saves without gender.

### Contact Tags

- Open `Contacts > Configuration > Contact Tags`.
- Confirm these tags exist exactly once:
  `Acheteur`, `Démarcheur`, `Professeur`, `Auteur`, `Fournisseur`, `Employé`, `Contractuel`, `Librairie`, `Ecole`, `Administration publique`, `ONG`, `Institution privée`.
- Assign one of the required tags to an individual contact.
- Assign one of the required tags to a company contact.
- Open one of the required tag records and try to rename, archive, or delete it.
- Confirm Odoo blocks the operation with `This contact tag is protected by the contact setup module.`
- Create a non-protected tag and confirm normal rename, archive, and delete behavior still works.

### French UI

- Switch the user language to French.
- Confirm `Gender` displays as `Sexe`.
- Confirm `Male` and `Female` display as `Homme` and `Femme`.
- Confirm the name placeholder displays as `Nom d'abord, puis prénom`.
- Confirm the missing-gender validation message displays as `Le sexe est obligatoire pour les contacts individuels.`
- Confirm the protected-tag error displays as `Cette étiquette de contact est protégée par le module de configuration des contacts.`
