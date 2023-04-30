const messageInput = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");

// Get a reference to the message list container
const messageList = document.querySelector(".message-list");

// Add a click event listener to the send button
sendButton.addEventListener("click", sendMessage);

// Add a keyup event listener to the input element to detect "Enter" key presses
messageInput.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    sendMessage();
  }
});

function sendMessage() {
  // Get the message from the input element
  const message = messageInput.value.trim();

  // If the message is not empty, create a new message element and add it to the message list
  if (message !== "") {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.textContent = message;
    messageList.appendChild(messageElement);

    // Clear the input element
    messageInput.value = "";
  }
}
