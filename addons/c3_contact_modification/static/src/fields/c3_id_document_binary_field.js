import { _t } from "@web/core/l10n/translation";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";
import { registry } from "@web/core/registry";
import { url } from "@web/core/utils/urls";
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
    static template = "c3_contact_modification.IdDocumentBinaryField";
    static components = {
        ...BinaryField.components,
        FileUploader: C3IdDocumentFileUploader,
    };

    setup() {
        super.setup();
        this.fileViewer = useFileViewer();
    }

    onFilePreview() {
        const { name, record } = this.props;
        const route = `/web/content/${record.resModel}/${record.resId}/${name}`;
        const queryParams = {
            filename: this.fileName,
            filename_field: this.props.fileNameField,
        };
        const source = url(route, queryParams);
        this.fileViewer.open({
            defaultSource: source,
            downloadUrl: url(route, { ...queryParams, download: true }),
            isImage: true,
            isViewable: true,
            name: this.fileName,
        });
    }
}

registry.category("fields").add("c3_id_document_binary", {
    ...binaryField,
    component: C3IdDocumentBinaryField,
});
