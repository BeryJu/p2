function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

$('[data-api-url]').on('click', (e) => {
  $(e.currentTarget).prepend(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`);
  // Make the actual request
  let headers = new Headers();
  headers.append('X-CSRFToken', getCookie('csrftoken'));
  let request = new Request($(e.currentTarget).data('api-url'));
  fetch(request, {
    method: 'POST',
    headers: headers
  }).then(response => {
    $(e.currentTarget).find('span.spinner-border').remove();
  });
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
