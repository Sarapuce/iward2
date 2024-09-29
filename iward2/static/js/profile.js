function toggleDebug() {
    var debugText = document.getElementById("debug-text");

    if (debugText.style.display === "none") {
        debugText.style.display = "block";
    } else {
        debugText.style.display = "none";
    }
}

async function submitDisconnect(event) {
    try {
        const response = await fetch('/disconnect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        });

        if (response.ok) {
            window.location.href = '/';
        } else {
            document.getElementById('error-message').textContent = 'An error occurred during disconnect. Please try again later.';
        }
    } catch (error) {
        document.getElementById('error-message').textContent = 'An error occurred. Please try again later.';
    }
}

function showMessage(type, message) {
    let messageElement;

    if (type === 'info') {
        messageElement = document.getElementById('information-message');
        messageElement.style.backgroundColor = '#3498db';
        messageElement.style.color = 'white';
        messageElement.style.border = '1px solid #2980b9';
    } else if (type === 'error') {
        messageElement = document.getElementById('error-message');
        messageElement.style.backgroundColor = '#e74c3c';
        messageElement.style.color = 'white';
        messageElement.style.border = '1px solid #c0392b';
    }

    // Set text content and display the message
    messageElement.textContent = message;
    messageElement.style.display = 'block';
    messageElement.style.opacity = '1'; // Full opacity
    messageElement.style.position = 'fixed';
    messageElement.style.bottom = '20px';
    messageElement.style.left = '50%';
    messageElement.style.transform = 'translateX(-50%)';
    messageElement.style.padding = '15px 20px';
    messageElement.style.borderRadius = '5px';
    messageElement.style.fontSize = '1em';
    messageElement.style.zIndex = '1000';

    setTimeout(() => {
        let opacity = 1;
        const fadeInterval = setInterval(() => {
            if (opacity <= 0) {
                clearInterval(fadeInterval);
                messageElement.style.display = 'none';
            } else {
                opacity -= 0.05;
                messageElement.style.opacity = opacity.toString();
            }
        }, 50);
    }, 5000);
}

async function submitValidation() {
    const number = document.getElementById('validation-number').value;

    try {
        const response = await fetch('/validate_steps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ step_number: number }),
        });

        if (response.ok) {
            showMessage('info', 'Validation done.');
            setTimeout(() => {
                window.location.reload();  // Refresh the page
            }, 1000);
        } else {
            showMessage('error', 'Validation failed. Please try again.');
        }
    } catch (error) {
        showMessage('error', 'An error occurred. Please try again later.');
    }
}
