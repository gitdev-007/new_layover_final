import codecs
import re

def sync_planner_state():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Define the new centralized planner state engine
    engine_script = """
window.getPlannerState = function(listToCalculate = window.layoverList) {
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
        let mins = 0;
        const durStr = (item.duration || '').toLowerCase();
        if (durStr.includes('h')) mins += parseFloat(durStr) * 60;
        else if (durStr.includes('m')) mins += parseFloat(durStr);
        
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
        travelMins += Math.round((currentDist * 3) + 15); // Return trip
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
    let state = window.getPlannerState(window.layoverList);
    return { expMins: state.totalExperienceMinutes, worstTravelMins: state.totalTransitMinutes };
};

window.calculateTimingForDraft = function() {
    let state = window.getPlannerState(window.draftLayoverList);
    return { expMins: state.totalExperienceMinutes, worstTravelMins: state.totalTransitMinutes };
};
"""

    html = re.sub(r'window\.calculateTiming = function\(\) \{.*?(?=window\.draftMoveUp = function)', engine_script, html, flags=re.DOTALL)

    update_calculations = """
window.updateTimeCalculations = function() {
    const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

    let state = window.getPlannerState(window.layoverList);
    
    const flightDepartureRaw = localStorage.getItem('flight_departure') || '';
    if (flightDepartureRaw) {
        if (flightDepartureRaw.includes(':') && flightDepartureRaw.length <= 5) {
            document.getElementById('time-departure').textContent = `Departure ${flightDepartureRaw}`;
        } else {
            try {
                const depDate = new Date(flightDepartureRaw);
                if (!isNaN(depDate.getTime())) {
                    const hours = depDate.getHours().toString().padStart(2, '0');
                    const mins = depDate.getMinutes().toString().padStart(2, '0');
                    document.getElementById('time-departure').textContent = `Departure ${hours}:${mins}`;
                }
            } catch(e) {}
        }
    }

    document.getElementById('time-total').textContent = state.layoverDurationMinutes > 0 ? formatTime(state.layoverDurationMinutes) : '--';
    document.getElementById('time-buffer').textContent = formatTime(state.airportBufferMinutes);
    document.getElementById('time-travel').textContent = formatTime(state.totalTransitMinutes);
    document.getElementById('time-exp').textContent = formatTime(state.totalExperienceMinutes);

    if (state.layoverDurationMinutes > 0) {
        let remaining = state.remainingMinutes;
        const remContainer = document.getElementById('rem-container');
        const remLabel = document.getElementById('rem-label');
        const remTime = document.getElementById('time-remaining');

        if (remaining < 0) {
            window.isRisk = true;
            remContainer.className = 'bg-error-container py-3 px-3 rounded-2xl border border-error/50 shadow-sm flex flex-col justify-center min-w-[80px] transition-colors';
            remLabel.className = 'font-label-caps text-[9px] text-error leading-tight uppercase tracking-widest mb-1';
            remLabel.textContent = 'Over by';
            remTime.className = 'font-h3 text-[15px] text-error font-bold tracking-tight';
            remTime.textContent = formatTime(Math.abs(remaining));
        } else if (remaining < 60) {
            window.isRisk = false;
            remContainer.className = 'bg-tertiary-fixed py-3 px-3 rounded-2xl border border-tertiary-container/30 shadow-sm flex flex-col justify-center min-w-[80px] transition-colors';
            remLabel.className = 'font-label-caps text-[9px] text-tertiary-container leading-tight uppercase tracking-widest mb-1';
            remLabel.textContent = 'Tight';
            remTime.className = 'font-h3 text-[15px] text-tertiary-container font-bold tracking-tight';
            remTime.textContent = formatTime(remaining);
        } else {
            window.isRisk = false;
            remContainer.className = 'bg-emerald-50 py-3 px-3 rounded-2xl border border-emerald-100/50 shadow-sm flex flex-col justify-center min-w-[80px] transition-colors';
            remLabel.className = 'font-label-caps text-[9px] text-emerald-800 leading-tight uppercase tracking-widest mb-1';
            remLabel.textContent = 'Remaining';
            remTime.className = 'font-h3 text-[15px] text-emerald-700 font-bold tracking-tight';
            remTime.textContent = formatTime(remaining);
        }
    }
};
"""

    html = re.sub(r'window\.updateTimeCalculations = function\(\) \{.*?(?=window\.updateListIndicator = function)', update_calculations, html, flags=re.DOTALL)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed marketplace calculations.")

sync_planner_state()
