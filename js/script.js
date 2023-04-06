$(document).ready(function () {
  const onSubmit = () => {
    const result = $(".chat-input").val();
    $(".chat-input").val("");
    if (!/^\s*$/.test(result)) {
      $(".messages").append(`
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

  $(".chat-send-btn").click(() => onSubmit());
  $(".chat-input").on("keydown", (e) => {
    if (e.keyCode == 13 && !e.shiftKey) {
      e.preventDefault(); // Prevent default "Enter" behavior
      onSubmit(); // Submit the form
    } else if (e.keyCode == 13 && e.shiftKey) {
      $(this).val(function (i, val) {
        return val + "\n"; // Add a new line
      });
    }
  });
  /*
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
