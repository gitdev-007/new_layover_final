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

let pollCount = 0;
const MAX_POLLS = 15; // stop after ~30 sec
let pollInterval;
let lastProgress = 0;

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

async function checkStatus() {
  if (!fileUrl) return;
  pollCount++;
  console.log(`Checking status (Poll ${pollCount})...`);

  try {
    const res = await fetch(`https://layoverbackend.onrender.com/api/qr-status?url=${encodeURIComponent(fileUrl)}`);
    const data = await res.json();

    console.log("API response:", data);

    // Update progress UI - ONLY INCREASE
    if (data.progress !== undefined) {
      if (data.progress > lastProgress) {
        lastProgress = data.progress;
      }
      updateProgressUI(lastProgress);
    }

    // Save extracted data if available
    if (data.extractedInfo && Object.keys(data.extractedInfo).length > 0) {
      localStorage.setItem("qr_extracted_info", JSON.stringify(data.extractedInfo));
      console.log("Saved extracted info:", data.extractedInfo);
    }

    // If completed → go to verification
    if (data.status === "completed") {
      clearInterval(pollInterval);
      updateProgressUI(100);

      setTimeout(() => {
        window.location.href = "/QR_Verification_State.html";
      }, 500);
      return;
    }

    // Fail-safe: stop infinite loop
    if (pollCount >= MAX_POLLS) {
      clearInterval(pollInterval);
      console.warn("Backend stuck — forcing completion");
      updateProgressUI(100);

      setTimeout(() => {
        window.location.href = "/QR_Verification_State.html";
      }, 1000);
    }

  } catch (err) {
    console.error("Polling error:", err);
  }
}

// start polling
pollInterval = setInterval(checkStatus, 2000);
