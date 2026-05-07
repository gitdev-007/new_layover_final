import re

with open('hotel.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the SEARCH & FILTERS block
search_filters_replacement = """<div class="border border-outline-variant p-3 bg-surface rounded-lg mb-4">
<p class="text-meta-label text-outline mb-2">SEARCH &amp; FILTERS</p>
<div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-node-description">
<input class="bg-surface-container-high px-3 py-2 rounded border-0 text-node-description w-full focus:ring-1 focus:ring-primary outline-none transition-all" id="search-keyword" placeholder="Search name, location, keyword..." type="text" oninput="renderHotels()"/>
<input class="bg-surface-container-high px-3 py-2 rounded border-0 text-node-description w-full focus:ring-1 focus:ring-primary outline-none transition-all" id="filter-distance" placeholder="Max distance (km)" type="number" step="0.1" oninput="renderHotels()"/>
<select class="bg-surface-container-high px-3 py-2 rounded border-0 text-node-description w-full focus:ring-1 focus:ring-primary outline-none transition-all cursor-pointer" id="sort-distance" onchange="renderHotels()">
<option value="asc">Sort: Nearest First</option>
<option value="desc">Sort: Furthest First</option>
</select>
</div>
</div>"""

html = re.sub(r'<div class="border border-outline-variant p-3">.*?<p class="text-meta-label text-outline mb-1">SEARCH &amp; FILTERS</p>.*?</div>\s*</div>', search_filters_replacement, html, flags=re.DOTALL)

# 2. Replace the Grid Preview block
grid_preview_replacement = """<!-- Grid Preview -->
<div class="border-2 border-dashed border-outline-variant p-3 rounded-lg bg-surface-container-lowest">
<p class="text-meta-label text-outline mb-3" id="inventory-count">HOTEL INVENTORY (0 HOTELS FOUND)</p>
<div class="rounded-lg">
<div class="grid grid-cols-1 md:grid-cols-2 gap-3" id="hotel-grid">
<!-- Hotels injected dynamically -->
</div>
</div>
</div>"""

html = re.sub(r'<!-- Grid Preview -->.*?<div class="border-2 border-dashed border-outline-variant p-3">.*?HOTEL INVENTORY.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', grid_preview_replacement, html, flags=re.DOTALL)

# 3. Replace the JS block
js_replacement = """<script>
    const hotels = [
      { id: 1, name: "The Orchid Hotel", distance: 0.9, distanceLabel: "0.9 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" },
      { id: 2, name: "Hotel Sahara Star", distance: 1.1, distanceLabel: "1.1 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" },
      { id: 3, name: "Taj Santacruz", distance: 1.6, distanceLabel: "1.6 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" },
      { id: 4, name: "Hotel Bawa International", distance: 1.7, distanceLabel: "1.7 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Standard" },
      { id: 5, name: "JW Marriott Mumbai Sahar", distance: 1.8, distanceLabel: "1.8 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" },
      { id: 6, name: "Hotel Midland", distance: 2.3, distanceLabel: "2.3 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Standard" },
      { id: 7, name: "ITC Maratha", distance: 2.4, distanceLabel: "2.4 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" },
      { id: 8, name: "The Leela Mumbai", distance: 2.5, distanceLabel: "2.5 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" },
      { id: 9, name: "Aurika Mumbai Airport", distance: 2.8, distanceLabel: "2.8 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" },
      { id: 10, name: "Lemon Tree Premier", distance: 3.2, distanceLabel: "3.2 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Standard" },
      { id: 11, name: "Holiday Inn Mumbai Airport", distance: 4.2, distanceLabel: "4.2 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Standard" },
      { id: 12, name: "Grand Hyatt Mumbai", distance: 6.1, distanceLabel: "6.1 km from T2 Terminal", terminal: "T2", city: "Mumbai", airport: "Chhatrapati Shivaji Maharaj International Airport", category: "Premium" }
    ];

    function renderHotels() {
        const grid = document.getElementById('hotel-grid');
        const countLabel = document.getElementById('inventory-count');
        
        const searchVal = (document.getElementById('search-keyword')?.value || '').toLowerCase();
        const maxDistVal = parseFloat(document.getElementById('filter-distance')?.value) || Infinity;
        const sortVal = document.getElementById('sort-distance')?.value || 'asc';
        
        // Filter
        let filtered = hotels.filter(h => {
            const matchesSearch = h.name.toLowerCase().includes(searchVal) || 
                                  h.distanceLabel.toLowerCase().includes(searchVal) || 
                                  h.city.toLowerCase().includes(searchVal) || 
                                  h.airport.toLowerCase().includes(searchVal) ||
                                  h.distance.toString().includes(searchVal);
            const matchesDist = h.distance <= maxDistVal;
            return matchesSearch && matchesDist;
        });
        
        // Sort
        filtered.sort((a, b) => sortVal === 'asc' ? a.distance - b.distance : b.distance - a.distance);
        
        // Render
        grid.innerHTML = '';
        filtered.forEach(h => {
            const isPremium = h.category === 'Premium';
            const bgClass = isPremium ? 'bg-primary/5 border-primary/20 hover:border-primary/50' : 'bg-surface border-outline-variant hover:border-outline';
            const iconColor = isPremium ? 'text-primary' : 'text-secondary';
            
            grid.innerHTML += `
                <div class="hotel-item p-3 border rounded-xl flex flex-col gap-2 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-md cursor-pointer ${bgClass}" 
                     data-name="${h.name}" data-distance="${h.distance}" data-category="${h.category}" data-terminal="${h.terminal}">
                    <div class="flex justify-between items-start gap-2">
                        <div class="font-bold text-xs sm:text-sm text-on-surface leading-tight">${h.name}</div>
                        ${isPremium ? '<span class="material-symbols-outlined text-[14px] text-primary" title="Premium">workspace_premium</span>' : ''}
                    </div>
                    <div class="text-[10px] sm:text-[11px] bg-white border border-outline-variant/50 px-2 py-1 rounded-md w-fit font-medium text-secondary flex items-center gap-1 shadow-sm">
                        <span class="material-symbols-outlined text-[12px] ${iconColor}">distance</span>
                        ${h.distanceLabel}
                    </div>
                </div>
            `;
        });
        
        countLabel.textContent = `HOTEL INVENTORY (${filtered.length} HOTELS FOUND)`;
    }

    // Initialize on load
    document.addEventListener('DOMContentLoaded', renderHotels);
</script>"""

# Using regex to replace everything from <script> to the end of the file except the closing </body></html>
html = re.sub(r'<script>.*?</script>\s*(?=</body>|</html>)', js_replacement, html, flags=re.DOTALL)

with open('hotel.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated hotel.html successfully")
