$('.dz').dropzone({
    previewTemplate: '<div style="display:none"></div>',
    init: function () {
        this.on("success", function (file) {
            dzPostUploadToast(file);
        });
    }
});

const dzPostUploadToast = function (file) {
    const template = `
        <div class="toast ml-auto" role="alert" data-delay="3000" data-autohide="true">
          <div class="toast-header">
            <strong class="mr-auto text-primary">Blob Upload</strong>
            <small class="text-muted">4 mins ago</small>
            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="toast-body">
            Successfully uploaded ${file.name}.
          </div>
        </div>`;
    $('.alert-container').append(template);
    // initialize and show Bootstrap 4 toast
    $('.toast').toast('show');
}
