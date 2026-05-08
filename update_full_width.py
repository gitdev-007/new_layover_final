import re

with open('marketplace.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_render_logic = r'''
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
        const config = window.FILTER_CONFIG['hotel.html'];
        container.innerHTML = `
            <div id="level1" class="layout-transition w-full max-w-4xl mx-auto flex-shrink-0 z-10 relative">
                <div class="flex items-center justify-between mb-4">
                    <span class="bg-primary text-white text-meta-label px-3 py-1 uppercase">Level 1: Listing</span>
                </div>
                <div class="bg-white border-2 border-blueprint-border p-6 shadow-sm">
                    <div class="flex justify-between items-start mb-6">
                        <h3 class="text-node-title-md text-primary uppercase cursor-pointer hover:underline" onclick="window.closeLevel2()">Recommended For You</h3>
                    </div>
                    <div class="border border-outline-variant p-3 bg-surface-container mb-4">
                        <p class="text-meta-label text-on-surface-variant mb-2">CURATED PICKS</p>
                        <p class="text-[11px] text-on-surface-variant">Top experiences based on your flight buffer.</p>
                    </div>
                    <div class="border-2 border-dashed border-blueprint-border p-4">
                        <p class="text-meta-label text-on-surface-variant mb-3">INVENTORY (3 ITEMS FOUND)</p>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-2" id="hotel-grid">
                            ${[window.LAYOVER_INVENTORY['Hotels'][2], window.LAYOVER_INVENTORY['Restaurants'][3], window.LAYOVER_INVENTORY['Spa'][1]].map(i => window.renderCard(i)).join('')}
                        </div>
                    </div>
                </div>
            </div>
            ${window.level2Template()}
        `;
        return;
    }

    const config = window.FILTER_CONFIG[catId];
    if (!config) return;

    let filterHTML = `
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <select id="filter-duration" onchange="window.renderItems()" class="w-full bg-white border border-slate-300 p-3 rounded text-[11px] font-bold uppercase tracking-widest text-slate-700 outline-none focus:border-primary transition-colors cursor-pointer shadow-sm">
                <option value="any">${config.durationLabel}</option>
                ${config.durations.map(d => `<option value="${d.v}">${d.l}</option>`).join('')}
            </select>
            <select id="filter-price" onchange="window.renderItems()" class="w-full bg-white border border-slate-300 p-3 rounded text-[11px] font-bold uppercase tracking-widest text-slate-700 outline-none focus:border-primary transition-colors cursor-pointer shadow-sm">
                <option value="any">Price Range</option>
                ${config.priceRange.map(p => `<option value="${p.v}">${p.l}</option>`).join('')}
            </select>
            <select id="filter-distance" onchange="window.renderItems()" class="w-full bg-white border border-slate-300 p-3 rounded text-[11px] font-bold uppercase tracking-widest text-slate-700 outline-none focus:border-primary transition-colors cursor-pointer shadow-sm">
                <option value="any">Distance</option>
                ${config.distance.map(d => `<option value="${d.v}">${d.l}</option>`).join('')}
            </select>
            <select id="filter-amenities" onchange="window.renderItems()" class="w-full bg-white border border-slate-300 p-3 rounded text-[11px] font-bold uppercase tracking-widest text-slate-700 outline-none focus:border-primary transition-colors cursor-pointer shadow-sm">
                <option value="any">Amenities</option>
                ${config.amenities.map(a => `<option value="${a.v}">${a.l}</option>`).join('')}
            </select>
        </div>
    `;

    container.innerHTML = `
        <div class="main-layout flex flex-col xl:flex-row items-start gap-8 w-full">
            <div id="level1" class="layout-transition w-full flex-shrink-0 z-10 relative bg-slate-50 border border-slate-200 rounded-3xl p-8 shadow-sm">
                <div class="flex justify-between items-end border-b border-slate-200 pb-6 mb-8">
                    <div>
                        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-1">LEVEL 1: LISTING</p>
                        <h3 class="text-3xl font-black text-primary uppercase tracking-tight" style="letter-spacing: -0.02em;">${config.title}</h3>
                    </div>
                    <span class="bg-primary text-white text-[10px] px-3 py-1 rounded font-bold uppercase tracking-widest shadow-sm">Global Discovery</span>
                </div>
                
                ${filterHTML}
                
                <div class="border-2 border-dashed border-slate-200 p-6 rounded-2xl bg-white/50">
                    <div class="flex justify-between items-center mb-6">
                        <p id="inventory-count" class="text-[11px] font-black text-primary uppercase tracking-widest">${config.inventoryLabel} INVENTORY (0 FOUND)</p>
                    </div>
                    <div id="hotel-grid" class="w-full"></div>
                </div>
            </div>
            
            ${window.level2Template()}
        </div>
    `;

    window.renderItems();
};

