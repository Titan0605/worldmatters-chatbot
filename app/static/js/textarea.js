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

    fetch('/text/send-text', {
        method: 'POST',
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({"text": this.value.split('\n').join(' ')})
      }
    )
    .then(data => data.json())
    .then(response =>
      console.log(response.message)
    )


    this.value = "";
    this.style.height = "auto";
  }
});
