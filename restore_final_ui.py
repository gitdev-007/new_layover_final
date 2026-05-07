import re

files = {
    'hotel.html': {
        'title': 'Hotels & Stays',
        'key': 'Hotels',
        'icon': 'hotel',
        'filters': """
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Stay Duration</option>
<option value="2">2 Hours</option>
<option value="4">4 Hours</option>
<option value="8">8 Hours</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-5000">₹0 – ₹5000 Budget</option>
<option value="5000-10000">₹5000 – ₹10000 Premium</option>
<option value="10000+">₹10000+ Luxury</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-5">0 – 5 km (Close)</option>
<option value="5-10">5 – 10 km (Moderate)</option>
<option value="10+">10+ km (Further)</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Hotel Types</option>
<option value="luxury">Luxury</option>
<option value="transit hub">Transit Hub</option>
<option value="eco stay">Eco Stay</option>
</select>
</div>
"""
    },
    'restaurant.html': {
        'title': 'Food & Dining',
        'key': 'Restaurants',
        'icon': 'restaurant',
        'filters': """
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Dining Duration</option>
<option value="1">1 Hour</option>
<option value="1.5">1.5 Hours</option>
<option value="2">2 Hours</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-1000">₹0 – ₹1000 Value</option>
<option value="1000-2000">₹1000 – ₹2000 Mid-range</option>
<option value="2000+">₹2000+ Fine Dining</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-5">0 – 5 km</option>
<option value="5-10">5 – 10 km</option>
<option value="10+">10+ km</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Cuisines</option>
<option value="premium thai">Premium Thai</option>
<option value="global buffet">Global Buffet</option>
<option value="quick bites">Quick Bites</option>
<option value="japanese">Japanese</option>
</select>
</div>
"""
    },
    'spa.html': {
        'title': 'Spa & Wellness',
        'key': 'Spa',
        'icon': 'spa',
        'filters': """
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Session Duration</option>
<option value="1">1 Hour</option>
<option value="1.5">1.5 Hours</option>
<option value="2">2 Hours</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-2000">₹0 – ₹2000 Refresh</option>
<option value="2000-5000">₹2000 – ₹5000 Relax</option>
<option value="5000+">₹5000+ Premium Retreat</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-5">0 – 5 km</option>
<option value="5-10">5 – 10 km</option>
<option value="10+">10+ km</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Therapies</option>
<option value="ayurvedic">Ayurvedic</option>
<option value="holistic">Holistic</option>
</select>
</div>
"""
    },
    'entertainment.html': {
        'title': 'Gaming & Entertainment',
        'key': 'Entertainment',
        'icon': 'sports_esports',
        'filters': """
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Experience Duration</option>
<option value="1">1 Hour</option>
<option value="2">2 Hours</option>
<option value="4">4 Hours</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-1000">₹0 – ₹1000 Value</option>
<option value="1000-2000">₹1000 – ₹2000 Standard</option>
<option value="2000+">₹2000+ Premium</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-20">0 – 20 km</option>
<option value="5-10">5 – 10 km</option>
<option value="10+">10+ km</option>
</select>
<select class="bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg w-full text-on-surface font-medium appearance-none shadow-sm" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Types</option>
<option value="vr arena">VR Arena</option>
<option value="escape room">Escape Room</option>
<option value="arcade">Arcade</option>
<option value="kids play zone">Kids Play Zone</option>
</select>
</div>
"""
    }
}

tailwind_config = """
<script id="tailwind-config">
tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
            "colors": {
                "primary": "#000000",
                "on-primary": "#ffffff",
                "surface": "#f9f9f9",
                "on-surface": "#1b1b1b",
                "surface-container": "#eeeeee",
                "surface-container-low": "#f3f3f3",
                "outline-variant": "#cfc4c5",
                "secondary": "#5d5f5f",
                "on-surface-variant": "#4c4546",
                "error": "#ba1a1a",
                "brand-purple": "#5d3fd3",
                "brand-accent": "#5d3fd3"
            },
            "fontFamily": {
                "sans": ["Inter", "sans-serif"]
            }
        }
    }
}
</script>
<style>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
.luxury-card {
    background: #ffffff;
    border: 1px solid #cfc4c5;
    transition: all 0.3s ease;
}
.luxury-card:hover {
    border-color: #000000;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
}
.no-scrollbar::-webkit-scrollbar { display: none; }
</style>
"""

