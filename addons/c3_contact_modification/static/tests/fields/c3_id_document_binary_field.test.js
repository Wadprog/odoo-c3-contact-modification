import { expect, test } from "@odoo/hoot";
import { click, setInputFiles, waitFor } from "@odoo/hoot-dom";
import { animationFrame } from "@odoo/hoot-mock";
import { getOrigin } from "@web/core/utils/urls";
import { defineModels, fields, models, mountView } from "@web/../tests/web_test_helpers";

import { C3_ID_DOCUMENT_MAX_SIZE } from "@c3_contact_modification/fields/c3_id_document_binary_field";

class Partner extends models.Model {
    _name = "res.partner";

    c3_id_document = fields.Binary();
    c3_id_document_filename = fields.Char();

    _records = [
        { id: 1 },
        {
            id: 2,
            c3_id_document: "10",
            c3_id_document_filename: "identity.png",
        },
    ];
}

defineModels([Partner]);

const ARCH = `
    <form>
        <field
            name="c3_id_document"
            filename="c3_id_document_filename"
            widget="c3_id_document_binary"
            options="{'allowed_mime_type': 'image/jpeg,image/png'}"
        />
        <field name="c3_id_document_filename" invisible="1"/>
    </form>
`;

const READONLY_ARCH = ARCH.replace("<form>", '<form edit="0">');

test("accepts an ID document at the 5 MB limit", async () => {
    await mountView({
        resModel: "res.partner",
        resId: 1,
        type: "form",
        arch: ARCH,
    });

    await click(".o_select_file_button");
    await animationFrame();
    const file = new File([new Uint8Array(C3_ID_DOCUMENT_MAX_SIZE)], "identity.png", {
        type: "image/png",
    });
    await setInputFiles([file]);

    await waitFor(".o_form_button_save:visible");
    expect(".o_field_binary input[type=text]").toHaveValue("identity.png");
});

test("rejects an ID document above 5 MB before updating the record", async () => {
    await mountView({
        resModel: "res.partner",
        resId: 1,
        type: "form",
        arch: ARCH,
    });

    await click(".o_select_file_button");
    await animationFrame();
    const file = new File([new Uint8Array(C3_ID_DOCUMENT_MAX_SIZE + 1)], "identity.png", {
        type: "image/png",
    });
    await setInputFiles([file]);
    await animationFrame();

    expect(".o_notification_content").toHaveText(
        "Identity document images must be 5 MB or smaller."
    );
    expect(".o_notification_bar").toHaveClass("bg-danger");
    expect(".o_form_button_save:visible").toHaveCount(0);
    expect(".o_select_file_button").toHaveCount(1);
});

test("preserves standard MIME type validation", async () => {
    await mountView({
        resModel: "res.partner",
        resId: 1,
        type: "form",
        arch: ARCH,
    });

    await click(".o_select_file_button");
    await animationFrame();
    const file = new File(["not an image"], "identity.txt", { type: "text/plain" });
    await setInputFiles([file]);
    await animationFrame();

    expect(".o_notification_content").toHaveText(
        "Oops! 'identity.txt' didn’t upload since its format isn’t allowed."
    );
    expect(".o_form_button_save:visible").toHaveCount(0);
});

test("loads a saved ID document only after Preview is clicked", async () => {
    await mountView({
        resModel: "res.partner",
        resId: 2,
        type: "form",
        arch: ARCH,
    });

    expect(".o_c3_preview_id_document_button").toHaveCount(1);
    expect(".o-FileViewer").toHaveCount(0);
    expect(".o-FileViewer-viewImage").toHaveCount(0);

    await click(".o_c3_preview_id_document_button");
    await animationFrame();

    expect(".o-FileViewer").toHaveCount(1);
    expect(".o-FileViewer-viewImage").toHaveAttribute(
        "src",
        `${getOrigin()}/web/content/res.partner/2/c3_id_document?filename=identity.png&filename_field=c3_id_document_filename`
    );
    expect(".o-FileViewer-download a").toHaveAttribute(
        "href",
        `${getOrigin()}/web/content/res.partner/2/c3_id_document?filename=identity.png&filename_field=c3_id_document_filename&download=true`
    );
});

test("does not display Preview without a saved ID document", async () => {
    await mountView({
        resModel: "res.partner",
        resId: 1,
        type: "form",
        arch: ARCH,
    });

    expect(".o_c3_preview_id_document_button").toHaveCount(0);
});

test("hides Preview while a replacement ID document is unsaved", async () => {
    await mountView({
        resModel: "res.partner",
        resId: 2,
        type: "form",
        arch: ARCH,
    });

    await click(".o_select_file_button");
    await animationFrame();
    const file = new File(["replacement"], "replacement.png", { type: "image/png" });
    await setInputFiles([file]);
    await waitFor(".o_form_button_save:visible");

    expect(".o_c3_preview_id_document_button").toHaveCount(0);
});

test("displays Preview for a saved readonly ID document", async () => {
    await mountView({
        resModel: "res.partner",
        resId: 2,
        type: "form",
        arch: READONLY_ARCH,
    });

    expect(".o_c3_preview_id_document_button").toHaveCount(1);
});
