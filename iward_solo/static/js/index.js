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
            document.getElementById('information-message').textContent = 'Mail sent';
        } else {
            document.getElementById('information-message').textContent = 'Failed to send email.';
        }
    } catch (error) {
        document.getElementById('information-message').textContent = 'Failed to send email.';
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
            document.getElementById('information-message').textContent = 'Code got';
        } else {
            document.getElementById('information-message').textContent = 'Failed to get code.';
        }
    } catch (error) {
        document.getElementById('information-message').textContent = 'Failed to get code.';
    }
}