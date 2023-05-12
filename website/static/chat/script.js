// Wait for the document to be fully loaded and then execute the enclosed function
$(document).ready(function () {
  const parseTime = (datetimeString) => {
    const timeComponents = datetimeString.split(' ')[1].split(':');
    const hour = timeComponents[0];
    const minute = timeComponents[1];
    return hour + ':' + minute;
  };

  // Get the current URL
  const url = window.location.href;
  console.log(url);

  // Resize the message-input textarea dynamically based on its content
  $('.message-input').on('input', function () {
    const $this = $(this);
    $this.css({
      'overflow-y': 'hidden',
      height: 'auto',
    });

    const scrollHeight = this.scrollHeight;
    $this.css('height', scrollHeight + 'px');

    if (scrollHeight > this.clientHeight) {
      $this.css('overflow-y', 'auto');
    }
  });

  // Submit the message on 'Enter' key press
  $('.message-input').on('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
      $(this).val('');
    }
  });

  $('#send-input').click(() => {
    onSubmit();
    $('.message-input').val('');
  });

  // Get the current time in a formatted string
  function getCurrentTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const formattedTime = `${hours}:${minutes}`;
    return formattedTime;
  }

  // Handle message submission
  const onSubmit = () => {
    console.log('submitting');
    const result = $('.message-input').val().trim();
    const username = localStorage.getItem('username');
    const api_url = window.location.origin + '/api/prompt';
    if (result) {
      try {
        // Append the user's input to the messages area
        $('.messages').append(`
                    <div class="chat-message user">
                        <div class="chat-bubble">
                            <div class="bubble">
                                <span>${result}</span>
                            </div>
                        </div>
                        <div class="info">
                            <div class="avatar"></div>
                            <span>${getCurrentTime()}</span>
                        </div>
                    </div>
                `);

        $('.messages').append(`
                    <div class="chat-message assistant" id="typing">

                        <div class="chat-bubble assistant">
                            <div class="bubble typing-container">
                                <div class="typing" id="typing-animation"></div>
                            </div>
                        </div>
                        <div class="info">
                            <div class="avatar"></div>
                            <span>${getCurrentTime()}</span>
                        </div>
                    </div>
                `);

        // Play the animation
        const typingBubble = $('.chat-message.assistant:last-child .typing')[0];
        const animationInstance = bodymovin.loadAnimation({
          container: typingBubble,
          renderer: 'svg',
          loop: true,
          autoplay: true,
          path: '../static/images/typing-animation.json',
        });

        $.ajax({
          url: api_url,
          type: 'POST',
          data: { input: result, username: username },
          success: function (response) {
            animationInstance.destroy();
            typingBubble.remove();
            $('.chat-message.assistant .bubble').removeClass(
              'typing-container'
            );

            const text = response.generated_text;
            // Append the chatbot's response to the messages area
            $('.chat-message.assistant:last-child .bubble').append(`
              <span>${text}</span>
            `);
          },
          error: function (error) {
            console.error(error);
            console.log(error);
          },
        });
      } catch (e) {
        console.log(e);
      }
    }
  };
});
