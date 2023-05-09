$('#loading-screen-app').show();
$(document).ready(function () {
  let dark_mode = localStorage.getItem('dark_mode');
  let body = $('body');

  setTimeout(() => {
    $('#loading-screen-app').fadeOut(500);
    console.log('fading out');
  }, 2000);

  const animation = bodymovin.loadAnimation({
    container: $('#loading-screen-app.lottie-animation')[0],
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '../static/images/loading.json',
  });

  $('button.profile-dropdown').on('click', () => {
    console.log('clicked');
    if ($('.dropdown').css('display') === 'block') {
      $('.dropdown').css('display', 'none');
    } else {
      $('.dropdown').css('display', 'block');
    }
  });

  const enableDarkMode = () => {
    body.addClass('dark');
    localStorage.setItem('dark_mode', 'active');
  };
  const disableDarkMode = () => {
    body.removeClass('dark');
    localStorage.setItem('dark_mode', 'inactive');
  };

  if (dark_mode === 'active') {
    enableDarkMode();
    $('.dark-mode-switcher').prop('checked', true);
  }

  $('.dark-mode-switcher').on('click', () => {
    dark_mode = localStorage.getItem('dark_mode');
    if (dark_mode === 'inactive') {
      $('#color-selector').prop('checked', true);
      enableDarkMode();
    } else {
      $('#color-selector').prop('checked', false);
      disableDarkMode();
    }
  });

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
