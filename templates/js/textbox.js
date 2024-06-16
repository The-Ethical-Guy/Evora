
function CopyCodeFunc(event) {
    var button = event.target; // The clicked button
    var messageBot = button.closest('.message-bot'); // Closest parent with class 'message-bot'
    var codeElement = messageBot.querySelector('pre code'); // The code block inside the message-bot div
    var codeContent = codeElement.textContent; // Get the text content of the code block

    // Copy the code content to clipboard
    navigator.clipboard.writeText(codeContent).then(function() {
        console.log('Code copied successfully!');
    }).catch(function(error) {
        console.error('Failed to copy code: ', error);
    });
}

document.addEventListener('click', function(event) {
    if (event.target && event.target.classList.contains('copy-button')) {
        CopyCodeFunc(event); // Call the function when a copy button is clicked
    }
});



copyCode.addEventListener("click", CopyCodeFunc);
