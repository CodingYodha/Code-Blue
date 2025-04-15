function filterTable() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("searchTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < 3; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

// Fetch data from the server and populate the table
function fetchPublicAIReport() {
  const tableBody = document.getElementById("searchTableBody");

  fetch("http://127.0.0.1:8000/public_ai_report")
    .then(async (res) => {
      if (!res.ok) {
        throw new Error("Failed to fetch data");
      }
      const data = await res.json();

      // Populate the table with data
      data.forEach((ai_report) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${ai_report.event_location}</td>
          <td>${ai_report.event_type}</td>
          <td><img style="height:250px;width: 250px;" src="uploads/${ai_report.event_photo}" alt="Event Photo" style="width:50px;height:50px;"></td>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch((err) => {
      console.error(err);
      const row = document.createElement("tr");
      row.innerHTML = `<td colspan="3" style="color: red;">Failed to load data</td>`;
      tableBody.appendChild(row);
    });
}

// Call the function to fetch and display data
fetchPublicAIReport();