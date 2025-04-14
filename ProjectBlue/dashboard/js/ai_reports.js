document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("reportTableBody");

  // Fetch data from the server
  fetch("http://localhost:8000/get_ai_report")
    .then(async (res) => {
      if (!res.ok) {
        throw new Error("Failed to fetch data");
      }
      const data = await res.json();

      // Populate the table with data
      data.forEach((ai_report) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${ai_report.zap_id}</td>
          <td>${ai_report.event_type}</td>
          <td><img src="${ai_report.event_photo}" alt="Event Photo" style="width: 50px; height: 50px;"></td>
          <td>${ai_report.person_contact}</td>
          <td>${ai_report.person_name}</td>
          <td>${ai_report.event_location}</td>
          <td>${ai_report.person_message}</td>
          <td>
            <input type="checkbox" class="gov-verified-checkbox" data-zap-id="${ai_report.zap_id}" ${
          ai_report.isGovVerified === 1 ? "checked" : ""
        }>
          </td>
        `;
        tableBody.appendChild(row);
      });

      // Add event listeners to checkboxes
      document.querySelectorAll(".gov-verified-checkbox").forEach((checkbox) => {
        checkbox.addEventListener("change", (event) => {
          const zapId = event.target.getAttribute("data-zap-id");
          const isChecked = event.target.checked ? 1 : 0;

          // Send update request to the server
          fetch("http://localhost:8000/update_gov_verified", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              zap_id: zapId,
              isGovVerified: isChecked,
            }),
          })
            .then((res) => {
              if (!res.ok) {
                throw new Error("Failed to update Gov Verified status");
              }
              return res.json();
            })
            .then((data) => {
              console.log(data.message);
            })
            .catch((err) => {
              console.error(err);
              alert("Failed to update Gov Verified status");
            });
        });
      });
    })
    .catch((err) => {
      console.error(err);
      const row = document.createElement("tr");
      row.innerHTML = `<td colspan="8" style="color: red;">Failed to load data</td>`;
      tableBody.appendChild(row);
    });
});