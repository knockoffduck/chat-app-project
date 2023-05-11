const loadingScreen = $('#loading-screen');
loadingScreen.show();
$(document).ready(function () {
  setTimeout(() => {
    $('#loading-screen').fadeOut(250, 'swing');
    console.log('fading out');
  }, 2000);

  const animation = bodymovin.loadAnimation({
    container: $('.lottie-animation')[0],
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '../static/images/loading.json',
  });
});
