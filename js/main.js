$(document).ready(function() {
    $('#burgerMenuButtonOpen').click(function() {
      $('#test').toggleClass('d-none');
      $('#test2').toggleClass('d-none');
    });
    $('#burgerMenuButtonClose').click(function() {
      $('#test').toggleClass('d-none');
      $('#test2').toggleClass('d-none');
    });
  });