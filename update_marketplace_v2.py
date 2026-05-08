import re

with open('marketplace.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Navbar items and add IDs
nav_old = r'''<nav class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-xs py-sm bg-surface dark:bg-surface-dim border-t border-outline-variant dark:border-outline">
<button onclick="window.location.reload()" class="flex flex-col items-center justify-center text-primary dark:text-inverse-primary font-semibold hover:text-primary dark:hover:text-inverse-primary transition-colors active:scale-95 transition-transform duration-150">
<span class="material-symbols-outlined" data-icon="explore" style="font-variation-settings: 'FILL' 1;">explore</span>
<span class="font-label-sm text-label-sm">Explore</span>
</button>
<button class="flex flex-col items-center justify-center text-secondary dark:text-secondary-fixed-dim hover:text-primary dark:hover:text-inverse-primary transition-colors active:scale-95 transition-transform duration-150">
<span class="material-symbols-outlined" data-icon="airplane_ticket">airplane_ticket</span>
<span class="font-label-sm text-label-sm">Trips</span>
</button>
<button class="flex flex-col items-center justify-center text-secondary dark:text-secondary-fixed-dim hover:text-primary dark:hover:text-inverse-primary transition-colors active:scale-95 transition-transform duration-150">
<span class="material-symbols-outlined" data-icon="person">person</span>
<span class="font-label-sm text-label-sm">Profile</span>
</button>
</nav>'''

nav_new = r'''<nav class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-xs py-sm bg-surface dark:bg-surface-dim border-t border-outline-variant dark:border-outline shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
<button id="nav-explore-tab" onclick="window.location.reload()" class="flex flex-col items-center justify-center text-primary dark:text-inverse-primary font-bold hover:text-primary transition-all active:scale-95 duration-150">
<span class="material-symbols-outlined text-[24px]" style="font-variation-settings: 'FILL' 1;">explore</span>
<span class="text-[10px] uppercase tracking-widest mt-1">Explore</span>
</button>
<button id="nav-trips-tab" class="flex flex-col items-center justify-center text-secondary hover:text-primary transition-all active:scale-95 duration-150">
<span class="material-symbols-outlined text-[24px]">airplane_ticket</span>
<span class="text-[10px] uppercase tracking-widest mt-1">Trips</span>
</button>
<button id="nav-profile-tab" class="flex flex-col items-center justify-center text-secondary hover:text-primary transition-all active:scale-95 duration-150">
<span class="material-symbols-outlined text-[24px]">person</span>
<span class="text-[10px] uppercase tracking-widest mt-1">Profile</span>
</button>
</nav>'''

# Standardizing navigation items and IDs
content = re.sub(r'<nav.*?</nav>', nav_new, content, flags=re.DOTALL)

# Refined script with better logic and synchronization
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

// --- DATA INITIALIZATION (Source of Truth) ---
window.LAYOVER_INVENTORY = {
    'Hotels': [
        { name: 'The Orchid Hotel', type: 'Eco Stay', distance: 0.9, rating: '4.8', reviews: '400+', category: 'Hotel', image: '', price: 4500, details: ['Business Room', 'Eco Stay environment', 'Focused on efficiency'], premium: false },
        { name: 'Hotel Sahara Star', type: 'Transit Hub', distance: 1.1, rating: '4.7', reviews: '300+', category: 'Hotel', image: '', price: 5200, details: ['Mercury Room - Modern styling', 'Earth Room - Garden view', 'Transit Hub convenience'], premium: true },
        { name: 'Taj Santacruz', type: 'Luxury', distance: 1.6, rating: '4.9', reviews: '500+', category: 'Hotel', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBwNzfcRJjijBDZgGuN06liNWs1qWY_wilvYW59m7gAyeP-YnTLGypLGymQixUFn5Cl-iK8NMX1dgWIFpJnzahNQQxXNJGudjm4hMIvyw3DPBsySLCSsZrbWDM_09zFL3iJO7BydG5JqCAILjaTw_zRDZFP3qrpcTHnTQw6cN1aNngn8O9_qo_APqOyNQEnYvIbQD00kNj6KSkpuZCUV22YVMhtQ0Il3NMEJAUovV1-m0Z0NjZtsrsEHqDdN6hCunHxeHg9jt5arWQy', price: 8200, details: ['King Suite with Pool view', 'Butler service included', 'Grand Club Lounge access'], premium: true },
        { name: 'JW Marriott Mumbai Sahar', type: 'Luxury', distance: 1.8, rating: '4.8', reviews: '450+', category: 'Hotel', image: '', price: 7800, details: ['Studio Room with workspace', 'Executive Premium city view', 'Resort Stay features'], premium: true },
        { name: 'ITC Maratha', type: 'Luxury', distance: 2.4, rating: '4.8', reviews: '465+', category: 'Hotel', image: '', price: 7500, details: ['Heritage luxury rooms', 'Signature dining', 'Transit-friendly check-in'], premium: true },
        { name: 'Aurika Mumbai Airport', type: 'Luxury', distance: 2.8, rating: '4.6', reviews: '318+', category: 'Hotel', image: '', price: 4500, details: ['Modern rooms', 'Fast check-in', 'Layover dining packages'], premium: true },
        { name: 'Lemon Tree Premier', type: 'Standard', distance: 3.2, rating: '4.4', reviews: '331+', category: 'Hotel', image: '', price: 3200, details: ['Reliable business rooms', 'Breakfast options', 'Near airport road'], premium: false },
        { name: 'Holiday Inn Mumbai Airport', type: 'Standard', distance: 4.2, rating: '4.5', reviews: '367+', category: 'Hotel', image: '', price: 4500, details: ['Rooftop pool', 'Airport shuttle support', 'Comfortable day-use rooms'], premium: false }
    ],
    'Restaurants': [
        { name: 'Thai Naam', type: 'Premium Thai', distance: 1.8, rating: '4.8', reviews: '200+', category: 'Restaurant', image: '', price: 3800, details: ['Chef Tasting', 'Set Lunch'], premium: true },
        { name: 'JW Cafe', type: 'Global Buffet', distance: 1.8, rating: '4.7', reviews: '300+', category: 'Restaurant', image: '', price: 1800, details: ['Sunday Brunch'], premium: true },
        { name: 'Cafe Coffee Day', type: 'Quick Bites', distance: 0.4, rating: '4.2', reviews: '1k+', category: 'Restaurant', image: '', price: 550, details: ['Combo Deal'], premium: false },
        { name: 'Sake & Stone', type: 'Japanese', distance: 1.8, rating: '4.9', reviews: '150+', category: 'Restaurant', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCEHVvr-KaB3u9h4V-312uBZ5YCpyIPs7kZEuC15dMwLgEFEdf-Go7ztOhHMKjxdVRtEFFehrI-V1C078nB0nQJajGjAjmVUwj4MIV63prrEH0xqpHwo1tfqmdvNjVl1EIpu7KJTT6QwIKAIMh9Ic1AF_clXq1ZzSqhjrQgJ4exxuwih9Hk3FW6x-99ZZJIKQayUPI9bKBp7sinvN0a9K63ak3SX0xQKRugYBmQFD0oMMtTayp4jRp0xdS1YlKUrFOB-aWZKObVv2Sz', price: 4500, details: ['Sashimi Platter'], premium: true }
    ],
    'Spa': [
        { name: 'Jiva Spa', type: 'Ayurvedic', distance: 1.6, rating: '4.9', reviews: '100+', category: 'Spa', image: '', price: 3500, details: ['Vishudhi', 'Sushupti'], premium: true },
        { name: 'Aura Wellness', type: 'Holistic', distance: 1.6, rating: '4.7', reviews: '250+', category: 'Spa', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCCnlikk1QQwO6H7p5wmjMMSTz3-coe_ACFYTs9AmXRKI-nJwpTolWRuFhAe7t4GMI-483U8N39X5yzgNhajjHVvzKatotYftMWFMLAObmgqxr9aX65t-9aunRgOJvJGCv_4jvAPtInQjt_oMCnBkU-Ls9aTJE2aPf1n03vV7lSh3CdaAq_53sISit2fSaiOSGNOLIWb3uBb1a45HXz40We1lfxL3r2H7tlpJIOdyOM7CLuZzN5Pn2qcXPm9t05bkMfXCaYGh8S4xp1', price: 2800, details: ['Deep Tissue Massage'], premium: true }
    ],
    'Entertainment': [
        { name: 'KidZania', type: 'Kids Play Zone', distance: 7.9, rating: '4.8', reviews: '1.2k', category: 'Gaming & Entertainment', image: '', price: 2500, details: ['Role-play activities', 'Interactive City'], premium: true },
        { name: 'Zero Latency', type: 'VR Arena', distance: 16.5, rating: '4.9', reviews: '850+', category: 'Gaming & Entertainment', image: '', price: 3500, details: ['Free-Roam VR', 'Zombie Survival'], premium: true },
        { name: 'Timezone', type: 'Arcade', distance: 8.5, rating: '4.3', reviews: '1.8k', category: 'Gaming & Entertainment', image: '', price: 1800, details: ['Arcade Games', 'Bowling'], premium: false }
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

window.addToList = function(btn, itemName, category, duration, distance, image) {
    if (!duration) return;
    const existing = window.layoverList.find(i => i.name === itemName);
    if (!existing) {
        window.layoverList.push({ name: itemName, category, duration, distance: parseFloat(distance) || 0, image: image || '' });
        localStorage.setItem('layoverList', JSON.stringify(window.layoverList));
    }
    btn.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span> Added';
    btn.className = "w-full bg-emerald-50 text-emerald-700 border border-emerald-200 py-4 rounded-xl text-sm font-bold flex items-center justify-center gap-2 cursor-default";
    btn.disabled = true;
    window.updateListIndicator();
    window.updateTimeCalculations();
};

window.removeFromList = function(itemName) {
    window.layoverList = window.layoverList.filter(i => i.name !== itemName);
    localStorage.setItem('layoverList', JSON.stringify(window.layoverList));
    window.renderCategory(window.activeCategory);
    window.updateListIndicator();
    window.updateTimeCalculations();
};

window.updateTimeCalculations = function() {
    const layoverHours = parseInt(localStorage.getItem('layover_duration') || '8', 10);
    let totalMins = layoverHours * 60;
    let bufferMins = 120;
    let expMins = 0;
    let travelMins = 0;
    let maxDist = 0;

    window.layoverList.forEach(item => {
        let m = 0;
        if (item.duration.includes('h')) m = parseFloat(item.duration) * 60;
        else if (item.duration.includes('m')) m = parseFloat(item.duration);
        expMins += m;
        if (item.distance > maxDist) maxDist = item.distance;
    });

    if (window.layoverList.length > 0) travelMins = Math.round(window.calculateDynamicTravelMins(maxDist) * 2 + 30);
    let remainingMins = totalMins - bufferMins - travelMins - expMins;

    const format = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';

    document.getElementById('time-total').textContent = layoverHours + 'h';
    document.getElementById('time-travel').textContent = format(travelMins);
    document.getElementById('time-exp').textContent = format(expMins);
    
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

window.renderCategory = function(catId) {
    window.activeCategory = catId;
    const config = CATEGORY_CONFIG[catId];
    const container = document.getElementById('marketplace-content');
    
    document.querySelectorAll('.category-pill').forEach(btn => {
        const isTarget = btn.getAttribute('onclick').includes(`'${catId}'`);
        btn.className = isTarget ? 'category-pill bg-primary text-on-primary px-lg py-xs rounded-full font-label-sm text-label-sm whitespace-nowrap active:scale-95 transition-transform duration-150 shadow-sm' : 'category-pill bg-white border border-outline-variant text-on-surface px-lg py-xs rounded-full font-label-sm text-label-sm whitespace-nowrap hover:bg-surface-container-low active:scale-95 transition-all duration-150';
    });

    if (catId === 'recommended') {
        const picks = [window.LAYOVER_INVENTORY['Hotels'][2], window.LAYOVER_INVENTORY['Restaurants'][3], window.LAYOVER_INVENTORY['Spa'][1]];
        container.innerHTML = `
            <div class="space-y-6">
                <div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm">
                    <div class="flex justify-between items-center mb-6 border-b pb-4">
                        <div>
                            <h3 class="text-xl font-bold text-primary">Recommended For You</h3>
                            <p class="text-xs text-secondary mt-1">Smart matches based on your flight timing</p>
                        </div>
                        <span class="bg-emerald-100 text-emerald-700 text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider shadow-sm">Verified Selection</span>
                    </div>
                    <div class="space-y-4">
                        ${picks.map(i => window.createItemCard(i)).join('')}
                    </div>
                </div>
            </div>
        `;
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
                        <div>
                            <h3 class="text-2xl font-black text-primary uppercase tracking-tight">${config.title}</h3>
                        </div>
                        <span class="text-[10px] font-bold text-outline uppercase tracking-widest">${items.length} FOUND</span>
                    </div>
                    <div class="space-y-6">
                        <div class="bg-surface-container-low p-4 rounded-xl border border-outline-variant flex flex-wrap gap-2 shadow-inner">
                            <select class="flex-1 min-w-[100px] p-2 rounded-lg border border-outline-variant text-[10px] font-bold uppercase"><option>Duration</option></select>
                            <select class="flex-1 min-w-[100px] p-2 rounded-lg border border-outline-variant text-[10px] font-bold uppercase"><option>Price</option></select>
                            <select class="flex-1 min-w-[100px] p-2 rounded-lg border border-outline-variant text-[10px] font-bold uppercase"><option>Distance</option></select>
                        </div>
                        <div class="space-y-8">
                            ${premium.length ? `<div><p class="text-[10px] font-bold text-brand-purple uppercase tracking-widest mb-3 flex items-center gap-2"><span class="material-symbols-outlined text-sm">workspace_premium</span> Premium Selection</p><div class="space-y-4">${premium.map(i => window.createItemCard(i)).join('')}</div></div>` : ''}
                            ${standard.length ? `<div><p class="text-[10px] font-bold text-outline uppercase tracking-widest mb-3">Standard Options</p><div class="space-y-4">${standard.map(i => window.createItemCard(i)).join('')}</div></div>` : ''}
                        </div>
                    </div>
                </div>
            </div>
            <div id="level2" class="w-full lg:w-1/2 hidden opacity-0 transition-all duration-300">
                <div class="bg-white border border-outline-variant rounded-2xl shadow-2xl overflow-hidden sticky top-24" id="level2-content"></div>
            </div>
        </div>
    `;
};

window.createItemCard = function(item) {
    const travel = Math.round(window.calculateDynamicTravelMins(item.distance));
    return `
        <div class="flex gap-4 bg-surface border border-outline-variant rounded-2xl p-4 hover:border-primary/30 hover:shadow-lg transition-all cursor-pointer group" onclick="window.showDetail('${item.name}')">
            <div class="w-28 h-28 rounded-xl overflow-hidden bg-slate-200 shrink-0 shadow-sm relative">
                ${item.image ? `<img src="${item.image}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">` : `<div class="w-full h-full flex items-center justify-center text-outline-variant"><span class="material-symbols-outlined text-[32px]">${CATEGORY_CONFIG[window.activeCategory === 'recommended' ? (item.category === 'Hotel' ? 'hotel.html' : item.category === 'Restaurant' ? 'restaurant.html' : 'spa.html') : window.activeCategory].icon}</span></div>`}
                <div class="absolute top-2 right-2 bg-black/60 backdrop-blur-md px-1.5 py-0.5 rounded border border-white/10">
                    <span class="text-white text-[8px] font-bold">${item.rating} ★</span>
                </div>
            </div>
            <div class="flex-1 flex flex-col justify-between py-1">
                <div>
                    <h4 class="font-bold text-base text-primary tracking-tight group-hover:text-brand-accent transition-colors">${item.name}</h4>
                    <div class="flex flex-wrap gap-2 text-secondary mt-1.5">
                        <span class="bg-surface-container-low px-2 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider border border-outline-variant/30">${item.type}</span>
                        <span class="flex items-center gap-1 text-[9px] font-bold uppercase tracking-wider"><span class="material-symbols-outlined text-[14px]">directions_car</span> ${travel}m travel</span>
                    </div>
                </div>
                <div class="flex justify-between items-center mt-3">
                    <span class="text-[9px] font-black text-emerald-600 uppercase tracking-widest flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">verified</span> Recommended</span>
                    <span class="text-[10px] font-bold text-primary group-hover:underline flex items-center gap-1">Details <span class="material-symbols-outlined text-sm">arrow_forward</span></span>
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
    const isAdded = window.layoverList.find(i => i.name === item.name);
    
    // Auto-resolve config for recommended items
    let config = CATEGORY_CONFIG[window.activeCategory];
    if (window.activeCategory === 'recommended') {
         if (item.category === 'Hotel') config = CATEGORY_CONFIG['hotel.html'];
         else if (item.category === 'Restaurant') config = CATEGORY_CONFIG['restaurant.html'];
         else if (item.category === 'Spa') config = CATEGORY_CONFIG['spa.html'];
    }
    const durs = config.durations || ['1h', '2h'];

    content.innerHTML = `
        <div class="p-8 space-y-8 max-h-[75vh] overflow-y-auto no-scrollbar">
            <div class="flex justify-between items-start">
                <div>
                    <span class="bg-primary/90 text-white px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-widest mb-2 inline-block">${item.type}</span>
                    <h2 class="text-3xl font-black text-primary tracking-tighter leading-tight">${item.name}</h2>
                    <p class="text-sm text-secondary font-medium mt-1 flex items-center gap-2"><span class="material-symbols-outlined text-emerald-600 text-sm">location_on</span> ${item.distance} km from T2 Terminal</p>
                </div>
                <button onclick="window.hideDetail()" class="p-2 rounded-full hover:bg-slate-100 transition-colors"><span class="material-symbols-outlined">close</span></button>
            </div>
            <div class="h-64 rounded-2xl overflow-hidden bg-slate-100 shadow-inner">
                ${item.image ? `<img src="${item.image}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center text-outline-variant"><span class="material-symbols-outlined text-[64px]">${config.icon}</span></div>`}
            </div>
            <div class="bg-surface p-6 rounded-2xl border border-outline-variant shadow-sm space-y-4">
                <p class="text-[10px] font-bold text-primary uppercase tracking-widest flex items-center gap-2 border-b pb-3"><span class="material-symbols-outlined text-sm">info</span> Feature Highlights</p>
                <ul class="text-sm font-medium space-y-3">
                    ${item.details.map(d => `<li class="flex items-start gap-3"><span class="material-symbols-outlined text-emerald-600 text-[18px]">check_circle</span> <span>${d}</span></li>`).join('')}
                </ul>
            </div>
            <div class="bg-primary/5 border-2 border-primary/10 p-6 rounded-2xl space-y-5 shadow-inner">
                <div>
                    <label class="block text-[10px] font-bold text-primary uppercase tracking-widest mb-3 flex items-center gap-2"><span class="material-symbols-outlined text-sm">schedule</span> Choose Stay Duration <span class="text-error">*</span></label>
                    <select id="det-dur" class="w-full bg-white border border-outline-variant p-4 rounded-xl text-sm font-bold outline-none shadow-sm focus:border-primary appearance-none cursor-pointer" onchange="document.getElementById('det-add').disabled = !this.value">
                        <option value="" disabled selected hidden>Select timing to proceed...</option>
                        ${durs.map(d => `<option value="${d}">${d.replace('h', ' Hours').replace('m', ' Mins').replace('1 Hours', '1 Hour')}</option>`).join('')}
                    </select>
                </div>
                <button id="det-add" ${isAdded ? 'disabled' : 'disabled'} onclick="window.addToList(this, '${item.name}', '${item.category}', document.getElementById('det-dur').value, ${item.distance}, '${item.image}')" class="w-full bg-primary hover:bg-black text-white font-black py-5 rounded-2xl text-sm uppercase tracking-widest shadow-xl active:scale-[0.98] transition-all disabled:opacity-30 flex items-center justify-center gap-2">
                    ${isAdded ? '<span class="material-symbols-outlined">check</span> IN LIST' : '<span class="material-symbols-outlined">add_task</span> ADD TO LIST'}
                </button>
            </div>
        </div>
    `;
    l2.classList.remove('hidden');
    setTimeout(() => { l2.classList.remove('opacity-0'); l2.classList.add('opacity-100'); }, 10);
    document.getElementById('app-layout').classList.add('lg:justify-start');
};

window.hideDetail = function() {
    const l2 = document.getElementById('level2');
    l2.classList.add('opacity-0');
    setTimeout(() => {
        l2.classList.add('hidden');
        document.getElementById('app-layout').classList.remove('lg:justify-start');
        document.getElementById('app-layout').classList.add('justify-center');
    }, 300);
};

window.updateListIndicator = function() {
    const tripPlanActivated = localStorage.getItem('tripPlanActivated') === 'true';
    const tripsTab = document.getElementById('nav-trips-tab');
    if (tripsTab && tripPlanActivated) {
         tripsTab.style.opacity = '1';
         tripsTab.style.pointerEvents = 'auto';
         tripsTab.style.cursor = 'pointer';
    }

    let indicator = document.getElementById('global-list-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'global-list-indicator';
        indicator.className = 'fixed bottom-[90px] left-1/2 -translate-x-1/2 z-[100] transition-all duration-300 pointer-events-auto';
        document.body.appendChild(indicator);
    }
    if (window.layoverList.length > 0) {
        indicator.style.display = 'flex';
        indicator.innerHTML = `
            <div class="flex items-center gap-2 bg-white/90 backdrop-blur-md border border-outline-variant p-2 rounded-full shadow-2xl">
                <button onclick="window.toggleListDrawer()" class="bg-surface-container-low hover:bg-surface-container px-5 py-2.5 rounded-full font-black text-[10px] uppercase tracking-wider text-primary border border-outline-variant/30">List (${window.layoverList.length})</button>
                <button onclick="window.proceedToPlan(this)" class="bg-primary hover:bg-black text-white px-6 py-2.5 rounded-full font-black text-[10px] uppercase tracking-wider flex items-center gap-2 shadow-lg active:scale-95 transition-all">Plan My List <span class="material-symbols-outlined text-sm">arrow_forward</span></button>
            </div>`;
    } else {
        indicator.style.display = 'none';
    }
};

window.proceedToPlan = function(btn) {
    if (window.isRisk) {
        alert("Insufficient safe buffer time. Please reduce experiences or travel duration before planning your trip.");
        return;
    }
    localStorage.setItem("tripPlanActivated", "true");
    window.location.href = 'yourplan.html';
};

document.addEventListener('DOMContentLoaded', () => {
    window.renderCategory('recommended');
    window.updateTimeCalculations();
    window.updateListIndicator();
});
</script>'''

# Correctly identifying and replacing the script
content = re.sub(r'<script>.*?</script>', new_script, content, flags=re.DOTALL)

with open('marketplace.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated marketplace.html with refined UI and local rendering logic.")
