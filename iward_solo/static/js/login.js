async function submitForm(event) {
    event.preventDefault();
    const password = document.getElementById('password').value;
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password }),
        });
        window.location.href = '/';
    } catch (error) {
        document.getElementById('error-message').textContent = 'An error occurred. Please try again later.';
    }
}