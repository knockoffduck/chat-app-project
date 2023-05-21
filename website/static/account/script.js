$(document).ready(function () {
  $('#upload-avatar-button').click(function () {
    var fileInput = $('#user_avatar')[0];
    var file = fileInput.files[0];

    var formData = new FormData();
    formData.append('avatar', file);

    $.ajax({
      url: '/api/avatar_upload',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        // Handle the success response
        console.log(response);
        location.reload();
      },
      error: function (xhr, status, error) {
        // Handle the error response
        console.log(error);
      },
    });
  });
});
