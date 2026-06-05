import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";
import { FileUploader } from "@web/views/fields/file_handler";

export const C3_ID_DOCUMENT_MAX_SIZE = 5 * 1024 * 1024;

export class C3IdDocumentFileUploader extends FileUploader {
    async onFileChange(ev) {
        if ([...ev.target.files].some((file) => file.size > C3_ID_DOCUMENT_MAX_SIZE)) {
            this.notification.add(_t("Identity document images must be 5 MB or smaller."), {
                type: "danger",
            });
            ev.target.value = null;
            return;
        }
        return super.onFileChange(ev);
    }
}

export class C3IdDocumentBinaryField extends BinaryField {
    static components = {
        ...BinaryField.components,
        FileUploader: C3IdDocumentFileUploader,
    };
}

registry.category("fields").add("c3_id_document_binary", {
    ...binaryField,
    component: C3IdDocumentBinaryField,
});
