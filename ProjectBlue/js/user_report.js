/* user_report.js */
document.getElementById('report-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Here, you would typically make an API call to submit the form data.
    // For now, let's just log the form data.
    const formData = new FormData(event.target);
    for (let pair of formData.entries()) {
      console.log(pair[0] + ': ' + pair[1]);
    }
    alert('Report submitted successfully!');
  });