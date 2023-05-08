const activeMutesTable = document.getElementById("active-mutes");
const muteForm = document.getElementById("mute-form");
const muteTypeSelect = document.getElementById("mute-type");
const startTimePicker = document.getElementById("start-time-picker");
const siteSelect = document.getElementById("site-select");

document.addEventListener("DOMContentLoaded", () => {
  fetchSites();
  fetchActiveMutes();
});

muteTypeSelect.addEventListener("change", () => {
  if (muteTypeSelect.value === "schedule") {
    startTimePicker.style.display = "block";
  } else {
    startTimePicker.style.display = "none";
  }
});

muteForm.addEventListener("submit", (e) => {
  e.preventDefault();
  addMute();
});

async function fetchSites() {
  const response = await fetch("/get-sites");
  const sites = await response.json();
  populateSiteSelection(sites);
}


function populateSiteSelection(sites) {
  const siteSelect = document.querySelector("#site-select");
  sites.forEach((site) => {
    const option = document.createElement("option");
    option.value = site.id; // Use "id" instead of "site_id"
    option.textContent = site.name;
    siteSelect.appendChild(option);
  });
}


async function fetchActiveMutes() {
  const response = await fetch("/get-active-mutes");
  const activeMutes = await response.json();

  for (const mute of activeMutes) {
    const tr = document.createElement("tr");

    const siteCell = document.createElement("td");
    siteCell.textContent = mute.site_name;
    tr.appendChild(siteCell);

    const startTimeCell = document.createElement("td");
    startTimeCell.textContent = mute.start_time;
    tr.appendChild(startTimeCell);

    const endTimeCell = document.createElement("td");
    endTimeCell.textContent = mute.end_time;
    tr.appendChild(endTimeCell);

    const muteStatusCell = document.createElement("td");
    muteStatusCell.textContent = mute.mute_status;
    tr.appendChild(muteStatusCell);

    activeMutesTable.querySelector("tbody").appendChild(tr);
  }
}

async function addMute() {
  const formData = new FormData(muteForm);
  const requestData = {
    id: formData.get("id"),
    mute_option: formData.get("mute_option"),
    start_time: formData.get("start_time"),
    duration: formData.get("duration"),
  };

  console.log(requestData);

  const response = await fetch("/add-mute", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  });

  if (response.ok) {
    alert("Mute added successfully!");
    location.reload();
    muteForm.reset(); // Add this line to reset the form values
    } else {
    alert("An error occurred while adding the mute.");
  }
}


function setMinMaxDatetime() {
  const startTimeInput = document.getElementById("start-time");
  const now = new Date();
  const minDatetime = now.toISOString().slice(0, 16); // Convert to datetime-local compatible format
  startTimeInput.setAttribute("min", minDatetime);

  const maxDate = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000); // One week from now
  const maxDatetime = maxDate.toISOString().slice(0, 16); // Convert to datetime-local compatible format
  startTimeInput.setAttribute("max", maxDatetime);
}

document.addEventListener("DOMContentLoaded", () => {
  setMinMaxDatetime();
});