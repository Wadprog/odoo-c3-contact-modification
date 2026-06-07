# Odoo Contact Date of Birth PRD

## Problem Statement

The Odoo 19 Contacts app needs to capture a date of birth for individual contacts in a consistent way. Today, there is no dedicated date of birth field on contacts, so users must rely on notes, custom fields, or other informal storage. That makes the information hard to validate and inconsistent to use.

## Solution

Build a custom Odoo 19 addon that extends the existing Contacts app. The addon will modify the `res.partner` model to add a date of birth field, inherit the existing contact form to display that field only for individual contacts, and enforce that the field is required for individual contacts.

The field must support English and French user interfaces:

- English label: `Date of Birth`
- French label: `Date de naissance`

The field must be hidden for company contacts and required for individual contacts. It must reject future dates, but it must not impose any minimum age restriction.

The module must not introduce a standalone app, menu, or separate custom view flow. Users should keep working inside the standard Odoo Contacts app.

## User Stories

1. As a Contacts user, I want to record an individual contact's date of birth, so that contact records contain the information needed for identity and profile management.
2. As a Contacts user, I want the date of birth field to appear directly in the standard contact form for individuals, so that I do not need to open a separate screen.
3. As a Contacts user, I want the date of birth field to be stored on the contact record, so that the value remains available anywhere `res.partner` is used.
4. As a Contacts user, I want the date of birth field to be searchable or filterable where Odoo supports date field search behavior, so that I can segment contacts by age-related information if needed.
5. As a Contacts user, I do not want to see the date of birth field on company contacts, so that company forms stay relevant.
6. As a Contacts user, I want Odoo to show an error when saving a new or edited individual contact without a date of birth, so that required individual contact data is captured.
7. As a Contacts user, I want Odoo to block future dates, so that invalid birth dates cannot be saved.
8. As a French-speaking user, I want the field label and validation messages in French, so that the customization fits the French UI.
9. As an English-speaking user, I want the field label and validation messages in English, so that the customization fits the English UI.
10. As a developer, I want this customization isolated in a dedicated addon, so that it can be installed, updated, or removed independently.
11. As a developer, I want the addon to depend on the official Contacts functionality, so that model and view inheritance are loaded in the correct order.
12. As a maintainer, I want the module to avoid unrelated contact behavior changes, so that the customization remains low-risk.

## Functional Requirements

The date of birth field applies only to individual contacts. Company contacts must not show the field and must not require it.

Existing individual contacts without a date of birth are allowed to remain in the database after module installation. The requirement is enforced when a user creates or edits an individual contact through the normal contact form.

Validation messages must be translated:

- English required message: `Date of birth is required for individual contacts.`
- French required message: `La date de naissance est obligatoire pour les contacts individuels.`
- English future-date message: `Date of birth cannot be in the future.`
- French future-date message: `La date de naissance ne peut pas être dans le futur.`

## Implementation Decisions

- Build a custom Odoo addon under the local `addons` directory.
- The addon should depend on the Odoo Contacts module, which provides `res.partner` and the Contacts app views.
- Extend the contact model rather than creating a separate model. The date of birth field belongs on `res.partner`.
- Add the date of birth field as a `fields.Date`.
- Inherit the existing Odoo contact form to place the field in the main contact area for individual contacts.
- Hide the date of birth field for company contacts.
- Enforce the individual-contact date of birth requirement in the standard create/edit flow without blocking module installation for existing records.
- Reject future dates in backend validation so the rule cannot be bypassed.
- Do not impose any minimum age restriction.
- Do not add a new app launcher entry, top-level menu, or independent contact management screen.
- Translate field labels and validation messages for English and French.
- Keep the addon small and focused on contact metadata.

## Testing Decisions

- Test the external behavior of the addon: model field availability and view inheritance loading.
- Verify the module installs cleanly in the current Docker-based Odoo 19 environment.
- Verify the date of birth field exists on `res.partner` after installation.
- Verify the Contacts form loads and displays the date of birth field for individual contacts.
- Verify the Contacts form hides the date of birth field for company contacts.
- Verify an individual contact cannot be saved without a date of birth through the normal form flow.
- Verify a company contact can be saved without a date of birth.
- Verify future dates are rejected with the translated validation message.
- Verify existing individual contacts without a date of birth do not block installation.
- Verify English and French translations are loaded for labels and validation messages.
- Avoid testing internal implementation details such as exact helper function structure unless they become part of a stable interface.

## Out of Scope

- Creating a new Contacts replacement app.
- Creating custom standalone menus or independent contact views.
- Requiring a minimum age.
- Allowing future dates.
- Adding reports, dashboards, or analytics.
- Adding languages beyond English and French.
- Inferring age or date of birth from names or other contact data.

## Further Notes

The phrase "no view" is interpreted as "no standalone custom view or menu." The implementation still needs inherited Odoo view definitions to show the date of birth field inside the existing Contacts app.

This feature should follow the same pattern as the existing gender requirement: visible only for individual contacts, hidden for companies, required on create/edit, and enforced server-side so it cannot be bypassed by a modified client.
