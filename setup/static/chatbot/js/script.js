const chatbotForm = get('.chatbot-form');
const userInput = get(".chatbot-input");
const chatbotChat = get(".chatbot-chat");

const BOT_IMG = "robot";
const PERSON_IMG = "user";
const BOT_NAME = "Bot";
const PERSON_NAME = "You";

chatbotForm.addEventListener("submit", event => {
  event.preventDefault();

  const userMessage = userInput.value;
  if (!userMessage) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", userMessage);
  userInput.value = "";

  appendMessage(BOT_NAME, BOT_IMG, "left", "Checking...");

  sendMessage(userMessage)
    .then(botMessage => {
      botResponse(botMessage.replace(/\n/g, '<br />'));
    })
    .catch(errorMessage => {
      botResponse(errorMessage);
  })
});

async function sendMessage(userMessage) {
  const csrftoken = get('[name=csrfmiddlewaretoken]').value;

  const response = await fetch("/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({'message': userMessage})
  });

  if (response.ok) {
      const jsonResponse = await response.json();
      return jsonResponse.message;
  } else {
      console.error("Error:", response.status);
      return "Failed to get the response. Status: " + response.status;
  }
}

function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img">
        <i class="fa-solid fa-${img} fa-2xl"></i>
      </div>

      <div class="msg-box">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  chatbotChat.insertAdjacentHTML("beforeend", msgHTML);
  chatbotChat.scrollTop += 500;
}

function updateCheckingMessage(text) {
  var elementTime = getLast(".msg-info-time");
  var elementMessage = getLast(".msg-text");
  elementTime.innerText = formatDate(new Date());
  elementMessage.innerHTML = text;
  chatbotChat.scrollTop += 500;
}

function botResponse(message) {
    updateCheckingMessage(message);
}

function get(selector, root = document) {
  return root.querySelector(selector);
}

function getLast(selector, root = document) {
  const elements = root.querySelectorAll(selector);
  return elements[elements.length - 1];
}


function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}
