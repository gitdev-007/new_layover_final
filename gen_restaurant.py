import codecs
import re

def generate_restaurant():
    with codecs.open('hotel.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Change title and header
    html = html.replace('Hotel Booking Sitemap', 'Restaurant Discovery')
    html = html.replace('Hotels Listing Page', 'Restaurants Listing Page')
    html = html.replace('Hotel Detail Page', 'Restaurant Detail Page')
    html = html.replace('HOTEL INVENTORY', 'FOOD & DINING INVENTORY')
    html = html.replace('HOTELS FOUND', 'RESTAURANTS FOUND')
    html = html.replace('Premium Hotels', 'PREMIUM RESTAURANTS')
    html = html.replace('Standard Hotels', 'STANDARD RESTAURANTS')
    
    # Replace search and filters block
    filters_html = """
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                            <select id="filter-cuisine" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Cuisine Type</option>
                                <option value="Indian">Indian</option>
                                <option value="Continental">Continental</option>
                                <option value="Asian">Asian</option>
                                <option value="Italian">Italian</option>
                                <option value="Cafe">Cafe</option>
                            </select>
                            
                            <select id="filter-price" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Price Range</option>
                                <option value="0-1000">0 - 1000</option>
                                <option value="1000-3000">1000 - 3000</option>
                                <option value="3000+">3000+</option>
                            </select>

                            <select id="filter-distance" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Distance</option>
                                <option value="1">Within 1 km</option>
                                <option value="3">Within 3 km</option>
                                <option value="5">Within 5 km</option>
                                <option value="10">Within 10 km</option>
                            </select>

                            <select id="filter-style" onchange="renderItems()" class="bg-white border border-outline-variant px-2 py-1 text-[11px] text-on-surface font-medium outline-none rounded-none cursor-pointer">
                                <option value="any">Dining Style</option>
                                <option value="Fine Dining">Fine Dining</option>
                                <option value="Casual Dining">Casual Dining</option>
                                <option value="Lounge">Lounge</option>
                                <option value="Rooftop">Rooftop</option>
                                <option value="Cafe">Cafe</option>
                            </select>
                        </div>"""
    html = re.sub(r'<div class="grid grid-cols-2 md:grid-cols-4 gap-2">.*?</div>', filters_html, html, flags=re.DOTALL)
    
    # Replace dataset and JS logic
    dataset_js = """
        const items = [
            { id: 1, name: "Masala Kraft", distance: 4.2, category: "Premium", rating: "4.8", price: 3500, type: "Indian", style: "Fine Dining", features: ["Fine Dining", "Authentic Spices", "Indoor Seating"] },
            { id: 2, name: "Peshawri", distance: 3.9, category: "Premium", rating: "4.9", price: 4000, type: "Indian", style: "Fine Dining", features: ["Fine Dining", "Tandoori", "Indoor Seating"] },
            { id: 3, name: "Dum Pukht", distance: 5.1, category: "Premium", rating: "4.9", price: 4500, type: "Indian", style: "Fine Dining", features: ["Fine Dining", "Royal Awadhi", "Indoor Seating"] },
            { id: 4, name: "Aer Lounge", distance: 6.0, category: "Premium", rating: "4.7", price: 3200, type: "Continental", style: "Rooftop", features: ["Rooftop Seating", "City Views", "Outdoor Seating"] },
            { id: 5, name: "Fifty Five East", distance: 2.8, category: "Premium", rating: "4.6", price: 3000, type: "Asian", style: "Lounge", features: ["Business Dining", "Global Cuisine", "Mixed Seating"] },
            { id: 6, name: "Celini", distance: 3.4, category: "Premium", rating: "4.7", price: 3500, type: "Italian", style: "Fine Dining", features: ["Fine Dining", "Wood-fired Pizza", "Indoor Seating"] },
            { id: 7, name: "Lotus Cafe", distance: 4.7, category: "Premium", rating: "4.6", price: 2500, type: "Continental", style: "Cafe", features: ["Business Dining", "Buffet", "Indoor Seating"] },
            { id: 8, name: "Citrus", distance: 2.5, category: "Premium", rating: "4.5", price: 2800, type: "Continental", style: "Fine Dining", features: ["Fine Dining", "Fresh Juices", "Indoor Seating"] },
            { id: 9, name: "Cafe Coffee Day", distance: 0.8, category: "Standard", rating: "4.1", price: 500, type: "Cafe", style: "Cafe", features: ["Late Night Dining", "Quick Bites", "Indoor Seating"] },
            { id: 10, name: "Boulevard", distance: 1.9, category: "Standard", rating: "4.0", price: 1800, type: "Continental", style: "Casual Dining", features: ["Vegetarian Options", "Buffet", "Mixed Seating"] },
            { id: 11, name: "Hotel Midland Restaurant", distance: 2.3, category: "Standard", rating: "3.9", price: 800, type: "Indian", style: "Casual Dining", features: ["Vegetarian Options", "Thali", "Indoor Seating"] },
            { id: 12, name: "Bawa Cafe", distance: 1.7, category: "Standard", rating: "4.2", price: 900, type: "Cafe", style: "Cafe", features: ["Late Night Dining", "Parsi Snacks", "Indoor Seating"] }
        ];

        let activeItemId = null;

        function renderItems() {
            const grid = document.getElementById('hotel-grid');
            
            const cuisineVal = document.getElementById('filter-cuisine').value;
            const priceVal = document.getElementById('filter-price').value;
            const distVal = document.getElementById('filter-distance').value;
            const styleVal = document.getElementById('filter-style').value;

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
                        const [min, max] = priceVal.split('-').map(Number);
                        if (h.price < min || h.price > max) match = false;
                    }
                }
                if (styleVal !== 'any' && match) {
                    if (h.style !== styleVal) match = false;
                }
                return match;
            });

            document.getElementById('inventory-count').textContent = `FOOD & DINING INVENTORY (${filtered.length} RESTAURANTS FOUND)`;

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
    
    # Change "Room Options" to "Dining Options"
    html = html.replace('Room Options', 'Dining Options')
    html = html.replace('bed', 'restaurant_menu')

    # Remove ADD TO LIST from HTML block to match standard
    html = re.sub(
        r'<button id="add-list-btn" class="(.*?)">\s*ADD TO LIST\s*</button>',
        r'<button id="add-list-btn" class="\1">\n                            PLAN LAYOVER\n                        </button>',
        html
    )

    # Make sure onclick closeLevel2() is updated correctly if needed
    
    # Write to restaurant.html
    with codecs.open('restaurant.html', 'w', encoding='utf-8') as f:
        f.write(html)

generate_restaurant()
