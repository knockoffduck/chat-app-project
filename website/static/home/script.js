// This code waits for the document to be fully loaded and then executes the function

$(document).ready(function () {
  // This creates a new IntersectionObserver object that takes a callback function as an argument
  const observer = new IntersectionObserver(function (entries) {
    // This loops through all the entries that are observed by the IntersectionObserver
    entries.forEach(function (entry) {
      // This checks if the current entry is intersecting with the viewport
      if (entry.isIntersecting) {
        // If the entry is intersecting, it adds a CSS class called 'show' to the entry's target element
        $(entry.target).addClass('active');
      } else {
        // If the entry is not intersecting, it removes the CSS class called 'show' from the entry's target element
        $(entry.target).removeClass('active');
      }
    });
  });

  // This selects all the elements with the CSS class 'hidden'
  $('.inactive').each(function () {
    // This observes each of the selected elements
    observer.observe(this);
  });
});
