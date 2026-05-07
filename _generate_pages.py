import re
import codecs

with codecs.open('_hotel_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Helper function to generate a page
def generate_page(filename, sitemap_title, l1_title, l2_title, inventory_label, premium_label, standard_label, filters_html, js_data_and_logic, entity_header_fields):
    
    html = template
    
    # Text replacements
    html = html.replace('Hotel Booking Sitemap', sitemap_title)
    html = html.replace('Hotels Listing Page', l1_title)
    html = html.replace('Hotel Detail Page', l2_title)
    html = html.replace('HOTEL INVENTORY', inventory_label)
    html = html.replace('Premium Hotels', premium_label)
    html = html.replace('Standard Hotels', standard_label)
    
    # Replace PLAN LAYOVER with PLAN EXPERIENCE
    html = html.replace('PLAN LAYOVER', 'PLAN EXPERIENCE')
    
    # Replace filters
    html = re.sub(
        r'<div class="grid grid-cols-2 md:grid-cols-4 gap-2">.*?</div>\s*</div>\s*<!-- Grid Preview -->',
        f'<div class="grid grid-cols-2 md:grid-cols-4 gap-2">\n{filters_html}\n</div>\n</div>\n<!-- Grid Preview -->',
        html,
        flags=re.DOTALL
    )
    
    # Replace entity header labels
    html = re.sub(
        r'<h4 id="l2-name".*?</h4>\s*<div class="flex items-center gap-2 mt-1">.*?</div>',
        entity_header_fields,
        html,
        flags=re.DOTALL
    )
    
    # Replace JS script block (from const hotels = to function closeLevel2)
    # Wait, it's easier to just replace the whole `<script>` block and re-add the modal logic.
    # Actually, we can replace the entire script logic for data.
    script_start = html.find('<script>') + 8
    script_end = html.find('function openVerificationModal()')
    
    new_script = js_data_and_logic
    
    html = html[:script_start] + '\n' + new_script + '\n        ' + html[script_end:]
    
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

################################################################################
# RESTAURANTS
################################################################################
filters_rest = """
<select id="filter-1" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Cuisine Type</option>
    <option value="Indian">Indian</option>
    <option value="Italian">Italian</option>
    <option value="Asian">Asian</option>
    <option value="Continental">Continental</option>
    <option value="Fast Food">Fast Food</option>
    <option value="Cafe">Cafe</option>
</select>
<select id="filter-2" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Price Range</option>
    <option value="500-1000">₹500 – ₹1000</option>
    <option value="1000-3000">₹1000 – ₹3000</option>
    <option value="3000+">₹3000+</option>
</select>
<select id="filter-3" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Distance</option>
    <option value="1">Within 1 km</option>
    <option value="3">Within 3 km</option>
    <option value="5">Within 5 km</option>
</select>
<select id="filter-4" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Dining Style</option>
    <option value="Fine Dining">Fine Dining</option>
    <option value="Casual Dining">Casual Dining</option>
    <option value="Lounge">Lounge</option>
    <option value="Rooftop">Rooftop</option>
    <option value="Cafe">Cafe</option>
</select>
"""

header_rest = """<h4 id="l2-name" class="text-[14px] font-bold">Restaurant Name</h4>
<div class="flex items-center gap-2 mt-1">
    <span id="l2-rating" class="bg-secondary-container text-secondary text-[10px] px-1 font-semibold">4.8 ★</span>
    <span id="l2-distance" class="text-[10px] text-on-surface-variant">1.6 km from T2</span>
</div>
<div class="text-[10px] text-on-surface-variant mt-1">
    <span id="l2-type" class="font-semibold text-primary">Indian</span> • <span id="l2-style">Fine Dining</span>
</div>"""

js_rest = """
const items = [
    { id: 1, name: "Masala Kraft", distance: 1.6, category: "Premium", rating: "4.8", price: 3500, type: "Indian", style: "Fine Dining", features: ["Operating Hours: 12PM-11PM", "Key Highlights: Authentic Spices", "Seating: Indoor"] },
    { id: 2, name: "Peshawri", distance: 2.4, category: "Premium", rating: "4.9", price: 4000, type: "Indian", style: "Fine Dining", features: ["Operating Hours: 12PM-11PM", "Key Highlights: Tandoori", "Seating: Indoor"] },
    { id: 3, name: "Dum Pukht", distance: 2.4, category: "Premium", rating: "4.9", price: 4500, type: "Indian", style: "Fine Dining", features: ["Operating Hours: 7PM-11PM", "Key Highlights: Royal Awadhi", "Seating: Indoor"] },
    { id: 4, name: "Aer Lounge", distance: 1.1, category: "Premium", rating: "4.7", price: 3200, type: "Continental", style: "Rooftop", features: ["Operating Hours: 5PM-1AM", "Key Highlights: City Views", "Seating: Outdoor"] },
    { id: 5, name: "Fifty Five East", distance: 6.1, category: "Premium", rating: "4.6", price: 3000, type: "Asian", style: "Lounge", features: ["Operating Hours: 24/7", "Key Highlights: Global Cuisine", "Seating: Mixed"] },
    { id: 6, name: "Celini", distance: 6.1, category: "Premium", rating: "4.7", price: 3500, type: "Italian", style: "Fine Dining", features: ["Operating Hours: 12PM-11PM", "Key Highlights: Wood-fired Pizza", "Seating: Indoor"] },
    { id: 7, name: "Lotus Cafe", distance: 1.8, category: "Premium", rating: "4.6", price: 2500, type: "Continental", style: "Cafe", features: ["Operating Hours: 24/7", "Key Highlights: Buffet", "Seating: Indoor"] },
    { id: 8, name: "Citrus", distance: 2.5, category: "Premium", rating: "4.5", price: 2800, type: "Continental", style: "Fine Dining", features: ["Operating Hours: 6AM-11PM", "Key Highlights: Fresh Juices", "Seating: Indoor"] },
    { id: 9, name: "Citrus Cafe", distance: 3.2, category: "Standard", rating: "4.1", price: 1500, type: "Cafe", style: "Casual Dining", features: ["Operating Hours: 24/7", "Key Highlights: Quick Bites", "Seating: Indoor"] },
    { id: 10, name: "Boulevard", distance: 4.2, category: "Standard", rating: "4.0", price: 1800, type: "Continental", style: "Casual Dining", features: ["Operating Hours: 6AM-11PM", "Key Highlights: Buffet", "Seating: Mixed"] },
    { id: 11, name: "Hotel Midland Restaurant", distance: 2.3, category: "Standard", rating: "3.9", price: 800, type: "Indian", style: "Casual Dining", features: ["Operating Hours: 11AM-10PM", "Key Highlights: Thali", "Seating: Indoor"] },
    { id: 12, name: "Bawa Cafe", distance: 1.7, category: "Standard", rating: "4.2", price: 900, type: "Cafe", style: "Cafe", features: ["Operating Hours: 7AM-11PM", "Key Highlights: Parsi Snacks", "Seating: Indoor"] }
];

let activeItemId = null;

function renderItems() {
    const grid = document.getElementById('hotel-grid');
    const filter1 = document.getElementById('filter-1').value;
    const filter2 = document.getElementById('filter-2').value;
    const filter3 = document.getElementById('filter-3').value;
    const filter4 = document.getElementById('filter-4').value;

    const filtered = items.filter(h => {
        let match = true;
        if (filter1 !== 'any' && h.type !== filter1) match = false;
        if (filter3 !== 'any') {
            if (h.distance > parseFloat(filter3)) match = false;
        }
        if (filter4 !== 'any' && h.style !== filter4) match = false;
        if (filter2 !== 'any') {
            if (filter2 === '3000+' && h.price < 3000) match = false;
            if (filter2 !== '3000+') {
                const [min, max] = filter2.split('-').map(Number);
                if (h.price < min || h.price > max) match = false;
            }
        }
        return match;
    });

    document.getElementById('inventory-count').textContent = `RESTAURANT INVENTORY (${filtered.length} RESTAURANTS FOUND)`;
    grid.innerHTML = '';
    
    const premiumItems = filtered.filter(h => h.category === "Premium");
    const standardItems = filtered.filter(h => h.category === "Standard");

    const renderCard = (h) => {
        const isActive = h.id === activeItemId;
        const isPremium = h.category === "Premium";
        const bgClass = isActive ? 'bg-primary/10 border-primary' : (isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-primary/50');
        return `
            <div onclick="openLevel2(${h.id})" class="p-2 border cursor-pointer transition-colors text-[11px] font-medium text-on-surface flex flex-col justify-between h-16 ${bgClass}">
                <div class="flex justify-between items-start">
                    <span class="truncate pr-1">${h.name}</span>
                    ${isPremium ? '<span class="material-symbols-outlined text-[12px] text-primary shrink-0">workspace_premium</span>' : ''}
                </div>
                <div class="text-[9px] text-on-surface-variant flex justify-between items-center mt-1">
                    <span>${h.distance} km</span>
                    <span class="font-bold text-secondary">${h.rating}</span>
                </div>
            </div>
        `;
    };

    if (premiumItems.length > 0) {
        grid.innerHTML += `<div class="col-span-full mt-2 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end"><h4 class="text-meta-label text-primary uppercase">Premium Restaurants</h4><span class="text-[10px] font-bold text-on-surface-variant">(${premiumItems.length})</span></div>`;
        premiumItems.forEach(h => { grid.innerHTML += renderCard(h); });
    }
    if (standardItems.length > 0) {
        grid.innerHTML += `<div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end"><h4 class="text-meta-label text-primary uppercase">Standard Restaurants</h4><span class="text-[10px] font-bold text-on-surface-variant">(${standardItems.length})</span></div>`;
        standardItems.forEach(h => { grid.innerHTML += renderCard(h); });
    }
}

function openLevel2(id) {
    activeItemId = id;
    renderItems(); 
    const item = items.find(h => h.id === id);
    if(!item) return;

    document.getElementById('l2-name').textContent = item.name;
    document.getElementById('l2-rating').textContent = `${item.rating} ★`;
    document.getElementById('l2-distance').textContent = `${item.distance} km from T2`;
    document.getElementById('l2-type').textContent = item.type;
    document.getElementById('l2-style').textContent = item.style;
    
    const amCont = document.getElementById('l2-amenities');
    amCont.innerHTML = item.features.length 
        ? item.features.map(a => `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${a}</div>`).join('') 
        : '<div class="text-[11px] text-on-surface-variant italic">Standard options included</div>';

    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    l1.classList.remove('max-w-4xl', 'mx-auto');
    l1.classList.add('lg:w-[55%]');
    l2.classList.remove('hidden');
    requestAnimationFrame(() => { l2.classList.remove('opacity-0'); });
}

function closeLevel2() {
    activeItemId = null;
    renderItems();
    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    l2.classList.add('opacity-0');
    setTimeout(() => {
        l2.classList.add('hidden');
        l1.classList.remove('lg:w-[55%]');
        l1.classList.add('max-w-4xl', 'mx-auto');
    }, 300);
}

// Ensure alias exists for legacy html code
function renderHotels() { renderItems(); }
"""

generate_page('restaurants.html', 'Restaurants Sitemap', 'RESTAURANTS LISTING PAGE', 'RESTAURANT DETAIL PAGE', 'RESTAURANT INVENTORY', 'Premium Restaurants', 'Standard Restaurants', filters_rest, js_rest, header_rest)

################################################################################
# SPAS
################################################################################
filters_spas = """
<select id="filter-1" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Therapy Type</option>
    <option value="Ayurvedic">Ayurvedic</option>
    <option value="Deep Tissue">Deep Tissue</option>
    <option value="Aromatherapy">Aromatherapy</option>
    <option value="Thai Massage">Thai Massage</option>
    <option value="Reflexology">Reflexology</option>
</select>
<select id="filter-2" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Price Range</option>
    <option value="1000-3000">₹1000 – ₹3000</option>
    <option value="3000-6000">₹3000 – ₹6000</option>
    <option value="6000+">₹6000+</option>
</select>
<select id="filter-3" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Distance</option>
    <option value="1">Within 1 km</option>
    <option value="3">Within 3 km</option>
    <option value="5">Within 5 km</option>
</select>
<select id="filter-4" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Wellness Features</option>
    <option value="Steam">Steam</option>
    <option value="Jacuzzi">Jacuzzi</option>
    <option value="Couple Therapy">Couple Therapy</option>
    <option value="Sauna">Sauna</option>
    <option value="Luxury Spa">Luxury Spa</option>
</select>
"""

header_spas = """<h4 id="l2-name" class="text-[14px] font-bold">Spa Name</h4>
<div class="flex items-center gap-2 mt-1">
    <span id="l2-rating" class="bg-secondary-container text-secondary text-[10px] px-1 font-semibold">4.8 ★</span>
    <span id="l2-distance" class="text-[10px] text-on-surface-variant">1.6 km from T2</span>
</div>
<div class="text-[10px] text-on-surface-variant mt-1">
    <span id="l2-type" class="font-semibold text-primary">Ayurvedic</span>
</div>"""

js_spas = """
const items = [
    { id: 1, name: "Jiva Spa", distance: 1.6, category: "Premium", rating: "4.9", price: 6500, type: "Ayurvedic", style: "Luxury Spa", features: ["Duration: 90 Mins", "Facilities: Steam, Jacuzzi"] },
    { id: 2, name: "Quan Spa", distance: 1.8, category: "Premium", rating: "4.8", price: 5500, type: "Deep Tissue", style: "Couple Therapy", features: ["Duration: 60 Mins", "Facilities: Sauna"] },
    { id: 3, name: "Kaya Kalp Spa", distance: 2.4, category: "Premium", rating: "4.9", price: 7000, type: "Aromatherapy", style: "Luxury Spa", features: ["Duration: 120 Mins", "Facilities: Jacuzzi, Steam"] },
    { id: 4, name: "The Leela Spa", distance: 2.5, category: "Premium", rating: "4.8", price: 6000, type: "Thai Massage", style: "Luxury Spa", features: ["Duration: 90 Mins", "Facilities: Sauna"] },
    { id: 5, name: "Soma Spa", distance: 6.1, category: "Premium", rating: "4.7", price: 4500, type: "Reflexology", style: "Couple Therapy", features: ["Duration: 60 Mins", "Facilities: Steam"] },
    { id: 6, name: "Lemon Tree Wellness", distance: 3.2, category: "Standard", rating: "4.2", price: 2500, type: "Ayurvedic", style: "Steam", features: ["Duration: 45 Mins", "Facilities: Basic"] },
    { id: 7, name: "Holiday Inn Wellness", distance: 4.2, category: "Standard", rating: "4.3", price: 2800, type: "Deep Tissue", style: "Sauna", features: ["Duration: 60 Mins", "Facilities: Sauna"] },
    { id: 8, name: "Midland Relaxation", distance: 2.3, category: "Standard", rating: "4.0", price: 1500, type: "Reflexology", style: "Steam", features: ["Duration: 30 Mins", "Facilities: Basic"] }
];

let activeItemId = null;

function renderItems() {
    const grid = document.getElementById('hotel-grid');
    const filter1 = document.getElementById('filter-1').value;
    const filter2 = document.getElementById('filter-2').value;
    const filter3 = document.getElementById('filter-3').value;
    const filter4 = document.getElementById('filter-4').value;

    const filtered = items.filter(h => {
        let match = true;
        if (filter1 !== 'any' && h.type !== filter1) match = false;
        if (filter3 !== 'any' && h.distance > parseFloat(filter3)) match = false;
        if (filter4 !== 'any' && h.style !== filter4 && !h.features.join(' ').includes(filter4)) match = false;
        if (filter2 !== 'any') {
            if (filter2 === '6000+' && h.price < 6000) match = false;
            if (filter2 !== '6000+') {
                const [min, max] = filter2.split('-').map(Number);
                if (h.price < min || h.price > max) match = false;
            }
        }
        return match;
    });

    document.getElementById('inventory-count').textContent = `SPA INVENTORY (${filtered.length} SPAS FOUND)`;
    grid.innerHTML = '';
    
    const premiumItems = filtered.filter(h => h.category === "Premium");
    const standardItems = filtered.filter(h => h.category === "Standard");

    const renderCard = (h) => {
        const isActive = h.id === activeItemId;
        const isPremium = h.category === "Premium";
        const bgClass = isActive ? 'bg-primary/10 border-primary' : (isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-primary/50');
        return `
            <div onclick="openLevel2(${h.id})" class="p-2 border cursor-pointer transition-colors text-[11px] font-medium text-on-surface flex flex-col justify-between h-16 ${bgClass}">
                <div class="flex justify-between items-start">
                    <span class="truncate pr-1">${h.name}</span>
                    ${isPremium ? '<span class="material-symbols-outlined text-[12px] text-primary shrink-0">workspace_premium</span>' : ''}
                </div>
                <div class="text-[9px] text-on-surface-variant flex justify-between items-center mt-1">
                    <span>${h.distance} km</span>
                    <span class="font-bold text-secondary">${h.rating}</span>
                </div>
            </div>
        `;
    };

    if (premiumItems.length > 0) {
        grid.innerHTML += `<div class="col-span-full mt-2 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end"><h4 class="text-meta-label text-primary uppercase">Premium Spas</h4><span class="text-[10px] font-bold text-on-surface-variant">(${premiumItems.length})</span></div>`;
        premiumItems.forEach(h => { grid.innerHTML += renderCard(h); });
    }
    if (standardItems.length > 0) {
        grid.innerHTML += `<div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end"><h4 class="text-meta-label text-primary uppercase">Standard Spas</h4><span class="text-[10px] font-bold text-on-surface-variant">(${standardItems.length})</span></div>`;
        standardItems.forEach(h => { grid.innerHTML += renderCard(h); });
    }
}

function openLevel2(id) {
    activeItemId = id;
    renderItems(); 
    const item = items.find(h => h.id === id);
    if(!item) return;

    document.getElementById('l2-name').textContent = item.name;
    document.getElementById('l2-rating').textContent = `${item.rating} ★`;
    document.getElementById('l2-distance').textContent = `${item.distance} km from T2`;
    document.getElementById('l2-type').textContent = item.type;
    
    const amCont = document.getElementById('l2-amenities');
    amCont.innerHTML = item.features.length 
        ? item.features.map(a => `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${a}</div>`).join('') 
        : '<div class="text-[11px] text-on-surface-variant italic">Standard options included</div>';

    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    l1.classList.remove('max-w-4xl', 'mx-auto');
    l1.classList.add('lg:w-[55%]');
    l2.classList.remove('hidden');
    requestAnimationFrame(() => { l2.classList.remove('opacity-0'); });
}

function closeLevel2() {
    activeItemId = null;
    renderItems();
    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    l2.classList.add('opacity-0');
    setTimeout(() => {
        l2.classList.add('hidden');
        l1.classList.remove('lg:w-[55%]');
        l1.classList.add('max-w-4xl', 'mx-auto');
    }, 300);
}

function renderHotels() { renderItems(); }
"""

generate_page('spas.html', 'Spa & Wellness Sitemap', 'SPA & WELLNESS PAGE', 'SPA DETAIL PAGE', 'SPA INVENTORY', 'Premium Spas', 'Standard Spas', filters_spas, js_spas, header_spas)

################################################################################
# ENTERTAINMENT
################################################################################
filters_ent = """
<select id="filter-1" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Experience Type</option>
    <option value="Gaming">Gaming</option>
    <option value="Bowling">Bowling</option>
    <option value="VR Experience">VR Experience</option>
    <option value="Lounge">Lounge</option>
    <option value="Cinema">Cinema</option>
    <option value="Arcade">Arcade</option>
</select>
<select id="filter-2" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Price Range</option>
    <option value="500-2000">₹500 – ₹2000</option>
    <option value="2000-5000">₹2000 – ₹5000</option>
    <option value="5000+">₹5000+</option>
</select>
<select id="filter-3" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Distance</option>
    <option value="1">Within 1 km</option>
    <option value="3">Within 3 km</option>
    <option value="5">Within 5 km</option>
</select>
<select id="filter-4" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
    <option value="any">Features</option>
    <option value="Multiplayer">Multiplayer</option>
    <option value="VR Gaming">VR Gaming</option>
    <option value="Premium Lounge">Premium Lounge</option>
    <option value="Family Friendly">Family Friendly</option>
    <option value="Nightlife">Nightlife</option>
</select>
"""

header_ent = """<h4 id="l2-name" class="text-[14px] font-bold">Venue Name</h4>
<div class="flex items-center gap-2 mt-1">
    <span id="l2-rating" class="bg-secondary-container text-secondary text-[10px] px-1 font-semibold">4.8 ★</span>
    <span id="l2-distance" class="text-[10px] text-on-surface-variant">1.6 km from T2</span>
</div>
<div class="text-[10px] text-on-surface-variant mt-1">
    <span id="l2-type" class="font-semibold text-primary">Gaming</span>
</div>"""

js_ent = """
const items = [
    { id: 1, name: "SMAAASH Mumbai", distance: 5.8, category: "Premium", rating: "4.7", price: 3000, type: "Gaming", style: "VR Gaming", features: ["Timings: 11AM-11PM", "Capacity: Large", "Features: Multiplayer, VR Gaming"] },
    { id: 2, name: "Amoeba Sports Bar", distance: 4.5, category: "Premium", rating: "4.5", price: 2500, type: "Bowling", style: "Nightlife", features: ["Timings: 12PM-1AM", "Capacity: Medium", "Features: Bowling, Multiplayer"] },
    { id: 3, name: "Playboy Club Lounge", distance: 5.2, category: "Premium", rating: "4.8", price: 5500, type: "Lounge", style: "Premium Lounge", features: ["Timings: 8PM-3AM", "Capacity: Medium", "Features: Premium Lounge, Nightlife"] },
    { id: 4, name: "VR Galaxy Arena", distance: 3.9, category: "Premium", rating: "4.6", price: 2200, type: "VR Experience", style: "VR Gaming", features: ["Timings: 10AM-10PM", "Capacity: Small", "Features: VR Gaming, Family Friendly"] },
    { id: 5, name: "Timezone Arcade", distance: 3.1, category: "Standard", rating: "4.3", price: 1500, type: "Arcade", style: "Family Friendly", features: ["Timings: 11AM-10PM", "Capacity: Medium", "Features: Family Friendly, Multiplayer"] },
    { id: 6, name: "Fun Republic Gaming", distance: 4.0, category: "Standard", rating: "4.2", price: 1200, type: "Gaming", style: "Family Friendly", features: ["Timings: 10AM-11PM", "Capacity: Large", "Features: Family Friendly"] },
    { id: 7, name: "Airport Lounge Hub", distance: 1.2, category: "Standard", rating: "4.0", price: 800, type: "Lounge", style: "Premium Lounge", features: ["Timings: 24/7", "Capacity: Medium", "Features: Premium Lounge"] },
    { id: 8, name: "Midnight Bowling Club", distance: 4.8, category: "Standard", rating: "4.4", price: 1800, type: "Bowling", style: "Nightlife", features: ["Timings: 6PM-2AM", "Capacity: Medium", "Features: Nightlife, Multiplayer"] }
];

let activeItemId = null;

function renderItems() {
    const grid = document.getElementById('hotel-grid');
    const filter1 = document.getElementById('filter-1').value;
    const filter2 = document.getElementById('filter-2').value;
    const filter3 = document.getElementById('filter-3').value;
    const filter4 = document.getElementById('filter-4').value;

    const filtered = items.filter(h => {
        let match = true;
        if (filter1 !== 'any' && h.type !== filter1) match = false;
        if (filter3 !== 'any' && h.distance > parseFloat(filter3)) match = false;
        if (filter4 !== 'any' && h.style !== filter4 && !h.features.join(' ').includes(filter4)) match = false;
        if (filter2 !== 'any') {
            if (filter2 === '5000+' && h.price < 5000) match = false;
            if (filter2 !== '5000+') {
                const [min, max] = filter2.split('-').map(Number);
                if (h.price < min || h.price > max) match = false;
            }
        }
        return match;
    });

    document.getElementById('inventory-count').textContent = `ENTERTAINMENT INVENTORY (${filtered.length} VENUES FOUND)`;
    grid.innerHTML = '';
    
    const premiumItems = filtered.filter(h => h.category === "Premium");
    const standardItems = filtered.filter(h => h.category === "Standard");

    const renderCard = (h) => {
        const isActive = h.id === activeItemId;
        const isPremium = h.category === "Premium";
        const bgClass = isActive ? 'bg-primary/10 border-primary' : (isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-primary/50');
        return `
            <div onclick="openLevel2(${h.id})" class="p-2 border cursor-pointer transition-colors text-[11px] font-medium text-on-surface flex flex-col justify-between h-16 ${bgClass}">
                <div class="flex justify-between items-start">
                    <span class="truncate pr-1">${h.name}</span>
                    ${isPremium ? '<span class="material-symbols-outlined text-[12px] text-primary shrink-0">workspace_premium</span>' : ''}
                </div>
                <div class="text-[9px] text-on-surface-variant flex justify-between items-center mt-1">
                    <span>${h.distance} km</span>
                    <span class="font-bold text-secondary">${h.rating}</span>
                </div>
            </div>
        `;
    };

    if (premiumItems.length > 0) {
        grid.innerHTML += `<div class="col-span-full mt-2 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end"><h4 class="text-meta-label text-primary uppercase">Premium Entertainment</h4><span class="text-[10px] font-bold text-on-surface-variant">(${premiumItems.length})</span></div>`;
        premiumItems.forEach(h => { grid.innerHTML += renderCard(h); });
    }
    if (standardItems.length > 0) {
        grid.innerHTML += `<div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end"><h4 class="text-meta-label text-primary uppercase">Standard Entertainment</h4><span class="text-[10px] font-bold text-on-surface-variant">(${standardItems.length})</span></div>`;
        standardItems.forEach(h => { grid.innerHTML += renderCard(h); });
    }
}

function openLevel2(id) {
    activeItemId = id;
    renderItems(); 
    const item = items.find(h => h.id === id);
    if(!item) return;

    document.getElementById('l2-name').textContent = item.name;
    document.getElementById('l2-rating').textContent = `${item.rating} ★`;
    document.getElementById('l2-distance').textContent = `${item.distance} km from T2`;
    document.getElementById('l2-type').textContent = item.type;
    
    const amCont = document.getElementById('l2-amenities');
    amCont.innerHTML = item.features.length 
        ? item.features.map(a => `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${a}</div>`).join('') 
        : '<div class="text-[11px] text-on-surface-variant italic">Standard options included</div>';

    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    l1.classList.remove('max-w-4xl', 'mx-auto');
    l1.classList.add('lg:w-[55%]');
    l2.classList.remove('hidden');
    requestAnimationFrame(() => { l2.classList.remove('opacity-0'); });
}

function closeLevel2() {
    activeItemId = null;
    renderItems();
    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    l2.classList.add('opacity-0');
    setTimeout(() => {
        l2.classList.add('hidden');
        l1.classList.remove('lg:w-[55%]');
        l1.classList.add('max-w-4xl', 'mx-auto');
    }, 300);
}

function renderHotels() { renderItems(); }
"""

generate_page('entertainment.html', 'Entertainment Sitemap', 'ENTERTAINMENT & GAMING PAGE', 'ENTERTAINMENT DETAIL PAGE', 'ENTERTAINMENT INVENTORY', 'Premium Entertainment', 'Standard Entertainment', filters_ent, js_ent, header_ent)

print("Generated all 3 pages successfully.")
