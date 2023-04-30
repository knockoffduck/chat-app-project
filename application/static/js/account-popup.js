<script>
      function showAccountPopup() {
        // Get the user's name and display it in the popup
        const userName = "John Doe"; // replace with actual user's name
        const popupContent = `<p>Hello, ${userName}!</p><button>Sign Out</button>`;

        // Create a new HTML element for the popup and add it to the page
        const popup = document.createElement("div");
        popup.innerHTML = popupContent;
        popup.style.position = "fixed";
        popup.style.top = "50%";
        popup.style.left = "50%";
        popup.style.transform = "translate(-50%, -50%)";
        popup.style.padding = "20px";
        popup.style.border = "1px solid #ccc";
        popup.style.backgroundColor = "#fff";
        document.body.appendChild(popup);

        // Add a click event listener to the sign-out button
        const signOutButton = popup.querySelector("button");
        signOutButton.addEventListener("click", function() {
          // TODO: implement sign-out functionality
          console.log("Signing out...");
          // Remove the popup from the page
          document.body.removeChild(popup);
        });
      }

      $(document).ready(function() {
        // code for handling click events here
      });
    </script>
    // Get references to the input and send button elements
