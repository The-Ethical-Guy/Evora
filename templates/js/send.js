var chatbox = document.getElementById("chatbox");
var message = document.getElementById("message");
var send = document.getElementById("send");

function escapeHtml(text) {
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function sendMessage() {
    var userMessage = message.value.trim(); 
    if (userMessage === "") {
        return;
    }

    userMessage = escapeHtml(userMessage);
    userMessage = userMessage.replace(/\n/g, "<br>");
    var userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.innerHTML = "<strong class='you'>You</strong><br>" + userMessage;
    chatbox.appendChild(userDiv);
    chatbox.scrollTop = chatbox.scrollHeight;

    message.value = "";

    fetch("/get_response?message=" + encodeURIComponent(userMessage))
        .then(function(response) {
            return response.text();
        })
        .then(function(botMessage) {
            botMessage = escapeHtml(botMessage);
            botMessage = botMessage.replace(/\n/g, "<br>");
            botMessage = botMessage.replace(/Evora:/g, "<strong class='evora'>Evora</strong><br>");
            var botDiv = document.createElement("div");
            botDiv.className = "message-bot";
            botDiv.innerHTML = botMessage + "<br><br>";
            chatbox.appendChild(botDiv);

            chatbox.scrollTop = chatbox.scrollHeight;
        });
}

send.addEventListener("click", sendMessage);

message.addEventListener("keydown", function(event) {
    if (event.keyCode === 13) { // Enter key
        event.preventDefault(); // Prevent the default behavior of the Enter key
        sendMessage();
    }
});
