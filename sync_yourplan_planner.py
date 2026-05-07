import codecs
import re

def sync_yourplan_planner():
    filepath = 'yourplan.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_calc = """
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
        let state = window.getPlannerState(layoverList);
        return { expMins: state.totalExperienceMinutes, travelMins: state.totalTransitMinutes };
    };
"""

    html = re.sub(r'window\.calculateTiming = function\(\) \{.*?(?=window\.renderItinerary = function)', new_calc, html, flags=re.DOTALL)

    # In yourplan.html, renderItinerary needs to be updated to use state
    update_itinerary = """
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
                            <button onclick="removeItem('${item.name.replace(/'/g, "\\\\'")}')" class="text-outline-variant hover:text-error transition-colors p-2 rounded-md hover:bg-error-container shrink-0">
                                <span class="material-symbols-outlined">delete</span>
                            </button>
                        </div>
                    </div>
                `;
            });
            listContainer.innerHTML = html;
        }

        const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

        let state = window.getPlannerState(layoverList);
        let journeyMins = state.remainingMinutes;
        
        let journeyTimeEl = document.getElementById('plan-journey-time');
        let journeyCard = journeyTimeEl.closest('div');
        
        if (state.layoverDurationMinutes > 0) {
            document.getElementById('plan-total-duration').textContent = formatTime(state.layoverDurationMinutes);
        } else {
            document.getElementById('plan-total-duration').textContent = '--';
        }

        if (journeyMins < 0) {
            journeyTimeEl.className = 'font-display text-h2 text-error';
            journeyTimeEl.previousElementSibling.className = 'font-label-caps text-label-caps text-error';
            journeyCard.className = 'p-md bg-error-container rounded-lg flex flex-col gap-xs border border-error transition-colors';
            journeyTimeEl.textContent = formatTime(Math.abs(journeyMins)) + ' Over';
        } else if (journeyMins < 60) {
            journeyTimeEl.className = 'font-display text-h2 text-tertiary-container';
            journeyTimeEl.previousElementSibling.className = 'font-label-caps text-label-caps text-tertiary-container';
            journeyCard.className = 'p-md bg-tertiary-fixed rounded-lg flex flex-col gap-xs border border-tertiary-container/30 transition-colors';
            journeyTimeEl.textContent = formatTime(journeyMins) + ' Left';
        } else {
            journeyTimeEl.className = 'font-display text-h2 text-primary';
            journeyTimeEl.previousElementSibling.className = 'font-label-caps text-label-caps text-primary';
            journeyCard.className = 'p-md bg-primary-fixed rounded-lg flex flex-col gap-xs transition-colors';
            journeyTimeEl.textContent = formatTime(journeyMins) + ' Left';
        }

        document.getElementById('plan-travel-time').textContent = formatTime(state.totalTransitMinutes);
    };
"""

    html = re.sub(r'window\.renderItinerary = function\(\) \{.*?(?=window\.moveUp = function)', update_itinerary, html, flags=re.DOTALL)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed yourplan calculations.")

sync_yourplan_planner()
