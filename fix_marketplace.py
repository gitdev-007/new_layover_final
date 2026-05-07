import codecs
import re

def fix_marketplace():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_script = """window.calculateTiming = function() {
    let expMins = 0;
    window.layoverList.forEach(item => {
        let mins = 0;
        const durStr = (item.duration || '').toLowerCase();
        if (durStr.includes('h')) {
            mins = parseFloat(durStr) * 60;
        } else if (durStr.includes('m')) {
            mins = parseFloat(durStr);
        }
        expMins += mins;
    });

    let worstTravelMins = 0;
    if (window.layoverList.length > 0) {
        let currentDist = 0;
        window.layoverList.forEach(item => {
            let legDistance = (currentDist === 0) ? item.distance : (currentDist + item.distance);
            worstTravelMins += Math.round((legDistance * 3) + 15);
            currentDist = item.distance;
        });
        worstTravelMins += Math.round((currentDist * 3) + 15);
    }
    return { expMins, worstTravelMins };
};

window.calculateTimingForDraft = function() {
    let expMins = 0;
    window.draftLayoverList.forEach(item => {
        let mins = 0;
        const durStr = (item.duration || '').toLowerCase();
        if (durStr.includes('h')) {
            mins = parseFloat(durStr) * 60;
        } else if (durStr.includes('m')) {
            mins = parseFloat(durStr);
        }
        expMins += mins;
    });

    let worstTravelMins = 0;
    if (window.draftLayoverList.length > 0) {
        let currentDist = 0;
        window.draftLayoverList.forEach(item => {
            let legDistance = (currentDist === 0) ? item.distance : (currentDist + item.distance);
            worstTravelMins += Math.round((legDistance * 3) + 15);
            currentDist = item.distance;
        });
        worstTravelMins += Math.round((currentDist * 3) + 15);
    }
    return { expMins, worstTravelMins };
};

window.toggleListDrawer = function() {
    let drawer = document.getElementById('list-drawer');
    let overlay = document.getElementById('drawer-overlay');
    if (!drawer) {
        drawer = document.createElement('div');
        drawer.id = 'list-drawer';
        drawer.className = 'fixed bottom-4 left-1/2 -translate-x-1/2 w-[95%] max-w-[400px] max-h-[80vh] bg-surface-container-low shadow-2xl rounded-xl z-[100] transition-all duration-300 opacity-0 scale-95 pointer-events-none flex flex-col border border-outline-variant';
        document.body.appendChild(drawer);

        overlay = document.createElement('div');
        overlay.id = 'drawer-overlay';
        overlay.className = 'fixed inset-0 bg-black/40 z-[95] transition-opacity duration-300 opacity-0 pointer-events-none backdrop-blur-sm';
        overlay.onclick = () => window.toggleListDrawer();
        document.body.appendChild(overlay);
    }

    const isOpen = drawer.classList.contains('opacity-100');
    if (isOpen) {
        drawer.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
        drawer.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
        overlay.classList.remove('opacity-100', 'pointer-events-auto');
        overlay.classList.add('opacity-0', 'pointer-events-none');
    } else {
        window.draftLayoverList = JSON.parse(JSON.stringify(window.layoverList));
        window.renderListDrawer();
        drawer.classList.remove('opacity-0', 'scale-95', 'pointer-events-none');
        drawer.classList.add('opacity-100', 'scale-100', 'pointer-events-auto');
        overlay.classList.remove('opacity-0', 'pointer-events-none');
        overlay.classList.add('opacity-100', 'pointer-events-auto');
    }
};

window.draftMoveUp = function(i) {
    if (i > 0) {
        let temp = window.draftLayoverList[i];
        window.draftLayoverList[i] = window.draftLayoverList[i-1];
        window.draftLayoverList[i-1] = temp;
        window.renderListDrawer();
    }
};

window.draftMoveDown = function(i) {
    if (i < window.draftLayoverList.length - 1) {
        let temp = window.draftLayoverList[i];
        window.draftLayoverList[i] = window.draftLayoverList[i+1];
        window.draftLayoverList[i+1] = temp;
        window.renderListDrawer();
    }
};

window.draftRemove = function(i) {
    window.draftLayoverList.splice(i, 1);
    window.renderListDrawer();
};

window.draftUpdateDuration = function(i, val) {
    window.draftLayoverList[i].duration = val;
    window.renderListDrawer();
};

window.saveListEdits = function() {
    window.layoverList = JSON.parse(JSON.stringify(window.draftLayoverList));
    window.saveLayoverList();
    window.toggleListDrawer();
    window.updateListIndicator();
    window.updateTimeCalculations();
};

window.renderListDrawer = function() {
    let drawer = document.getElementById('list-drawer');
    if (!drawer) return;
    
    let html = `
        <div class="px-4 py-3 border-b border-outline-variant flex justify-between items-center bg-surface-container-lowest rounded-t-xl shrink-0">
            <h4 class="font-bold text-sm text-primary flex items-center gap-2"><span class="material-symbols-outlined text-[16px]">list_alt</span> Edit Experiences</h4>
            <button onclick="window.toggleListDrawer()" class="text-secondary hover:text-primary"><span class="material-symbols-outlined text-[18px]">close</span></button>
        </div>
        <div class="p-4 overflow-y-auto flex-1 space-y-3">
    `;
    
    if (window.draftLayoverList.length === 0) {
        html += `<p class="text-xs text-secondary text-center py-4">No items added yet.</p>`;
    } else {
        let { expMins, worstTravelMins } = window.calculateTimingForDraft();
        const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

        window.draftLayoverList.forEach((item, index) => {
            let indTravel = Math.round((item.distance * 3) + 15);
            
            let optionsHTML = '';
            const cat = (item.category || '').toLowerCase();
            
            if (cat.includes('hotel')) {
                const opts = ['3h', '4h', '6h', '8h', '10h', '12h', '16h', '24h'];
                opts.forEach(o => {
                    const label = o.replace('h', ' Hours');
                    optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                });
            } else if (cat.includes('restaurant')) {
                const opts = ['30m', '1h', '1.5h', '2h'];
                opts.forEach(o => {
                    const label = o === '30m' ? '30 Min' : o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                    optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                });
            } else if (cat.includes('spa')) {
                const opts = ['30m', '1h', '1.5h', '2h', '2.5h', '3h'];
                opts.forEach(o => {
                    const label = o === '30m' ? '30 Min' : o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                    optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                });
            } else {
                const opts = ['30m', '1h', '2h', '3h', '4h'];
                opts.forEach(o => {
                    const label = o === '30m' ? '30 Min' : o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                    optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                });
            }

            html += `
                <div class="flex flex-col gap-2 bg-surface p-3 rounded-lg border border-outline-variant relative group">
                    <div class="flex items-center gap-3">
                        <span class="font-bold text-primary text-[14px] w-4 text-center">${index + 1}</span>
                        ${item.image ? `<img src="${item.image}" class="w-10 h-10 rounded object-cover">` : `<div class="w-10 h-10 rounded bg-secondary-container flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-on-secondary-container text-[16px]">image</span></div>`}
                        <div class="flex-1 min-w-0">
                            <p class="font-bold text-[11px] text-primary truncate">${item.name}</p>
                            <p class="text-[9px] text-secondary mt-0.5">${item.category} &bull; Est ${formatTime(indTravel)} travel</p>
                        </div>
                        <div class="flex flex-col gap-1 items-end">
                            <div class="flex gap-1">
                                <button onclick="window.draftMoveUp(${index})" class="p-0.5 border rounded hover:bg-surface-container-high ${index === 0 ? 'opacity-30 pointer-events-none' : ''}"><span class="material-symbols-outlined text-[14px]">arrow_upward</span></button>
                                <button onclick="window.draftMoveDown(${index})" class="p-0.5 border rounded hover:bg-surface-container-high ${index === window.draftLayoverList.length - 1 ? 'opacity-30 pointer-events-none' : ''}"><span class="material-symbols-outlined text-[14px]">arrow_downward</span></button>
                            </div>
                            <button onclick="window.draftRemove(${index})" class="text-error hover:bg-error-container p-0.5 rounded-md mt-1 transition-colors">
                                <span class="material-symbols-outlined text-[14px]">delete</span>
                            </button>
                        </div>
                    </div>
                    <div class="flex gap-2 items-center mt-1 border-t border-outline-variant pt-2">
                        <div class="flex-1">
                            <span class="text-[9px] text-secondary block mb-0.5">Duration</span>
                            <div class="relative flex items-center">
                                <select onchange="window.draftUpdateDuration(${index}, this.value)" class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-1.5 pr-4 py-1 text-[9px] font-bold text-primary outline-none cursor-pointer hover:bg-surface-container-low transition-colors appearance-none">
                                    ${optionsHTML}
                                </select>
                                <span class="material-symbols-outlined absolute right-1 text-[12px] pointer-events-none text-primary/70">arrow_drop_down</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        html += `
            <div class="mt-2 pt-3 border-t border-outline-variant flex flex-col gap-1 text-[10px] text-secondary font-medium">
                <div class="flex justify-between">
                    <span>Experience Time:</span>
                    <span class="font-bold text-primary">${formatTime(expMins)}</span>
                </div>
                <div class="flex justify-between">
                    <span>Est. Travel Overhead:</span>
                    <span class="font-bold text-primary">${formatTime(worstTravelMins)}</span>
                </div>
            </div>
        `;
    }
    
    html += `</div>
        <div class="p-3 bg-surface-container-lowest border-t border-outline-variant flex justify-between gap-3 shrink-0 rounded-b-xl">
            <button onclick="window.toggleListDrawer()" class="flex-1 py-2 rounded-lg border border-outline-variant font-bold text-xs text-secondary hover:bg-surface-container-high transition-colors">Cancel</button>
            <button onclick="window.saveListEdits()" class="flex-1 py-2 rounded-lg bg-primary text-white font-bold text-xs shadow-md hover:bg-primary/90 transition-colors">Save Changes</button>
        </div>
    `;
    drawer.innerHTML = html;
};

window.updateTimeCalculations = function() {
    const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

    const layoverDurationRaw = localStorage.getItem('layover_duration') || '0';
    const totalLayoverMins = parseInt(layoverDurationRaw, 10) * 60;
    
    const flightDepartureRaw = localStorage.getItem('flight_departure') || '';
    if (flightDepartureRaw) {
        try {
            const depDate = new Date(flightDepartureRaw);
            if (!isNaN(depDate.getTime())) {
                const hours = depDate.getHours().toString().padStart(2, '0');
                const mins = depDate.getMinutes().toString().padStart(2, '0');
                document.getElementById('time-departure').textContent = `Departure ${hours}:${mins}`;
            }
        } catch(e) {}
    }

    let bufferMins = 120;
    document.getElementById('time-total').textContent = totalLayoverMins > 0 ? formatTime(totalLayoverMins) : '--';
    document.getElementById('time-buffer').textContent = formatTime(bufferMins);

    let { expMins, worstTravelMins } = window.calculateTiming();
    
    document.getElementById('time-travel').textContent = formatTime(worstTravelMins);
    document.getElementById('time-exp').textContent = formatTime(expMins);

    if (totalLayoverMins > 0) {
        let remaining = totalLayoverMins - bufferMins - worstTravelMins - expMins;
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

window.updateListIndicator = function() {
    let indicator = document.getElementById('global-list-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'global-list-indicator';
        indicator.className = 'fixed bottom-[75px] left-1/2 -translate-x-1/2 bg-white border border-outline-variant p-1.5 rounded-full shadow-lg z-[90] flex items-center gap-2 transition-all duration-300';
        document.body.appendChild(indicator);
    }

    const panel = document.getElementById('planner-summary-panel');
    if (window.layoverList.length > 0) {
        if (panel) {
            panel.classList.remove('hidden');
            let { expMins, worstTravelMins } = window.calculateTiming();
            const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';
            document.getElementById('summary-items').textContent = window.layoverList.length;
            document.getElementById('summary-exp-time').textContent = formatTime(expMins);
            document.getElementById('summary-transit-time').textContent = formatTime(worstTravelMins);
        }
    
        indicator.innerHTML = `
            <button onclick="window.toggleListDrawer()" class="flex items-center gap-2 bg-surface-container-low hover:bg-surface-container-highest text-primary px-4 py-2 rounded-full font-label-sm transition-colors border border-outline-variant/50">
                <span class="bg-primary text-white w-4 h-4 flex items-center justify-center rounded-full font-bold text-[9px]">${window.layoverList.length}</span>
                <span class="font-semibold tracking-wide text-xs">View List</span>
            </button>
            <button id="btn-plan-my-list" onclick="window.proceedToPlan(this)" class="flex items-center gap-1.5 px-5 py-2 rounded-full font-label-sm transition-colors shadow-sm ${window.isRisk ? 'bg-secondary-fixed text-secondary cursor-not-allowed' : 'bg-primary hover:bg-primary/90 text-white'}">
                <span class="font-semibold tracking-wide text-xs">Plan My List</span>
                <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
            </button>
        `;
        indicator.style.display = 'flex';
    } else {
        indicator.style.display = 'none';
        if(panel) panel.classList.add('hidden');
        let drawer = document.getElementById('list-drawer');
        if (drawer) {
            drawer.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
            drawer.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
        }
    }
};

window.proceedToPlan = function(btn) {
    if (window.layoverList.length === 0) return;
    
    if (window.isRisk) {
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<span class="font-bold tracking-wide px-2 whitespace-nowrap text-error">Insufficient safe buffer time. Please reduce experiences or travel duration before planning your trip.</span>';
        setTimeout(() => { btn.innerHTML = originalHtml; }, 3000);
        return;
    }
    
    localStorage.setItem("tripPlanActivated", "true");
    btn.classList.add('opacity-90', 'cursor-wait');
    
    setTimeout(() => {
        window.location.href = 'yourplan.html';
    }, 400);
};"""

    html = re.sub(r'window\.calculateTiming = function\(\) \{.*window\.proceedToPlan = function\(btn\) \{.*?\};\n</script>', new_script + '\n</script>', html, flags=re.DOTALL)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed marketplace.html.")

fix_marketplace()
