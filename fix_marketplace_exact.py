import re

with open('hotel.html', 'r', encoding='utf-8') as f:
    hotel_content = f.read()

# Extract styles from hotel.html
style_match = re.search(r'<style>.*?</style>', hotel_content, re.DOTALL)
styles = style_match.group(0) if style_match else ''

# Extract Tailwind config from hotel.html
tw_match = re.search(r'<script id=\"tailwind-config\">.*?</script>', hotel_content, re.DOTALL)
tw_config = tw_match.group(0) if tw_match else ''

# Read marketplace.html
with open('marketplace.html', 'r', encoding='utf-8') as f:
    market_content = f.read()

# Replace Tailwind config
if tw_config:
    market_content = re.sub(r'<script id=\"tailwind-config\">.*?</script>', tw_config, market_content, flags=re.DOTALL)

# Inject styles just before </head>
market_content = re.sub(r'</head>', styles + '\n</head>', market_content)

new_script = r'''<script>
// --- GLOBAL STATE & CONFIG ---
window.layoverList = [];
window.activeCategory = 'hotel.html'; 
window.activeItem = null;
window.isRisk = false;

window.LAYOVER_INVENTORY = {
    'Hotels': [
        { id: 1, name: "The Orchid Hotel", distance: 0.9, terminal: "T2", category: "Premium", rating: "4.8", price: 4500, durations: [3, 4, 6, 8, 10, 12, 16, 24], amenities: ["Airport Shuttle", "Pool", "Spa"], type: 'Hotel' },
        { id: 2, name: "Hotel Sahara Star", distance: 1.1, terminal: "T2", category: "Premium", rating: "4.7", price: 5200, durations: [3, 4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Spa"], type: 'Hotel' },
        { id: 3, name: "Taj Santacruz", distance: 1.6, terminal: "T2", category: "Premium", rating: "4.9", price: 8200, durations: [6, 8, 10, 12, 16, 24], amenities: ["Airport Shuttle", "Spa", "Business Center"], type: 'Hotel' },
        { id: 4, name: "Hotel Bawa Intl.", distance: 1.7, terminal: "T2", category: "Standard", rating: "4.2", price: 2800, durations: [3, 4, 6, 8, 10, 12], amenities: ["Business Center"], type: 'Hotel' },
        { id: 5, name: "JW Marriott Sahar", distance: 1.8, terminal: "T2", category: "Premium", rating: "4.8", price: 7800, durations: [4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Spa", "Business Center"], type: 'Hotel' },
        { id: 6, name: "Hotel Midland", distance: 2.3, terminal: "T2", category: "Standard", rating: "4.0", price: 2500, durations: [3, 4, 6, 8, 10, 12], amenities: [], type: 'Hotel' },
        { id: 7, name: "ITC Maratha", distance: 2.4, terminal: "T2", category: "Premium", rating: "4.8", price: 7600, durations: [8, 10, 12, 16, 24], amenities: ["Pool", "Spa", "Business Center"], type: 'Hotel' },
        { id: 8, name: "The Leela Mumbai", distance: 2.5, terminal: "T2", category: "Premium", rating: "4.7", price: 7200, durations: [6, 8, 10, 12, 16, 24], amenities: ["Pool", "Airport Shuttle", "Business Center"], type: 'Hotel' },
        { id: 9, name: "Aurika Mumbai", distance: 2.8, terminal: "T2", category: "Premium", rating: "4.6", price: 6200, durations: [4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Business Center"], type: 'Hotel' },
        { id: 10, name: "Lemon Tree Premier", distance: 3.2, terminal: "T2", category: "Standard", rating: "4.2", price: 3800, durations: [3, 4, 6, 8, 10, 12, 16], amenities: ["Airport Shuttle"], type: 'Hotel' },
        { id: 11, name: "Holiday Inn", distance: 4.2, terminal: "T2", category: "Standard", rating: "4.4", price: 4200, durations: [4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Business Center"], type: 'Hotel' },
        { id: 12, name: "Grand Hyatt", distance: 6.1, terminal: "T2", category: "Premium", rating: "4.7", price: 7000, durations: [8, 10, 12, 16, 24], amenities: ["Pool", "Spa", "Business Center"], type: 'Hotel' }
    ],
    'Restaurants': [
        { id: 201, name: "Thai Naam", distance: 1.8, terminal: "T2", category: "Fine Dining", rating: "4.8", price: 3800, durations: [1, 1.5, 2], amenities: ["Chef Tasting"], type: 'Restaurant' },
        { id: 202, name: "JW Cafe", distance: 1.8, terminal: "T2", category: "Fine Dining", rating: "4.7", price: 1800, durations: [1, 1.5, 2], amenities: ["Buffet"], type: 'Restaurant' },
        { id: 203, name: "Cafe Coffee Day", distance: 0.4, terminal: "T2", category: "Cafes", rating: "4.2", price: 550, durations: [0.5, 1], amenities: ["Quick Bites"], type: 'Restaurant' },
        { id: 204, name: "Sake & Stone", distance: 1.8, terminal: "T2", category: "Fine Dining", rating: "4.9", price: 4500, durations: [1.5, 2], amenities: ["Sashimi"], type: 'Restaurant' },
        { id: 205, name: "Subway", distance: 0.2, terminal: "T2", category: "Fast Dining", rating: "4.0", price: 400, durations: [0.5, 1], amenities: ["Quick Bites"], type: 'Restaurant' }
    ],
    'Spa': [
        { id: 301, name: "Jiva Spa", distance: 1.6, terminal: "T2", category: "Premium Spa", rating: "4.9", price: 3500, durations: [1, 1.5, 2, 2.5, 3], amenities: ["Ayurvedic"], type: 'Spa' },
        { id: 302, name: "Aura Wellness", distance: 1.6, terminal: "T2", category: "Wellness", rating: "4.7", price: 2800, durations: [0.5, 1, 1.5, 2], amenities: ["Holistic"], type: 'Spa' },
        { id: 303, name: "O2 Spa Express", distance: 0.5, terminal: "T2", category: "Express Treatments", rating: "4.4", price: 1200, durations: [0.5, 1], amenities: ["Foot Reflexology"], type: 'Spa' }
    ],
    'Entertainment': [
        { id: 401, name: "KidZania", distance: 7.9, terminal: "T2", category: "Kids", rating: "4.8", price: 2500, durations: [2, 3, 4], amenities: ["Role-play"], type: 'Entertainment' },
        { id: 402, name: "Zero Latency VR", distance: 16.5, terminal: "T2", category: "VR", rating: "4.9", price: 3500, durations: [1, 2], amenities: ["Free-Roam VR"], type: 'Entertainment' },
        { id: 403, name: "T2 Premium Lounge", distance: 0.1, terminal: "T2", category: "Lounges", rating: "4.6", price: 1500, durations: [1, 2, 3, 4], amenities: ["Food & Drinks", "Wi-Fi"], type: 'Entertainment' },
        { id: 404, name: "Timezone", distance: 8.5, terminal: "T2", category: "Gaming", rating: "4.3", price: 1800, durations: [1, 2, 3], amenities: ["Arcade"], type: 'Entertainment' }
    ]
};

const FILTER_CONFIG = {
    'hotel.html': {
        title: "HOTELS LISTING PAGE",
        inventoryLabel: "HOTEL",
        durationLabel: "Duration",
        durations: [{v:'3',l:'3 Hours'}, {v:'4',l:'4 Hours'}, {v:'6',l:'6 Hours'}, {v:'8',l:'8 Hours'}, {v:'10',l:'10 Hours'}, {v:'12',l:'12 Hours'}, {v:'16',l:'16 Hours'}, {v:'24',l:'24 Hours'}],
        priceRange: [{v:'0-3000',l:'₹0 – ₹3000'}, {v:'3000-6000',l:'₹3000 – ₹6000'}, {v:'6000-10000',l:'₹6000 – ₹10000'}, {v:'10000+',l:'₹10000+'}],
        distance: [{v:'1',l:'Within 1 km'}, {v:'3',l:'Within 3 km'}, {v:'5',l:'Within 5 km'}, {v:'10',l:'Within 10 km'}],
        amenities: [{v:'Airport Shuttle',l:'Airport Shuttle'}, {v:'Pool',l:'Pool'}, {v:'Spa',l:'Spa'}, {v:'Business Center',l:'Business Center'}],
        groups: [{key:'Premium', title:'PREMIUM HOTELS'}, {key:'Standard', title:'STANDARD HOTELS'}]
    },
    'restaurant.html': {
        title: "RESTAURANTS LISTING PAGE",
        inventoryLabel: "RESTAURANT",
        durationLabel: "Duration",
        durations: [{v:'0.5',l:'30 Min'}, {v:'1',l:'1 Hour'}, {v:'1.5',l:'1.5 Hours'}, {v:'2',l:'2 Hours'}],
        priceRange: [{v:'0-1000',l:'₹0 – ₹1000'}, {v:'1000-2500',l:'₹1000 – ₹2500'}, {v:'2500-5000',l:'₹2500 – ₹5000'}, {v:'5000+',l:'₹5000+'}],
        distance: [{v:'1',l:'Within 1 km'}, {v:'3',l:'Within 3 km'}, {v:'5',l:'Within 5 km'}],
        amenities: [{v:'Chef Tasting',l:'Chef Tasting'}, {v:'Buffet',l:'Buffet'}, {v:'Quick Bites',l:'Quick Bites'}, {v:'Sashimi',l:'Sashimi'}],
        groups: [{key:'Fine Dining', title:'FINE DINING'}, {key:'Fast Dining', title:'FAST DINING'}, {key:'Cafes', title:'CAFES'}]
    },
    'spa.html': {
        title: "SPA & WELLNESS LISTING PAGE",
        inventoryLabel: "SPA",
        durationLabel: "Duration",
        durations: [{v:'0.5',l:'30 Min'}, {v:'1',l:'1 Hour'}, {v:'1.5',l:'1.5 Hours'}, {v:'2',l:'2 Hours'}, {v:'2.5',l:'2.5 Hours'}, {v:'3',l:'3 Hours'}],
        priceRange: [{v:'0-1500',l:'₹0 – ₹1500'}, {v:'1500-3000',l:'₹1500 – ₹3000'}, {v:'3000-5000',l:'₹3000 – ₹5000'}, {v:'5000+',l:'₹5000+'}],
        distance: [{v:'1',l:'Within 1 km'}, {v:'3',l:'Within 3 km'}, {v:'5',l:'Within 5 km'}],
        amenities: [{v:'Ayurvedic',l:'Ayurvedic'}, {v:'Holistic',l:'Holistic'}, {v:'Foot Reflexology',l:'Foot Reflexology'}],
        groups: [{key:'Premium Spa', title:'PREMIUM SPA'}, {key:'Wellness', title:'WELLNESS'}, {key:'Express Treatments', title:'EXPRESS TREATMENTS'}]
    },
    'entertainment.html': {
        title: "GAMING & ENTERTAINMENT LISTING PAGE",
        inventoryLabel: "ENTERTAINMENT",
        durationLabel: "Duration",
        durations: [{v:'1',l:'1 Hour'}, {v:'2',l:'2 Hours'}, {v:'3',l:'3 Hours'}, {v:'4',l:'4 Hours'}],
        priceRange: [{v:'0-1000',l:'₹0 – ₹1000'}, {v:'1000-2500',l:'₹1000 – ₹2500'}, {v:'2500-5000',l:'₹2500 – ₹5000'}, {v:'5000+',l:'₹5000+'}],
        distance: [{v:'1',l:'Within 1 km'}, {v:'5',l:'Within 5 km'}, {v:'10',l:'Within 10 km'}, {v:'20',l:'Within 20 km'}],
        amenities: [{v:'Role-play',l:'Role-play'}, {v:'Free-Roam VR',l:'Free-Roam VR'}, {v:'Arcade',l:'Arcade'}, {v:'Food & Drinks',l:'Food & Drinks'}],
        groups: [{key:'Lounges', title:'LOUNGES'}, {key:'VR', title:'VR'}, {key:'Gaming', title:'GAMING'}, {key:'Kids', title:'KIDS'}]
    }
};

window.calculateDynamicTravelMins = function(distance) {
    const transportType = localStorage.getItem("transportType") || "Luxury";
    const speedMap = { walking: 5, cab: 28, metro: 40, bike: 18, Sedan: 40, SUV: 38, XL: 35, Luxury: 45, Shuttle: 30 };
    const speed = speedMap[transportType] || 28;
    let trafficMultiplier = 1.3;
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
            const dur = String(item.duration || '0');
            if (dur.includes('h')) m = parseFloat(dur) * 60;
            else if (dur.includes('m')) m = parseFloat(dur);
            else m = parseFloat(dur) * 60; // Default generic numeric to hours
            expMins += m;
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
        if (remainingMins < 0) {
            window.isRisk = true;
            remEl.textContent = 'Risk';
            remEl.style.color = '#dc2626';
            remContainer.style.backgroundColor = '#fef2f2';
        } else {
            window.isRisk = false;
            remEl.textContent = format(remainingMins);
            remEl.style.color = '#15803d';
            remContainer.style.backgroundColor = '#ecfdf5';
        }
    }
};

window.renderCategory = function(catId, btn) {
    if (btn) {
        document.querySelectorAll('.category-pill').forEach(pill => {
            pill.classList.remove('bg-primary', 'text-white');
            pill.classList.add('bg-white', 'text-on-surface');
        });
        btn.classList.remove('bg-white', 'text-on-surface');
        btn.classList.add('bg-primary', 'text-white');
    }

    window.activeCategory = catId;
    const container = document.getElementById('marketplace-content');
    
    if (catId === 'recommended') {
        container.innerHTML = `
            <div id="level1" class="layout-transition w-full max-w-4xl mx-auto flex-shrink-0 z-10 relative">
                <div class="flex items-center justify-between mb-4">
                    <span class="bg-primary text-white text-meta-label px-3 py-1 uppercase">Level 1: Listing</span>
                </div>
                <div class="bg-white border-2 border-primary-container p-6 shadow-sm">
                    <div class="flex justify-between items-start mb-6">
                        <h3 class="text-node-title-md text-primary uppercase cursor-pointer hover:underline" onclick="closeLevel2()">Recommended For You</h3>
                    </div>
                    <div class="border border-outline-variant p-3 bg-surface-container mb-4">
                        <p class="text-meta-label text-on-surface-variant mb-2">CURATED PICKS</p>
                        <p class="text-[11px] text-on-surface-variant">Top experiences based on your flight buffer.</p>
                    </div>
                    <div class="border-2 border-dashed border-outline-variant p-4">
                        <p class="text-meta-label text-on-surface-variant mb-3">INVENTORY (3 ITEMS FOUND)</p>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-2" id="hotel-grid">
                            ${[window.LAYOVER_INVENTORY['Hotels'][2], window.LAYOVER_INVENTORY['Restaurants'][3], window.LAYOVER_INVENTORY['Spa'][1]].map(i => renderCard(i)).join('')}
                        </div>
                    </div>
                </div>
            </div>
            ${level2Template()}
        `;
        return;
    }

    const config = FILTER_CONFIG[catId];
    if (!config) return;

    let filterHTML = `
        <div class="border border-outline-variant p-3 bg-surface-container mb-4">
            <p class="text-meta-label text-on-surface-variant mb-2">SEARCH &amp; FILTERS</p>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                <select id="filter-duration" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                    <option value="any">${config.durationLabel}</option>
                    ${config.durations.map(d => `<option value="${d.v}">${d.l}</option>`).join('')}
                </select>
                <select id="filter-price" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                    <option value="any">Price Range</option>
                    ${config.priceRange.map(p => `<option value="${p.v}">${p.l}</option>`).join('')}
                </select>
                <select id="filter-distance" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                    <option value="any">Distance</option>
                    ${config.distance.map(d => `<option value="${d.v}">${d.l}</option>`).join('')}
                </select>
                <select id="filter-amenities" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                    <option value="any">Amenities</option>
                    ${config.amenities.map(a => `<option value="${a.v}">${a.l}</option>`).join('')}
                </select>
            </div>
        </div>
    `;

    container.innerHTML = `
        <div id="level1" class="layout-transition w-full max-w-4xl mx-auto flex-shrink-0 z-10 relative flex flex-col items-center">
            <div class="w-full flex items-center justify-between mb-4">
                <span class="bg-primary text-white text-meta-label px-3 py-1 uppercase">Level 1: Listing</span>
            </div>
            <div class="w-full bg-white border-2 border-primary-container p-6 shadow-sm">
                <div class="flex justify-between items-start mb-6">
                    <h3 class="text-node-title-md text-primary uppercase cursor-pointer hover:underline" onclick="closeLevel2()">${config.title}</h3>
                </div>
                ${filterHTML}
                <div class="border-2 border-dashed border-outline-variant p-4">
                    <p id="inventory-count" class="text-meta-label text-on-surface-variant mb-3">${config.inventoryLabel} INVENTORY (0 FOUND)</p>
                    <div id="hotel-grid" class="grid grid-cols-2 md:grid-cols-4 gap-2"></div>
                </div>
            </div>
        </div>
        ${level2Template()}
    `;

    renderItems();
};

function level2Template() {
    return `
        <div id="level2" class="layout-transition hidden opacity-0 w-full max-w-4xl mx-auto flex-shrink-0 z-20 relative mt-6 lg:mt-0 flex flex-col items-center">
            <div class="w-full flex items-center justify-between mb-4">
                <span class="bg-secondary text-white text-meta-label px-3 py-1 uppercase">Level 2: Details</span>
            </div>
            <div class="w-full bg-white border-2 border-secondary p-6 shadow-sm flex flex-col">
                <div class="flex justify-between items-start mb-6 shrink-0">
                    <h3 class="text-node-title-md text-secondary uppercase">Detail Page</h3>
                    <button onclick="closeLevel2()" class="text-on-surface-variant hover:text-primary"><span class="material-symbols-outlined text-[16px]">close</span></button>
                </div>
                
                <div class="space-y-4 overflow-y-auto hide-scrollbar flex-grow pb-4">
                    <div class="wireframe-box p-3 bg-secondary/5 border-outline-variant">
                        <p class="text-meta-label text-secondary mb-1">ENTITY HEADER</p>
                        <h4 id="l2-name" class="text-[14px] font-bold">Item Name</h4>
                        <div class="flex items-center gap-2 mt-1">
                            <span id="l2-rating" class="bg-secondary-container text-secondary text-[10px] px-1 font-semibold">4.8 ★</span>
                            <span id="l2-distance" class="text-[10px] text-on-surface-variant">0.9 km from T2</span>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <div class="wireframe-box p-2 text-center bg-surface-container">
                            <span class="material-symbols-outlined text-secondary text-[18px]">grid_view</span>
                            <p class="text-[10px] mt-1 font-bold">Media Gallery</p>
                        </div>
                        <div class="wireframe-box p-2 text-center bg-surface-container">
                            <span class="material-symbols-outlined text-secondary text-[18px]">list_alt</span>
                            <p class="text-[10px] mt-1 font-bold">Options</p>
                        </div>
                    </div>

                    <div class="wireframe-box p-3 bg-surface-container">
                        <p class="text-meta-label text-on-surface-variant mb-2">KEY DIFFERENTIATORS</p>
                        <div id="l2-amenities" class="text-[11px] space-y-1"></div>
                    </div>

                    <div class="border-2 border-secondary p-3 bg-secondary/10 mt-4">
                        <select id="item-duration" class="w-full mb-3 bg-white border border-outline-variant px-2 py-2 text-[11px] text-on-surface font-medium outline-none cursor-pointer"></select>
                        <button id="add-list-btn" class="w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors">
                            ADD TO LIST
                        </button>
                    </div>

                    <div class="grid grid-cols-2 gap-3 text-meta-label mt-4">
                        <div class="wireframe-box p-2">
                            <p class="text-on-surface-variant mb-1">REVIEWS</p>
                            <p class="font-semibold text-secondary">Verified</p>
                        </div>
                        <div class="wireframe-box p-2">
                            <p class="text-on-surface-variant mb-1">CONTACT</p>
                            <p class="font-semibold text-secondary">Quick Inquiry</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function renderCard(h) {
    const isActive = window.activeItem && window.activeItem.id === h.id;
    // Defining premium based on the group property to match Explore layout grouping
    let isPremium = false;
    let configKey = 'hotel.html';
    if (h.type === 'Hotel') configKey = 'hotel.html';
    if (h.type === 'Restaurant') configKey = 'restaurant.html';
    if (h.type === 'Spa') configKey = 'spa.html';
    if (h.type === 'Entertainment') configKey = 'entertainment.html';

    const config = FILTER_CONFIG[configKey];
    if (config) {
        isPremium = (h.category === config.groups[0].key);
    }
    
    const bgClass = isActive 
        ? 'bg-primary/10 border-primary' 
        : (isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-primary/50');
    
    return `
        <div onclick="window.openLevel2(${h.id})" class="p-2 border cursor-pointer transition-colors text-[11px] font-medium text-on-surface flex flex-col justify-between h-16 ${bgClass}">
            <div class="flex justify-between items-start">
                <span class="truncate pr-1">${h.name}</span>
                ${isPremium ? '<span class="material-symbols-outlined text-[12px] text-primary shrink-0">workspace_premium</span>' : ''}
            </div>
            <div class="text-[9px] text-on-surface-variant flex justify-between items-center mt-1">
                <span>${h.distance} km</span>
                <span class="font-bold text-secondary">${h.rating} ★</span>
            </div>
        </div>
    `;
}

window.renderItems = function() {
    if (window.activeCategory === 'recommended') return; // Recommended has static rendering

    let configKey = 'Hotels';
    if (window.activeCategory === 'restaurant.html') configKey = 'Restaurants';
    else if (window.activeCategory === 'spa.html') configKey = 'Spa';
    else if (window.activeCategory === 'entertainment.html') configKey = 'Entertainment';

    const fullList = window.LAYOVER_INVENTORY[configKey] || [];
    const grid = document.getElementById('hotel-grid');
    if (!grid) return;

    const durVal = document.getElementById('filter-duration') ? document.getElementById('filter-duration').value : 'any';
    const priceVal = document.getElementById('filter-price') ? document.getElementById('filter-price').value : 'any';
    const distVal = document.getElementById('filter-distance') ? document.getElementById('filter-distance').value : 'any';
    const amenVal = document.getElementById('filter-amenities') ? document.getElementById('filter-amenities').value : 'any';

    const filtered = fullList.filter(h => {
        let match = true;
        if (durVal !== 'any' && match) {
            if (!h.durations.includes(parseFloat(durVal))) match = false;
        }
        if (distVal !== 'any' && match) {
            const maxD = parseFloat(distVal);
            if (h.distance > maxD) match = false;
        }
        if (priceVal !== 'any' && match) {
            if (priceVal.includes('+')) {
                const min = parseFloat(priceVal.replace('+',''));
                if (h.price < min) match = false;
            } else {
                const [min, max] = priceVal.split('-').map(Number);
                if (h.price < min || h.price > max) match = false;
            }
        }
        if (amenVal !== 'any' && match) {
            if (!h.amenities.includes(amenVal)) match = false;
        }
        return match;
    });

    const config = FILTER_CONFIG[window.activeCategory];
    document.getElementById('inventory-count').textContent = `${config.inventoryLabel} INVENTORY (${filtered.length} FOUND)`;

    grid.innerHTML = '';
    
    // Group rendering dynamically based on config groups
    config.groups.forEach(grp => {
        const groupItems = filtered.filter(h => h.category === grp.key);
        if (groupItems.length > 0) {
            grid.innerHTML += `
                <div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                    <h4 class="text-meta-label text-primary uppercase">${grp.title}</h4>
                    <span class="text-[10px] font-bold text-on-surface-variant">(${groupItems.length})</span>
                </div>
            `;
            groupItems.forEach(h => {
                grid.innerHTML += renderCard(h);
            });
        }
    });

    // If some items don't map to predefined groups
    const mappedCategories = config.groups.map(g => g.key);
    const unmappedItems = filtered.filter(h => !mappedCategories.includes(h.category));
    if (unmappedItems.length > 0) {
        grid.innerHTML += `
            <div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                <h4 class="text-meta-label text-primary uppercase">Other Options</h4>
                <span class="text-[10px] font-bold text-on-surface-variant">(${unmappedItems.length})</span>
            </div>
        `;
        unmappedItems.forEach(h => {
            grid.innerHTML += renderCard(h);
        });
    }
};

window.openLevel2 = function(id) {
    let item = null;
    Object.values(window.LAYOVER_INVENTORY).forEach(cat => {
        const found = cat.find(i => i.id === id);
        if (found) item = found;
    });
    if (!item) return;

    window.activeItem = item;
    
    // Re-render to highlight active card
    if (window.activeCategory !== 'recommended') {
        window.renderItems();
    } else {
        // Quick re-render for recommended
        const grid = document.getElementById('hotel-grid');
        if (grid) {
            grid.innerHTML = [window.LAYOVER_INVENTORY['Hotels'][2], window.LAYOVER_INVENTORY['Restaurants'][3], window.LAYOVER_INVENTORY['Spa'][1]].map(i => renderCard(i)).join('');
        }
    }

    document.getElementById('l2-name').textContent = item.name;
    document.getElementById('l2-rating').textContent = `${item.rating} ★`;
    document.getElementById('l2-distance').textContent = `${item.distance} km from ${item.terminal}`;
    
    const amCont = document.getElementById('l2-amenities');
    amCont.innerHTML = item.amenities.length 
        ? item.amenities.map(a => `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${a}</div>`).join('') 
        : '<div class="text-[11px] text-on-surface-variant italic">Standard amenities included</div>';

    // Populate Durations specific to category
    let config = FILTER_CONFIG[window.activeCategory];
    if (window.activeCategory === 'recommended') {
        if (item.type === 'Hotel') config = FILTER_CONFIG['hotel.html'];
        else if (item.type === 'Restaurant') config = FILTER_CONFIG['restaurant.html'];
        else config = FILTER_CONFIG['spa.html'];
    }

    const itemDur = document.getElementById('item-duration');
    if (itemDur) {
        itemDur.innerHTML = '';
        config.durations.forEach(d => {
            itemDur.add(new Option(d.l, d.v));
        });
    }

    const btn = document.getElementById('add-list-btn');
    if (btn) {
        if (btn.dataset.originalClasses) {
            btn.className = btn.dataset.originalClasses;
            btn.innerHTML = btn.dataset.originalHtml;
            btn.disabled = false;
        }
        
        const existingList = window.layoverList || [];
        const alreadyAdded = existingList.some(i => i.name === item.name);
        
        if (alreadyAdded) {
            btn.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span> ADDED';
            btn.className = 'w-full py-2 text-sm tracking-widest uppercase transition-colors bg-emerald-50 text-emerald-700 border border-emerald-200 cursor-default';
            btn.disabled = true;
            if(itemDur) itemDur.disabled = true;
        } else {
            if (!btn.dataset.originalClasses) {
                btn.dataset.originalClasses = btn.className;
                btn.dataset.originalHtml = btn.innerHTML;
            }
            btn.innerHTML = 'ADD TO LIST';
            btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
            btn.disabled = false;
            if(itemDur) itemDur.disabled = false;
            
            btn.onclick = function() {
                const duration = itemDur ? (itemDur.options[itemDur.selectedIndex].text) : '1h'; // store string label
                window.addToList(btn, item.name, item.type, duration, item.distance, '');
            };
        }
    }

    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    
    l2.classList.remove('hidden');
    requestAnimationFrame(() => { 
        l2.classList.remove('opacity-0'); 
        setTimeout(() => {
            l2.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    });
};

window.closeLevel2 = function() {
    window.activeItem = null;
    if (window.activeCategory !== 'recommended') {
        window.renderItems();
    } else {
        const grid = document.getElementById('hotel-grid');
        if (grid) {
            grid.innerHTML = [window.LAYOVER_INVENTORY['Hotels'][2], window.LAYOVER_INVENTORY['Restaurants'][3], window.LAYOVER_INVENTORY['Spa'][1]].map(i => renderCard(i)).join('');
        }
    }
    
    const l2 = document.getElementById('level2');
    if (l2) {
        l2.classList.add('opacity-0');
        setTimeout(() => {
            l2.classList.add('hidden');
        }, 300);
    }
};

window.addToList = function(btn, itemName, category, duration, distance, image) {
    if (!duration) return;
    const existing = window.layoverList.find(i => i.name === itemName);
    if (!existing) {
        window.layoverList.push({ name: itemName, category, duration, distance: parseFloat(distance) || 0, image: image || '' });
        localStorage.setItem('layoverList', JSON.stringify(window.layoverList));
    }
    btn.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span> ADDED';
    btn.className = 'w-full py-2 text-sm tracking-widest uppercase transition-colors bg-emerald-50 text-emerald-700 border border-emerald-200 cursor-default';
    btn.disabled = true;
    const itemDur = document.getElementById('item-duration');
    if(itemDur) itemDur.disabled = true;
    window.updateListIndicator();
    window.updateTimeCalculations();
};

window.updateListIndicator = function() {
    // Basic indicator to show cart/list
    let indicator = document.getElementById('global-list-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'global-list-indicator';
        indicator.className = 'fixed bottom-[100px] left-1/2 -translate-x-1/2 z-[100] transition-all duration-300';
        document.body.appendChild(indicator);
    }
    
    if (window.layoverList.length > 0) {
        indicator.style.display = 'flex';
        indicator.innerHTML = `
            <div class="flex items-center gap-2 bg-white/95 backdrop-blur-md border border-outline-variant p-2 shadow-lg">
                <button onclick=\"window.toggleListDrawer()\" class="bg-surface-container hover:bg-outline-variant px-6 py-2 font-bold text-[10px] uppercase tracking-widest text-on-surface border border-outline-variant transition-colors">View List (${window.layoverList.length})</button>
                <button onclick=\"window.proceedToPlan(this)\" class=\"bg-secondary text-white px-8 py-2 font-bold text-[10px] uppercase tracking-widest flex items-center gap-2 hover:bg-orange-700 transition-all\">Plan My Trip <span class=\"material-symbols-outlined text-sm\">arrow_forward</span></button>
            </div>`;
    } else {
        indicator.style.display = 'none';
    }
};

window.toggleListDrawer = function() {
    alert("Items in list: \n" + window.layoverList.map(i => i.name + " (" + i.duration + ")").join("\n"));
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
    try {
        const stored = localStorage.getItem('layoverList');
        window.layoverList = stored ? JSON.parse(stored) : [];
    } catch(e) { window.layoverList = []; }

    window.renderCategory('hotel.html', document.querySelectorAll('.category-pill')[1]); // Default to hotels
    window.updateTimeCalculations();
    window.updateListIndicator();
});
</script>
'''

new_content = re.sub(r'<script>.*?</script>', new_script, market_content, flags=re.DOTALL)

with open('marketplace.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated marketplace.html with exact Explore blueprint")
