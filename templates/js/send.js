var chatbox = document.getElementById("chatbox");
var message = document.getElementById("message");
var send = document.getElementById("send");

function escapeHtml(text) {
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function rescapeHtml(text) {
    var map = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        "&#39;": "'"
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function replaceNewlinesWithBr(text) {
    return text.replace(/\n/g, "<br>");
}

function formatCodeBlocks(text) {
    return text.split(/(```[\s\S]*?```)/g).map(function(part) {
        if (part.startsWith("```") && part.endsWith("```")) {
            var codeContent = part.slice(3, -3).trim();
            var codeLines = codeContent.split('\n');
            var langName = 'plaintext'; 
            
            try {
                if (codeLines.length > 0) {
                langName = codeLines[0].trim();
                codeContent = codeLines.slice(1).join('\n').trim(); 
                }
                
                highlightedCode = hljs.highlight(langName, codeContent).value;
                finalLangName = langName
                finalCode = highlightedCode
                
            } catch (error) {
                finalLangName = ' ';
                codeContent = codeLines.join('\n').trim()
                finalCode = codeContent
            }
            

            return "<div class='code-bot'>" + "<h1 class='lang-name'>" + escapeHtml(finalLangName) + "</h1>" + "<button onclick='copyCODE(this)' class='copy-button'><img class='copy-button-icon' src='/style/img/copy.png'></button>" + "<div class='code-section'>" + "<pre><code class='hljs " + escapeHtml(finalLangName) + "'>" + finalCode + "</code></pre>" + "</div>" + "</div>" + "<br>";
        } else {
            return part;
        }
    }).join("");
}


function copyCODE(button) {
    var messageBot = button.parentElement;
    var codeElement = messageBot.querySelector("pre code");
    var fullCode = codeElement.innerText; 
    navigator.clipboard.writeText(fullCode).then(function() {
        console.log('Code copied successfully!');
    }).catch(function(error) {
        console.error('Failed to copy code: ', error);
    });
}

function sendMessage() {
    console.log("sendMessage called");
    var userMessage = message.value.trim();
    if (userMessage === "") {
        return;
    }

    var UserStatement;
    if (userMessage.startsWith("/system")) {
        UserStatement = 1;
    } else {
        UserStatement = 0;
    }

    userMessage = escapeHtml(userMessage);
    userMessage = replaceNewlinesWithBr(userMessage);
    var userDiv = document.createElement("div");
    userDiv.className = "message-user";
    userDiv.innerHTML = "<strong class='you'>You</strong><br>" + userMessage + "<br><br>";
    chatbox.appendChild(userDiv);
    chatbox.scrollTop = chatbox.scrollHeight;

    message.value = "";

    var url;
    userMessage = rescapeHtml(userMessage); 
    if (UserStatement === 0) {
        url = "/get_response?message=" + encodeURIComponent(userMessage);
    } else if (UserStatement === 1) {
        url = "/exec_system?command=" + encodeURIComponent(userMessage);
    } else {
        return; 
    }

    fetch(url)
        .then(function(response) {
            return response.text();
        })
        .then(function(botMessage) {
            botMessage = formatCodeBlocks(botMessage);
            botMessage = marked.parse(botMessage);
            


            botMessage = botMessage.replace(/Evora:/g, "");

            var botDiv = document.createElement("div");
            botDiv.className = "message-bot markdown-body";
            botDiv.innerHTML = "<strong class='evora'>Evora</strong>" + botMessage + "<br>";
            chatbox.appendChild(botDiv);

            chatbox.scrollTop = chatbox.scrollHeight;
        }).catch(function(error) {
            console.error('Fetch error:', error);
        });
}

send.addEventListener("click", sendMessage);

message.addEventListener("keydown", function(event) {
    if (event.keyCode === 13) { 
        event.preventDefault(); 
        sendMessage();
    }
});
