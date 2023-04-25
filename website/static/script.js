$(document).ready(function () {
  // Function to handle chat input submission
  const onSubmit = () => {
    // Get the user's input and username
    const result = $('.chat-input').val();
    const username = $('.username-input').val();

    // Clear the input field
    $('.chat-input').val('');

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
            <div class="message-area-bot">
              <div class="message-avatar">
                <i class="bi-robot"></i>
              </div>
              <div class="message-box">
                <span class="message">${text}</span>
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
        <div class="message-area-user">
          <div class="message-avatar">
            <i class="bi-person"></i>
          </div>
          <div class="message-box">
            <span class="message">${result}</span>
          </div>
        </div>
      `);
    }
  };

  // Attach the onSubmit function to the chat send button
  $('.chat-send-btn').click(() => {
    onSubmit();
  });

  // Handle keyboard input in the chat input field
  $('.chat-input').on('keydown', (e) => {
    if (e.keyCode == 13 && !e.shiftKey) {
      e.preventDefault(); // Prevent default "Enter" behavior
      onSubmit(); // Submit the form
    } else if (e.keyCode == 13 && e.shiftKey) {
      $(this).val(function (i, val) {
        return val + '\n'; // Add a new line
      });
    }
  });

  /*
  // Code for burger menu buttons (not currently used)
  $("#burgerMenuButtonOpen").click(function () {
    $("#test").toggleClass("d-none");
    $("#test2").toggleClass("d-none");
  });
  $("#burgerMenuButtonClose").click(function () {
    $("#test").toggleClass("d-none");
    $("#test2").toggleClass("d-none");
  });
  */
});
