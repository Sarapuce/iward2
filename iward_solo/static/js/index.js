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
        const response = await fetch('/add_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ activation_link: activationLink }),
        });

        if (response.ok) {
            alert('User added successfully!');
        } else {
            alert('Failed to add user.');
        }
    } catch (error) {
        alert('An error occurred.');
    }
}