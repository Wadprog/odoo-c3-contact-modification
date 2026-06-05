# C3 Contact Modification

[![Odoo Addon Tests](https://github.com/Wadprog/odoo-c3-contact-modification/actions/workflows/odoo-tests.yml/badge.svg)](https://github.com/Wadprog/odoo-c3-contact-modification/actions/workflows/odoo-tests.yml)

An Odoo 19 addon that extends the standard Contacts app with consistent person
data, protected classification tags, and secure identity-document handling.

**Module page:** https://wadprog.github.io/odoo-c3-contact-modification/

<img src="docs/icon.png" alt="C3 Contact Modification icon" width="160">

## Features

- Adds a required **Gender** field for individual contacts:
  - Male / Homme
  - Female / Femme
- Hides gender for companies.
- Guides users to enter individual names with the last name first.
- Installs protected contact tags for individuals and companies:
  - Acheteur
  - Démarcheur
  - Professeur
  - Auteur
  - Fournisseur
  - Employé
  - Contractuel
  - Librairie
  - Ecole
  - Administration publique
  - ONG
  - Institution privée
- Prevents protected tags from being renamed, archived, or deleted.
- Lets individual contacts store one attachment-backed ID document.
- Accepts JPG, JPEG, and PNG ID images up to 5 MB.
- Supports upload, download, replace, delete, and click-to-preview workflows.
- Loads the full ID image only after the user clicks Preview.
- Provides English and French labels and validation messages.

The addon extends Odoo's existing `res.partner` model and Contacts form. It
does not add a separate application, menu, or parallel contact workflow.

## Compatibility

| Component | Supported |
| --- | --- |
| Odoo | 19.0 |
| Languages | English, French |
| License | LGPL-3 |
| Module name | `c3_contact_modification` |

## Installation

Add the repository's `addons` directory to the Odoo addons path, update the app
list, and install the module:

```bash
odoo -d <database> -i c3_contact_modification --stop-after-init
```

Upgrade an existing installation after deploying changes:

```bash
odoo -d <database> -u c3_contact_modification --stop-after-init
```

## Usage

### Individual contacts

1. Open the standard **Contacts** app.
2. Create or edit an individual contact.
3. Enter the last name followed by the first name.
4. Select Male or Female.
5. Assign any relevant C3 contact tags.

### ID documents

1. Open an existing individual contact.
2. Open the **ID Document** tab.
3. Upload a JPG, JPEG, or PNG image no larger than 5 MB.
4. Save the contact.
5. Use Preview, Download, Replace, or Delete as needed.

The ID Document tab is not displayed for companies. A contact with an ID
document cannot be changed into a company until the document is removed.

## Security and privacy

- ID documents use Odoo's attachment-backed Binary field storage.
- Access follows normal Odoo contact and attachment permissions.
- Preview uses an authenticated `res.partner` field route.
- Preview does not create or expose a public document URL.
- Opening a contact or the ID Document tab does not load the full image.
- Backend validation remains authoritative if frontend validation is bypassed.

## Local development

The repository includes a Docker Compose setup for Odoo 19 and PostgreSQL.

Start the services:

```bash
docker compose up -d
```

Open Odoo at:

```text
http://localhost:8069
```

Stop the services:

```bash
docker compose down
```

## Testing

Run the complete addon test suite:

```bash
docker compose run --rm web odoo \
  -d c3_contact_modification_test \
  -i c3_contact_modification \
  --test-enable \
  --test-tags /c3_contact_modification \
  --stop-after-init \
  --without-demo=all
```

GitHub Actions runs the addon suite on every push and pull request to `main`.
Frontend behavior tests are registered in `web.assets_unit_tests`.

## Project structure

```text
addons/c3_contact_modification/  Odoo addon
docs/                            GitHub Pages site, PRDs, and verification guide
.github/workflows/               Continuous integration
docker-compose.yaml              Local Odoo and PostgreSQL services
```

## Documentation

- [Module page](https://wadprog.github.io/odoo-c3-contact-modification/)
- [Contact extension PRD](docs/contact_extension_prd.md)
- [ID document PRD](docs/contact_id_document_prd.md)
- [End-to-end verification guide](docs/end_to_end_verification.md)
- [Addon README](addons/c3_contact_modification/README.md)

## License

This addon is licensed under [LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html).
