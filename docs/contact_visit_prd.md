# Odoo Contact Visit PRD

## Problem Statement

The Odoo 19 Contacts app needs a simple way to record visit history for a contact. Today, visit information would have to live in notes or ad hoc custom fields, which makes it hard to see when a contact was visited, why they were visited, and which site the visit belongs to.

## Solution

Build a custom Odoo 19 addon that extends the existing Contacts app with a dedicated Visits tab on the contact form. The addon will store visits in a separate model linked to `res.partner`, store configurable visit reasons in a separate model, and show the visit history directly on the contact.

The visit history must stay inside the standard Contacts app. No standalone app, top-level menu, or separate workflow should be added.

The feature must support these visible labels in English and French:

- English tab label: `Visits`
- French tab label: `Visites`
- English reason label: `Visit Reason`
- French reason label: `Motif de visite`
- English site label: `Site`
- French site label: `Site`
- English notes label: `Notes`
- French notes label: `Notes`

Visits are created only from the contact form. Each visit must be linked to the contact being viewed, must require one selectable reason, must require one site selected from contacts carrying the site tag, and may include optional notes. The visit timestamp should come from the record creation time, so the contact visit history is automatically time-stamped without a separate editable date field.

## User Stories

1. As a Contacts user, I want to record a visit on a contact, so that I can keep a history of contact activity inside the contact record.
2. As a Contacts user, I want visits to appear in their own tab on the contact form, so that visit history is easy to find.
3. As a Contacts user, I want each visit to store a required reason, so that the visit history explains why the contact was visited.
4. As a Contacts user, I want each visit to store a required site, so that I can see where the visit took place.
5. As a Contacts user, I want each visit to store optional notes, so that I can add short context when needed.
6. As a Contacts user, I want the visit timestamp to be recorded automatically, so that I do not need to enter the time manually.
7. As a Contacts user, I want visit records to be visible in a simple list, so that I can scan the history quickly.
8. As a Contacts user, I want to select the site from contacts tagged as a site, so that site selection stays consistent with the contact system.
9. As a Contacts user, I want to configure visit reasons, so that the available reasons match our organization's vocabulary.
10. As an administrator, I want configurable visit reasons to be stored separately from visit history, so that reason choices can be managed centrally.
11. As a Contacts user, I want to create visit records only from the contact form, so that the workflow stays simple.
12. As a Contacts user, I do not want to edit or delete visit records after creation, so that the history remains trustworthy.
13. As a Contacts user, I want only users who can edit the contact to add visits, so that permissions follow the existing Contacts app behavior.
14. As a site manager, I want sites to be normal contacts that can carry a site tag, so that we do not need a separate site app or model.
15. As a French-speaking user, I want the visit labels translated into French, so that the feature fits the French UI.
16. As an English-speaking user, I want the visit labels translated into English, so that the feature fits the English UI.
17. As a maintainer, I want the visit feature isolated in a dedicated addon, so that it can be installed, updated, or removed independently.
18. As a maintainer, I want the visit feature to reuse the standard Contacts form, so that the customization stays native to Odoo.
19. As a maintainer, I want the site selector to reuse the existing contact/tag model, so that the feature remains easy to extend.
20. As a maintainer, I want the visit history to avoid extra workflow complexity, so that the module stays focused and low-risk.

## Functional Requirements

The visit feature applies only inside the standard contact form. The visit tab must appear after the existing `ID Document` tab.

Visits must be stored in a separate model linked to `res.partner`. Each visit must contain:

- a required contact reference
- a required visit reason
- a required site reference
- optional notes
- an automatic creation timestamp used as the visit time

The visible visit tab and field labels must be translated:

- English tab label: `Visits`
- French tab label: `Visites`
- English reason label: `Visit Reason`
- French reason label: `Motif de visite`
- English site label: `Site`
- French site label: `Site`
- English notes label: `Notes`
- French notes label: `Notes`

Visit reasons must be stored in a separate configurable model so users can add new reasons in configuration. The available reasons should be selectable on each visit.

The site selector on a visit must show contacts that carry the site tag. Normal contacts may also carry the site tag. The implementation should rely on the standard contact model and tag relationships rather than creating a dedicated site app.

Visits are append-only. After creation, users must not be able to edit or delete visit records through the normal UI.

Any user who can edit a contact may create a visit for that contact. No additional custom security group is required for the base feature.

The visit history must be simple. A basic list is enough; no special analytics, timeline, grouping, or dashboard is required for this version.

## Validation and Error Messages

Visit validation messages must be translated:

- English required message for the reason: `Visit reason is required.`
- French required message for the reason: `Le motif de visite est obligatoire.`
- English required message for the site: `Site is required.`
- French required message for the site: `Le site est obligatoire.`

## Implementation Decisions

- Build the feature as part of the existing Odoo 19 addon under the local `addons` directory.
- Extend the contact form with a new notebook tab after the existing ID document tab.
- Store visits in a separate model linked to `res.partner` instead of embedding visit data directly on the contact.
- Store visit reasons in a separate configuration model so users can manage the selectable reasons centrally.
- Use the standard `ir.model.fields`/Odoo relation patterns to connect each visit to one contact, one reason, and one site.
- Use the contact creation timestamp as the visit time instead of adding a manual date/time field.
- Make visit records append-only by preventing normal edit and delete flows after creation.
- Restrict site selection to contacts tagged as site contacts.
- Allow normal contacts to carry the site tag, since the user requested the tag category remain usable on ordinary contacts.
- Keep the visit history UI simple with a list-style presentation.
- Do not add a new app launcher entry, top-level menu, or separate contact workflow.
- Translate labels and validation messages for English and French.
- Keep the addon focused on visit logging and visit reason configuration.

## Testing Decisions

- Test the external behavior of the addon: model availability, view inheritance, and visit record creation flow.
- Verify the module installs cleanly in the current Docker-based Odoo 19 environment.
- Verify the Visits tab appears on the contact form after the ID Document tab.
- Verify visits can be created only from the contact form.
- Verify a visit requires a reason.
- Verify a visit requires a site.
- Verify a visit can include optional notes.
- Verify the visit timestamp comes from record creation time.
- Verify visit reasons can be created in configuration and selected on visits.
- Verify site selection is limited to contacts with the site tag.
- Verify site contacts may still be normal contacts with the site tag.
- Verify visit records cannot be edited or deleted after creation through the normal UI.
- Verify users who can edit a contact can create visits without an additional custom group.
- Verify English and French translations are loaded for labels and validation messages.
- Avoid testing internal implementation details such as exact helper function structure unless they become part of a stable interface.

## Out of Scope

- Creating a new app or top-level menu.
- Creating a separate visit management screen outside the contact form.
- Allowing visit records to be edited after creation.
- Allowing visit records to be deleted after creation through the normal UI.
- Adding visit duration, visitor name, or other extra attendance metadata.
- Allowing multiple sites on a single visit.
- Allowing the site selector to choose non-contact records.
- Adding reports, dashboards, or analytics.
- Adding languages beyond English and French.
- Auto-generating visit reasons from contact history.

## Further Notes

The site concept is intentionally kept simple: a site is still a contact that can be tagged as a site, and the visit selector should pull from those tagged contacts.

This feature should follow the same general pattern as the existing contact extensions: it lives inside the standard Contacts app, uses inherited views, and keeps the user workflow centered on `res.partner`.
