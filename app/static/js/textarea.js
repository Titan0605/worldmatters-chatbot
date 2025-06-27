function scrollToBottom() {
  const messagesContainer = document.getElementById("messages-container");
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

window.addEventListener("load", scrollToBottom);

const textarea = document.querySelector("textarea");
textarea.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 120) + "px";
});

textarea.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    console.log("Enviar mensaje:", this.value);

    const messagesContainer = document.getElementById("messages-container");

    // Add user message
    const userMessage = document.createElement("div");
    userMessage.className = "flex items-start space-x-3 justify-end";
    userMessage.innerHTML = `
      <div class="bg-blue-400 rounded-lg rounded-tr-none p-3 max-w-md">
        <p class="text-white">${this.value}</p>
        <span class="text-xs text-blue-100 mt-1 block">Ahora</span>
      </div>
      <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center flex-shrink-0">
        <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
        </svg>
      </div>
    `;
    messagesContainer.appendChild(userMessage);
    scrollToBottom();

    fetch("/text/send-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: this.value.split("\n").join(" ") }),
    })
      .then((data) => data.json())
      .then((response) => {
        // Add bot response
        const botMessage = document.createElement("div");
        botMessage.className = "flex items-start space-x-3";

        let botResponse = "";
        if (response.ambiguous) {
          botResponse = `
          <p class="text-gray-800">${response.message}</p>
          <div class="mt-2">
            <p class="text-gray-700 font-medium">¿Te refieres a alguna de estas preguntas?</p>
            <ul class="mt-1 space-y-1">
              ${response.suggestions
                .map(
                  (q) => `
                <li class="text-blue-600 hover:text-blue-700 cursor-pointer">
                  ${q.question}
                </li>
              `
                )
                .join("")}
            </ul>
          </div>
        `;
        } else if (response.response) {
          botResponse = `
          <p class="text-gray-800">${response.response.response_text}</p>
        `;
        } else {
          botResponse = `<p class="text-gray-800">${response.message}</p>`;
        }

        botMessage.innerHTML = `
        <div class="w-8 h-8 bg-blue-400 rounded-full flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="bg-gray-50 rounded-lg rounded-tl-none p-3 max-w-lg">
          ${botResponse}
          <span class="text-xs text-gray-500 mt-1 block">Ahora</span>
        </div>
      `;

        messagesContainer.appendChild(botMessage);
        scrollToBottom();
      })
      .catch((error) => {
        console.error("Error:", error);
        const messagesContainer = document.getElementById("messages-container");
        const errorMessage = document.createElement("div");
        errorMessage.className = "flex items-start space-x-3";
        errorMessage.innerHTML = `
        <div class="w-8 h-8 bg-red-400 rounded-full flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="bg-red-50 rounded-lg rounded-tl-none p-3 max-w-lg">
          <p class="text-red-800">Lo siento, ha ocurrido un error al procesar tu mensaje.</p>
          <span class="text-xs text-red-500 mt-1 block">Ahora</span>
        </div>
      `;
        messagesContainer.appendChild(errorMessage);
        scrollToBottom();
      });

    this.value = "";
    this.style.height = "auto";
  }
});
