/* user_report.js */
document.getElementById('report-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect form data
    const zap_id = document.getElementById('zap-id').value;
    const event_type = document.getElementById('event-type').value;
    const event_photo = "image.jpg"; // Get file name
   // document.getElementById('photos').files[0]?.name

    const person_contact = document.getElementById('contact').value;
    const person_name = document.getElementById('name').value;
    const event_location = document.getElementById('location').value;
    const person_message = document.getElementById('message').value;

    // Send data to the backend
    fetch("http://localhost:8000/issue_report", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ zap_id, event_type, event_photo, person_contact, person_name, event_location, person_message })
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok) {
            alert(data.message);
        } else {
            alert(data.message || "Something went wrong.");
        }
    })
    .catch(err => {
        alert("Failed to connect to server.");
        console.error(err);
    });
});