// This code waits for the document to be fully loaded and then executes the enclosed function
$(document).ready(function () {
  // Get the current URL
  var url = window.location.href;
  console.log(url);

  // Loop through each anchor tag in the navigation
  $('nav ul li a').each(function () {
    // Get the value of the href attribute
    var href = $(this).attr('href');

    // Check if the current URL contains the href value
    if (url.indexOf(href) > -1) {
      // Add the active-nav class to the parent li element
      $(this).closest('li').addClass('active-nav');
    } else {
      // Remove the active-nav class from the parent li element
      $(this).closest('li').removeClass('active-nav');
    }
  });

  // This resizes the message-input textarea dynamically based on its content
  $('.message-input').on('input', function () {
    $(this).css('overflow-y', 'hidden');
    $(this).css('height', 'auto');
    $(this).css('height', this.scrollHeight + 'px');
    if (this.scrollHeight > this.clientHeight) {
      $(this).css('overflow-y', 'auto');
    }
  });

  // This listens for the 'keydown' event on the message-input textarea
  $('.message-input').on('keydown', function (e) {
    // Check if the Enter key is pressed
    if (e.key === 'Enter') {
      // Prevent the default behavior (newline) if Shift is not pressed
      if (!e.shiftKey) {
        e.preventDefault();
        // Submit the text
        onSubmit();
        // Clear the textarea
        $(this).val('');
      }
    }
  });

  // This function returns the current time in a formatted string
  function getCurrentTime() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    const formattedTime =
      String(hours).padStart(2, '0') + ':' + minutes + ' ' + ampm;
    return formattedTime;
  }

  const onSubmit = () => {
    // Get the user's input and username
    const result = $('.message-input').val();
    const username = $('#username').val();
    // Check that the input is not empty
    if (!/^\s*$/.test(result)) {
      // Send the user's input and username to the server to generate a response
      $.ajax({
        url: 'http://127.0.0.1:5000/chat/prompt',
        type: 'POST',
        data: { input: result, username: username },
        success: function (response) {
          // Append the chatbot's response to the messages area
          const text = response.generated_text;
          $('.messages').append(`
          <div class="chat-message-bot">
            <div class="info">
                <div class="avatar"></div>
                <p>${getCurrentTime()}</p>
            </div>
          <div class="chat-bubble-bot">
            <div class="triangle"></div>
            <div class="bubble">
              <p>${text}</p>
            </div>
          </div>
        </div>
          `);
        },
        error: function (error) {
          console.error(error);
        },
      });
      // Append the user's input to the messages area
      $('.messages').append(`
      <div class="chat-message-user">
      <div class="chat-bubble-user">
        <div class="bubble">
          <p>
            ${result}
          </p>
        </div>
        <div class="triangle"></div>
      </div>
        <div class="info">
            <div class="avatar"></div>
            <p>${getCurrentTime()}</p>
        </div>
    </div>
      `);
    }
  };
});

// $('.icon').click(() => {
//   let x = document.getElementById("side-panel");
//   if (x.className === "side-pane") {
//     x.className = x.className + " responsive";
//   } else {
//     x.className = "side-pane";
//   }
// });