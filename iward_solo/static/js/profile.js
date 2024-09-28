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

async function submitValidation() {
    const number = document.getElementById('validation-number').value;

    try {
        const response = await fetch('/validate_step', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ number: number }),
        });

        if (response.ok) {
            document.getElementById('information-message').textContent = 'Validation done.';
            document.getElementById('information-message').style.display = 'block';
            document.getElementById('error-message').style.display = 'none';
        } else {
            document.getElementById('error-message').textContent = 'Validation failed. Please try again.';
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('information-message').style.display = 'none';
        }
    } catch (error) {
        document.getElementById('error-message').textContent = 'An error occurred. Please try again later.';
        document.getElementById('error-message').style.display = 'block';
        document.getElementById('information-message').style.display = 'none';
    }
}