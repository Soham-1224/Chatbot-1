function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    let chatbox = document.getElementById("chatbox");

    if (userMessage.trim() === "") return;

    chatbox.innerHTML += "<p><strong>You:</strong> " + userMessage + "</p>";
    document.getElementById("userInput").value = "";

    fetch("/get", {
        method: "POST",
        body: new URLSearchParams({ "msg": userMessage }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.text())
    .then(data => {
        chatbox.innerHTML += "<p><strong>Bot:</strong> " + data + "</p>";
        chatbox.scrollTop = chatbox.scrollHeight;
    });
}
