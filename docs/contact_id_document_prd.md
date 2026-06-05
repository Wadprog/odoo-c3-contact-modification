# Odoo Contact ID Document PRD

## Problem Statement

The Odoo 19 Contacts app needs a structured way to store one identity document image for an individual contact. Today, users can only rely on general attachments or ad hoc storage, which makes national ID, passport, or similar document handling inconsistent.

## Solution

Extend the existing Contacts app so users can upload, view, replace, and delete one optional ID document image for each individual contact. The feature should behave similarly to the ID upload experience in the Odoo Employee app, but inside the standard contact form.

The feature must not introduce a standalone app, top-level menu, or separate contact workflow. Users should keep working inside the standard Odoo Contacts app.

## User Stories

1. As a Contacts user, I want to upload one ID document image for an individual contact, so that national ID, passport, or similar identification can be stored with the contact.
2. As a Contacts user, I want the ID document area hidden for companies, so that company contact forms do not show irrelevant individual-person fields.
3. As a Contacts user, I want to view an uploaded ID document in Odoo's document viewer, so that I can inspect the document from the contact form.
4. As a Contacts user, I want to replace or delete the uploaded ID document, so that outdated or incorrect documents can be corrected.
5. As a Contacts user, I want invalid files and oversized images blocked, so that only supported ID document images are stored.
6. As a maintainer, I want ID document storage to allow only one current document per contact, so that the workflow remains simple and predictable.

## Functional Requirements

The ID document feature applies only to individual contacts. Company contacts must not show the ID document tab, upload control, viewer, or related actions.

The visible label must be translated:

- English: `ID Document`
- French: `Pièce d'identité`

The ID document UI must appear in its own tab next to the standard contact `Notes` tab. The tab should contain only the document viewer and the controls needed to upload, replace, or delete the ID document.

The uploaded ID must be stored as a dedicated Odoo attachment linked to the contact. It must be separate from general contact attachments and must not rely on the chatter attachment list as the primary UI. The implementation should use a dedicated reference or metadata strategy so the addon can reliably identify the one ID document attachment for each contact.

Only one ID document may be stored per contact. Replacing the ID document must delete the previous ID attachment and store the new one as the current ID document. Deleting the ID document must remove the attachment.

Allowed file formats:

- JPG
- JPEG
- PNG

Uploads must be blocked when the file is not one of the allowed image formats. Uploads must also be blocked when the file is larger than 5 MB.

The document viewer is only required after the contact has been saved. Unsaved-contact preview is out of scope.

Any user who can view and edit the contact may view, upload, replace, and delete the contact's ID document. No additional access group is required for this feature.

Duplicating an individual contact that has an ID document must create the duplicate without copying the ID document.

Changing an individual contact to a company must be blocked while an ID document exists. The user must delete the ID document before changing the contact to a company.

Deleting a contact must delete its dedicated ID document attachment.

## Validation and Error Messages

ID document upload validation messages must be translated:

- English: `Only JPG and PNG identity document images are allowed.`
- French: `Seules les images JPG et PNG de pièce d'identité sont autorisées.`

ID document size validation messages must be translated:

- English: `Identity document images must be 5 MB or smaller.`
- French: `Les images de pièce d'identité doivent faire 5 Mo ou moins.`

## Implementation Decisions

- Build this as part of the existing Odoo 19 addon under the local `addons` directory.
- Store individual contact ID documents as dedicated `ir.attachment` records linked to the contact.
- Track the dedicated ID document attachment separately from general contact attachments so the feature can enforce one current ID document per contact.
- Add an inherited Contacts form tab next to `Notes` for the ID document viewer and upload/replace/delete controls.
- Hide the ID document tab and controls for company contacts.
- Validate ID document uploads by MIME type and/or file extension so only JPG, JPEG, and PNG images are accepted.
- Enforce a 5 MB maximum ID document image size.
- Delete the previous ID document attachment when a replacement is uploaded.
- Delete the dedicated ID document attachment when the contact is deleted.
- Prevent changing an individual contact with an ID document into a company until the ID document is removed.
- Avoid copying the ID document attachment when duplicating a contact.
- Translate labels and validation messages for English and French.
- Do not add a new app launcher entry, top-level menu, or independent contact management screen.

## Testing Decisions

- Verify the ID document tab appears for individual contacts and is hidden for companies.
- Verify an individual contact can upload one JPG, JPEG, or PNG ID document up to 5 MB.
- Verify unsupported file formats are rejected with the translated validation message.
- Verify image files larger than 5 MB are rejected with the translated validation message.
- Verify the uploaded ID document opens in Odoo's document viewer after the contact is saved.
- Verify replacing an ID document deletes the previous ID attachment.
- Verify deleting an ID document removes the dedicated attachment.
- Verify duplicating a contact does not copy the ID document.
- Verify changing an individual contact with an ID document into a company is blocked until the ID document is deleted.
- Verify deleting a contact deletes its dedicated ID document attachment.
- Verify users with contact access can view, upload, replace, and delete the ID document without an additional custom security group.
- Verify English and French translations are loaded for labels and validation messages.
- Avoid testing internal implementation details unless they become part of a stable interface.

## Out of Scope

- Supporting ID documents for company contacts.
- Supporting more than one ID document per contact.
- Supporting non-image ID document files such as PDFs or Word documents.
- Showing an ID document preview before the contact is saved.
- Keeping historical versions of replaced ID documents.
- Adding extra ID document metadata such as uploaded-by or upload date in the contact form.
- Creating a new Contacts replacement app.
- Creating custom standalone menus or independent contact views.
- Adding reports, dashboards, or analytics.
- Adding languages beyond English and French.
