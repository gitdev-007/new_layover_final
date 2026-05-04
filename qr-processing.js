console.log("Processing page loaded");

if (localStorage.getItem("qr_process_done") === "true") {
  console.log("Already processed — redirecting to verification");
  window.location.href = "/QR_Verification_State.html";
}

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
let redirected = false;

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
  if (progress < 90) {
    progress += 8;
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

    // ENSURE progress only increases
    if (data.progress !== undefined && data.progress > progress) {
      progress = data.progress;
      updateProgressUI(progress);
    }

    if (data.status === "completed" || data.status === "verified") {
      // SAVE DATA BEFORE REDIRECT
      console.log("Extracted Info:", data.extractedInfo);
      localStorage.setItem("qr_process_done", "true");
      localStorage.setItem("qr_extracted_info", JSON.stringify(data.extractedInfo || {}));
      
      if (data.id) localStorage.setItem("qr_id", String(data.id));

      progress = 100;
      updateProgressUI(100);

      clearInterval(fakeProgress);
      clearInterval(pollInterval);

      if (!redirected) {
        redirected = true;
        setTimeout(() => {
          window.location.href = `/QR_Verification_State.html?url=${encodeURIComponent(fileUrl)}`;
        }, 1000);
      }
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

        localStorage.setItem("qr_process_done", "true");

        if (!redirected) {
          redirected = true;
          window.location.href = `/QR_Verification_State.html?url=${encodeURIComponent(fileUrl || "")}`;
        }
      }
    }, 10000);
  }
}

// Run polling
pollInterval = setInterval(checkStatus, 1500);
