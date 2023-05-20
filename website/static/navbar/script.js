$(document).ready(function () {
  let dark_mode = localStorage.getItem('dark_mode');
  let body = $('body');

  $('button.profile-dropdown').on('click', () => {
    if ($('.dropdown').hasClass('show')) {
      $('.dropdown').removeClass('show');
      $('.dropdown').addClass('hide');
    } else {
      $('.dropdown').removeClass('hide');
      $('.dropdown').addClass('show');
    }
  });

  $(document).mouseup((event) => {
    const dropdownMenu = $('.dropdown');
    const dropdownButton = $('.profile-dropdown');
    console.log(event.target);
    // If the clicked element is not a dropdown button or a dropdown menu item
    if (!$(event.target).closest('.dropdown').length && dropdownMenu.hasClass('show')) {
      $('.dropdown').removeClass('show');
      $('.dropdown').addClass('hide');
    }
  });

  // Highlight the active link in the navigation
  // Get current page URL
  const url = window.location.pathname;

  // Iterate over all nav links
  $('.side-navbar a').each(function () {
    // Get href of the link
    const href = $(this).attr('href');

    // Check if the href matches the current URL
    if (url.includes(href)) {
      // If it matches, add class
      $(this).parent().addClass('active-nav');
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
