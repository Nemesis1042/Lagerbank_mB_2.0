// static/js/flash.js

function displayFlashMessages(flashMessages) {
    if (flashMessages && flashMessages.length > 0) {
        flashMessages.forEach(message => {
            alert(message);
        });
    }
}
