function scrollToBottom() {
  const messagesContainer = document.getElementById("messages-container");
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function scrollHistoryToBottom() {
  const historyContainer = document.getElementById("history-logs");
  historyContainer.scrollTop = historyContainer.scrollHeight;
}

function getHistory() {
  fetch("/history", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.status === "success" && data.history) {
        const historyContainer = document.getElementById("history-logs");
        historyContainer.innerHTML = "";

        const formatDate = (dateString) => {
          if (!dateString || dateString === "Ahora") return "Ahora";
          try {
            const date = new Date(dateString);
            const options = {
              weekday: "short",
              day: "2-digit",
              month: "short",
              hour: "2-digit",
              minute: "2-digit",
              hour12: false,
            };
            return date.toLocaleDateString("en-EN", options);
          } catch (error) {
            return dateString;
          }
        };

        data.history.forEach((item) => {
          const newLog = document.createElement("div");
          newLog.className = "mb-4 p-5 bg-white rounded-xl border border-gray-200 hover:border-blue-300 transition-all duration-200 shadow-sm hover:shadow-md";
          newLog.innerHTML = `
            <div class="flex flex-col gap-2 items-center justify-between mb-4">
              <h4 class="text-sm font-semibold text-blue-600 bg-blue-50 p-3 py-1 rounded-full text-center">${item.topic || "Sin tema"}</h4>
              <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">${formatDate(item.time)}</span>
            </div>
            
            <div class="space-y-4">
              <div class="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-lg border-l-4 border-blue-500">
                <div class="flex items-center mb-2">
                  <svg class="w-4 h-4 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span class="text-sm font-semibold text-blue-700 uppercase tracking-wide">Pregunta</span>
                </div>
                <p class="text-sm text-gray-800 font-medium leading-relaxed">${item.question}</p>
              </div>
              
              <div class="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-lg border-l-4 border-green-500">
                <div class="flex items-center mb-2">
                  <svg class="w-4 h-4 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span class="text-sm font-semibold text-green-700 uppercase tracking-wide">Respuesta</span>
                </div>
                <p class="text-sm text-gray-800 leading-relaxed">${item.response}</p>
              </div>
            </div>
          `;
          historyContainer.appendChild(newLog);
          scrollHistoryToBottom();
        });
      } else {
        console.error("Error fetching history:", data);
      }
    })
    .catch((error) => {
      console.error("Error loading history:", error);
    });
}

window.addEventListener("load", () => {
  scrollToBottom();
  getHistory();
});

const textarea = document.querySelector("textarea");
const sendButton = document.getElementById("send-button");

textarea.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 120) + "px";
});

textarea.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    proccessQuestion(textarea.value);
  }
});

sendButton.addEventListener("click", (e) => {
  e.preventDefault();
  proccessQuestion(textarea.value);
});

