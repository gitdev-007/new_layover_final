<script>
document.addEventListener('DOMContentLoaded', () => {
    // ... existing initialization ...
    const finalizeBtn = document.getElementById('finalize-btn');
    if (finalizeBtn) {
        finalizeBtn.onclick = () => {
            if (layoverList.length === 0) {
                alert("Please add at least one experience to your itinerary.");
                return;
            }
            
            const finalState = window.parseDurationToMins = function(durStr) {
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

window.getPlannerState();
            localStorage.setItem('final_itinerary_data', JSON.stringify(finalState));
            window.location.href = 'finalize_itinerary.html';
        };
    }
    // ... rest of script ...
    // 1. Load basic user flight data
    const layoverDurationRaw = localStorage.getItem('layover_duration') || '8';
    const layoverDurationHours = parseInt(layoverDurationRaw, 10);
    const flightDepartureRaw = localStorage.getItem('flight_departure') || '';
    
    let depTimeStr = '--:--';
    let depDateStr = '';
    if (flightDepartureRaw) {
        if (flightDepartureRaw.includes(':') && flightDepartureRaw.length <= 5) {
            depTimeStr = flightDepartureRaw;
        } else {
            try {
                const depDate = new Date(flightDepartureRaw);
                if (!isNaN(depDate.getTime())) {
                    depTimeStr = depDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
                    depDateStr = depDate.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
                }
            } catch(e) {}
        }
    }

    const timeDepartureEl = document.getElementById('time-departure');
    if (timeDepartureEl) timeDepartureEl.textContent = `Departure ${depTimeStr}`;

    // 2. Load Layover List State
    let layoverList = [];
    try {
        const stored = localStorage.getItem('layoverList');
        layoverList = stored ? JSON.parse(stored) : [];
    } catch(e) {}

    
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

window.getPlannerState = function(listToCalculate = layoverList) {
        let totalLayoverMins = 0;
        const layoverDurationRaw = localStorage.getItem('layover_duration') || '';
        if (layoverDurationRaw.includes('h') || layoverDurationRaw.includes('H')) {
            totalLayoverMins = parseFloat(layoverDurationRaw) * 60;
        } else if (layoverDurationRaw) {
            totalLayoverMins = parseFloat(layoverDurationRaw) * 60;
        }
        
        let bufferMins = 120;
        let expMins = 0;
        let travelMins = 0;
        let currentDist = 0;
        
        let processedItems = listToCalculate.map((item, idx) => {
            let mins = window.parseDurationToMins(item.duration);
            
            let legDistance = (currentDist === 0) ? (item.distance || 0) : ((currentDist + (item.distance || 0)));
            let tMins = Math.round((legDistance * 3) + 15);
            
            currentDist = item.distance || 0;
            
            return {
                id: item.id || Date.now() + idx,
                category: item.category || 'Experience',
                title: item.name,
                selectedDurationMinutes: mins,
                transitOverheadMinutes: tMins,
                priority: idx + 1,
                originalItem: item
            };
        });
        
        processedItems.forEach(i => {
            expMins += i.selectedDurationMinutes;
            travelMins += i.transitOverheadMinutes;
        });
        
        if (processedItems.length > 0) {
            travelMins += Math.round((currentDist * 3) + 15);
        }
        
        let remaining = totalLayoverMins > 0 ? (totalLayoverMins - bufferMins - travelMins - expMins) : 0;
        
        return {
            layoverDurationMinutes: totalLayoverMins,
            airportBufferMinutes: bufferMins,
            selectedItems: processedItems,
            totalExperienceMinutes: expMins,
            totalTransitMinutes: travelMins,
            remainingMinutes: remaining
        };
    };

    window.calculateTiming = function() {
        let state = window.parseDurationToMins = function(durStr) {
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

window.getPlannerState(layoverList);
        return { expMins: state.totalExperienceMinutes, travelMins: state.totalTransitMinutes };
    };

    window.renderItinerary = function() {
        const listContainer = document.getElementById('itinerary-list');
        document.getElementById('plan-activity-count').textContent = `${layoverList.length} activit${layoverList.length === 1 ? 'y' : 'ies'} scheduled`;

        if (layoverList.length === 0) {
            listContainer.innerHTML = `
                <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-xl flex flex-col items-center justify-center text-center">
                    <span class="material-symbols-outlined text-[48px] text-outline-variant mb-4">list_alt_add</span>
                    <h4 class="font-h2 text-on-surface font-semibold mb-2">No Experiences Yet</h4>
                    <p class="font-body-md text-secondary">Browse the marketplace and add experiences to start planning your perfect layover.</p>
                </div>
            `;
        } else {
            let html = '';
            layoverList.forEach((item, index) => {
                html += `
                    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-md flex flex-col gap-3 group hover:border-primary/40 transition-colors shadow-sm relative">
                        <div class="flex items-center gap-md">
                            <div class="flex flex-col items-center justify-center text-outline-variant gap-1 shrink-0">
                                <button onclick="moveUp(${index})" class="hover:text-primary ${index===0?'opacity-30 pointer-events-none':''}"><span class="material-symbols-outlined text-[20px]">keyboard_arrow_up</span></button>
                                <span class="font-bold text-sm w-6 text-center text-primary bg-primary-fixed rounded-full aspect-square flex items-center justify-center">${index + 1}</span>
                                <button onclick="moveDown(${index})" class="hover:text-primary ${index===layoverList.length-1?'opacity-30 pointer-events-none':''}"><span class="material-symbols-outlined text-[20px]">keyboard_arrow_down</span></button>
                            </div>
                            
                            <div class="w-16 h-16 rounded-lg bg-surface-container overflow-hidden shrink-0 border border-outline-variant/30 hidden sm:block">
                                ${item.image ? `<img class="w-full h-full object-cover" src="${item.image}"/>` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-outline-variant">image</span></div>`}
                            </div>
                            <div class="flex-grow min-w-0">
                                <div class="flex items-center flex-wrap">
                                    <h4 class="font-h2 text-body-lg font-semibold truncate">${item.name}</h4>
                                </div>
                                <p class="font-body-md text-secondary flex items-center gap-1 mt-0.5 text-sm">
                                    ${item.category} • ${item.duration ? item.duration + ' stay' : ''} ${item.distance ? `• Est ${Math.round(item.distance*3 + 15)}m travel` : ''}
                                </p>
                            </div>
                            <button onclick="removeItem('${item.name.replace(/'/g, "\'")}')" class="text-outline-variant hover:text-error transition-colors p-2 rounded-md hover:bg-error-container shrink-0">
                                <span class="material-symbols-outlined">delete</span>
                            </button>
                        </div>
                    </div>
                `;
            });
            listContainer.innerHTML = html;
        }

        const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

        let state = window.parseDurationToMins = function(durStr) {
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

window.getPlannerState(layoverList);
        let journeyMins = state.remainingMinutes;
        
        
        const timeTotalEl = document.getElementById('time-total');
        const timeTravelEl = document.getElementById('time-travel');
        const timeExpEl = document.getElementById('time-exp');
        
        if (timeTotalEl) timeTotalEl.textContent = formatTime(state.layoverDurationMinutes);
        if (timeTravelEl) timeTravelEl.textContent = formatTime(state.totalTransitMinutes);
        if (timeExpEl) timeExpEl.textContent = formatTime(state.totalExperienceMinutes);

        let remEl = document.getElementById('time-remaining');
        let remContainer = document.getElementById('rem-container');
        if (remEl && remContainer) {
            if (journeyMins < 15) {
                remEl.textContent = journeyMins < 0 ? Math.abs(journeyMins) + 'm Over' : formatTime(journeyMins);
                remEl.style.color = '#dc2626';
                remContainer.style.backgroundColor = '#fef2f2';
                remContainer.style.border = '1px solid #fee2e2';
            } else if (journeyMins <= 45) {
                remEl.textContent = formatTime(journeyMins);
                remEl.style.color = '#b45309';
                remContainer.style.backgroundColor = '#fffbeb';
                remContainer.style.border = '1px solid #fef3c7';
            } else {
                remEl.textContent = formatTime(journeyMins);
                remEl.style.color = '#15803d';
                remContainer.style.backgroundColor = '#ecfdf5';
                remContainer.style.border = '1px solid #d1fae5';
            }
        }

    };
window.moveUp = function(i) {
        if (i > 0) {
            let temp = layoverList[i];
            layoverList[i] = layoverList[i-1];
            layoverList[i-1] = temp;
            window.saveAndRender();
        }
    };
    window.moveDown = function(i) {
        if (i < layoverList.length - 1) {
            let temp = layoverList[i];
            layoverList[i] = layoverList[i+1];
            layoverList[i+1] = temp;
            window.saveAndRender();
        }
    };
    window.removeItem = function(name) {
        layoverList = layoverList.filter(i => i.name !== name);
        window.saveAndRender();
    };
    window.saveAndRender = function() {
        localStorage.setItem('layoverList', JSON.stringify(layoverList));
        window.renderItinerary();
    };

    // Initial render
    window.renderItinerary();
});
</script>