window.level2Template = function() {
    return `
        <div id="level2" class="layout-transition hidden opacity-0 w-full max-w-xl flex-shrink-0 z-20 relative">
            <div class="bg-white border border-slate-200 rounded-3xl p-6 shadow-xl flex flex-col h-[700px]">
                <div class="flex justify-between items-start mb-6 shrink-0 border-b border-slate-100 pb-4">
                    <div>
                        <span class="bg-primary/10 text-primary text-[9px] px-2 py-0.5 rounded font-bold uppercase tracking-widest mb-1 inline-block border border-primary/10">Level 2: Details</span>
                        <h3 class="text-xl font-black text-primary uppercase tracking-tight">Detail View</h3>
                    </div>
                    <button onclick="window.closeLevel2()" class="text-slate-400 hover:text-primary p-2 rounded-full hover:bg-slate-100 transition-colors"><span class="material-symbols-outlined text-[20px]">close</span></button>
                </div>
                
                <div class="space-y-6 overflow-y-auto hide-scrollbar flex-grow pb-4 px-2">
                    <div class="border border-slate-200 p-4 rounded-xl bg-slate-50">
                        <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-1">ENTITY HEADER</p>
                        <h4 id="l2-name" class="text-lg font-black text-primary tracking-tight">Item Name</h4>
                        <div class="flex items-center gap-2 mt-2">
                            <span id="l2-rating" class="bg-emerald-500 text-white text-[10px] px-2 py-0.5 rounded font-bold">4.8 ★</span>
                            <span id="l2-distance" class="text-[10px] text-slate-500 font-medium">0.9 km from T2</span>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div class="border border-slate-200 p-4 rounded-xl text-center bg-white shadow-sm hover:border-primary transition-colors cursor-pointer">
                            <span class="material-symbols-outlined text-primary text-[24px]">grid_view</span>
                            <p class="text-[10px] mt-2 font-bold text-primary uppercase tracking-widest">Media Gallery</p>
                        </div>
                        <div class="border border-slate-200 p-4 rounded-xl text-center bg-white shadow-sm hover:border-primary transition-colors cursor-pointer">
                            <span class="material-symbols-outlined text-primary text-[24px]">list_alt</span>
                            <p class="text-[10px] mt-2 font-bold text-primary uppercase tracking-widest">Options</p>
                        </div>
                    </div>

                    <div class="border border-slate-200 p-5 rounded-xl bg-white shadow-sm">
                        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">KEY DIFFERENTIATORS</p>
                        <div id="l2-amenities" class="text-xs font-semibold text-slate-600 space-y-2"></div>
                    </div>

                    <div class="border-2 border-primary/20 p-5 rounded-xl bg-primary/5 shadow-inner">
                        <label class="block text-[9px] font-bold text-primary uppercase tracking-widest mb-2">Selection Period <span class="text-red-500">*</span></label>
                        <select id="item-duration" class="w-full mb-4 bg-white border border-slate-300 px-4 py-3 text-sm text-primary font-bold outline-none cursor-pointer rounded-lg shadow-sm focus:border-primary focus:ring-1 focus:ring-primary"></select>
                        <button id="add-list-btn" class="w-full bg-primary text-white font-black py-4 rounded-xl text-sm tracking-widest uppercase hover:bg-black transition-colors shadow-lg active:scale-95">
                            ADD TO LIST
                        </button>
                    </div>

                    <div class="grid grid-cols-2 gap-4 text-meta-label">
                        <div class="border border-slate-200 p-4 rounded-xl bg-white shadow-sm">
                            <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-1">REVIEWS</p>
                            <p class="font-bold text-primary text-sm">Verified</p>
                        </div>
                        <div class="border border-slate-200 p-4 rounded-xl bg-white shadow-sm">
                            <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-1">CONTACT</p>
                            <p class="font-bold text-primary text-sm">Quick Inquiry</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.renderCard = function(h) {
    const isActive = window.activeItem && window.activeItem.id === h.id;
    let configKey = 'hotel.html';
    if (h.type === 'Hotel') configKey = 'hotel.html';
    if (h.type === 'Restaurant') configKey = 'restaurant.html';
    if (h.type === 'Spa') configKey = 'spa.html';
    if (h.type === 'Entertainment') configKey = 'entertainment.html';

    const config = window.FILTER_CONFIG[configKey];
    let isPremium = false;
    if (config) {
        isPremium = (h.category === config.groups[0].key);
    }
    
    const bgClass = isActive 
        ? 'bg-primary/10 border-primary ring-1 ring-primary shadow-md' 
        : 'bg-white border-slate-200 hover:border-primary/50 hover:shadow-md';
    
    const travel = window.calculateLegTravelTime(0, h.distance);
    
    return `
        <div onclick="window.openLevel2(${h.id})" class="p-4 border rounded-xl cursor-pointer transition-all flex flex-col h-full ${bgClass} group">
            <div class="flex justify-between items-start mb-3">
                <div class="pr-2">
                    <h4 class="font-bold text-sm text-primary leading-tight group-hover:text-brand-blue transition-colors line-clamp-1">${h.name}</h4>
                </div>
                ${isPremium ? '<span class="material-symbols-outlined text-[16px] text-brand-orange shrink-0">workspace_premium</span>' : '<span class="material-symbols-outlined text-[16px] text-slate-300 group-hover:text-primary transition-colors">arrow_outward</span>'}
            </div>
            <div class="mt-auto border-t border-slate-100 pt-3 flex justify-between items-end">
                <div class="flex flex-col">
                    <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Est. Travel</span>
                    <span class="text-[11px] font-black text-primary">${travel}m</span>
                </div>
                <div class="flex flex-col items-end">
                    <span class="text-[11px] font-black text-brand-orange">${h.rating} ★</span>
                </div>
            </div>
        </div>
    `;
}

window.renderItems = function() {
    if (window.activeCategory === 'recommended') return;

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

    const config = window.FILTER_CONFIG[window.activeCategory];
    document.getElementById('inventory-count').textContent = `${config.inventoryLabel} INVENTORY (${filtered.length} FOUND)`;

    grid.innerHTML = '';
    
    config.groups.forEach(grp => {
        const groupItems = filtered.filter(h => h.category === grp.key);
        if (groupItems.length > 0) {
            grid.innerHTML += `
                <div class="col-span-full mt-6 mb-3 flex items-center justify-between">
                    <h4 class="text-[11px] font-black text-primary uppercase tracking-[0.15em] flex items-center gap-2">
                        <span class="material-symbols-outlined text-sm">bookmark</span> ${grp.title}
                    </h4>
                    <div class="h-px bg-slate-200 flex-grow mx-4"></div>
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">${groupItems.length} ITEMS</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 w-full">
                    ${groupItems.map(h => window.renderCard(h)).join('')}
                </div>
            `;
        }
    });

    const mappedCategories = config.groups.map(g => g.key);
    const unmappedItems = filtered.filter(h => !mappedCategories.includes(h.category));
    if (unmappedItems.length > 0) {
        grid.innerHTML += `
            <div class="col-span-full mt-6 mb-3 flex items-center justify-between">
                <h4 class="text-[11px] font-black text-primary uppercase tracking-[0.15em] flex items-center gap-2">
                    <span class="material-symbols-outlined text-sm">more_horiz</span> Other Options
                </h4>
                <div class="h-px bg-slate-200 flex-grow mx-4"></div>
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">${unmappedItems.length} ITEMS</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 w-full">
                ${unmappedItems.map(h => window.renderCard(h)).join('')}
            </div>
        `;
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
    
    if (window.activeCategory !== 'recommended') {
        window.renderItems();
    }

    document.getElementById('l2-name').textContent = item.name;
    document.getElementById('l2-rating').textContent = `${item.rating} ★`;
    document.getElementById('l2-distance').textContent = `${item.distance} km from T2`;
    
    const amCont = document.getElementById('l2-amenities');
    amCont.innerHTML = item.amenities.length 
        ? item.amenities.map(a => `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${a}</div>`).join('') 
        : '<div class="text-[11px] text-on-surface-variant italic">Standard amenities included</div>';

    let config = window.FILTER_CONFIG[window.activeCategory];
    if (window.activeCategory === 'recommended') {
        if (item.type === 'Hotel') config = window.FILTER_CONFIG['hotel.html'];
        else if (item.type === 'Restaurant') config = window.FILTER_CONFIG['restaurant.html'];
        else config = window.FILTER_CONFIG['spa.html'];
    }

    const itemDur = document.getElementById('item-duration');
    if (itemDur) {
        itemDur.innerHTML = '';
        config.durations.forEach(d => {
            itemDur.add(new Option(d.l, d.l));
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
            btn.className = 'w-full py-4 text-sm tracking-widest uppercase transition-colors bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-xl font-black cursor-default shadow-sm';
            btn.disabled = true;
            if(itemDur) itemDur.disabled = true;
        } else {
            if (!btn.dataset.originalClasses) {
                btn.dataset.originalClasses = btn.className;
                btn.dataset.originalHtml = btn.innerHTML;
            }
            btn.innerHTML = 'ADD TO LIST';
            btn.className = 'w-full bg-primary text-white font-black py-4 rounded-xl text-sm tracking-widest uppercase hover:bg-black transition-colors shadow-lg active:scale-95';
            btn.disabled = false;
            if(itemDur) itemDur.disabled = false;
            
            btn.onclick = function() {
                const duration = itemDur ? (itemDur.options[itemDur.selectedIndex].text) : '1h';
                window.addToList(btn, item.name, item.type, duration, item.distance, '');
            };
        }
    }

    const l1 = document.getElementById('level1');
    const l2 = document.getElementById('level2');
    
    if (l1 && l2) {
        l2.classList.remove('hidden');
        requestAnimationFrame(() => { 
            l2.classList.remove('opacity-0'); 
            setTimeout(() => {
                l2.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        });
    }
};

window.closeLevel2 = function() {
    window.activeItem = null;
    if (window.activeCategory !== 'recommended') {
        window.renderItems();
    }
    
    const l2 = document.getElementById('level2');
    if (l2) {
        l2.classList.add('opacity-0');
        setTimeout(() => {
            l2.classList.add('hidden');
        }, 300);
    }
};
'''

content = re.sub(
    r'window\.renderCategory = function\(catId, btn\) \{.*?window\.closeLevel2 = function\(\) \{.*?\};',
    new_render_logic,
    content,
    flags=re.DOTALL
)

with open('marketplace.html', 'w', encoding='utf-8') as f:
    f.write(content)
