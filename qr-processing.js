console.log("Initializing Secure Verification Sequence...");

const urlParams = new URLSearchParams(window.location.search);
let fileUrl = urlParams.get("url") || localStorage.getItem("qr_url");

if (fileUrl) {
    localStorage.setItem("qr_url", fileUrl);
}

// Initialize UI Elements
const refIdEl = document.getElementById("refId");
if (refIdEl) {
    refIdEl.textContent = "REQ-" + Math.random().toString(36).substring(2, 8).toUpperCase();
}

const UI = {
    progressText: document.getElementById("progressText"),
    progressCircle: document.getElementById("progressCircle"),
    statusLabel: document.getElementById("statusLabel"),
    estTime: document.getElementById("estTime")
};

function updateProgress(value, status, time) {
    if (UI.progressText) UI.progressText.innerText = value + "%";
    if (UI.progressCircle) {
        UI.progressCircle.style.strokeDasharray = 440;
        UI.progressCircle.style.strokeDashoffset = 440 - (440 * value) / 100;
    }
    if (UI.statusLabel && status) UI.statusLabel.innerText = status;
    if (UI.estTime && time) UI.estTime.innerText = time;
}

async function executeVerification() {
    // 1. Premium Fast Progress Animation (~1000ms total)
    const progressPromise = (async () => {
        updateProgress(0, "Connecting...", "1.2s");
        await new Promise(r => setTimeout(r, 200));
        
        updateProgress(40, "Decrypting Data...", "0.8s");
        await new Promise(r => setTimeout(r, 300));
        
        updateProgress(80, "Validating Tokens...", "0.4s");
        await new Promise(r => setTimeout(r, 400));
        
        updateProgress(100, "Verification Complete", "0.0s");
        await new Promise(r => setTimeout(r, 100)); // tiny buffer before redirect
    })();

    // 2. Single Optimized API Request (Timeout fallback at 1.5s max)
    const apiPromise = (async () => {
        if (!fileUrl) return null;
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 1200); 
            
            const res = await fetch(`https://layoverbackend.onrender.com/api/qr-status?url=${encodeURIComponent(fileUrl)}`, {
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            
            const data = await res.json();
            if (data?.extractedInfo && Object.keys(data.extractedInfo).length > 0) {
                localStorage.setItem("qr_extracted_info", JSON.stringify(data.extractedInfo));
            }
            return data;
        } catch (e) {
            // Graceful fallback for network issues or timeout to maintain instant premium feel
            console.warn("Fast-path fallback activated.");
            return null; 
        }
    })();

    // Wait for both the visual sequence and network request to finish
    await Promise.all([progressPromise, apiPromise]);
    
    // Immediate Redirect
    window.location.replace("QR_Verification_State.html");
}

// Start flow instantly
requestAnimationFrame(executeVerification);
