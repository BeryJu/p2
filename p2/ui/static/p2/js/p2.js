$('.dz').dropzone({
    previewTemplate: '<div style="display:none"></div>',
    init: function () {
        this.on('error', function (file, errorMessage) {
            dzPostUploadToast(errorMessage.detail, false);
        });
        this.on("success", function (file) {
            dzPostUploadToast(file.name, true);
        });
    }
});

const dzPostUploadToast = function (message, uploadSucceeded) {
    let text = '';
    if (uploadSucceeded) {
        text = `Successfully uploaded ${message}.`;
    } else {
        text = `Failed to upload file: ${message}.`;
    }
    const template = `
        <div class="toast ml-auto" role="alert" data-delay="3000" data-autohide="true">
          <div class="toast-header">
            <strong class="mr-auto text-primary">Blob Upload</strong>
            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="toast-body">
            ${text}
          </div>
        </div>`;
    $('.alert-container').append(template);
    // initialize and show Bootstrap 4 toast
    $('.toast').toast('show');
}
