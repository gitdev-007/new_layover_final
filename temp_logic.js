window.calculateDynamicTravelMins = function(distance) {
    const transportType = localStorage.getItem("transportType") || "Luxury";
    const speedMap = { walking: 5, cab: 28, metro: 40, bike: 18, Sedan: 40, SUV: 38, XL: 35, Luxury: 45, Shuttle: 30 };
    const speed = speedMap[transportType] || 28;
    let trafficMultiplier = 1.3;
    return (distance / speed) * 60 * trafficMultiplier;
};

window.parseDurationToMins = function(durStr) {
    if (!durStr) return 0;
    const lowerStr = String(durStr).toLowerCase();
    let totalMins = 0;
    const hMatch = lowerStr.match(/([\d\.]+)\s*(h|hour|hours)/);
    if (hMatch) totalMins += parseFloat(hMatch[1]) * 60;
    
    const mMatch = lowerStr.match(/([\d\.]+)\s*(m|min|mins|minute|minutes)/);
    if (mMatch) totalMins += parseFloat(mMatch[1]);
    
    if (!hMatch && !mMatch) {
        const val = parseFloat(lowerStr);
        if (!isNaN(val)) {
            if (val <= 24) totalMins += val * 60;
            else totalMins += val;
        }
    }
    return totalMins;
};

window.updateTimeCalculations = function() {
    const layoverDurationRaw = localStorage.getItem('layover_duration') || '8';
    const layoverDurationHours = parseInt(layoverDurationRaw, 10);
    const flightDepartureRaw = localStorage.getItem('flight_departure') || '';
    
    let totalMins = layoverDurationHours * 60;
    let bufferMins = 120;
    let expMins = 0;
    let worstTravelMins = 0;

    if (window.layoverList.length > 0) {
        let maxDist = 0;
        window.layoverList.forEach(item => {
            expMins += window.parseDurationToMins(item.duration);
            if (item.distance > maxDist) maxDist = item.distance;
        });
        worstTravelMins = Math.round(window.calculateDynamicTravelMins(maxDist) * 2 + 30);
    }

    let remainingMins = totalMins - bufferMins - worstTravelMins - expMins;
    const format = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

    const timeTotalEl = document.getElementById('time-total');
    const timeTravelEl = document.getElementById('time-travel');
    const timeExpEl = document.getElementById('time-exp');
    
    if (timeTotalEl) timeTotalEl.textContent = layoverDurationHours + 'h';
    if (timeTravelEl) timeTravelEl.textContent = format(worstTravelMins);
    if (timeExpEl) timeExpEl.textContent = format(expMins);
    
    let depTimeStr = '--:--';
    if (flightDepartureRaw) {
        try {
            const depDate = new Date(flightDepartureRaw);
            if (!isNaN(depDate.getTime())) {
                depTimeStr = depDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
            }
        } catch(e) {}
    }
    const timeDepartureEl = document.getElementById('time-departure');
    if (timeDepartureEl) timeDepartureEl.textContent = `Departure ${depTimeStr}`;

    let remEl = document.getElementById('time-remaining');
    let remContainer = document.getElementById('rem-container');
    if (remEl && remContainer) {
        if (remainingMins < 15) {
            window.isRisk = true;
            remEl.textContent = remainingMins < 0 ? Math.abs(remainingMins) + 'm Over' : format(remainingMins);
            remEl.style.color = '#dc2626';
            remContainer.style.backgroundColor = '#fef2f2';
            remContainer.style.border = '1px solid #fee2e2';
        } else if (remainingMins <= 45) {
            window.isRisk = false;
            remEl.textContent = format(remainingMins);
            remEl.style.color = '#b45309';
            remContainer.style.backgroundColor = '#fffbeb';
            remContainer.style.border = '1px solid #fef3c7';
        } else {
            window.isRisk = false;
            remEl.textContent = format(remainingMins);
            remEl.style.color = '#15803d';
            remContainer.style.backgroundColor = '#ecfdf5';
            remContainer.style.border = '1px solid #d1fae5';
        }
    }
};