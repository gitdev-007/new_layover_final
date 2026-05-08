import codecs
import re

def fix_hotel_durations_data():
    filepath = 'hotel.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_hotels_data = """const hotels = [
            { id: 1, name: "The Orchid Hotel", distance: 0.9, terminal: "T2", category: "Premium", rating: "4.8", price: 4500, durations: [3, 4, 6, 8, 10, 12, 16, 24], amenities: ["Airport Shuttle", "Pool", "Spa"] },
            { id: 2, name: "Hotel Sahara Star", distance: 1.1, terminal: "T2", category: "Premium", rating: "4.7", price: 5200, durations: [3, 4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Spa"] },
            { id: 3, name: "Taj Santacruz", distance: 1.6, terminal: "T2", category: "Premium", rating: "4.9", price: 8200, durations: [6, 8, 10, 12, 16, 24], amenities: ["Airport Shuttle", "Spa", "Business Center"] },
            { id: 4, name: "Hotel Bawa Intl.", distance: 1.7, terminal: "T2", category: "Standard", rating: "4.2", price: 2800, durations: [3, 4, 6, 8, 10, 12], amenities: ["Business Center"] },
            { id: 5, name: "JW Marriott Sahar", distance: 1.8, terminal: "T2", category: "Premium", rating: "4.8", price: 7800, durations: [4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Spa", "Business Center"] },
            { id: 6, name: "Hotel Midland", distance: 2.3, terminal: "T2", category: "Standard", rating: "4.0", price: 2500, durations: [3, 4, 6, 8, 10, 12], amenities: [] },
            { id: 7, name: "ITC Maratha", distance: 2.4, terminal: "T2", category: "Premium", rating: "4.8", price: 7600, durations: [8, 10, 12, 16, 24], amenities: ["Pool", "Spa", "Business Center"] },
            { id: 8, name: "The Leela Mumbai", distance: 2.5, terminal: "T2", category: "Premium", rating: "4.7", price: 7200, durations: [6, 8, 10, 12, 16, 24], amenities: ["Pool", "Airport Shuttle", "Business Center"] },
            { id: 9, name: "Aurika Mumbai", distance: 2.8, terminal: "T2", category: "Premium", rating: "4.6", price: 6200, durations: [4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Business Center"] },
            { id: 10, name: "Lemon Tree Premier", distance: 3.2, terminal: "T2", category: "Standard", rating: "4.2", price: 3800, durations: [3, 4, 6, 8, 10, 12, 16], amenities: ["Airport Shuttle"] },
            { id: 11, name: "Holiday Inn", distance: 4.2, terminal: "T2", category: "Standard", rating: "4.4", price: 4200, durations: [4, 6, 8, 10, 12, 16, 24], amenities: ["Pool", "Business Center"] },
            { id: 12, name: "Grand Hyatt", distance: 6.1, terminal: "T2", category: "Premium", rating: "4.7", price: 7000, durations: [8, 10, 12, 16, 24], amenities: ["Pool", "Spa", "Business Center"] }
        ];"""

    html = re.sub(r'const hotels = \[.*?\];', new_hotels_data, html, flags=re.DOTALL)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed hotel data in hotel.html.")

fix_hotel_durations_data()
