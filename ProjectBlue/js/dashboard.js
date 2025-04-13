/* dashboard.js */
document.getElementById('logout-button').addEventListener('click', function() {
    window.location.href = 'government_login.html'; // Redirect to login page
  });
  
  // Simulate fetching data for the dashboard
  document.getElementById('user-data').innerHTML = '<p>Local complaint/issue data submitted will be loaded here...</p>';
  document.getElementById('support-reports').innerHTML = '<p>AI predicted reports will be loaded here...</p>';
  document.getElementById('live-updates').innerHTML = '<p>Live updates will be loaded here...</p>';
  document.getElementById('oil-spills').innerHTML = '<p>You can contact us for platform support through here...</p>';
  
  // In a real application, you would fetch data from your backend API and update these sections dynamically.