console.log("Processing page loaded");

const urlParams = new URLSearchParams(window.location.search);
const fileUrl = urlParams.get("url");

if (!fileUrl) {
  console.error("No file URL found");
}

console.log("File URL:", fileUrl);

let progress = 0;

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
    progress += 5;
    updateProgressUI(progress);
  }
}, 500);

// API polling
async function checkStatus() {
  console.log("Checking status...");

  try {
    const res = await fetch(`/api/qr-status?url=${encodeURIComponent(fileUrl)}`);
    const data = await res.json();

    console.log("API response:", data);

    if (data.progress !== undefined) {
      progress = data.progress;
      updateProgressUI(progress);
    }

    if (data.status === "completed") {
      progress = 100;
      updateProgressUI(100);

      clearInterval(fakeProgress);

      setTimeout(() => {
        window.location.href = `/QR_Verification_State.html?url=${encodeURIComponent(fileUrl)}`;
      }, 1000);
    }

  } catch (err) {
    console.error("API error:", err);
  }
}

// Run polling
setInterval(checkStatus, 2000);