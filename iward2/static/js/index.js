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


async function submitEmailForm(event) {
    event.preventDefault();
    document.getElementById('information-message').textContent = ''
    const email = document.getElementById('email').value;
    
    try {
        const response = await fetch('/send_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
        });

        if (response.ok) {
            showMessage('info', 'Email sent.');
        } else {
            showMessage('error', 'Failed to send mail. Please try again.');
        }
    } catch (error) {
        showMessage('error', 'Failed to send mail. Please try again.');
    }
}

async function submitActivationForm(event) {
    event.preventDefault();

    const activationLink = document.getElementById('activation-link').value;

    try {
        const response = await fetch('/get_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ link: activationLink }),
        });

        if (response.ok) {
            showMessage('info', 'Code got');
            setTimeout(() => {
                window.location.reload();  // Refresh the page
            }, 1000);
        } else {
            showMessage('error', 'Failed to get code');
        }
    } catch (error) {
        showMessage('error', 'Failed to get code');
    }
}