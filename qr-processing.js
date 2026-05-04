console.log("Processing page loaded");

const urlParams = new URLSearchParams(window.location.search);
let fileUrl = urlParams.get("url");

// fallback from localStorage
if (!fileUrl) {
  fileUrl = localStorage.getItem("qr_url");
}

// SAVE URL FOR FUTURE USE
if (fileUrl) {
  localStorage.setItem("qr_url", fileUrl);
}

console.log("Final File URL:", fileUrl);

if (!fileUrl) {
  console.error("No file URL found — stopping API calls");
}

let progress = 0;
let pollInterval;
let fallbackStarted = false;

// Update UI
function updateProgressUI(value) {
  const text = document.getElementById("progressText");
  if (text) text.innerText = value + "%";

  const circle = document.getElementById("progressCircle");
  if (circle) {
    circle.style.strokeDasharray = 440;
    circle.style.strokeDashoffset = 440 - (440 * value) / 100;
  }
}

// Fake progress (smooth UI)
const fakeProgress = setInterval(() => {
  if (progress < 85) {
    progress += 10;
    updateProgressUI(progress);
  }
}, 300);

// API polling
async function checkStatus() {
  if (!fileUrl) return;
  console.log("Checking status...");

  try {
    const res = await fetch(`https://layoverbackend.onrender.com/api/qr-status?url=${encodeURIComponent(fileUrl)}`);
    
    let data;
    try {
      data = await res.json();
    } catch (e) {
      console.error("Invalid JSON response");
      return;
    }

    console.log("API response:", data);

    if (data.progress !== undefined) {
      progress = data.progress;
      updateProgressUI(progress);
    }

    if (data.status === "completed" || data.status === "verified") {
      progress = 100;
      updateProgressUI(100);

      clearInterval(fakeProgress);
      clearInterval(pollInterval);

      setTimeout(() => {
        window.location.href = `/QR_Verification_State.html?url=${encodeURIComponent(fileUrl)}`;
      }, 1000);
    }

  } catch (err) {
    console.error("API error:", err);
  }

  // fallback force complete after 10 sec
  if (!fallbackStarted) {
    fallbackStarted = true;
    setTimeout(() => {
      if (progress < 100) {
        progress = 100;
        updateProgressUI(100);

        clearInterval(fakeProgress);
        clearInterval(pollInterval);

        window.location.href = `/QR_Verification_State.html?url=${encodeURIComponent(fileUrl || "")}`;
      }
    }, 10000);
  }
}

// Run polling
pollInterval = setInterval(checkStatus, 1500);