for file, data in files.items():
    html_template = f"""<!DOCTYPE html>
<html class="light" lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>StayMarket | {data['title']}</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
{tailwind_config}
</head>
<body class="bg-surface text-on-surface font-sans antialiased overflow-x-hidden">
<main class="max-w-[1400px] mx-auto p-4 sm:p-8">
<div class="main-layout flex flex-col lg:flex-row items-start gap-8">

<!-- LEVEL 1: LISTING PAGE -->
<div class="level1 relative z-10 w-full lg:w-[45%] flex-shrink-0 transition-all duration-300">
    <div class="flex justify-between items-start mb-6">
        <div>
            <h3 class="text-2xl font-black text-primary tracking-tight uppercase">{data['title']}</h3>
            <p class="text-sm text-secondary mt-1 font-medium">Curated selections for your layover</p>
        </div>
        <span class="bg-primary text-white text-[10px] px-3 py-1 rounded-full font-bold uppercase tracking-widest shadow-sm">Level 1 : Discovery</span>
    </div>

    <div class="space-y-8">
        <!-- Search & Filters -->
        <div>
            <p class="text-[10px] font-bold text-secondary uppercase tracking-widest mb-3">Search &amp; Filters</p>
            {data['filters']}
        </div>

        <!-- Inventory List -->
        <div>
            <div class="flex justify-between items-center mb-4 border-b border-outline-variant pb-2">
                <p class="text-[10px] font-bold text-primary uppercase tracking-widest" id="inventory-count">{data['key'].upper()} INVENTORY (0 FOUND)</p>
            </div>
            <div class="grid grid-cols-1 gap-6" id="inventory-list"></div>
        </div>
    </div>
</div>

<!-- LEVEL 2: DETAIL PAGE -->
<div class="level2 relative z-10 w-full lg:w-[55%] flex-shrink-0 transition-all duration-300 hidden opacity-0 transform translate-x-4">
<div class="bg-white border border-outline-variant p-0 rounded-2xl shadow-xl flex flex-col h-full max-h-[85vh] sticky top-4">
    <div class="flex justify-between items-center p-5 border-b border-outline-variant bg-surface-container-low sticky top-0 z-20">
        <div>
            <span class="bg-primary text-white text-[10px] px-3 py-1 rounded-full font-bold uppercase tracking-widest shadow-sm">Level 2 : Details</span>
        </div>
        <button onclick="hideLevel2()" class="text-secondary hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container border border-transparent hover:border-outline-variant shadow-sm"><span class="material-symbols-outlined text-[20px]">close</span></button>
    </div>
    
    <div class="overflow-y-auto overflow-x-hidden p-6 space-y-8 hide-scrollbar bg-surface" id="level2-content">
        <!-- Dynamic Content Injected Here -->
    </div>
</div>
</div>

</div>
</main>
<script>
    var level2 = document.querySelector('.level2');
    var level1 = document.querySelector('.level1');
    var mainLayout = document.querySelector('.main-layout');
    var filterFields = document.querySelectorAll('[data-filter-field]');
    var filterState = {{}};

    var updateFilterState = (field) => {{
        filterState[field.dataset.filterField] = field.value.trim().toLowerCase();
    }};

    var inventoryData = window.LAYOVER_INVENTORY ? window.LAYOVER_INVENTORY['{data['key']}'] : [];

    var renderList = () => {{
        var listContainer = document.getElementById('inventory-list');
        var html = '';
        var visibleCount = 0;

        inventoryData.forEach(item => {{
            var strictMatch = true;

            var filterDistance = filterState.distance || '';
            if (filterDistance) {{
                if (filterDistance.endsWith('+')) {{
                    var min = parseFloat(filterDistance);
                    if (item.distance < min) strictMatch = false;
                }} else {{
                    var parts = filterDistance.split('-');
                    if (parts.length === 2) {{
                        if (item.distance < parseFloat(parts[0]) || item.distance > parseFloat(parts[1])) strictMatch = false;
                    }}
                }}
            }}

            var filterPrice = filterState.priceRange || '';
            if (strictMatch && filterPrice) {{
                var p = item.price || 0;
                if (filterPrice.endsWith('+')) {{
                    var min = parseInt(filterPrice, 10);
                    if (p < min) strictMatch = false;
                }} else {{
                    var parts = filterPrice.split('-');
                    if (parts.length === 2) {{
                        if (p < parseInt(parts[0], 10) || p > parseInt(parts[1], 10)) strictMatch = false;
                    }}
                }}
            }}

            var filterType = filterState.type || '';
            if (strictMatch && filterType) {{
                if (item.type.toLowerCase() !== filterType) strictMatch = false;
            }}

            if (strictMatch) {{
                visibleCount++;
                var indTravel = 0;
                if (window.calculateDynamicTravelMins) {{
                    indTravel = Math.round(window.calculateDynamicTravelMins(item.distance));
                }}
                var travelStr = indTravel > 0 ? `Est ${{indTravel}}m travel` : `${{item.distance}} KM`;

                html += `
                <div class="luxury-card rounded-2xl overflow-hidden group cursor-pointer" onclick="showLevel2('${{item.name}}')">
                    <div class="h-56 overflow-hidden relative">
                        ${{item.image ? `<img class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" src="${{item.image}}"/>` : `<div class="w-full h-full flex items-center justify-center bg-surface-container"><span class="material-symbols-outlined text-[48px] text-outline-variant">{data['icon']}</span></div>`}}
                        <div class="absolute top-4 right-4 px-3 py-1 bg-black/60 backdrop-blur-md rounded-full border border-white/10">
                            <span class="text-[10px] font-bold text-white uppercase tracking-widest">High Compatibility</span>
                        </div>
                    </div>
                    <div class="p-6 space-y-4">
                        <div class="flex justify-between items-start">
                            <div>
                                <h3 class="font-bold text-xl text-primary mb-1 tracking-tight">${{item.name}}</h3>
                                <p class="text-sm text-secondary font-medium">${{item.type}}</p>
                            </div>
                            <div class="flex items-center gap-1.5 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100 shadow-sm">
                                <span class="material-symbols-outlined text-emerald-700 text-[18px]" style="font-variation-settings: 'FILL' 1;">star</span>
                                <span class="font-bold text-sm text-emerald-700">${{item.rating.split(' ')[0]}}</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-8 border-t border-outline-variant/60 pt-4">
                            <div class="flex flex-col">
                                <span class="text-[9px] font-bold text-secondary uppercase tracking-widest mb-1">Est. Travel</span>
                                <span class="text-sm font-bold text-primary flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px] text-brand-purple">directions_car</span> ${{indTravel}} min</span>
                            </div>
                            <div class="flex flex-col">
                                <span class="text-[9px] font-bold text-secondary uppercase tracking-widest mb-1">Distance</span>
                                <span class="text-sm font-bold text-primary flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px]">location_on</span> ${{item.distance}} km</span>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            }}
        }});

        listContainer.innerHTML = html || '<div class="p-8 text-center bg-surface border border-dashed border-outline-variant rounded-2xl"><p class="text-sm font-bold text-primary">No matching experiences</p></div>';
        document.getElementById('inventory-count').innerHTML = `{data['key'].upper()} INVENTORY <span class="text-brand-purple">(${{visibleCount}} FOUND)</span>`;
    }};

    var applyFilters = () => {{
        filterFields.forEach(field => updateFilterState(field));
        renderList();
    }};

    var hideLevel2 = () => {{
        if (level2) {{
            level2.classList.remove('opacity-100', 'translate-x-0');
            level2.classList.add('opacity-0', 'translate-x-4');
            setTimeout(() => {{ level2.style.display = 'none'; }}, 300);
            if (level1) level1.style.width = '100%';
        }}
    }};

    window.showLevel2 = (name) => {{
        var detail = inventoryData.find(i => i.name === name);
        if (!detail || !level2) return;
        
        var durFilter = filterState.duration || '';
        
        var indTravel = 0;
        if (window.calculateDynamicTravelMins) {{
            indTravel = Math.round(window.calculateDynamicTravelMins(detail.distance));
        }}
        
        var content = document.getElementById('level2-content');
        content.innerHTML = `
<!-- Experience Overview & Gallery -->
<div class="relative w-full h-64 rounded-2xl overflow-hidden mb-2 bg-slate-100 shadow-md">
    ${{detail.image ? `<img src="${{detail.image}}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-[64px] text-outline-variant">{data['icon']}</span></div>`}}
    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex items-end p-6">
        <div class="text-white w-full">
            <div class="flex justify-between items-end w-full">
                <div>
                    <span class="bg-primary/90 backdrop-blur-md text-white px-3 py-1 rounded text-[10px] font-bold uppercase tracking-widest mb-2 inline-block border border-white/20 shadow-sm">${{detail.type}}</span>
                    <h4 class="text-3xl font-black leading-tight tracking-tight">${{detail.name}}</h4>
                </div>
                <div class="flex items-center gap-1.5 bg-emerald-500/20 backdrop-blur-md px-3 py-1.5 rounded-lg border border-emerald-400/30">
                    <span class="material-symbols-outlined text-emerald-400 text-[18px]" style="font-variation-settings: 'FILL' 1;">star</span>
                    <span class="font-bold text-emerald-50">${{detail.rating}}</span>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Key Metadata Grid -->
<div class="grid grid-cols-3 gap-4">
    <div class="bg-white border border-outline-variant/60 p-4 rounded-xl flex flex-col items-center justify-center text-center shadow-sm hover:shadow-md transition-shadow cursor-default">
        <div class="w-10 h-10 rounded-full bg-primary/5 flex items-center justify-center mb-2">
            <span class="material-symbols-outlined text-primary">verified_user</span>
        </div>
        <span class="font-bold text-sm text-primary">${{detail.reviews}}</span>
        <span class="text-[10px] text-secondary font-bold uppercase tracking-widest mt-0.5">Reviews</span>
    </div>
    <div class="bg-white border border-outline-variant/60 p-4 rounded-xl flex flex-col items-center justify-center text-center shadow-sm hover:shadow-md transition-shadow cursor-default">
        <div class="w-10 h-10 rounded-full bg-primary/5 flex items-center justify-center mb-2">
            <span class="material-symbols-outlined text-primary">distance</span>
        </div>
        <span class="font-bold text-sm text-primary">${{detail.distance}} km</span>
        <span class="text-[10px] text-secondary font-bold uppercase tracking-widest mt-0.5">From T2</span>
    </div>
    <div class="bg-white border border-outline-variant/60 p-4 rounded-xl flex flex-col items-center justify-center text-center shadow-sm hover:shadow-md transition-shadow cursor-default">
        <div class="w-10 h-10 rounded-full bg-brand-purple/10 flex items-center justify-center mb-2">
            <span class="material-symbols-outlined text-brand-purple">directions_car</span>
        </div>
        <span class="font-bold text-sm text-brand-purple">${{indTravel}} min</span>
        <span class="text-[10px] text-brand-purple font-bold uppercase tracking-widest mt-0.5">Est. Travel</span>
    </div>
</div>

<!-- Service Information & Highlights -->
<div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm">
    <p class="text-xs font-bold text-primary uppercase tracking-widest mb-4 flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">info</span> Feature Highlights &amp; Amenities</p>
    <div class="bg-surface-container-lowest rounded-xl">
        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-y-3 gap-x-6 text-sm text-on-surface font-medium">
            ${{detail.details.map((item) => `<li class="flex items-start gap-3"><span class="material-symbols-outlined text-[18px] text-emerald-600 shrink-0">check_circle</span> ${{item}}</li>`).join('')}}
            <li class="flex items-start gap-3"><span class="material-symbols-outlined text-[18px] text-emerald-600 shrink-0">check_circle</span> Instant Booking Confirmation</li>
            <li class="flex items-start gap-3"><span class="material-symbols-outlined text-[18px] text-emerald-600 shrink-0">check_circle</span> Flexible Layover Cancellation</li>
        </ul>
    </div>
</div>

<!-- Travel Breakdown & Route -->
<div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm">
    <p class="text-xs font-bold text-primary uppercase tracking-widest mb-4 flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">route</span> Route &amp; Travel Breakdown</p>
    <div class="bg-surface p-5 rounded-xl border border-outline-variant/60 flex flex-col gap-5 relative">
        <div class="absolute left-[33px] top-8 bottom-8 w-0.5 bg-outline-variant/40 border-l-2 border-dashed border-outline-variant/40"></div>
        <div class="flex items-center gap-4 relative z-10">
            <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center shrink-0 font-black text-sm shadow-md ring-4 ring-surface">T2</div>
            <div>
                <p class="font-bold text-base text-primary">Airport Departure</p>
                <p class="text-xs text-secondary font-medium">Terminal 2 VIP Exit</p>
            </div>
        </div>
        <div class="ml-16 py-1">
            <span class="text-[11px] font-bold text-brand-accent bg-brand-accent/10 px-3 py-1 rounded-full inline-flex items-center gap-1.5 shadow-sm border border-brand-accent/20"><span class="material-symbols-outlined text-[14px]">directions_car</span> ${{indTravel}} mins drive</span>
        </div>
        <div class="flex items-center gap-4 relative z-10">
            <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 shadow-sm ring-4 ring-surface border border-emerald-200"><span class="material-symbols-outlined text-[20px]" style="font-variation-settings: 'FILL' 1;">location_on</span></div>
            <div>
                <p class="font-bold text-base text-primary">${{detail.name}}</p>
                <p class="text-xs text-secondary font-medium">Arrival &amp; Check-in</p>
            </div>
        </div>
    </div>
</div>

<!-- Duration Pricing Info Panel -->
<div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm">
    <p class="text-xs font-bold text-primary uppercase tracking-widest mb-4 flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">payments</span> Duration-Based Pricing</p>
    <div class="grid grid-cols-3 gap-3">
        <div class="bg-surface border border-outline-variant/60 rounded-xl p-4 text-center shadow-sm">
            <p class="text-[10px] font-bold text-secondary uppercase tracking-widest mb-2">1-2 Hours</p>
            <p class="font-black text-xl text-primary">${{detail.prices && detail.prices.one ? detail.prices.one : '-'}}</p>
        </div>
        <div class="bg-surface border border-outline-variant/60 rounded-xl p-4 text-center shadow-sm">
            <p class="text-[10px] font-bold text-secondary uppercase tracking-widest mb-2">3-4 Hours</p>
            <p class="font-black text-xl text-primary">${{detail.prices && detail.prices.two ? detail.prices.two : '-'}}</p>
        </div>
        <div class="bg-primary/5 border border-primary/20 rounded-xl p-4 text-center shadow-sm">
            <p class="text-[10px] font-bold text-primary uppercase tracking-widest mb-2">Full Day</p>
            <p class="font-black text-xl text-primary">${{detail.prices && detail.prices.three ? detail.prices.three : '-'}}</p>
        </div>
    </div>
</div>

<!-- Add to List Area -->
<div class="bg-surface-container-low border border-outline-variant p-6 rounded-2xl shadow-md">
    <div class="flex flex-col gap-4 w-full">
        <div>
            <label class="block text-[10px] font-bold text-primary uppercase tracking-widest mb-3 flex items-center gap-2"><span class="material-symbols-outlined text-[16px] text-brand-accent">hourglass_bottom</span> Select Stay Duration <span class="text-error">*</span></label>
            <select class="w-full bg-white border border-outline-variant p-4 rounded-xl text-sm font-bold focus:outline-none focus:border-brand-accent focus:ring-2 focus:ring-brand-accent/20 shadow-sm appearance-none cursor-pointer" onchange="this.nextElementSibling.disabled = !this.value; this.nextElementSibling.dataset.duration = this.value;">
                <option value="" disabled selected hidden>Select exact duration to unlock booking...</option>
                <option value="30m">30 mins</option>
                <option value="1h" ${{durFilter === '1' ? 'selected' : ''}}>1 hour</option>
                <option value="1.5h" ${{durFilter === '1.5' ? 'selected' : ''}}>1.5 hours</option>
                <option value="2h" ${{durFilter === '2' ? 'selected' : ''}}>2 hours</option>
                <option value="3h" ${{durFilter === '3' ? 'selected' : ''}}>3 hours</option>
                <option value="4h" ${{durFilter === '4' ? 'selected' : ''}}>4 hours</option>
                <option value="6h" ${{durFilter === '6' ? 'selected' : ''}}>6 hours</option>
                <option value="8h" ${{durFilter === '8' ? 'selected' : ''}}>8 hours</option>
            </select>
            <button disabled data-duration="" onclick="window.addToList && window.addToList(this, '${{detail.name}}', '${{detail.category}}', this.dataset.duration, ${{detail.distance}}, '${{detail.image}}')" class="mt-4 w-full bg-primary hover:bg-primary/90 text-white font-bold py-4 rounded-xl text-base tracking-wide flex justify-center items-center gap-2 transition-all duration-300 shadow-xl disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-2xl active:scale-[0.98]">
                <span class="material-symbols-outlined text-[20px]">add_task</span> Add to List
            </button>
        </div>
    </div>
</div>

<!-- Similar Experiences (Recommendations) -->
<div class="mt-4 pt-6">
    <p class="text-[10px] font-bold text-primary uppercase tracking-widest mb-4 flex items-center gap-2"><span class="material-symbols-outlined text-[16px]">travel_explore</span> Similar Experiences Nearby</p>
    <div class="grid grid-cols-2 gap-4">
        ${{inventoryData.filter(i => i.name !== detail.name).slice(0, 2).map(sim => `
            <div class="border border-outline-variant rounded-xl overflow-hidden bg-white cursor-pointer hover:border-primary hover:shadow-md transition-all group/sim" onclick="showLevel2('${{sim.name}}')">
                <div class="h-24 relative overflow-hidden">
                    ${{sim.image ? `<img src="${{sim.image}}" class="w-full h-full object-cover group-hover/sim:scale-105 transition-transform duration-500">` : `<div class="w-full h-full flex items-center justify-center bg-slate-100"><span class="material-symbols-outlined text-outline-variant text-[24px]">{data['icon']}</span></div>`}}
                </div>
                <div class="p-3">
                    <p class="font-bold text-xs text-primary truncate">${{sim.name}}</p>
                    <p class="text-[9px] text-secondary mt-1 font-medium">${{sim.distance}} km away</p>
                </div>
            </div>
        `).join('')}}
    </div>
</div>
"""

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html_template.format(
            title=data['title'], 
            key=data['key'], 
            filters=data['filters'], 
            icon=data['icon'], 
            tailwind_config=tailwind_config,
            level2_template=level2_template
        ))

print("Restored complete original Level 1 and Level 2 experience flow for all categories with rich UI components.")
