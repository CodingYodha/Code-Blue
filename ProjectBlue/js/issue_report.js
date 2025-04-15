const imageInput = document.getElementById('imageFileInput');

/* user_report.js */
document.getElementById('report-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect form data
    const zap_id = document.getElementById('zap-id').value;
    const event_type = document.getElementById('event-type').value;
    const person_contact = document.getElementById('contact').value;
    const person_name = document.getElementById('name').value;
    const event_location = document.getElementById('location').value;
    const person_message = document.getElementById('message').value;
    const file = imageInput.files[0];

    if (!file) {
        alert('Please select an image file first.');
        return;
    }

    // Create FormData object
    const formData = new FormData();
    formData.append('zap_id', zap_id); 
    formData.append('event_type', event_type);
    formData.append('person_contact', person_contact);
    formData.append('person_name', person_name);
    formData.append('event_location', event_location);
    formData.append('person_message', person_message);
    formData.append('event_photo', file);

    // Send data to the backend
    fetch("http://127.0.0.1:8000/issue_report", {
        method: "POST",
        body: formData,
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok) {
            alert(data.message || "Report submitted successfully!");
        } else {
            alert(data.detail || "Something went wrong.");
        }
    })
    .catch(err => {
        alert("Failed to connect to server: " + err.message);
    });
});

imageInput.addEventListener('change', () => {
    if (imageInput.files.length > 0) {
        console.log(`File selected: ${imageInput.files[0].name}`);
    }
});