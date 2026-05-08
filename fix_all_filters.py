import codecs
import re

def fix_all_filters():
    files = ['restaurant.html', 'spa.html', 'entertainment.html']
    
    for filepath in files:
        with codecs.open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Let's ensure the render logic doesn't crash.
        # We will wrap it in try-catch and alert/console.error just in case, but also simplify the logic.
        
        if filepath == 'restaurant.html':
            new_render = """
        window.renderItems = function() {
            try {
                const grid = document.getElementById('hotel-grid');
                if (!grid) return;
                
                const cuisineEl = document.getElementById('filter-cuisine');
                const priceEl = document.getElementById('filter-price');
                const distEl = document.getElementById('filter-distance');
                const styleEl = document.getElementById('filter-style');
                
                const cuisineVal = cuisineEl ? cuisineEl.value : 'any';
                const priceVal = priceEl ? priceEl.value : 'any';
                const distVal = distEl ? distEl.value : 'any';
                const styleVal = styleEl ? styleEl.value : 'any';

                const filtered = items.filter(h => {
                    let match = true;
                    if (cuisineVal !== 'any' && match) {
                        if (h.type !== cuisineVal) match = false;
                    }
                    if (distVal !== 'any' && match) {
                        const maxD = parseFloat(distVal);
                        if (h.distance > maxD) match = false;
                    }
                    if (priceVal !== 'any' && match) {
                        if (priceVal === '3000+') {
                            if (h.price < 3000) match = false;
                        } else {
                            const parts = priceVal.split('-');
                            if (parts.length === 2) {
                                const min = parseInt(parts[0]);
                                const max = parseInt(parts[1]);
                                if (h.price < min || h.price > max) match = false;
                            }
                        }
                    }
                    if (styleVal !== 'any' && match) {
                        if (h.style !== styleVal) match = false;
                    }
                    return match;
                });

                const countEl = document.getElementById('inventory-count');
                if (countEl) countEl.textContent = `FOOD & DINING INVENTORY (${filtered.length} RESTAURANTS FOUND)`;

                grid.innerHTML = '';
                
                const premiumItems = filtered.filter(h => h.category === "Premium");
                const standardItems = filtered.filter(h => h.category === "Standard");

                const renderCard = (h) => {
                    const isActive = h.id === activeItemId;
                    const isPremium = h.category === "Premium";
                    const bgClass = isActive 
                        ? 'bg-primary/10 border-primary' 
                        : (isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-primary/50');
                    
                    return `
                        <div onclick="openLevel2(${h.id})" class="p-2 border cursor-pointer transition-colors text-[11px] font-medium text-on-surface flex flex-col justify-between h-16 ${bgClass}">
                            <div class="flex justify-between items-start">
                                <span class="truncate pr-1">${h.name}</span>
                                ${isPremium ? '<span class="material-symbols-outlined text-[12px] text-primary shrink-0">workspace_premium</span>' : ''}
                            </div>
                            <div class="text-[9px] text-on-surface-variant flex justify-between items-center mt-1">
                                <span>${h.distance} km from T2</span>
                                <span class="font-bold text-secondary">${h.rating} ★</span>
                            </div>
                        </div>
                    `;
                };

                if (premiumItems.length > 0) {
                    grid.innerHTML += `
                        <div class="col-span-full mt-2 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                            <h4 class="text-meta-label text-primary uppercase">PREMIUM RESTAURANTS</h4>
                            <span class="text-[10px] font-bold text-on-surface-variant">(${premiumItems.length})</span>
                        </div>
                    `;
                    premiumItems.forEach(h => {
                        grid.innerHTML += renderCard(h);
                    });
                }

                if (standardItems.length > 0) {
                    grid.innerHTML += `
                        <div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                            <h4 class="text-meta-label text-primary uppercase">STANDARD RESTAURANTS</h4>
                            <span class="text-[10px] font-bold text-on-surface-variant">(${standardItems.length})</span>
                        </div>
                    `;
                    standardItems.forEach(h => {
                        grid.innerHTML += renderCard(h);
                    });
                }
            } catch(e) {
                console.error("Error in renderItems:", e);
            }
        }
        window.renderItems = renderItems;
"""
            html = re.sub(r'function renderItems\(\) \{.*?(?=function openLevel2)', new_render, html, flags=re.DOTALL)
            html = html.replace('onchange="renderItems()"', 'onchange="window.renderItems()"')

        elif filepath == 'spa.html':
            new_render = """
        window.renderItems = function() {
            try {
                const grid = document.getElementById('hotel-grid');
                if (!grid) return;
                
                const typeEl = document.getElementById('filter-therapy');
                const priceEl = document.getElementById('filter-price');
                const distEl = document.getElementById('filter-distance');
                const featureEl = document.getElementById('filter-feature');
                
                const typeVal = typeEl ? typeEl.value : 'any';
                const priceVal = priceEl ? priceEl.value : 'any';
                const distVal = distEl ? distEl.value : 'any';
                const featureVal = featureEl ? featureEl.value : 'any';

                const filtered = items.filter(h => {
                    let match = true;
                    if (typeVal !== 'any' && match) {
                        if (h.type !== typeVal) match = false;
                    }
                    if (distVal !== 'any' && match) {
                        const maxD = parseFloat(distVal);
                        if (h.distance > maxD) match = false;
                    }
                    if (priceVal !== 'any' && match) {
                        if (priceVal === '5000+') {
                            if (h.price < 5000) match = false;
                        } else {
                            const parts = priceVal.split('-');
                            if (parts.length === 2) {
                                const min = parseInt(parts[0]);
                                const max = parseInt(parts[1]);
                                if (h.price < min || h.price > max) match = false;
                            }
                        }
                    }
                    if (featureVal !== 'any' && match) {
                        if (h.feature !== featureVal && !h.features.includes(featureVal)) match = false;
                    }
                    return match;
                });

                const countEl = document.getElementById('inventory-count');
                if (countEl) countEl.textContent = `WELLNESS INVENTORY (${filtered.length} SPAS FOUND)`;

                grid.innerHTML = '';
                
                const premiumItems = filtered.filter(h => h.category === "Premium");
                const standardItems = filtered.filter(h => h.category === "Standard");

                const renderCard = (h) => {
                    const isActive = h.id === activeItemId;
                    const isPremium = h.category === "Premium";
                    const bgClass = isActive 
                        ? 'bg-primary/10 border-primary' 
                        : (isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-primary/50');
                    
                    return `
                        <div onclick="openLevel2(${h.id})" class="p-2 border cursor-pointer transition-colors text-[11px] font-medium text-on-surface flex flex-col justify-between h-16 ${bgClass}">
                            <div class="flex justify-between items-start">
                                <span class="truncate pr-1">${h.name}</span>
                                ${isPremium ? '<span class="material-symbols-outlined text-[12px] text-primary shrink-0">workspace_premium</span>' : ''}
                            </div>
                            <div class="text-[9px] text-on-surface-variant flex justify-between items-center mt-1">
                                <span>${h.distance} km from T2</span>
                                <span class="font-bold text-secondary">${h.rating} ★</span>
                            </div>
                        </div>
                    `;
                };

                if (premiumItems.length > 0) {
                    grid.innerHTML += `
                        <div class="col-span-full mt-2 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                            <h4 class="text-meta-label text-primary uppercase">PREMIUM SPAS</h4>
                            <span class="text-[10px] font-bold text-on-surface-variant">(${premiumItems.length})</span>
                        </div>
                    `;
                    premiumItems.forEach(h => {
                        grid.innerHTML += renderCard(h);
                    });
                }

                if (standardItems.length > 0) {
                    grid.innerHTML += `
                        <div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                            <h4 class="text-meta-label text-primary uppercase">STANDARD SPAS</h4>
                            <span class="text-[10px] font-bold text-on-surface-variant">(${standardItems.length})</span>
                        </div>
                    `;
                    standardItems.forEach(h => {
                        grid.innerHTML += renderCard(h);
                    });
                }
            } catch(e) {
                console.error(e);
            }
        }
        window.renderItems = renderItems;
"""
            html = re.sub(r'function renderItems\(\) \{.*?(?=function openLevel2)', new_render, html, flags=re.DOTALL)
            html = html.replace('onchange="renderItems()"', 'onchange="window.renderItems()"')

        elif filepath == 'entertainment.html':
            new_render = """
    window.renderItems = function() {
        try {
            const grid = document.getElementById('hotel-grid');
            if (!grid) return;
            
            const filter1El = document.getElementById('filter-1');
            const filter2El = document.getElementById('filter-2');
            const filter3El = document.getElementById('filter-3');
            const filter4El = document.getElementById('filter-4');
            
            const filter1 = filter1El ? filter1El.value : 'any';
            const filter2 = filter2El ? filter2El.value : 'any';
            const filter3 = filter3El ? filter3El.value : 'any';
            const filter4 = filter4El ? filter4El.value : 'any';

            const filtered = items.filter(h => {
                let match = true;
                if (filter1 !== 'any' && h.type !== filter1) match = false;
                if (filter3 !== 'any' && h.distance > parseFloat(filter3)) match = false;
                if (filter4 !== 'any' && h.style !== filter4 && !h.features.join(' ').includes(filter4)) match = false;
                if (filter2 !== 'any') {
                    if (filter2 === '5000+' && h.price < 5000) match = false;
                    if (filter2 !== '5000+') {
                        const parts = filter2.split('-');
                        if (parts.length === 2) {
                            const min = parseInt(parts[0]);
                            const max = parseInt(parts[1]);
                            if (h.price < min || h.price > max) match = false;
                        }
                    }
                }
                return match;
            });

            const countEl = document.getElementById('inventory-count');
            if (countEl) countEl.textContent = `ENTERTAINMENT INVENTORY (${filtered.length} EXPERIENCES FOUND)`;

            grid.innerHTML = '';
            
            const premiumItems = filtered.filter(h => h.category === "Premium");
            const standardItems = filtered.filter(h => h.category === "Standard");

            const renderCard = (h) => {
                const isActive = h.id === activeItemId;
                const isPremium = h.category === "Premium";
                const bgClass = isActive 
                    ? 'bg-primary/10 border-primary' 
                    : (isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-primary/50');
                
                return `
                    <div onclick="openLevel2(${h.id})" class="p-2 border cursor-pointer transition-colors text-[11px] font-medium text-on-surface flex flex-col justify-between h-16 ${bgClass}">
                        <div class="flex justify-between items-start">
                            <span class="truncate pr-1">${h.name}</span>
                            ${isPremium ? '<span class="material-symbols-outlined text-[12px] text-primary shrink-0">workspace_premium</span>' : ''}
                        </div>
                        <div class="text-[9px] text-on-surface-variant flex justify-between items-center mt-1">
                            <span>${h.distance} km from T2</span>
                            <span class="font-bold text-secondary">${h.rating} ★</span>
                        </div>
                    </div>
                `;
            };

            if (premiumItems.length > 0) {
                grid.innerHTML += `
                    <div class="col-span-full mt-2 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                        <h4 class="text-meta-label text-primary uppercase">PREMIUM EXPERIENCES</h4>
                        <span class="text-[10px] font-bold text-on-surface-variant">(${premiumItems.length})</span>
                    </div>
                `;
                premiumItems.forEach(h => {
                    grid.innerHTML += renderCard(h);
                });
            }

            if (standardItems.length > 0) {
                grid.innerHTML += `
                    <div class="col-span-full mt-4 mb-1 border-b border-outline-variant/50 pb-1 flex justify-between items-end">
                        <h4 class="text-meta-label text-primary uppercase">STANDARD EXPERIENCES</h4>
                        <span class="text-[10px] font-bold text-on-surface-variant">(${standardItems.length})</span>
                    </div>
                `;
                standardItems.forEach(h => {
                    grid.innerHTML += renderCard(h);
                });
            }
        } catch (e) {
            console.error(e);
        }
    }
    window.renderItems = renderItems;
"""
            html = re.sub(r'function renderItems\(\) \{.*?(?=function openLevel2)', new_render, html, flags=re.DOTALL)
            html = html.replace('onchange="renderItems()"', 'onchange="window.renderItems()"')

        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    print("Fixed all filters logic.")

fix_all_filters()
