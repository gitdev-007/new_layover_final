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

// API polling
async function checkStatus() {
  if (!fileUrl) return;
  console.log("Checking status...");

  try {
    const res = await fetch(`https://layoverbackend.onrender.com/api/qr-status?url=${encodeURIComponent(fileUrl)}`);
    const data = await res.json();

    console.log("API response:", data);

    // STORE DATA IF AVAILABLE
    if (data.extractedInfo && Object.keys(data.extractedInfo).length > 0) {
      localStorage.setItem("qr_extracted_info", JSON.stringify(data.extractedInfo));
      console.log("Saved extracted info");
    }

    // UPDATE UI PROGRESS
    if (data.progress !== undefined) {
      progress = data.progress;
      updateProgressUI(progress);
    }

    // REDIRECT ONLY WHEN DONE
    if (data.status === "completed" || data.status === "verified") {
      clearInterval(pollInterval);
      updateProgressUI(100);
      
      if (data.id) localStorage.setItem("qr_id", String(data.id));

      setTimeout(() => {
        window.location.href = "/QR_Verification_State.html";
      }, 500);
    }

  } catch (err) {
    console.error("API error:", err);
  }
}

// Run polling
pollInterval = setInterval(checkStatus, 1500);
