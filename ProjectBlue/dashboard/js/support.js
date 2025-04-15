document.getElementById('support-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect form data
    const sup_subject = document.getElementById('subject').value;
    const sup_message = document.getElementById('message').value;

    // Send data to the backend
    fetch("http://127.0.0.1:8000/support_form", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ sup_subject, sup_message })
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok) {
            alert("Support request submitted successfully!");
        } else {
            alert(data.detail || "Something went wrong.");
        }
    })
    .catch(err => {
        alert("Failed to connect to server.");
        console.error(err);
    });
});
