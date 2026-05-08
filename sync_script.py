import re

with open('yourplan.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('temp_logic.js', 'r', encoding='utf-8') as f:
    logic = f.read()

new_script = r'''<script>
window.layoverList = [];

''' + logic + r'''

document.addEventListener('DOMContentLoaded', () => {
    const finalizeBtn = document.getElementById('finalize-btn');
    if (finalizeBtn) {
        finalizeBtn.onclick = () => {
            if (window.layoverList.length === 0) {
                alert('Please add at least one experience to your itinerary.');
                return;
            }
            
            // To maintain compatibility with finalize_itinerary.html, construct the state it expects
            const layoverDurationRaw = localStorage.getItem('layover_duration') || '8';
            let layoverDurationMinutes = parseInt(layoverDurationRaw, 10) * 60;
            let totalExperienceMinutes = 0;
            let maxDist = 0;
            
            let processedItems = window.layoverList.map((item, idx) => {
                let mins = window.parseDurationToMins(item.duration);
                if (item.distance > maxDist) maxDist = item.distance;
                totalExperienceMinutes += mins;
                
                return {
                    id: item.id || Date.now() + idx,
                    category: item.category || 'Experience',
                    title: item.name,
                    selectedDurationMinutes: mins,
                    transitOverheadMinutes: 0, // Will be handled globally in final view now
                    priority: idx + 1,
                    originalItem: item
                };
            });
            
            let totalTransitMinutes = window.layoverList.length > 0 ? Math.round(window.calculateDynamicTravelMins(maxDist) * 2 + 30) : 0;
            let remainingMinutes = layoverDurationMinutes - 120 - totalTransitMinutes - totalExperienceMinutes;
            
            const finalState = {
                layoverDurationMinutes: layoverDurationMinutes,
                airportBufferMinutes: 120,
                selectedItems: processedItems,
                totalExperienceMinutes: totalExperienceMinutes,
                totalTransitMinutes: totalTransitMinutes,
                remainingMinutes: remainingMinutes
            };
            
            localStorage.setItem('final_itinerary_data', JSON.stringify(finalState));
            window.location.href = 'finalize_itinerary.html';
        };
    }

    try {
        const stored = localStorage.getItem('layoverList');
        window.layoverList = stored ? JSON.parse(stored) : [];
    } catch(e) { window.layoverList = []; }

    window.moveUp = function(i) {
        if (i > 0) {
            let temp = window.layoverList[i];
            window.layoverList[i] = window.layoverList[i-1];
            window.layoverList[i-1] = temp;
            window.saveAndRender();
        }
    };
    
    window.moveDown = function(i) {
        if (i < window.layoverList.length - 1) {
            let temp = window.layoverList[i];
            window.layoverList[i] = window.layoverList[i+1];
            window.layoverList[i+1] = temp;
            window.saveAndRender();
        }
    };
    
    window.removeItem = function(name) {
        window.layoverList = window.layoverList.filter(i => i.name !== name);
        window.saveAndRender();
    };
    
    window.saveAndRender = function() {
        localStorage.setItem('layoverList', JSON.stringify(window.layoverList));
        window.renderItinerary();
    };

    window.renderItinerary = function() {
        const listContainer = document.getElementById('itinerary-list');
        const countEl = document.getElementById('plan-activity-count');
        if (countEl) countEl.textContent = `${window.layoverList.length} activit${window.layoverList.length === 1 ? 'y' : 'ies'} scheduled`;

        if (window.layoverList.length === 0) {
            listContainer.innerHTML = `
                <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-xl flex flex-col items-center justify-center text-center">
                    <span class="material-symbols-outlined text-[48px] text-outline-variant mb-4">list_alt_add</span>
                    <h4 class="font-h2 text-on-surface font-semibold mb-2">No Experiences Yet</h4>
                    <p class="font-body-md text-secondary">Browse the marketplace and add experiences to start planning your perfect layover.</p>
                </div>
            `;
        } else {
            let html = '';
            window.layoverList.forEach((item, index) => {
                html += `
                    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-md flex flex-col gap-3 group hover:border-primary/40 transition-colors shadow-sm relative">
                        <div class="flex items-center gap-md">
                            <div class="flex flex-col items-center justify-center text-outline-variant gap-1 shrink-0">
                                <button onclick="window.moveUp(${index})" class="hover:text-primary ${index===0?'opacity-30 pointer-events-none':''}"><span class="material-symbols-outlined text-[20px]">keyboard_arrow_up</span></button>
                                <span class="font-bold text-sm w-6 text-center text-primary bg-primary-fixed rounded-full aspect-square flex items-center justify-center">${index + 1}</span>
                                <button onclick="window.moveDown(${index})" class="hover:text-primary ${index===window.layoverList.length-1?'opacity-30 pointer-events-none':''}"><span class="material-symbols-outlined text-[20px]">keyboard_arrow_down</span></button>
                            </div>
                            
                            <div class="w-16 h-16 rounded-lg bg-surface-container overflow-hidden shrink-0 border border-outline-variant/30 hidden sm:block">
                                ${item.image ? `<img class="w-full h-full object-cover" src="${item.image}"/>` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-outline-variant">image</span></div>`}
                            </div>
                            <div class="flex-grow min-w-0">
                                <div class="flex items-center flex-wrap">
                                    <h4 class="font-h2 text-body-lg font-semibold truncate">${item.name}</h4>
                                </div>
                                <p class="font-body-md text-secondary flex items-center gap-1 mt-0.5 text-sm">
                                    ${item.category} • ${item.duration ? item.duration.replace('h', ' hr').replace('m', ' min') + ' stay' : ''} ${item.distance ? `• ${item.distance} km` : ''}
                                </p>
                            </div>
                            <button onclick="window.removeItem('${item.name.replace(/'/g, "\\'")}')" class="text-outline-variant hover:text-error transition-colors p-2 rounded-md hover:bg-error-container shrink-0">
                                <span class="material-symbols-outlined">delete</span>
                            </button>
                        </div>
                    </div>
                `;
            });
            listContainer.innerHTML = html;
        }

        window.updateTimeCalculations();
    };

    window.renderItinerary();
});
</script>'''

# Manual replacement to avoid re parsing issues
start_idx = content.find('<script>')
end_idx = content.rfind('</script>') + len('</script>')

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + new_script + content[end_idx:]
    with open('yourplan.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Synchronized yourplan.html state to match marketplace.")
else:
    print("Could not find script tags.")
