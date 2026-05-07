import codecs
import re

def generate_spa():
    with codecs.open('hotel.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Change title and header
    html = html.replace('Hotel Booking Sitemap', 'Spa & Wellness Discovery')
    html = html.replace('Hotels Listing Page', 'Spa & Wellness Listing Page')
    html = html.replace('Hotel Detail Page', 'Spa Detail Page')
    html = html.replace('HOTEL INVENTORY', 'SPA & WELLNESS INVENTORY')
    html = html.replace('HOTELS FOUND', 'SPAS FOUND')
    html = html.replace('Premium Hotels', 'PREMIUM SPAS')
    html = html.replace('Standard Hotels', 'STANDARD SPAS')
    
    # Replace search and filters block
    filters_html = """
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                            <select id="filter-therapy" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Therapy Type</option>
                                <option value="Ayurvedic">Ayurvedic</option>
                                <option value="Swedish">Swedish</option>
                                <option value="Aromatherapy">Aromatherapy</option>
                                <option value="Express">Express</option>
                            </select>
                            
                            <select id="filter-price" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Price Range</option>
                                <option value="0-2000">0 - 2000</option>
                                <option value="2000-5000">2000 - 5000</option>
                                <option value="5000+">5000+</option>
                            </select>

                            <select id="filter-distance" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Distance</option>
                                <option value="2">Within 2 km</option>
                                <option value="4">Within 4 km</option>
                                <option value="6">Within 6 km</option>
                            </select>

                            <select id="filter-feature" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Wellness Features</option>
                                <option value="Steam & Sauna">Steam & Sauna</option>
                                <option value="Couple Therapy">Couple Therapy</option>
                                <option value="Wellness Lounge">Wellness Lounge</option>
                            </select>
                        </div>"""
    html = re.sub(r'<div class="grid grid-cols-2 md:grid-cols-4 gap-2">.*?</div>', filters_html, html, flags=re.DOTALL)
    
    # Replace dataset and JS logic
    dataset_js = """
        const items = [
            { id: 1, name: "Jiva Spa", distance: 3.1, category: "Premium", rating: "4.9", price: 6500, type: "Ayurvedic", feature: "Couple Therapy", features: ["Ayurvedic Therapy", "Couple Therapy", "Steam & Sauna"] },
            { id: 2, name: "Quan Spa", distance: 2.7, category: "Premium", rating: "4.8", price: 5500, type: "Swedish", feature: "Steam & Sauna", features: ["Steam & Sauna", "Express Relaxation Sessions", "Wellness Lounge"] },
            { id: 3, name: "Kaya Kalp Spa", distance: 5.4, category: "Premium", rating: "4.9", price: 7000, type: "Ayurvedic", feature: "Steam & Sauna", features: ["Ayurvedic Therapy", "Steam & Sauna", "Couple Therapy"] },
            { id: 4, name: "The Leela Spa", distance: 2.5, category: "Premium", rating: "4.7", price: 5800, type: "Aromatherapy", feature: "Wellness Lounge", features: ["Aromatherapy", "Airport Shuttle Nearby", "Wellness Lounge"] },
            { id: 5, name: "Soma Spa", distance: 4.2, category: "Premium", rating: "4.6", price: 4500, type: "Swedish", feature: "Steam & Sauna", features: ["Swedish Therapy", "Steam & Sauna", "Express Relaxation Sessions"] },
            { id: 6, name: "Lemon Tree Wellness Spa", distance: 3.2, category: "Standard", rating: "4.2", price: 2500, type: "Express", feature: "Wellness Lounge", features: ["Express Relaxation Sessions", "Wellness Lounge"] },
            { id: 7, name: "Holiday Inn Wellness", distance: 4.1, category: "Standard", rating: "4.3", price: 3000, type: "Swedish", feature: "Steam & Sauna", features: ["Swedish Therapy", "Steam & Sauna", "Airport Shuttle Nearby"] },
            { id: 8, name: "Midland Relaxation Spa", distance: 2.3, category: "Standard", rating: "4.0", price: 1800, type: "Express", feature: "Wellness Lounge", features: ["Express Relaxation Sessions", "Ayurvedic Therapy"] }
        ];

        let activeItemId = null;

        function renderItems() {
            const grid = document.getElementById('hotel-grid');
            
            const typeVal = document.getElementById('filter-therapy').value;
            const priceVal = document.getElementById('filter-price').value;
            const distVal = document.getElementById('filter-distance').value;
            const featureVal = document.getElementById('filter-feature').value;

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
                        const [min, max] = priceVal.split('-').map(Number);
                        if (h.price < min || h.price > max) match = false;
                    }
                }
                if (featureVal !== 'any' && match) {
                    if (!h.features.includes(featureVal)) match = false;
                }
                return match;
            });

            document.getElementById('inventory-count').textContent = `SPA & WELLNESS INVENTORY (${filtered.length} SPAS FOUND)`;

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
        }

        function openLevel2(id) {
            activeItemId = id;
            renderItems(); 
            
            const item = items.find(h => h.id === id);
            if(!item) return;

            document.getElementById('l2-name').textContent = item.name;
            document.getElementById('l2-rating').textContent = `${item.rating} ★`;
            document.getElementById('l2-distance').textContent = `${item.distance} km from T2`;
            
            const amCont = document.getElementById('l2-amenities');
            amCont.innerHTML = item.features.length 
                ? item.features.map(a => `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${a}</div>`).join('') 
                : '<div class="text-[11px] text-on-surface-variant italic">Standard options included</div>';

            const l1 = document.getElementById('level1');
            const l2 = document.getElementById('level2');
            
            const btn = document.getElementById('add-list-btn');
            if (btn) {
                // Reset styling
                if (btn.dataset.originalClasses) {
                    btn.className = btn.dataset.originalClasses;
                    btn.innerHTML = btn.dataset.originalHtml;
                }
                
                btn.innerHTML = 'PLAN LAYOVER';
                btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
                btn.onclick = function() {
                    window.location.href = 'QR_Upload_State.html';
                };
            }
            
            l2.classList.remove('hidden');
    
            requestAnimationFrame(() => { 
                l2.classList.remove('opacity-0'); 
                setTimeout(() => {
                    l2.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 100);
            });
        }

        function closeLevel2() {
            activeItemId = null;
            renderItems();
            
            const l1 = document.getElementById('level1');
            const l2 = document.getElementById('level2');
            
            l2.classList.add('opacity-0');
            setTimeout(() => {
                l2.classList.add('hidden');
            }, 300);
        }

        document.addEventListener('DOMContentLoaded', renderItems);"""
    
    # Find the script tag and replace it entirely
    html = re.sub(r'const hotels = \[.*?</script>', dataset_js + '\n    </script>', html, flags=re.DOTALL)
    
    # Change "Room Options" to "Wellness Options"
    html = html.replace('Room Options', 'Wellness Options')
    html = html.replace('bed', 'self_care')

    # Remove ADD TO LIST dynamic marketplace logic and hardcode to PLAN LAYOVER since instructions say:
    # "Do NOT: use ADD TO LIST, use marketplace planner logic"
    html = re.sub(
        r'<button id="add-list-btn" class="(.*?)">\s*ADD TO LIST\s*</button>',
        r'<button id="add-list-btn" class="\1">\n                            PLAN LAYOVER\n                        </button>',
        html
    )
    
    # Write to spas.html
    with codecs.open('spas.html', 'w', encoding='utf-8') as f:
        f.write(html)

generate_spa()
