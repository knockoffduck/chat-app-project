$(document).ready(function () {
  $('#burger-button').click(() => {
    if ($('#burger-menu-section').hasClass('show')) {
      $('#burger-menu-section').removeClass('show');
      $('#burger-menu-section').addClass('hide');
    } else {
      $('#burger-menu-section').addClass('show');
      $('#burger-menu-section').removeClass('hide');
    }
  });
  $('#close-button').click(() => {
    if ($('#burger-menu-section').hasClass('show')) {
      $('#burger-menu-section').removeClass('show');
      $('#burger-menu-section').addClass('hide');
    } else {
      $('#burger-menu-section').addClass('show');
      $('#burger-menu-section').removeClass('hide');
    }
  });
});
