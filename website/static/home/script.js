$(document).ready(function () {
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        $(entry.target).addClass('show');
      } else {
        $(entry.target).removeClass('show');
      }
    });
  });

  $('.hidden').each(function () {
    observer.observe(this);
  });
});