function proccessQuestion(questionText) {
  console.log("Enviar mensaje:", questionText);

  const messagesContainer = document.getElementById("messages-container");

  // Add user message
  const userMessage = document.createElement("div");
  userMessage.className = "flex items-start space-x-3 justify-end";
  userMessage.innerHTML = `
      <div class="bg-blue-400 rounded-lg rounded-tr-none p-3 max-w-md">
        <p class="text-white">${questionText}</p>
        <span class="text-xs text-blue-100 mt-1 block">Ahora</span>
      </div>
      <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center flex-shrink-0">
        <i class="fa-solid fa-user text-gray-600"></i>
      </div>
    `;
  messagesContainer.appendChild(userMessage);
  scrollToBottom();

  // Add loading message for bot
  const loadingMessage = document.createElement("div");
  loadingMessage.className = "flex items-start space-x-3 bot-loading";
  loadingMessage.innerHTML = `
      <div class="w-8 h-8 bg-blue-400 rounded-full flex items-center justify-center flex-shrink-0">
        <i class="fa-solid fa-robot text-white"></i>
      </div>
      <div class="bg-gray-50 rounded-lg rounded-tl-none p-3">
        <div class="flex space-x-1">
          <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
          <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
          <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
        <span class="text-xs text-gray-500 block mt-1">Procesando...</span>
      </div>
    `;
  messagesContainer.appendChild(loadingMessage);
  scrollToBottom();

  fetch("/text/send-text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: (questionText || "").split("\n").join(" ") }),
  })
    .then((data) => data.json())
    .then((response) => {
      // Remove loading message
      const loading = document.querySelector(".bot-loading");
      if (loading) loading.remove();

      // Add bot response
      const botMessage = document.createElement("div");
      botMessage.className = "flex items-start space-x-3";

      let botResponse = "";
      if (response.ambiguous) {
        botResponse = `
            <div class="mb-2">
              <span class="inline-flex items-center px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded-full">
                <svg class="w-4 h-4 mr-1 text-yellow-500 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M12 20a8 8 0 100-16 8 8 0 000 16z" /></svg>
                Ambigüedad
              </span>
            </div>
            <p class="text-gray-800 font-medium mb-2">${response.message}</p>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p class="text-gray-700 font-semibold mb-1">¿Te refieres a alguna de estas preguntas?</p>
              <ul class="space-y-2">
                ${response.suggestions
                  .map(
                    (q, idx) => `
                  <li class="p-2 bg-white rounded hover:bg-blue-100 border border-blue-100 cursor-pointer transition suggested-question" data-question="${encodeURIComponent(q.question)}">
                    <span class="font-medium text-blue-700">${idx + 1}.</span> <span class="text-gray-800">${q.question}</span>
                  </li>
                `
                  )
                  .join("")}
              </ul>
            </div>
          `;
      } else if (response.response) {
        botResponse = `
            <div class="mb-2 flex items-center space-x-2">
              <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4" /></svg>
              <span class="text-green-700 font-semibold">Respuesta encontrada</span>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg p-3 mb-2">
              <p class="text-gray-900 leading-relaxed">${response.response.response_text}</p>
            </div>
            ${
              response.response.follow_up && response.response.follow_up.length
                ? `
              <div class="mt-2">
                <span class="text-xs text-gray-500 font-medium">¿Te interesa saber más?</span>
                <ul class="mt-1 space-y-1">
                  ${response.response.follow_up.map((fu) => `<li class="text-blue-600 hover:text-blue-700 cursor-pointer text-sm">• ${fu}</li>`).join("")}
                </ul>
              </div>
            `
                : ""
            }
          `;
      } else {
        botResponse = `<p class="text-gray-800">${response.message}</p>`;
      }

      botMessage.innerHTML = `
        <div class="w-8 h-8 bg-blue-400 rounded-full flex items-center justify-center flex-shrink-0">
          <i class="fa-solid fa-robot text-white"></i>
        </div>
        <div class="bg-gray-50 rounded-lg rounded-tl-none p-3 max-w-lg">
          ${botResponse}
          <span class="text-xs text-gray-500 mt-1 block">Ahora</span>
        </div>
      `;

      messagesContainer.appendChild(botMessage);
      scrollToBottom();

      const suggestedQuestions = botMessage.querySelectorAll(".suggested-question");
      suggestedQuestions.forEach((suggested_question) => {
        suggested_question.addEventListener("click", function () {
          const question = decodeURIComponent(this.getAttribute("data-question"));
          textarea.value = question;
          textarea.focus();
          // Ajustar altura del textarea
          textarea.style.height = "auto";
          textarea.style.height = Math.min(textarea.scrollHeight, 120) + "px";
        });
      });
      getHistory();
    })
    .catch((error) => {
      // Remove loading message if error
      const loading = document.querySelector(".bot-loading");
      if (loading) loading.remove();
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
  textarea.value = "";
  textarea.style.height = "auto";
}
