import re

with open('marketplace.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update pill buttons to use the correct function call (renderCategory)
# Ensure we pass 'this' and the correct catId
content = content.replace("onclick=\"renderCategory('recommended', this)\"", "onclick=\"renderCategory('recommended', this)\"")
content = content.replace("onclick=\"renderCategory('hotel.html', this)\"", "onclick=\"renderCategory('hotel.html', this)\"")
content = content.replace("onclick=\"renderCategory('restaurant.html', this)\"", "onclick=\"renderCategory('restaurant.html', this)\"")
content = content.replace("onclick=\"renderCategory('spa.html', this)\"", "onclick=\"renderCategory('spa.html', this)\"")
content = content.replace("onclick=\"renderCategory('entertainment.html', this)\"", "onclick=\"renderCategory('entertainment.html', this)\"")

new_script = r'''<script>
// --- GLOBAL STATE & CONFIG ---
window.layoverList = [];
window.activeCategory = 'recommended';
window.selectedItem = null;
window.isRisk = false;

const CATEGORY_CONFIG = {
    'recommended': { title: 'Recommended For You', key: 'Recommended', icon: 'auto_awesome' },
    'hotel.html': { title: 'Hotels & Stays', key: 'Hotels', icon: 'hotel', durations: ['3h', '4h', '6h', '8h', '10h', '12h', '16h', '24h'] },
    'restaurant.html': { title: 'Food & Dining', key: 'Restaurants', icon: 'restaurant', durations: ['30m', '1h', '1.5h', '2h'] },
    'spa.html': { title: 'Spa & Wellness', key: 'Spa', icon: 'spa', durations: ['30m', '1h', '1.5h', '2h', '2.5h', '3h'] },
    'entertainment.html': { title: 'Gaming & Entertainment', key: 'Entertainment', icon: 'sports_esports', durations: ['30m', '1h', '2h', '3h', '4h'] }
};

// --- DATA INITIALIZATION ---
window.LAYOVER_INVENTORY = {
    'Hotels': [
        { name: 'The Orchid Hotel', type: 'Eco Stay', distance: 0.9, rating: '4.8 ★', reviews: '400+', category: 'Hotel', image: '', price: 4500, details: ['Business Room', 'Eco Stay environment'], premium: false },
        { name: 'Hotel Sahara Star', type: 'Transit Hub', distance: 1.1, rating: '4.7 ★', reviews: '300+', category: 'Hotel', image: '', price: 5200, details: ['Mercury Room', 'Transit Hub convenience'], premium: true },
        { name: 'Taj Santacruz', type: 'Luxury', distance: 1.6, rating: '4.9 ★', reviews: '500+', category: 'Hotel', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBwNzfcRJjijBDZgGuN06liNWs1qWY_wilvYW59m7gAyeP-YnTLGypLGymQixUFn5Cl-iK8NMX1dgWIFpJnzahNQQxXNJGudjm4hMIvyw3DPBsySLCSsZrbWDM_09zFL3iJO7BydG5JqCAILjaTw_zRDZFP3qrpcTHnTQw6cN1aNngn8O9_qo_APqOyNQEnYvIbQD00kNj6KSkpuZCUV22YVMhtQ0Il3NMEJAUovV1-m0Z0NjZtsrsEHqDdN6hCunHxeHg9jt5arWQy', price: 8200, details: ['King Suite', 'Butler service included'], premium: true },
        { name: 'JW Marriott Mumbai Sahar', type: 'Luxury', distance: 1.8, rating: '4.8 ★', reviews: '450+', category: 'Hotel', image: '', price: 7800, details: ['Studio Room', 'Resort features'], premium: true },
        { name: 'ITC Maratha', type: 'Luxury', distance: 2.4, rating: '4.8 ★', reviews: '465+', category: 'Hotel', image: '', price: 7500, details: ['Heritage luxury rooms', 'Signature dining'], premium: true },
        { name: 'Aurika Mumbai Airport', type: 'Luxury', distance: 2.8, rating: '4.6 ★', reviews: '318+', category: 'Hotel', image: '', price: 4500, details: ['Modern rooms', 'Fast check-in'], premium: true },
        { name: 'Lemon Tree Premier', type: 'Standard', distance: 3.2, rating: '4.4 ★', reviews: '331+', category: 'Hotel', image: '', price: 3200, details: ['Reliable business rooms'], premium: false },
        { name: 'Holiday Inn Mumbai Airport', type: 'Standard', distance: 4.2, rating: '4.5 ★', reviews: '367+', category: 'Hotel', image: '', price: 4500, details: ['Comfortable day-use rooms'], premium: false }
    ],
    'Restaurants': [
        { name: 'Thai Naam', type: 'Premium Thai', distance: 1.8, rating: '4.8 ★', reviews: '200+', category: 'Restaurant', image: '', price: 3800, details: ['Chef Tasting', 'Set Lunch'], premium: true },
        { name: 'JW Cafe', type: 'Global Buffet', distance: 1.8, rating: '4.7 ★', reviews: '300+', category: 'Restaurant', image: '', price: 1800, details: ['Sunday Brunch'], premium: true },
        { name: 'Cafe Coffee Day', type: 'Quick Bites', distance: 0.4, rating: '4.2 ★', reviews: '1k+', category: 'Restaurant', image: '', price: 550, details: ['Combo Deal'], premium: false },
        { name: 'Sake & Stone', type: 'Japanese', distance: 1.8, rating: '4.9 ★', reviews: '150+', category: 'Restaurant', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCEHVvr-KaB3u9h4V-312uBZ5YCpyIPs7kZEuC15dMwLgEFEdf-Go7ztOhHMKjxdVRtEFFehrI-V1C078nB0nQJajGjAjmVUwj4MIV63prrEH0xqpHwo1tfqmdvNjVl1EIpu7KJTT6QwIKAIMh9Ic1AF_clXq1ZzSqhjrQgJ4exxuwih9Hk3FW6x-99ZZJIKQayUPI9bKBp7sinvN0a9K63ak3SX0xQKRugYBmQFD0oMMtTayp4jRp0xdS1YlKUrFOB-aWZKObVv2Sz', price: 4500, details: ['Sashimi Platter'], premium: true }
    ],
    'Spa': [
        { name: 'Jiva Spa', type: 'Ayurvedic', distance: 1.6, rating: '4.9 ★', reviews: '100+', category: 'Spa', image: '', price: 3500, details: ['Ayurvedic massage'], premium: true },
        { name: 'Aura Wellness', type: 'Holistic', distance: 1.6, rating: '4.7 ★', reviews: '250+', category: 'Spa', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCCnlikk1QQwO6H7p5wmjMMSTz3-coe_ACFYTs9AmXRKI-nJwpTolWRuFhAe7t4GMI-483U8N39X5yzgNhajjHVvzKatotYftMWFMLAObmgqxr9aX65t-9aunRgOJvJGCv_4jvAPtInQjt_oMCnBkU-Ls9aTJE2aPf1n03vV7lSh3CdaAq_53sISit2fSaiOSGNOLIWb3uBb1a45HXz40We1lfxL3r2H7tlpJIOdyOM7CLuZzN5Pn2qcXPm9t05bkMfXCaYGh8S4xp1', price: 2800, details: ['Deep Tissue'], premium: true }
    ],
    'Entertainment': [
        { name: 'KidZania', type: 'Kids Play Zone', distance: 7.9, rating: '4.8 ★', reviews: '1.2k', category: 'Gaming & Entertainment', image: '', price: 2500, details: ['Role-play'], premium: true },
        { name: 'Zero Latency', type: 'VR Arena', distance: 16.5, rating: '4.9 ★', reviews: '850+', category: 'Gaming & Entertainment', image: '', price: 3500, details: ['Free-Roam VR'], premium: true }
    ]
};

// --- CORE FUNCTIONS ---

window.calculateDynamicTravelMins = function(distance) {
    const transportType = localStorage.getItem("transportType") || "Luxury";
    const speedMap = { walking: 5, cab: 28, metro: 40, bike: 18, Sedan: 40, SUV: 38, XL: 35, Luxury: 45, Shuttle: 30 };
    const speed = speedMap[transportType] || 28;
    let trafficMultiplier = 1.3;
    const flightDepartureRaw = localStorage.getItem('flight_departure');
    if (flightDepartureRaw) {
        try {
            const date = new Date(flightDepartureRaw);
            const hour = date.getHours();
            if ((hour >= 7 && hour < 10) || (hour >= 17 && hour < 21)) trafficMultiplier = 1.7;
        } catch(e) {}
    }
    return (distance / speed) * 60 * trafficMultiplier;
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
            let m = 0;
            if (item.duration.includes('h')) m = parseFloat(item.duration) * 60;
            else if (item.duration.includes('m')) m = parseFloat(item.duration);
            expMins += m;
            if (item.distance > maxDist) maxDist = item.distance;
        });
        worstTravelMins = Math.round(window.calculateDynamicTravelMins(maxDist) * 2 + 30);
    }

    let remainingMins = totalMins - bufferMins - worstTravelMins - expMins;
    const format = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

    document.getElementById('time-total').textContent = layoverDurationHours + 'h';
    document.getElementById('time-travel').textContent = format(worstTravelMins);
    document.getElementById('time-exp').textContent = format(expMins);
    
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
    if (remainingMins < 0) {
        window.isRisk = true;
        remEl.textContent = 'Risk';
        remContainer.className = 'bg-red-50 py-3 px-3 rounded-2xl border border-red-200 flex flex-col justify-center min-w-[80px]';
    } else {
        window.isRisk = false;
        remEl.textContent = format(remainingMins);
        remContainer.className = remainingMins < 60 ? 'bg-amber-50 py-3 px-3 rounded-2xl border border-amber-200 flex flex-col justify-center min-w-[80px]' : 'bg-emerald-50 py-3 px-3 rounded-2xl border border-emerald-100/50 flex flex-col justify-center min-w-[80px]';
    }
};

window.renderCategory = function(catId, btn) {
    window.activeCategory = catId;
    const config = CATEGORY_CONFIG[catId];
    if (!config) return;
    
    const container = document.getElementById('marketplace-content');
    
    // Update pill styles
    document.querySelectorAll('.category-pill').forEach(pill => {
        pill.classList.remove('bg-primary', 'text-on-primary', 'shadow-sm');
        pill.classList.add('bg-white', 'border', 'text-on-surface');
    });
    if (btn) {
        btn.classList.remove('bg-white', 'border', 'text-on-surface');
        btn.classList.add('bg-primary', 'text-on-primary', 'shadow-sm');
    } else {
        document.querySelectorAll('.category-pill').forEach(pill => {
            if (pill.getAttribute('onclick').includes(`'${catId}'`)) {
                pill.classList.remove('bg-white', 'border', 'text-on-surface');
                pill.classList.add('bg-primary', 'text-on-primary', 'shadow-sm');
            }
        });
    }

    if (catId === 'recommended') {
        const picks = [window.LAYOVER_INVENTORY['Hotels'][2], window.LAYOVER_INVENTORY['Restaurants'][3], window.LAYOVER_INVENTORY['Spa'][1]];
        container.innerHTML = `<div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm"><h3 class="text-xl font-bold text-primary mb-4 tracking-tight">Recommended For You</h3><div class="space-y-4">${picks.map(i => window.createItemCard(i)).join('')}</div></div>`;
        return;
    }

    const items = window.LAYOVER_INVENTORY[config.key] || [];
    const premium = items.filter(i => i.premium);
    const standard = items.filter(i => !i.premium);

    container.innerHTML = `
        <div class="main-layout flex flex-col lg:flex-row items-start gap-8">
            <div id="level1" class="w-full lg:w-1/2 space-y-6">
                <div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm">
                    <div class="flex justify-between items-center mb-6 border-b pb-4">
                        <h3 class="text-2xl font-black text-primary uppercase tracking-tight">${config.title}</h3>
                        <span class="text-[10px] font-bold text-outline uppercase tracking-widest">${items.length} FOUND</span>
                    </div>
                    <div class="space-y-6">
                        ${premium.length ? `<div><p class="text-[10px] font-bold text-brand-accent uppercase mb-3 tracking-widest flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">workspace_premium</span> Premium Options</p><div class="space-y-4">${premium.map(i => window.createItemCard(i)).join('')}</div></div>` : ''}
                        ${standard.length ? `<div><p class="text-[10px] font-bold text-outline uppercase mb-3 tracking-widest flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">list</span> Standard Options</p><div class="space-y-4">${standard.map(i => window.createItemCard(i)).join('')}</div></div>` : ''}
                    </div>
                </div>
            </div>
            <div id="level2" class="w-full lg:w-1/2 hidden opacity-0 transition-all duration-300">
                <div class="bg-white border border-outline-variant rounded-2xl shadow-xl overflow-hidden sticky top-24" id="level2-content"></div>
            </div>
        </div>
    `;
};

window.createItemCard = function(item) {
    const travel = Math.round(window.calculateDynamicTravelMins(item.distance));
    let catConfig = CATEGORY_CONFIG[item.category === 'Hotel' ? 'hotel.html' : item.category === 'Restaurant' ? 'restaurant.html' : 'spa.html'] || CATEGORY_CONFIG['hotel.html'];
    return `
        <div class="flex gap-4 bg-surface border border-outline-variant rounded-xl p-3 hover:border-primary/30 transition-all cursor-pointer group" onclick="window.showDetail('${item.name}')">
            <div class="w-20 h-20 rounded-lg overflow-hidden bg-slate-200 shrink-0">
                ${item.image ? `<img src="${item.image}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center text-outline-variant"><span class="material-symbols-outlined">${catConfig.icon}</span></div>`}
            </div>
            <div class="flex-1 flex flex-col justify-between py-0.5 min-w-0">
                <div>
                    <div class="flex justify-between items-start">
                        <h4 class="font-bold text-sm text-primary truncate pr-2">${item.name}</h4>
                        <span class="text-[10px] font-bold text-emerald-700 shrink-0">${item.rating}</span>
                    </div>
                    <p class="text-[10px] text-secondary mt-1">${item.type} • ${travel}m away</p>
                </div>
                <div class="flex justify-between items-center mt-2">
                    <span class="text-[9px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-100 uppercase tracking-widest">Compatible</span>
                    <span class="text-[10px] font-bold text-primary group-hover:underline">Details</span>
                </div>
            </div>
        </div>
    `;
};

window.showDetail = function(name) {
    let item;
    Object.values(window.LAYOVER_INVENTORY).forEach(cat => { const found = cat.find(i => i.name === name); if (found) item = found; });
    const l2 = document.getElementById('level2');
    const content = document.getElementById('level2-content');
    const config = CATEGORY_CONFIG[item.category === 'Hotel' ? 'hotel.html' : item.category === 'Restaurant' ? 'restaurant.html' : item.category === 'Spa' ? 'spa.html' : 'entertainment.html'] || CATEGORY_CONFIG['hotel.html'];
    const durs = config.durations || ['1h', '2h'];
    const isAdded = window.layoverList.find(i => i.name === item.name);

    content.innerHTML = `
        <div class="p-6 space-y-6 max-h-[80vh] overflow-y-auto no-scrollbar">
            <div class="flex justify-between items-start">
                <div>
                    <h2 class="text-2xl font-black text-primary tracking-tight">${item.name}</h2>
                    <p class="text-sm text-secondary font-medium">${item.rating} • ${item.distance} km from T2</p>
                </div>
                <button onclick="window.hideDetail()" class="p-2 rounded-full hover:bg-slate-100"><span class="material-symbols-outlined">close</span></button>
            </div>
            <div class="h-40 rounded-xl overflow-hidden bg-slate-100">
                ${item.image ? `<img src="${item.image}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center text-outline-variant"><span class="material-symbols-outlined text-[48px]">${config.icon}</span></div>`}
            </div>
            <div class="bg-primary/5 border border-primary/20 p-5 rounded-xl space-y-4">
                <label class="block text-[10px] font-bold text-primary uppercase tracking-widest">Select Stay Duration</label>
                <select id="det-dur" class="w-full bg-white border border-outline-variant p-3 rounded-lg text-sm font-bold outline-none" onchange="document.getElementById('det-add').disabled = !this.value">
                    <option value="" disabled selected hidden>Choose duration...</option>
                    ${durs.map(d => `<option value="${d}">${d.replace('h', ' Hours').replace('m', ' Mins')}</option>`).join('')}
                </select>
                <button id="det-add" ${isAdded ? 'disabled' : 'disabled'} onclick="window.addToList(this, '${item.name}', '${item.category}', document.getElementById('det-dur').value, ${item.distance}, '${item.image}')" class="w-full bg-primary text-white font-bold py-4 rounded-xl text-sm uppercase tracking-widest shadow-lg active:scale-95 transition-all disabled:opacity-50">
                    ${isAdded ? '✓ Added' : 'Add to List'}
                </button>
            </div>
        </div>
    `;
    l2.classList.remove('hidden');
    setTimeout(() => { l2.classList.remove('opacity-0'); l2.classList.add('opacity-100'); }, 10);
};

window.hideDetail = function() {
    const l2 = document.getElementById('level2');
    if (l2) {
        l2.classList.add('opacity-0');
        setTimeout(() => l2.classList.add('hidden'), 300);
    }
};

window.addToList = function(btn, itemName, category, duration, distance, image) {
    if (!duration) return;
    const existing = window.layoverList.find(i => i.name === itemName);
    if (!existing) {
        window.layoverList.push({ name: itemName, category, duration, distance: parseFloat(distance) || 0, image: image || '' });
        localStorage.setItem('layoverList', JSON.stringify(window.layoverList));
    }
    btn.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span> Added';
    btn.classList.remove('bg-primary');
    btn.classList.add('bg-emerald-50', 'text-emerald-700', 'border', 'border-emerald-200', 'cursor-default');
    btn.disabled = true;
    window.updateListIndicator();
    window.updateTimeCalculations();
};

window.updateListIndicator = function() {
    const tripPlanActivated = localStorage.getItem('tripPlanActivated') === 'true';
    const tripsTab = document.getElementById('nav-trips-tab');
    if (tripsTab) {
        if (tripPlanActivated) {
            tripsTab.style.opacity = '1';
            tripsTab.style.pointerEvents = 'auto';
            tripsTab.style.cursor = 'pointer';
            tripsTab.onclick = () => window.location.href = 'yourplan.html';
        } else {
            tripsTab.style.opacity = '0.4';
            tripsTab.style.pointerEvents = 'none';
            tripsTab.style.cursor = 'not-allowed';
        }
    }

    let indicator = document.getElementById('global-list-indicator');
    if (!indicator) {
        const div = document.createElement('div');
        div.id = 'global-list-indicator';
        div.className = 'fixed bottom-[75px] left-1/2 -translate-x-1/2 z-[100] transition-all duration-300';
        document.body.appendChild(div);
    }
    const ind = document.getElementById('global-list-indicator');
    if (window.layoverList.length > 0) {
        ind.style.display = 'flex';
        ind.innerHTML = `
            <div class="flex items-center gap-2 bg-white border border-outline-variant p-1.5 rounded-full shadow-lg">
                <button onclick=\"window.toggleListDrawer()\" class="bg-surface-container-low px-4 py-2 rounded-full font-bold text-xs">Items: ${window.layoverList.length}</button>
                <button onclick=\"window.proceedToPlan(this)\" class=\"bg-primary text-white px-5 py-2 rounded-full font-bold text-xs flex items-center gap-1 shadow-sm active:scale-95 transition-all\">Plan My List <span class=\"material-symbols-outlined text-sm\">arrow_forward</span></button>
            </div>`;
    } else {
        ind.style.display = 'none';
    }
};

window.toggleListDrawer = function() {
    alert("Selected Items:\n" + window.layoverList.map(i => "- " + i.name + " (" + i.duration + ")").join("\n"));
};

window.proceedToPlan = function(btn) {
    if (window.isRisk) {
        alert("Your itinerary exceeds the available layover time. Reduce stay durations or remove experiences before proceeding.");
        return;
    }
    localStorage.setItem("tripPlanActivated", "true");
    window.location.href = 'yourplan.html';
};

document.addEventListener('DOMContentLoaded', () => {
    // Restore list from storage
    try {
        const stored = localStorage.getItem('layoverList');
        window.layoverList = stored ? JSON.parse(stored) : [];
    } catch(e) { window.layoverList = []; }

    window.renderCategory('recommended');
    window.updateTimeCalculations();
    window.updateListIndicator();
});
</script>'''

with open('marketplace.html', 'w', encoding='utf-8') as f:
    f.write(content)
