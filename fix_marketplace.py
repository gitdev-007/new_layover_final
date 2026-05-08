import re

with open('marketplace.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Navbar items
content = content.replace('<span class="font-label-sm text-label-sm">Saved</span>', '<span class="font-label-sm text-label-sm">Trips</span>')

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
        { name: 'The Orchid Hotel', type: 'Eco Stay', distance: 0.9, rating: '4.8 ★', reviews: '400+ Verified', category: 'Hotel', image: '', price: 4500, details: ['Business Room', 'Eco Stay environment', 'Focused on efficiency'], premium: false },
        { name: 'Hotel Sahara Star', type: 'Transit Hub', distance: 1.1, rating: '4.7 ★', reviews: '300+ Verified', category: 'Hotel', image: '', price: 5200, details: ['Mercury Room - Modern styling', 'Earth Room - Garden view', 'Transit Hub convenience'], premium: true },
        { name: 'Taj Santacruz', type: 'Luxury', distance: 1.6, rating: '4.9 ★', reviews: '500+ Verified', category: 'Hotel', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBwNzfcRJjijBDZgGuN06liNWs1qWY_wilvYW59m7gAyeP-YnTLGypLGymQixUFn5Cl-iK8NMX1dgWIFpJnzahNQQxXNJGudjm4hMIvyw3DPBsySLCSsZrbWDM_09zFL3iJO7BydG5JqCAILjaTw_zRDZFP3qrpcTHnTQw6cN1aNngn8O9_qo_APqOyNQEnYvIbQD00kNj6KSkpuZCUV22YVMhtQ0Il3NMEJAUovV1-m0Z0NjZtsrsEHqDdN6hCunHxeHg9jt5arWQy', details: ['King Suite with Pool view', 'Butler service included', 'Grand Club Lounge access'], premium: true },
        { name: 'Hotel Bawa International', type: 'Standard', distance: 1.7, rating: '4.2 ★', reviews: '200+ Verified', category: 'Hotel', image: '', price: 2200, details: ['Near terminal', 'Fast check-in'], premium: false },
        { name: 'JW Marriott Mumbai Sahar', type: 'Luxury', distance: 1.8, rating: '4.8 ★', reviews: '450+ Verified', category: 'Hotel', image: '', price: 7800, details: ['Studio Room with workspace', 'Executive Premium city view', 'Resort Stay features'], premium: true },
        { name: 'Hotel Midland', type: 'Standard', distance: 2.3, rating: '4.0 ★', reviews: '150+ Verified', category: 'Hotel', image: '', price: 1800, details: ['Convenient location'], premium: false },
        { name: 'ITC Maratha', type: 'Luxury', distance: 2.4, rating: '4.8 ★', reviews: '465+ Verified', category: 'Hotel', image: '', price: 7500, details: ['Heritage luxury rooms', 'Signature dining', 'Transit-friendly check-in'], premium: true },
        { name: 'The Leela Mumbai', type: 'Luxury', distance: 2.5, rating: '4.7 ★', reviews: '452+ Verified', category: 'Hotel', image: '', price: 6500, details: ['Garden-view stays', 'Premium airport shuttle', 'Quiet work-friendly rooms'], premium: true },
        { name: 'Aurika Mumbai Airport', type: 'Luxury', distance: 2.8, rating: '4.6 ★', reviews: '318+ Verified', category: 'Hotel', image: '', price: 4500, details: ['Modern rooms', 'Fast check-in', 'Layover dining packages'], premium: true },
        { name: 'Lemon Tree Premier', type: 'Standard', distance: 3.2, rating: '4.4 ★', reviews: '331+ Verified', category: 'Hotel', image: '', price: 3200, details: ['Reliable business rooms', 'Breakfast options', 'Near airport road'], premium: false },
        { name: 'Holiday Inn Mumbai Airport', type: 'Standard', distance: 4.2, rating: '4.5 ★', reviews: '367+ Verified', category: 'Hotel', image: '', price: 4500, details: ['Rooftop pool', 'Airport shuttle support', 'Comfortable day-use rooms'], premium: false },
        { name: 'Grand Hyatt Mumbai', type: 'Luxury', distance: 6.1, rating: '4.7 ★', reviews: '489+ Verified', category: 'Hotel', image: '', price: 8000, details: ['Large rooms', 'Multiple restaurants', 'Business center access'], premium: true }
    ],
    'Restaurants': [
        { name: 'Thai Naam', type: 'Premium Thai', distance: 1.8, rating: '4.8 ★', reviews: '200+ Verified', category: 'Restaurant', image: '', price: 3800, details: ['Chef Tasting', 'Set Lunch'], premium: true },
        { name: 'JW Cafe', type: 'Global Buffet', distance: 1.8, rating: '4.7 ★', reviews: '300+ Verified', category: 'Restaurant', image: '', price: 1800, details: ['Sunday Brunch'], premium: true },
        { name: 'Cafe Coffee Day', type: 'Quick Bites', distance: 0.4, rating: '4.2 ★', reviews: '1k+ Verified', category: 'Restaurant', image: '', price: 550, details: ['Combo Deal'], premium: false },
        { name: 'Sake & Stone', type: 'Japanese', distance: 1.8, rating: '4.9 ★', reviews: '150+ Verified', category: 'Restaurant', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCEHVvr-KaB3u9h4V-312uBZ5YCpyIPs7kZEuC15dMwLgEFEdf-Go7ztOhHMKjxdVRtEFFehrI-V1C078nB0nQJajGjAjmVUwj4MIV63prrEH0xqpHwo1tfqmdvNjVl1EIpu7KJTT6QwIKAIMh9Ic1AF_clXq1ZzSqhjrQgJ4exxuwih9Hk3FW6x-99ZZJIKQayUPI9bKBp7sinvN0a9K63ak3SX0xQKRugYBmQFD0oMMtTayp4jRp0xdS1YlKUrFOB-aWZKObVv2Sz', details: ['Sashimi Platter'], premium: true }
    ],
    'Spa': [
        { name: 'Jiva Spa', type: 'Ayurvedic', distance: 1.6, rating: '4.9 ★', reviews: '100+ Verified', category: 'Spa', image: '', price: 3500, details: ['Vishudhi', 'Sushupti'], premium: true },
        { name: 'Aura Wellness', type: 'Holistic', distance: 1.6, rating: '4.7 ★', reviews: '250+ Verified', category: 'Spa', image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCCnlikk1QQwO6H7p5wmjMMSTz3-coe_ACFYTs9AmXRKI-nJwpTolWRuFhAe7t4GMI-483U8N39X5yzgNhajjHVvzKatotYftMWFMLAObmgqxr9aX65t-9aunRgOJvJGCv_4jvAPtInQjt_oMCnBkU-Ls9aTJE2aPf1n03vV7lSh3CdaAq_53sISit2fSaiOSGNOLIWb3uBb1a45HXz40We1lfxL3r2H7tlpJIOdyOM7CLuZzN5Pn2qcXPm9t05bkMfXCaYGh8S4xp1', details: ['Deep Tissue Massage'], premium: true }
    ],
    'Entertainment': [
        { name: 'KidZania', type: 'Kids Play Zone', distance: 7.9, rating: '4.8 ★', reviews: '1.2k Verified', category: 'Gaming & Entertainment', image: '', price: 2500, details: ['Role-play activities', 'Interactive City', 'Career Simulation'], premium: true },
        { name: 'Shott Gaming', type: 'Arcade', distance: 8.6, rating: '4.6 ★', reviews: '400+ Verified', category: 'Gaming & Entertainment', image: '', price: 1400, details: ['Bowling Alley', 'VR Simulators', 'Laser Tag'], premium: true },
        { name: 'Zero Latency', type: 'VR Arena', distance: 16.5, rating: '4.9 ★', reviews: '850+ Verified', category: 'Gaming & Entertainment', image: '', price: 3500, details: ['Free-Roam VR', 'Zombie Survival', 'Space Mission'], premium: true },
        { name: 'SMAAASH', type: 'Arcade', distance: 16.8, rating: '4.5 ★', reviews: '2.5k Verified', category: 'Gaming & Entertainment', image: '', price: 2000, details: ['Virtual Cricket', 'Go-Karting', 'Arcade'], premium: true },
        { name: 'JUMPP', type: 'Kids Play Zone', distance: 3.9, rating: '4.2 ★', reviews: '150+ Verified', category: 'Gaming & Entertainment', image: '', price: 1600, details: ['Trampoline Park', 'Kids Play Area', 'Ninja Course'], premium: false },
        { name: 'Clue Hunt', type: 'Escape Room', distance: 8.3, rating: '4.7 ★', reviews: '600+ Verified', category: 'Gaming & Entertainment', image: '', price: 3200, details: ['Mystery Solving', 'Team Puzzles', 'Thematic Rooms'], premium: false },
        { name: 'Timezone', type: 'Arcade', distance: 8.5, rating: '4.3 ★', reviews: '1.8k Verified', category: 'Gaming & Entertainment', image: '', price: 1800, details: ['Arcade Games', 'Bowling', 'Bumper Cars'], premium: false },
        { name: 'Snow Kingdom', type: 'Kids Play Zone', distance: 17.8, rating: '4.4 ★', reviews: '900+ Verified', category: 'Gaming & Entertainment', image: '', price: 2800, details: ['Snow Slides', 'Ice Skating', 'Snow Fight Arena'], premium: false }
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
    btn.classList.remove('bg-primary', 'bg-brand-accent');
    btn.classList.add('bg-emerald-50', 'text-emerald-700', 'border', 'border-emerald-200', 'cursor-default');
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
    
    // Update pill styles
    document.querySelectorAll('.category-pill').forEach(btn => {
        const isTarget = btn.getAttribute('onclick').includes(`'${catId}'`);
        btn.className = isTarget ? 'category-pill bg-primary text-on-primary px-lg py-xs rounded-full font-label-sm text-label-sm whitespace-nowrap active:scale-95 transition-transform duration-150 shadow-sm' : 'category-pill bg-white border border-outline-variant text-on-surface px-lg py-xs rounded-full font-label-sm text-label-sm whitespace-nowrap hover:bg-surface-container-low active:scale-95 transition-all duration-150';
    });

    if (catId === 'recommended') {
        container.innerHTML = `<div class=\"bg-white border border-outline-variant p-6 rounded-2xl shadow-sm\"><h3 class=\"text-xl font-bold text-primary mb-4\">Recommended For You</h3><div class=\"space-y-4\" id=\"rec-list\"></div></div>`;
        const picks = [window.LAYOVER_INVENTORY['Hotels'][2], window.LAYOVER_INVENTORY['Restaurants'][3], window.LAYOVER_INVENTORY['Spa'][1]];
        document.getElementById('rec-list').innerHTML = picks.map(i => window.createItemCard(i)).join('');
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
                    <div class="space-y-8">
                        <div class="grid grid-cols-2 gap-2">
                            <select class="bg-surface border border-outline-variant rounded p-2 text-xs font-bold uppercase"><option>Duration</option></select>
                            <select class="bg-surface border border-outline-variant rounded p-2 text-xs font-bold uppercase"><option>Price</option></select>
                        </div>
                        <div class="space-y-6">
                            ${premium.length ? `<div><p class="text-[10px] font-bold text-brand-accent uppercase tracking-widest mb-3">Premium Options</p><div class="space-y-4">${premium.map(i => window.createItemCard(i)).join('')}</div></div>` : ''}
                            ${standard.length ? `<div><p class="text-[10px] font-bold text-outline uppercase tracking-widest mb-3">Standard Options</p><div class="space-y-4">${standard.map(i => window.createItemCard(i)).join('')}</div></div>` : ''}
                        </div>
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
    return `
        <div class="flex gap-4 bg-surface border border-outline-variant rounded-xl p-3 hover:border-primary/30 transition-all cursor-pointer group" onclick="window.showDetail('${item.name}')">
            <div class="w-24 h-24 rounded-lg overflow-hidden bg-slate-200 shrink-0">
                ${item.image ? `<img src="${item.image}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-outline-variant text-2xl">${CATEGORY_CONFIG[window.activeCategory === 'recommended' ? (item.category.toLowerCase().includes('hotel') ? 'hotel.html' : item.category.toLowerCase().includes('restaurant') ? 'restaurant.html' : 'spa.html') : window.activeCategory].icon}</span></div>`}
            </div>
            <div class="flex-1 flex flex-col justify-between py-0.5">
                <div>
                    <div class="flex justify-between items-start">
                        <h4 class="font-bold text-sm text-primary">${item.name}</h4>
                        <span class="text-[10px] font-bold text-emerald-700">${item.rating}</span>
                    </div>
                    <p class="text-[10px] text-secondary mt-1">${item.type} • ${travel}m travel</p>
                </div>
                <div class="flex justify-between items-center mt-2">
                    <span class="text-[9px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-100">COMPATIBLE</span>
                    <span class="text-[10px] font-bold text-primary group-hover:underline">Details →</span>
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
    const config = CATEGORY_CONFIG[window.activeCategory] || CATEGORY_CONFIG['hotel.html'];
    const durs = config.durations || ['1h', '2h'];
    const isAdded = window.layoverList.find(i => i.name === item.name);

    content.innerHTML = `
        <div class="p-6 space-y-6">
            <div class="flex justify-between items-start">
                <div>
                    <h2 class="text-2xl font-black text-primary tracking-tight">${item.name}</h2>
                    <p class="text-sm text-secondary font-medium">${item.rating} • ${item.distance} km from T2</p>
                </div>
                <button onclick="window.hideDetail()" class="p-2 rounded-full hover:bg-slate-100"><span class="material-symbols-outlined">close</span></button>
            </div>
            <div class="h-48 rounded-xl overflow-hidden bg-slate-100">
                ${item.image ? `<img src="${item.image}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-[48px] text-outline-variant">${CATEGORY_CONFIG[window.activeCategory].icon}</span></div>`}
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
    l2.classList.add('opacity-0');
    setTimeout(() => l2.classList.add('hidden'), 300);
};

window.updateListIndicator = function() {
    const indicator = document.getElementById('global-list-indicator');
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
                <button class="bg-surface-container-low px-4 py-2 rounded-full font-bold text-xs">Items: ${window.layoverList.length}</button>
                <button onclick=\"window.proceedToPlan(this)\" class=\"bg-primary text-white px-5 py-2 rounded-full font-bold text-xs flex items-center gap-1\">Plan My List <span class=\"material-symbols-outlined text-sm\">arrow_forward</span></button>
            </div>`;
    } else {
        ind.style.display = 'none';
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
});
</script>'''

# Replace the existing script content
content = re.sub(r'<script>.*?</script>', new_script, content, flags=re.DOTALL)

with open('marketplace.html', 'w', encoding='utf-8') as f:
    f.write(content)
