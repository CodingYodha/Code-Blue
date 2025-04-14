    const form = document.getElementById('login-form');
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      

      const email = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })
      .then(async response => {
        const data = await response.json();
        if (response.ok) {
          alert(`Login successful! Welcome, ${data.user}`);
          window.location.href = 'dashboard/dashboard.html'; // Redirect to dashboard
        } else {
          alert('Login failed: ' + data.detail);
        }
      })
      .catch(error => {
        alert('Error connecting to server: ' + error.message);
        console.error(error);
      });
    });
