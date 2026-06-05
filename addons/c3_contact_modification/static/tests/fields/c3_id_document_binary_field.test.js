import { expect, test } from "@odoo/hoot";
import { click, setInputFiles, waitFor } from "@odoo/hoot-dom";
import { animationFrame } from "@odoo/hoot-mock";
import { defineModels, fields, models, mountView } from "@web/../tests/web_test_helpers";

import { C3_ID_DOCUMENT_MAX_SIZE } from "@c3_contact_modification/fields/c3_id_document_binary_field";

class Partner extends models.Model {
    _name = "res.partner";

    c3_id_document = fields.Binary();
    c3_id_document_filename = fields.Char();

    _records = [{ id: 1 }];
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
