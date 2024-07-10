var chatbox = document.getElementById("chatbox");
var message = document.getElementById("message");
var send = document.getElementById("send");

function escapeHtml(text) {
    var map = {
        '&': '&',
        '<': '<',
        '>': '>',
        '"': '"',
        "'": "'"
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
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
            

            return "<div class='code-bot'>" + "<h1 class='lang-name'>" + escapeHtml(finalLangName) + "</h1>" + "<button onclick='copyCODE(this)' class='copy-button'><img class='copy-button-icon' src='/style/img/copy.png'></button>" + "<div class='code-section'>" + "<pre><code class='hljs " + escapeHtml(finalLangName) + "'>" + finalCode + "</code></pre>" + "</div>" + "</div>";
        } else {
            return part;
        }
    }).join("");
}

function copyCODE(button) {
    var messageBot = button.parentElement;
    var codeElement = messageBot.querySelector("pre code");
    var fullCode = codeElement.innerText; // Use innerText instead of textContent
    navigator.clipboard.writeText(fullCode).then(function() {
        console.log('Code copied successfully!');
    }).catch(function(error) {
        console.error('Failed to copy code: ', error);
    });
}


function replaceNewlinesWithBr(text) {
    return text.replace(/\n/g, "<br>");
}


function sendMessage() {
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
    userMessage = replaceNewlinesWithBr(userMessage); // Apply only to user message
    var userDiv = document.createElement("div");
    userDiv.className = "message-user";
    userDiv.innerHTML = "<strong class='you'>You</strong><br>" + userMessage + "<br><br>";
    chatbox.appendChild(userDiv);
    chatbox.scrollTop = chatbox.scrollHeight;

    message.value = "";

    var url;
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
            botMessage = escapeHtml(botMessage);
            botMessage = formatCodeBlocks(botMessage); // Apply code block formatting
            botMessage = botMessage.replace(/\n/g, "<br>");
            botMessage = botMessage.replace(/Evora:/g, "");
            botMessage = botMessage.split(/(<pre><code>[\s\S]*?<\/code><\/pre>)/g).map(function(part) {
                if (part.startsWith("<pre><code>") && part.endsWith("</code></pre>")) {
                    return part; // Skip replacing newlines for code blocks
                } else {
                    return replaceNewlinesWithBr(part); // Replace newlines for non-code blocks
                }
            }).join("");

            var botDiv = document.createElement("div");
            botDiv.className = "message-bot";
            botDiv.innerHTML = "<strong class='evora'>Evora</strong><br>" + botMessage + "<br><br>";
            chatbox.appendChild(botDiv);

            chatbox.scrollTop = chatbox.scrollHeight;
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    hljs.configure({useBR: true});
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

});

send.addEventListener("click", sendMessage);

message.addEventListener("keydown", function(event) {
    if (event.keyCode === 13) { // مفتاح Enter
        event.preventDefault(); // منع السلوك الافتراضي لمفتاح Enter
        sendMessage();
    }
});
