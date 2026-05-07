import os
import sys

def update_file(filename, category_name, category_key, icon_name, filters_html):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the level1 listing section
    
    # We will replace everything between <div class="space-y-4"> inside level1 and </div></div></div><!-- LEVEL 2
    # But wait, it's easier to just rebuild the entire <main> block, while keeping the <script> block and just replacing the render functions.
    
    # Let's rebuild the <main> element completely
    
    main_content = f"""<main class="max-w-7xl mx-auto space-y-12">
<div class="main-layout flex flex-col lg:flex-row items-start gap-8">
<!-- LEVEL 1: LISTING PAGE -->
<div class="level1 space-y-6 relative z-10 w-full lg:w-[600px] flex-shrink-0 transition-all duration-300">
<div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
<div class="flex justify-between items-start mb-6 border-b border-outline-variant pb-4">
<div>
<h3 class="text-xl font-bold text-primary">{category_name} Listing</h3>
<p class="text-sm text-secondary mt-1">Browse curated experiences for your layover</p>
</div>
<span class="bg-emerald-100 text-emerald-700 text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider">Finalized</span>
</div>
<div class="space-y-6">
<div class="bg-surface p-4 rounded-xl border border-outline-variant">
<p class="text-xs font-bold text-outline uppercase tracking-wider mb-3">Search &amp; Filters</p>
{filters_html}
</div>
<div>
<p class="text-xs font-bold text-outline uppercase tracking-wider mb-3" id="inventory-count">{category_key.upper()} INVENTORY (0 FOUND)</p>
<div class="space-y-4" id="inventory-list"></div>
</div>
</div>
</div>
</div>
<!-- LEVEL 2: DETAIL PAGE -->
<div class="level2 relative z-10 w-full lg:w-[600px] flex-shrink-0 transition-all duration-300 hidden opacity-0 transform translate-x-4">
<div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-lg">
<div class="flex justify-between items-start mb-6 border-b border-outline-variant pb-4">
<div>
<h3 class="text-xl font-bold text-primary">Experience Details</h3>
<p class="text-sm text-secondary mt-1">Complete overview and planning</p>
</div>
<button onclick="hideLevel2()" class="text-secondary hover:text-primary transition-colors p-1 rounded-full hover:bg-surface-container-low"><span class="material-symbols-outlined text-[20px]">close</span></button>
</div>
<div class="space-y-6" id="level2-content">
</div>
</div>
</div>
</div>
</main>"""

    # We need to replace the <main>...</main> in the file.
    import re
    new_content = re.sub(r'<main.*?</main>', main_content, content, flags=re.DOTALL)
    
    # Now for the JS block
    # We need to update the script to include the rich renderList and renderLevel2
    
    script_part = f"""
<script>
    var level2 = document.querySelector('.level2');
    var level1 = document.querySelector('.level1');
    var mainLayout = document.querySelector('.main-layout');
    var filterFields = document.querySelectorAll('[data-filter-field]');
    var filterState = {{}};

    var updateFilterState = (field) => {{
        filterState[field.dataset.filterField] = field.value.trim();
    }};

    var inventoryData = window.LAYOVER_INVENTORY ? window.LAYOVER_INVENTORY['{category_key}'] : [];

    var renderList = () => {{
        var listContainer = document.getElementById('inventory-list');
        var html = '';
        var visibleCount = 0;

        var durFilter = filterState.duration || '';

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
                if (item.type !== filterType) strictMatch = false;
            }}

            if (strictMatch) {{
                visibleCount++;
                var indTravel = 0;
                if (window.calculateDynamicTravelMins) {{
                    indTravel = Math.round(window.calculateDynamicTravelMins(item.distance));
                }}

                html += `
                <div class="flex gap-4 bg-white border border-outline-variant rounded-xl p-3 hover:shadow-md hover:border-primary/40 transition-all cursor-pointer group" onclick="showLevel2('${{item.name}}')">
                    <div class="w-32 h-32 flex-shrink-0 rounded-lg overflow-hidden bg-slate-100 relative">
                        ${{item.image ? `<img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="${{item.image}}"/>` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-[32px] text-outline-variant">{icon_name}</span></div>`}}
                    </div>
                    <div class="flex-grow flex flex-col justify-between py-1">
                        <div>
                            <div class="flex justify-between items-start">
                                <div>
                                    <span class="text-[9px] font-bold text-outline uppercase tracking-wider">${{item.category}}</span>
                                    <h3 class="font-bold text-base text-primary leading-tight mt-0.5 group-hover:text-brand-accent transition-colors">${{item.name}}</h3>
                                </div>
                                <div class="flex items-center gap-[2px] bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-100">
                                    <span class="font-bold text-[10px] text-emerald-700">${{item.rating}}</span>
                                </div>
                            </div>
                            <div class="flex gap-2 text-secondary mt-1.5 text-xs font-medium">
                                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">directions_car</span> Est ${{indTravel}}m travel</span>
                                <span>&bull;</span>
                                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">location_on</span> ${{item.distance}} km away</span>
                            </div>
                        </div>
                        <div class="flex justify-between items-center mt-3">
                            <span class="text-emerald-600 font-bold text-[9px] px-2 py-0.5 bg-emerald-50 border border-emerald-100 rounded-full uppercase tracking-wider">High Compatibility</span>
                            <span class="text-primary font-bold text-xs group-hover:underline">View Details →</span>
                        </div>
                    </div>
                </div>
                `;
            }}
        }});

        listContainer.innerHTML = html || '<p class="text-sm text-secondary text-center py-8 bg-surface rounded-xl border border-dashed border-outline-variant">No experiences match your filters.</p>';
        document.getElementById('inventory-count').textContent = `{category_key.upper()} INVENTORY (${{visibleCount}} FOUND)`;
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
        }}
    }};

    var showLevel2 = (name) => {{
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
<div class="relative w-full h-48 rounded-xl overflow-hidden mb-6 bg-slate-100">
    ${{detail.image ? `<img src="${{detail.image}}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-[48px] text-outline-variant">{icon_name}</span></div>`}}
    <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-4">
        <div class="text-white">
            <span class="bg-primary/80 backdrop-blur-sm text-white px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider mb-1 inline-block">${{detail.type}}</span>
            <h4 class="text-2xl font-bold leading-tight">${{detail.name}}</h4>
        </div>
    </div>
</div>

<!-- Key Metadata -->
<div class="grid grid-cols-3 gap-3 mb-6">
    <div class="bg-surface border border-outline-variant p-3 rounded-xl flex flex-col items-center justify-center text-center">
        <span class="material-symbols-outlined text-primary mb-1">star</span>
        <span class="font-bold text-sm text-primary">${{detail.rating}}</span>
        <span class="text-[9px] text-secondary uppercase tracking-wider">${{detail.reviews}}</span>
    </div>
    <div class="bg-surface border border-outline-variant p-3 rounded-xl flex flex-col items-center justify-center text-center">
        <span class="material-symbols-outlined text-primary mb-1">distance</span>
        <span class="font-bold text-sm text-primary">${{detail.distance}} km</span>
        <span class="text-[9px] text-secondary uppercase tracking-wider">From Airport</span>
    </div>
    <div class="bg-surface border border-outline-variant p-3 rounded-xl flex flex-col items-center justify-center text-center">
        <span class="material-symbols-outlined text-primary mb-1">directions_car</span>
        <span class="font-bold text-sm text-primary">${{indTravel}} min</span>
        <span class="text-[9px] text-secondary uppercase tracking-wider">Est. Travel</span>
    </div>
</div>

<!-- Feature Highlights -->
<div class="mb-6">
    <p class="text-xs font-bold text-outline uppercase tracking-wider mb-3">Feature Highlights &amp; Amenities</p>
    <div class="bg-surface-container-low p-4 rounded-xl border border-outline-variant">
        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-y-2 gap-x-4 text-sm text-primary font-medium">
            ${{detail.details.map((item) => `<li class="flex items-start gap-2"><span class="material-symbols-outlined text-[18px] text-emerald-600 shrink-0">check_circle</span> ${{item}}</li>`).join('')}}
            <li class="flex items-start gap-2"><span class="material-symbols-outlined text-[18px] text-emerald-600 shrink-0">check_circle</span> Instant Booking Confirmation</li>
            <li class="flex items-start gap-2"><span class="material-symbols-outlined text-[18px] text-emerald-600 shrink-0">check_circle</span> Flexible Layover Cancellation</li>
        </ul>
    </div>
</div>

<!-- Route Breakdown -->
<div class="mb-6">
    <p class="text-xs font-bold text-outline uppercase tracking-wider mb-3">Route &amp; Travel Breakdown</p>
    <div class="bg-surface p-4 rounded-xl border border-outline-variant flex flex-col gap-4">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0 font-bold text-xs">T2</div>
            <div>
                <p class="font-bold text-sm text-primary">Airport Departure</p>
                <p class="text-xs text-secondary">Terminal 2 Exit</p>
            </div>
        </div>
        <div class="ml-4 pl-4 border-l-2 border-dashed border-outline-variant py-2">
            <span class="text-xs font-bold text-brand-accent bg-brand-accent/10 px-2 py-0.5 rounded-full inline-flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">directions_car</span> ${{indTravel}} mins drive</span>
        </div>
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-[16px]">location_on</span></div>
            <div>
                <p class="font-bold text-sm text-primary">${{detail.name}}</p>
                <p class="text-xs text-secondary">Arrival &amp; Check-in</p>
            </div>
        </div>
    </div>
</div>

<!-- Duration Pricing Info Panel -->
<div class="mb-6">
    <p class="text-xs font-bold text-outline uppercase tracking-wider mb-3">Duration Pricing Info</p>
    <div class="grid grid-cols-3 gap-2">
        <div class="bg-white border border-outline-variant rounded-lg p-3 text-center shadow-sm">
            <p class="text-[10px] font-bold text-secondary uppercase tracking-widest mb-1">1-2 Hours</p>
            <p class="font-bold text-base text-primary">${{detail.prices && detail.prices.one ? detail.prices.one : '-'}}</p>
        </div>
        <div class="bg-white border border-outline-variant rounded-lg p-3 text-center shadow-sm">
            <p class="text-[10px] font-bold text-secondary uppercase tracking-widest mb-1">3-4 Hours</p>
            <p class="font-bold text-base text-primary">${{detail.prices && detail.prices.two ? detail.prices.two : '-'}}</p>
        </div>
        <div class="bg-surface-container-low border border-outline-variant rounded-lg p-3 text-center shadow-sm">
            <p class="text-[10px] font-bold text-secondary uppercase tracking-widest mb-1">Full Day</p>
            <p class="font-bold text-base text-primary">${{detail.prices && detail.prices.three ? detail.prices.three : '-'}}</p>
        </div>
    </div>
</div>

<!-- Add to List Area -->
<div class="bg-primary/5 border border-primary/20 p-5 rounded-xl">
    <div class="flex flex-col gap-3 w-full">
        <div>
            <label class="block text-xs font-bold text-primary uppercase tracking-wider mb-2">Select Stay Duration <span class="text-error">*</span></label>
            <select class="w-full bg-white border border-outline-variant p-3 rounded-lg text-sm font-medium focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary shadow-sm" onchange="this.nextElementSibling.disabled = !this.value; this.nextElementSibling.dataset.duration = this.value;">
                <option value="" disabled selected hidden>Select exact duration to unlock booking...</option>
                <option value="30m">30 mins (Quick Visit)</option>
                <option value="1h" ${{durFilter === '1' ? 'selected' : ''}}>1 hour</option>
                <option value="1.5h" ${{durFilter === '1.5' ? 'selected' : ''}}>1.5 hours</option>
                <option value="2h" ${{durFilter === '2' ? 'selected' : ''}}>2 hours</option>
                <option value="3h" ${{durFilter === '3' ? 'selected' : ''}}>3 hours</option>
                <option value="4h" ${{durFilter === '4' ? 'selected' : ''}}>4 hours</option>
                <option value="6h" ${{durFilter === '6' ? 'selected' : ''}}>6 hours</option>
                <option value="8h" ${{durFilter === '8' ? 'selected' : ''}}>8 hours</option>
            </select>
            <button disabled data-duration="" onclick="window.addToList && window.addToList(this, '${{detail.name}}', '${{detail.category}}', this.dataset.duration, ${{detail.distance}}, '${{detail.image}}')" class="mt-4 w-full bg-primary hover:bg-primary/90 text-white font-bold py-3.5 rounded-lg text-sm tracking-wide flex justify-center items-center gap-2 transition-all duration-300 shadow-lg disabled:opacity-40 disabled:cursor-not-allowed">
                <span class="material-symbols-outlined">add_task</span> Add to List
            </button>
        </div>
    </div>
</div>

<!-- Similar Experiences (Recommendations) -->
<div class="mt-8 pt-6 border-t border-outline-variant">
    <p class="text-xs font-bold text-outline uppercase tracking-wider mb-4">Similar Experiences Nearby</p>
    <div class="grid grid-cols-2 gap-3">
        ${{inventoryData.filter(i => i.name !== detail.name).slice(0, 2).map(sim => `
            <div class="border border-outline-variant rounded-xl overflow-hidden bg-white cursor-pointer hover:border-primary transition-colors" onclick="showLevel2('${{sim.name}}')">
                <div class="h-20 bg-slate-100 relative">
                    ${{sim.image ? `<img src="${{sim.image}}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-outline-variant">{icon_name}</span></div>`}}
                </div>
                <div class="p-2">
                    <p class="font-bold text-xs truncate">${{sim.name}}</p>
                    <p class="text-[9px] text-secondary mt-0.5">${{sim.distance}} km away</p>
                </div>
            </div>
        `).join('')}}
    </div>
</div>
        `;
        if (mainLayout) mainLayout.classList.add('active');
        if (level2) {{
            level2.style.display = 'block';
            setTimeout(() => {{
                level2.classList.remove('hidden', 'opacity-0', 'translate-x-4');
                level2.classList.add('opacity-100', 'translate-x-0');
            }}, 10);
        }}
        if (window.syncButtonStates) window.syncButtonStates();
    }};

    filterFields.forEach((field) => {{
        field.addEventListener('change', applyFilters);
    }});

    // Initialize with selected filter values if any were passed from external state
    applyFilters();
</script>
"""
    new_content = re.sub(r'<script>.*?</script>', script_part, new_content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

filters_hotel = """
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-node-description">
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Select Stay Duration</option>
<option value="2">2 hr</option>
<option value="4">4 hr</option>
<option value="8">8 hr</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-5000">₹0 – ₹5000 Budget</option>
<option value="5000-10000">₹5000 – ₹10000 Premium</option>
<option value="10000+">₹10000+ Luxury</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-5">0 – 5 km (Very Close)</option>
<option value="5-10">5 – 10 km (Moderate)</option>
<option value="10+">10+ km (Further)</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Hotel Types</option>
<option value="Luxury">Luxury</option>
<option value="Transit Hub">Transit Hub</option>
<option value="Eco Stay">Eco Stay</option>
</select>
</div>
"""

filters_rest = """
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-node-description">
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Select Stay Duration</option>
<option value="1">1 hr</option>
<option value="1.5">1.5 hr</option>
<option value="2">2 hr</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-1000">₹0 – ₹1000 Value</option>
<option value="1000-2000">₹1000 – ₹2000 Mid-range</option>
<option value="2000+">₹2000+ Fine Dining</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-5">0 – 5 km</option>
<option value="5-10">5 – 10 km</option>
<option value="10+">10+ km</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Cuisines</option>
<option value="Premium Thai">Premium Thai</option>
<option value="Global Buffet">Global Buffet</option>
<option value="Quick Bites">Quick Bites</option>
<option value="Japanese">Japanese</option>
</select>
</div>
"""

filters_spa = """
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-node-description">
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Select Stay Duration</option>
<option value="1">1 hr</option>
<option value="1.5">1.5 hr</option>
<option value="2">2 hr</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-2000">₹0 – ₹2000 Refresh</option>
<option value="2000-5000">₹2000 – ₹5000 Relax</option>
<option value="5000+">₹5000+ Premium Retreat</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-5">0 – 5 km</option>
<option value="5-10">5 – 10 km</option>
<option value="10+">10+ km</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Therapies</option>
<option value="Ayurvedic">Ayurvedic</option>
<option value="Holistic">Holistic</option>
</select>
</div>
"""

filters_ent = """
<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-node-description">
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="duration" onchange="applyFilters()">
<option value="" disabled selected hidden>Select Stay Duration</option>
<option value="1">1 hr</option>
<option value="2">2 hr</option>
<option value="4">4 hr</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="priceRange" onchange="applyFilters()">
<option selected value="0-1000">₹0 – ₹1000 Value</option>
<option value="1000-2000">₹1000 – ₹2000 Standard</option>
<option value="2000+">₹2000+ Premium</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="distance" onchange="applyFilters()">
<option selected value="0-20">0 – 20 km</option>
<option value="5-10">5 – 10 km</option>
<option value="10+">10+ km</option>
</select>
<select class="filter-field bg-white px-3 py-2 rounded-lg border border-outline-variant focus:border-primary transition-colors text-sm font-medium w-full appearance-none" data-filter-field="type" onchange="applyFilters()">
<option selected value="">All Types</option>
<option value="VR Arena">VR Arena</option>
<option value="Escape Room">Escape Room</option>
<option value="Arcade">Arcade</option>
<option value="Kids Play Zone">Kids Play Zone</option>
</select>
</div>
"""

update_file('hotel.html', 'Hotels & Stays', 'Hotels', 'hotel', filters_hotel)
update_file('restaurant.html', 'Food & Dining', 'Restaurants', 'restaurant', filters_rest)
update_file('spa.html', 'Spa & Wellness', 'Spa', 'spa', filters_spa)
update_file('entertainment.html', 'Gaming & Entertainment', 'Entertainment', 'sports_esports', filters_ent)
print("Updated all 4 category files successfully.")
