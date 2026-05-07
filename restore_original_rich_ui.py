import re
import os

files = {
    'hotel.html': 'Hotels',
    'restaurant.html': 'Restaurants',
    'spa.html': 'Spa',
    'entertainment.html': 'Entertainment'
}

for file, category_key in files.items():
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the hardcoded inventory with a dynamic container, preserving the wrapper.
    # Find the SEARCH & FILTERS block to keep it, but we need to find the INVENTORY block.
    # The inventory block usually starts with <p class="text-meta-label text-outline mb-2">HOTEL INVENTORY...
    
    # Let's just find the <div class="border-2 border-dashed border-outline-variant p-3">
    # and replace its contents.
    
    inv_pattern = re.compile(r'(<div class="border-2 border-dashed border-outline-variant p-3">).*?(</div>\s*</div>\s*</div>\s*</div>\s*<!-- LEVEL 2)', re.DOTALL)
    
    replacement_inv = r'''\1
<p class="text-meta-label text-outline mb-2" id="inventory-count">INVENTORY (0 FOUND)</p>
<div class="rounded-lg flex gap-3"><div class="space-y-4 w-full" id="inventory-list"></div></div>
\2'''
    
    content = inv_pattern.sub(replacement_inv, content)
    
    # 2. Replace the Level 2 content to be empty initially, we'll render it dynamically.
    # Wait, the original HTML has the Level 2 hardcoded too. Let's find LEVEL 2: DETAILS and clear its content, or just let our JS overwrite `level2.innerHTML`.
    # Our JS will just use `level2.innerHTML = renderLevel2(...)` so we don't need to clear the HTML, it will be overwritten.
    
    # 3. Replace the entire <script> block with our new dynamic script.
    
    # The original Level 2 structure we need to restore for renderLevel2:
    level2_template = """
<div class="flex items-center justify-between mb-4">
<span class="bg-secondary text-white text-meta-label px-3 py-1 font-bold">LEVEL 2: DETAILS</span>
</div>
<div class="bg-white border-2 border-secondary p-node-padding rounded shadow-sm">
<div class="flex justify-between items-start mb-6">
<h3 class="text-node-title-md font-node-title-md text-secondary">Detail Page</h3>
<span class="bg-purple-100 text-purple-700 text-[10px] px-2 py-0.5 rounded font-bold uppercase">Active</span>
</div>
<div class="space-y-4">
<div class="border border-outline-variant p-3 bg-secondary/5">
<p class="text-meta-label text-secondary mb-1">ENTITY HEADER</p>
<h4 class="text-node-title-md font-bold">${detail.name}</h4>
<div class="flex gap-2 mt-1">
<span class="text-[10px] bg-secondary-fixed text-on-secondary-fixed px-1 font-semibold">${detail.rating}</span>
<span class="text-[10px] text-outline">${detail.distance} km from Airport</span>
</div>
</div>
<div class="grid grid-cols-2 gap-3">
<div class="border border-outline-variant p-2 text-center bg-surface">
<span class="material-symbols-outlined text-secondary">grid_view</span>
<p class="text-[10px] mt-1 font-bold">Media Gallery</p>
</div>
<div class="border border-outline-variant p-2 text-center bg-surface">
<span class="material-symbols-outlined text-secondary">info</span>
<p class="text-[10px] mt-1 font-bold">Options</p>
</div>
</div>
<div class="border border-outline-variant p-3 bg-surface-container">
<p class="text-meta-label text-outline mb-2">KEY DIFFERENTIATORS</p>
<ul class="text-[11px] space-y-1">
${detail.details.map((item) => `<li class="flex items-center gap-2"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${item}</li>`).join('')}
</ul>
</div>
<div class="border-2 border-secondary p-3 rounded bg-secondary-fixed/20">
<p class="text-meta-label text-secondary font-bold mb-2">DURATION-BASED PRICING</p>
<div class="grid grid-cols-3 gap-1 text-center mb-4">
<div class="bg-white p-1 rounded border border-secondary-fixed"><p class="text-[9px] text-outline">1-2 HR</p><p class="font-bold text-[11px]">${detail.prices && detail.prices.one ? detail.prices.one : '-'}</p></div>
<div class="bg-white p-1 rounded border border-secondary-fixed"><p class="text-[9px] text-outline">3-4 HR</p><p class="font-bold text-[11px]">${detail.prices && detail.prices.two ? detail.prices.two : '-'}</p></div>
<div class="bg-white p-1 rounded border border-secondary bg-secondary/10"><p class="text-[9px] text-secondary font-bold">FULL</p><p class="font-bold text-[11px]">${detail.prices && detail.prices.three ? detail.prices.three : '-'}</p></div>
</div>
<div class="flex flex-col gap-2 w-full mt-2 pt-4 border-t border-secondary/20">
    <label class="block text-[9px] font-bold text-secondary uppercase">Select Stay Duration</label>
    <select class="w-full bg-surface border border-outline-variant p-2 rounded text-[11px] focus:outline-none focus:border-primary" onchange="this.nextElementSibling.disabled = !this.value; this.nextElementSibling.dataset.duration = this.value;">
        <option value="" disabled selected hidden>Select Duration</option>
        <option value="30m">30 mins</option>
        <option value="1h">1 hour</option>
        <option value="1.5h">1.5 hours</option>
        <option value="2h">2 hours</option>
        <option value="3h">3 hours</option>
        <option value="4h">4 hours</option>
        <option value="6h">6 hours</option>
    </select>
    <button disabled data-duration="" onclick="window.addToList && window.addToList(this, '${detail.name}', '${detail.category}', this.dataset.duration, ${detail.distance}, '${detail.image}')" class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 rounded-lg text-sm tracking-wide flex justify-center items-center gap-2 transition-all duration-200 shadow-md disabled:opacity-50 disabled:cursor-not-allowed">Add to List</button>
</div>
</div>
<div class="grid grid-cols-2 gap-3 text-meta-label mt-4">
<div class="border border-outline-variant p-2 rounded">
<p class="text-outline mb-1">REVIEWS</p>
<p class="font-semibold text-secondary">${detail.reviews}</p>
</div>
<div class="border border-outline-variant p-2 rounded">
<p class="text-outline mb-1">CONTACT</p>
<p class="font-semibold text-secondary">Quick Inquiry</p>
</div>
</div>
</div>
"""

    script_content = f"""
<script>
    var level2 = document.querySelector('.level2');
    var mainLayout = document.querySelector('.main-layout');
    var filterFields = document.querySelectorAll('[data-filter-field]');
    var filterState = {{}};

    var updateFilterState = (field) => {{
        filterState[field.dataset.filterField] = field.value.trim().toLowerCase();
    }};

    var inventoryData = window.LAYOVER_INVENTORY ? window.LAYOVER_INVENTORY['{category_key}'] : [];

    var renderList = () => {{
        var listContainer = document.getElementById('inventory-list');
        var html = '';
        var visibleCount = 0;

        inventoryData.forEach(item => {{
            var strictMatch = true;
            // Simple filtering logic
            if (strictMatch) {{
                visibleCount++;
                var indTravel = 0;
                if (window.calculateDynamicTravelMins) {{
                    indTravel = Math.round(window.calculateDynamicTravelMins(item.distance));
                }}
                var travelStr = indTravel > 0 ? `Est ${{indTravel}}m travel` : `${{item.distance}} KM`;

                html += `
                <div class="flex gap-4 bg-white border border-outline-variant rounded-xl p-4 hover:shadow-md transition-shadow cursor-pointer group" onclick="showLevel2('${{item.name}}')">
                    <div class="w-32 h-32 flex-shrink-0 rounded-lg overflow-hidden bg-slate-100">
                        ${{item.image ? `<img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="${{item.image}}"/>` : `<div class="w-full h-full flex items-center justify-center"><span class="material-symbols-outlined text-[32px] text-outline-variant">image</span></div>`}}
                    </div>
                    <div class="flex-grow flex flex-col justify-between">
                        <div>
                            <div class="flex justify-between items-start">
                                <h3 class="font-bold text-base text-primary">${{item.name}}</h3>
                                <div class="flex items-center gap-[2px] bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100">
                                    <span class="font-bold text-[10px] text-emerald-700">${{item.rating}}</span>
                                </div>
                            </div>
                            <div class="flex gap-2 text-secondary mt-1 text-xs">
                                <span>${{item.type}}</span>
                                <span>&bull;</span>
                                <span>${{travelStr}}</span>
                            </div>
                        </div>
                        <div class="flex justify-between items-center mt-3">
                            <span class="text-emerald-600 font-bold text-[9px] px-2 py-0.5 bg-emerald-50 rounded-full uppercase tracking-wider border border-emerald-100">High Compatibility</span>
                            <span class="text-brand-accent font-bold text-[11px] uppercase tracking-wider group-hover:underline">View Details</span>
                        </div>
                    </div>
                </div>
                `;
            }}
        }});

        listContainer.innerHTML = html || '<p class="text-xs text-secondary text-center py-4">No items found.</p>';
        document.getElementById('inventory-count').textContent = `INVENTORY (${{visibleCount}} FOUND)`;
    }};

    var applyFilters = () => {{
        filterFields.forEach(field => updateFilterState(field));
        renderList();
    }};

    window.showLevel2 = (name) => {{
        var detail = inventoryData.find(i => i.name === name);
        if (!detail || !level2) return;
        
        level2.innerHTML = `{level2_template}`;
        
        if (mainLayout) mainLayout.classList.add('side-by-side');
        if (level2) level2.style.display = 'block';
        if (window.syncButtonStates) window.syncButtonStates();
    }};

    filterFields.forEach((field) => {{
        field.addEventListener('change', applyFilters);
        field.addEventListener('input', applyFilters);
    }});

    applyFilters();
</script>
"""
    content = re.sub(r'<script>.*?</script>', script_content, content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated all category files.")
