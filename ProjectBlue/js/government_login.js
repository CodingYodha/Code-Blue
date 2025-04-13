/* government_login.js */
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Here, you would typically make an API call to authenticate the user.
    // For now, let's just simulate a successful login.
    alert('Login successful!');
    window.location.href = 'dashboard.html'; // Redirect to dashboard
  });