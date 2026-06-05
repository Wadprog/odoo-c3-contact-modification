# Odoo Contact Setup PRD

## Problem Statement

The Odoo 19 Contacts app needs to capture a contact's sex/gender for individual contacts and consistently provide a protected set of predefined contact tags used by the organization. Today, there is no dedicated sex/gender field on contacts, and users must rely on manually creating tags. This makes contact segmentation inconsistent and allows important tag names to be changed or removed accidentally.

## Solution

Build a custom Odoo 19 addon that extends the existing Contacts app. The addon will modify the `res.partner` model to add a sex/gender selection field, inherit the existing contact form to display that field only for individual contacts, and automatically create the required contact categories/tags when the module is installed or updated.

The field must support English and French user interfaces:

- English label: `Gender`
- French label: `Sexe`
- English values: `Male`, `Female`
- French values: `Homme`, `Femme`

The required tags must be available for manual assignment to both individuals and companies. They must be protected from deletion, renaming, archiving, or deactivation by every user, including administrators.

When users create or edit an individual contact, the main contact form must guide them to enter the contact name in a consistent order: last name first, then first name.

The module must not introduce a standalone app, menu, or separate custom view flow. Users should keep working inside the standard Odoo Contacts app.

## User Stories

1. As a Contacts user, I want to record an individual contact's sex/gender, so that contact records contain the information needed for internal classification.
2. As a Contacts user, I want the sex/gender field to appear directly in the standard contact form for individuals, so that I do not need to open a separate screen.
3. As a Contacts user, I want the gender field to be stored on the contact record, so that the value remains available anywhere `res.partner` is used.
4. As a Contacts user, I want the gender field to be searchable or filterable where Odoo supports contact field search behavior, so that I can segment contacts by gender.
5. As an administrator, I want the required contact tags to be created automatically, so that users do not need to create them manually after installing the module.
6. As an administrator, I want tag creation to be idempotent, so that reinstalling or upgrading the module does not create duplicate tags.
7. As an administrator, I want existing tags with matching names to be reused, so that existing contact data is preserved.
8. As a Contacts user, I want the standard Odoo Contacts app to remain the main working area, so that the customization feels native.
9. As a Contacts user, I do not want to see the gender field on company contacts, so that company forms stay relevant.
10. As a Contacts user, I want Odoo to show an error when saving a new or edited individual contact without gender, so that required individual contact data is captured.
11. As a French-speaking user, I want the field label, selection values, and validation messages in French, so that the customization fits the French UI.
12. As an English-speaking user, I want the field label, selection values, and validation messages in English, so that the customization fits the English UI.
13. As a Contacts user, I want the predefined tags to apply to both individuals and companies, so that users can classify either type of contact.
14. As an administrator, I want protected tags to keep their exact names, so that users cannot accidentally break the organization's classification vocabulary.
15. As an administrator, I want protected tags to be impossible to delete, archive, or deactivate, so that the classification vocabulary remains available.
16. As a Contacts user, I want helper text or placeholder guidance on the individual contact name field, so that I consistently enter last name first and first name second.
17. As a developer, I want this customization isolated in a dedicated addon, so that it can be installed, updated, or removed independently.
18. As a developer, I want the addon to depend on the official Contacts functionality, so that model and view inheritance are loaded in the correct order.
19. As a maintainer, I want the predefined tag list to be declared clearly, so that future changes are easy to review.
20. As a maintainer, I want the module to avoid unrelated contact behavior changes, so that the customization remains low-risk.
## Required Contact Tags

The addon must ensure these tags exist in Odoo contact categories and can be manually assigned to both individual contacts and companies:

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

These exact tag names are protected. No user, including an administrator, may delete, rename, archive, or deactivate these records through normal Odoo operations.

## Validation and Error Messages

The gender field is required only for individual contacts. Company contacts must not show the field and must not require it.

Existing individual contacts without a gender value are allowed to remain in the database after module installation. The requirement is enforced when a user creates or edits an individual contact through the normal contact form.

Validation messages must be translated:

- English: `Gender is required for individual contacts.`
- French: `Le sexe est obligatoire pour les contacts individuels.`

Protected tag error messages must be translated:

- English: `This contact tag is protected by the contact setup module.`
- French: `Cette étiquette de contact est protégée par le module de configuration des contacts.`

## Implementation Decisions

- Build a custom Odoo addon under the local `addons` directory.
- The addon should depend on the Odoo Contacts module, which provides `res.partner` and the Contacts app views.
- Extend the contact model rather than creating a separate model. The gender field belongs on `res.partner`.
- Add the gender field as a selection field, not a boolean. The stored values should be stable technical keys such as `male` and `female`, with translated labels for English and French.
- Inherit the existing Odoo contact form to place the gender field in the main contact area for individual contacts.
- Hide the gender field for company contacts.
- Add helper text or a placeholder on the individual contact name entry area indicating that users should enter last name first, then first name.
- Translate the name-order helper or placeholder for English and French.
- Enforce the individual-contact gender requirement in the standard create/edit flow without blocking module installation for existing records.
- Do not add a new app launcher entry, top-level menu, or independent contact management screen.
- Create the required tags using XML data or a module hook in a way that can be safely loaded more than once.
- Reuse existing tag records when possible and avoid duplicate records with the same visible name.
- Keep the tag names exactly as provided, including accents.
- Prevent protected tags from being deleted.
- Prevent protected tags from being renamed.
- Prevent protected tags from being archived or made inactive if the contact tag model supports archive/inactive behavior.
- Translate field labels, selection values, and validation messages for English and French.
- Keep the addon small and focused on contact metadata and predefined tags.

## Testing Decisions

- Test the external behavior of the addon: model field availability, view inheritance loading, and tag creation.
- Verify the module installs cleanly in the current Docker-based Odoo 19 environment.
- Verify the gender field exists on `res.partner` after installation.
- Verify the Contacts form loads and displays the gender field for individual contacts.
- Verify the Contacts form hides the gender field for company contacts.
- Verify the individual contact form shows name-entry guidance for last name first, then first name.
- Verify the name-entry guidance is translated in English and French.
- Verify an individual contact cannot be saved without gender through the normal form flow.
- Verify a company contact can be saved without gender.
- Verify existing individual contacts without gender do not block installation.
- Verify all required tags exist after installation.
- Verify reinstalling or upgrading the module does not create duplicate tags.
- Verify protected tags cannot be deleted.
- Verify protected tags cannot be renamed.
- Verify protected tags cannot be archived or deactivated if that operation exists in Odoo 19 contact tags.
- Verify English and French translations are loaded for labels, values, and validation messages.
- Avoid testing internal implementation details such as exact helper function structure unless they become part of a stable interface.

## Out of Scope

- Creating a new Contacts replacement app.
- Creating custom standalone menus or independent contact views.
- Automatically assigning the predefined tags to contacts.
- Importing contacts or migrating existing partner data.
- Requiring gender retroactively for all existing individual contacts at installation time.
- Adding reports, dashboards, or analytics.
- Adding languages beyond English and French.
- Inferring gender automatically from names or other contact data.

## Further Notes

The phrase "no view" is interpreted as "no standalone custom view or menu." The implementation still needs inherited Odoo view definitions to show the gender field inside the existing Contacts app.

The likely addon shape is a standard Odoo module with a manifest, a `res.partner` model extension, inherited contact form XML, translation files, and data or hook logic for the protected contact tags.

Automatic tag assignment rules are intentionally out of scope for this version. The available tags are created and protected so users can assign them manually.
