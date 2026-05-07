html_content = """<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>LayoverX | Hotel Booking</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
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
                        "surface-container-high": "#e5e5e5",
                        "surface-container-low": "#f3f3f3",
                        "outline-variant": "#cfc4c5",
                        "secondary": "#5d5f5f",
                        "brand-accent": "#5d3fd3"
                    },
                    "fontFamily": {
                        "sans": ["Inter", "sans-serif"],
                        "manrope": ["Manrope", "sans-serif"]
                    }
                }
            }
        }
    </script>
    <style>
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .layout-transition { transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
        .fade-in { animation: fadeIn 0.3s ease-in forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: translateX(0); } }
    </style>
</head>
<body class="bg-surface text-on-surface font-sans antialiased overflow-x-hidden min-h-screen flex flex-col">
    <!-- Navbar -->
    <header class="w-full bg-white border-b border-outline-variant/50 sticky top-0 z-50 shadow-sm">
        <div class="max-w-[1400px] mx-auto px-6 h-20 flex justify-between items-center">
            <div class="flex items-center gap-8">
                <a class="text-2xl font-black tracking-tighter text-primary font-manrope" href="#">LayoverX</a>
                <nav class="hidden md:flex gap-8 items-center">
                    <a class="text-primary font-semibold font-manrope text-sm border-b-2 border-primary pb-1" href="#">Browse</a>
                    <a class="text-secondary hover:text-primary transition-colors font-manrope text-sm font-medium" href="#">My Bookings</a>
                    <a class="text-secondary hover:text-primary transition-colors font-manrope text-sm font-medium" href="#">Support</a>
                </nav>
            </div>
            <div class="flex gap-4 items-center">
                <button class="p-2 text-secondary hover:text-primary hover:bg-surface-container rounded-full transition-colors"><span class="material-symbols-outlined">notifications</span></button>
                <button class="p-2 text-secondary hover:text-primary hover:bg-surface-container rounded-full transition-colors"><span class="material-symbols-outlined">account_circle</span></button>
            </div>
        </div>
    </header>

    <main class="flex-grow w-full max-w-[1400px] mx-auto p-4 sm:p-8 flex items-start gap-8 relative pb-20">
        
        <!-- LEVEL 1: LISTING -->
        <div id="level1" class="layout-transition w-full max-w-4xl mx-auto flex-shrink-0 z-10">
            <div class="flex justify-between items-end mb-8">
                <div>
                    <h1 id="level1-heading" class="text-3xl font-black text-primary tracking-tight font-manrope cursor-pointer hover:text-brand-accent transition-colors" onclick="closeLevel2()">HOTELS LISTING PAGE</h1>
                    <p class="text-secondary mt-2 font-medium">Curated luxury transit stays</p>
                </div>
            </div>

            <div class="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm mb-8">
                <p class="text-xs font-bold text-secondary uppercase tracking-widest mb-4">Search &amp; Filters</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                    <!-- Dropdowns -->
                    <div class="relative">
                        <select id="filter-duration" onchange="renderHotels()" class="w-full bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg text-sm font-medium appearance-none outline-none cursor-pointer">
                            <option value="any">Any Duration</option>
                            <option value="2">2 Hours</option>
                            <option value="4">4 Hours</option>
                            <option value="8">8 Hours</option>
                            <option value="12">12 Hours</option>
                            <option value="24">24 Hours</option>
                        </select>
                        <span class="material-symbols-outlined absolute right-3 top-3 pointer-events-none text-secondary">expand_more</span>
                    </div>
                    
                    <div class="relative">
                        <select id="filter-price" onchange="renderHotels()" class="w-full bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg text-sm font-medium appearance-none outline-none cursor-pointer">
                            <option value="any">Any Price</option>
                            <option value="0-3000">₹0 – ₹3000</option>
                            <option value="3000-6000">₹3000 – ₹6000</option>
                            <option value="6000-10000">₹6000 – ₹10000</option>
                            <option value="10000+">₹10000+</option>
                        </select>
                        <span class="material-symbols-outlined absolute right-3 top-3 pointer-events-none text-secondary">expand_more</span>
                    </div>

                    <div class="relative">
                        <select id="filter-distance" onchange="renderHotels()" class="w-full bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg text-sm font-medium appearance-none outline-none cursor-pointer">
                            <option value="any">Any Distance</option>
                            <option value="1">Within 1 km</option>
                            <option value="3">Within 3 km</option>
                            <option value="5">Within 5 km</option>
                        </select>
                        <span class="material-symbols-outlined absolute right-3 top-3 pointer-events-none text-secondary">expand_more</span>
                    </div>

                    <div class="relative">
                        <select id="filter-amenities" onchange="renderHotels()" class="w-full bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg text-sm font-medium appearance-none outline-none cursor-pointer">
                            <option value="any">Any Amenity</option>
                            <option value="Airport Shuttle">Airport Shuttle</option>
                            <option value="Pool">Pool</option>
                            <option value="Spa">Spa</option>
                            <option value="Business Center">Business Center</option>
                        </select>
                        <span class="material-symbols-outlined absolute right-3 top-3 pointer-events-none text-secondary">expand_more</span>
                    </div>
                </div>
            </div>

            <div>
                <p id="inventory-count" class="text-xs font-bold text-primary uppercase tracking-widest mb-4 pb-2 border-b border-outline-variant/50">HOTEL INVENTORY (12 HOTELS FOUND)</p>
                <div id="hotel-grid" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Dynamic Hotels -->
                </div>
            </div>
        </div>

        <!-- LEVEL 2: DETAIL -->
        <div id="level2" class="layout-transition hidden opacity-0 w-full lg:w-[45%] flex-shrink-0 z-20">
            <div class="bg-white border border-outline-variant p-0 rounded-2xl shadow-xl flex flex-col h-full max-h-[85vh] sticky top-28 overflow-hidden">
                <div class="flex justify-between items-center p-5 bg-surface-container-low border-b border-outline-variant">
                    <h3 class="text-sm font-black text-primary tracking-wider font-manrope">HOTEL DETAIL PAGE</h3>
                    <button onclick="closeLevel2()" class="w-8 h-8 flex justify-center items-center rounded-full hover:bg-surface-container text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[20px]">close</span>
                    </button>
                </div>
                
                <div class="p-6 overflow-y-auto hide-scrollbar flex-grow bg-surface">
                    <div id="l2-header" class="mb-6">
                        <h2 id="l2-name" class="text-2xl font-black text-primary mb-2 font-manrope">Hotel Name</h2>
                        <div class="flex flex-wrap items-center gap-2">
                            <span id="l2-rating" class="bg-orange-100 text-orange-800 text-xs font-bold px-2 py-1 rounded">4.8 ★</span>
                            <span class="text-secondary text-sm">•</span>
                            <span id="l2-distance" class="text-secondary text-sm font-medium">0.9 km from T2</span>
                        </div>
                    </div>
                    
                    <div class="bg-white border border-outline-variant/50 rounded-xl p-5 shadow-sm mb-6">
                        <p class="text-xs font-bold text-secondary uppercase tracking-widest mb-3">Amenities Included</p>
                        <div id="l2-amenities" class="flex flex-wrap gap-2">
                            <!-- amenities -->
                        </div>
                    </div>

                    <button onclick="openVerificationModal()" class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-4 rounded-xl text-sm tracking-widest uppercase flex justify-center items-center gap-2 transition-all duration-300 shadow-md hover:shadow-lg active:scale-[0.98]">
                        PLAN LAYOVER
                        <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
                    </button>
                </div>
            </div>
        </div>

    </main>

    <!-- VERIFICATION MODAL -->
    <div id="verification-modal" class="fixed inset-0 bg-primary/80 backdrop-blur-sm z-[100] hidden flex justify-center items-center opacity-0 transition-opacity duration-300 p-4">
        <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden transform scale-95 transition-transform duration-300" id="modal-content">
            <div class="p-6 border-b border-outline-variant/50 flex justify-between items-center bg-surface-container-low">
                <h3 class="text-lg font-black text-primary font-manrope">Layover Verification</h3>
                <button onclick="closeVerificationModal()" class="text-secondary hover:text-primary transition-colors p-1 rounded hover:bg-surface-container"><span class="material-symbols-outlined">close</span></button>
            </div>
            <div class="p-6 space-y-5">
                <p class="text-sm text-secondary font-medium mb-2">Please verify your details to continue booking this layover experience.</p>
                
                <div>
                    <label class="block text-xs font-bold text-secondary uppercase tracking-widest mb-2">Full Name</label>
                    <input type="text" class="w-full bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg text-sm font-medium outline-none transition-colors" placeholder="John Doe">
                </div>
                <div>
                    <label class="block text-xs font-bold text-secondary uppercase tracking-widest mb-2">Flight Number</label>
                    <input type="text" class="w-full bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg text-sm font-medium outline-none transition-colors" placeholder="e.g. AI 802">
                </div>
                <div>
                    <label class="block text-xs font-bold text-secondary uppercase tracking-widest mb-2">Mobile Number</label>
                    <input type="tel" class="w-full bg-surface-container border border-outline-variant focus:border-primary px-4 py-3 rounded-lg text-sm font-medium outline-none transition-colors" placeholder="+91 98765 43210">
                </div>

                <button onclick="submitVerification(event)" class="w-full mt-4 bg-primary hover:bg-primary/90 text-white font-bold py-4 rounded-xl text-sm tracking-widest uppercase transition-all duration-300 shadow-md flex justify-center items-center gap-2">
                    Verify &amp; Continue
                </button>
            </div>
        </div>
    </div>

    <script>
        const hotels = [
            { id: 1, name: "The Orchid Hotel", distance: 0.9, terminal: "T2", category: "Premium", rating: "4.8", price: 4500, durations: [2, 4, 8, 12, 24], amenities: ["Airport Shuttle", "Pool", "Spa"] },
            { id: 2, name: "Hotel Sahara Star", distance: 1.1, terminal: "T2", category: "Premium", rating: "4.7", price: 5200, durations: [4, 8, 12, 24], amenities: ["Pool", "Spa"] },
            { id: 3, name: "Taj Santacruz", distance: 1.6, terminal: "T2", category: "Premium", rating: "4.9", price: 8200, durations: [8, 12, 24], amenities: ["Airport Shuttle", "Spa", "Business Center"] },
            { id: 4, name: "Hotel Bawa International", distance: 1.7, terminal: "T2", category: "Standard", rating: "4.2", price: 2800, durations: [2, 4, 8, 12], amenities: ["Business Center"] },
            { id: 5, name: "JW Marriott Mumbai Sahar", distance: 1.8, terminal: "T2", category: "Premium", rating: "4.8", price: 7800, durations: [4, 8, 12, 24], amenities: ["Pool", "Spa", "Business Center"] },
            { id: 6, name: "Hotel Midland", distance: 2.3, terminal: "T2", category: "Standard", rating: "4.0", price: 2500, durations: [2, 4, 8, 12], amenities: [] },
            { id: 7, name: "ITC Maratha", distance: 2.4, terminal: "T2", category: "Premium", rating: "4.8", price: 7600, durations: [8, 12, 24], amenities: ["Pool", "Spa", "Business Center"] },
            { id: 8, name: "The Leela Mumbai", distance: 2.5, terminal: "T2", category: "Premium", rating: "4.7", price: 7200, durations: [4, 8, 12, 24], amenities: ["Pool", "Airport Shuttle", "Business Center"] },
            { id: 9, name: "Aurika Mumbai Airport", distance: 2.8, terminal: "T2", category: "Premium", rating: "4.6", price: 6200, durations: [4, 8, 12, 24], amenities: ["Pool", "Business Center"] },
            { id: 10, name: "Lemon Tree Premier", distance: 3.2, terminal: "T2", category: "Standard", rating: "4.2", price: 3800, durations: [2, 4, 8, 12], amenities: ["Airport Shuttle"] },
            { id: 11, name: "Holiday Inn Mumbai Airport", distance: 4.2, terminal: "T2", category: "Standard", rating: "4.4", price: 4200, durations: [4, 8, 12, 24], amenities: ["Pool", "Business Center"] },
            { id: 12, name: "Grand Hyatt Mumbai", distance: 6.1, terminal: "T2", category: "Premium", rating: "4.7", price: 7000, durations: [8, 12, 24], amenities: ["Pool", "Spa", "Business Center"] }
        ];

        let activeHotelId = null;

        function renderHotels() {
            const grid = document.getElementById('hotel-grid');
            
            const durVal = document.getElementById('filter-duration').value;
            const priceVal = document.getElementById('filter-price').value;
            const distVal = document.getElementById('filter-distance').value;
            const amenVal = document.getElementById('filter-amenities').value;

            const filtered = hotels.filter(h => {
                let match = true;
                
                // Duration Filter
                if (durVal !== 'any' && match) {
                    if (!h.durations.includes(parseInt(durVal))) match = false;
                }

                // Distance Filter
                if (distVal !== 'any' && match) {
                    const maxD = parseFloat(distVal);
                    if (h.distance > maxD) match = false;
                }

                // Price Filter
                if (priceVal !== 'any' && match) {
                    if (priceVal === '10000+') {
                        if (h.price < 10000) match = false;
                    } else {
                        const [min, max] = priceVal.split('-').map(Number);
                        if (h.price < min || h.price > max) match = false;
                    }
                }

                // Amenities Filter
                if (amenVal !== 'any' && match) {
                    if (!h.amenities.includes(amenVal)) match = false;
                }

                return match;
            });

            document.getElementById('inventory-count').textContent = `HOTEL INVENTORY (${filtered.length} HOTELS FOUND)`;

            grid.innerHTML = '';
            filtered.forEach(h => {
                const isActive = h.id === activeHotelId;
                const activeClasses = isActive ? 'border-primary ring-1 ring-primary shadow-md bg-surface-container-low' : 'border-outline-variant hover:border-primary/50 hover:shadow-sm bg-white';
                const premiumBadge = h.category === "Premium" ? `<span class="material-symbols-outlined text-[14px] text-brand-accent" title="Premium">workspace_premium</span>` : '';

                grid.innerHTML += `
                    <div onclick="openLevel2(${h.id})" class="p-5 border rounded-2xl flex flex-col gap-3 transition-all duration-300 cursor-pointer ${activeClasses}">
                        <div class="flex justify-between items-start gap-2">
                            <div>
                                <div class="font-bold text-base text-primary leading-tight flex items-center gap-1">${h.name} ${premiumBadge}</div>
                                <div class="text-[10px] font-bold text-secondary mt-1 uppercase tracking-widest">${h.category}</div>
                            </div>
                            <div class="flex items-center gap-1 bg-orange-50 px-2 py-1 rounded">
                                <span class="material-symbols-outlined text-[12px] text-orange-600" style="font-variation-settings: 'FILL' 1">star</span>
                                <span class="text-xs font-bold text-orange-900">${h.rating}</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-2 mt-auto pt-2 border-t border-outline-variant/30">
                            <span class="text-[11px] bg-white border border-outline-variant/50 px-2 py-1 rounded-md font-medium text-secondary flex items-center gap-1 shadow-sm">
                                <span class="material-symbols-outlined text-[14px]">distance</span>
                                ${h.distance} km from ${h.terminal}
                            </span>
                        </div>
                    </div>
                `;
            });
        }

        function openLevel2(id) {
            activeHotelId = id;
            renderHotels(); 
            
            const hotel = hotels.find(h => h.id === id);
            if(!hotel) return;

            // Populate L2
            document.getElementById('l2-name').textContent = hotel.name;
            document.getElementById('l2-rating').textContent = `${hotel.rating} ★`;
            document.getElementById('l2-distance').textContent = `${hotel.distance} km from ${hotel.terminal}`;
            
            const amCont = document.getElementById('l2-amenities');
            amCont.innerHTML = hotel.amenities.length 
                ? hotel.amenities.map(a => `<span class="bg-white border border-outline-variant/50 text-secondary text-xs px-2 py-1.5 rounded-lg font-medium flex items-center gap-1 shadow-sm"><span class="material-symbols-outlined text-[14px] text-green-600">check_circle</span> ${a}</span>`).join('') 
                : '<span class="text-xs text-secondary italic">Standard amenities included</span>';

            // Layout Animation
            const l1 = document.getElementById('level1');
            const l2 = document.getElementById('level2');
            
            l1.classList.remove('max-w-4xl', 'mx-auto');
            l1.classList.add('lg:w-[55%]');
            
            l2.classList.remove('hidden');
            
            requestAnimationFrame(() => {
                l2.classList.remove('opacity-0');
            });
        }

        function closeLevel2() {
            activeHotelId = null;
            renderHotels();
            
            const l1 = document.getElementById('level1');
            const l2 = document.getElementById('level2');
            
            l2.classList.add('opacity-0');
            setTimeout(() => {
                l2.classList.add('hidden');
                l1.classList.remove('lg:w-[55%]');
                l1.classList.add('max-w-4xl', 'mx-auto');
            }, 300);
        }

        function openVerificationModal() {
            const modal = document.getElementById('verification-modal');
            const content = document.getElementById('modal-content');
            
            modal.classList.remove('hidden');
            void modal.offsetWidth; // force reflow
            
            modal.classList.remove('opacity-0');
            content.classList.remove('scale-95');
            content.classList.add('scale-100');
        }

        function closeVerificationModal() {
            const modal = document.getElementById('verification-modal');
            const content = document.getElementById('modal-content');
            
            modal.classList.add('opacity-0');
            content.classList.remove('scale-100');
            content.classList.add('scale-95');
            
            setTimeout(() => {
                modal.classList.add('hidden');
            }, 300);
        }

        function submitVerification(event) {
            const btn = event.currentTarget;
            const original = btn.innerHTML;
            btn.innerHTML = '<span class="material-symbols-outlined animate-spin text-[18px]">refresh</span> Verifying...';
            btn.style.pointerEvents = 'none';
            btn.classList.add('opacity-90');
            
            setTimeout(() => {
                closeVerificationModal();
                btn.innerHTML = original;
                btn.style.pointerEvents = 'auto';
                btn.classList.remove('opacity-90');
                
                // Show success flow or redirect
                setTimeout(() => {
                    alert("Verification complete. Redirecting to booking confirmation.");
                }, 400);
            }, 1500);
        }

        document.addEventListener('DOMContentLoaded', renderHotels);
    </script>
</body>
</html>
"""

with open("c:/Users/Dev Tinker/Desktop/layoverX_dummy/hotel.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Updated hotel.html")
