import re

path = r'c:\Users\Dev Tinker\Desktop\layoverX_dummy\hotel.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Hotel data: (name, price, duration, distance, amenities)
hotel_data = [
    ('The Orchid Hotel', 1200, 2, 3, 'wifi'),
    ('Hotel Sahara Star', 1400, 2, 2, 'wifi'),
    ('Taj Santacruz', 2200, 2, 4, 'wifi'),
    ('JW Marriott Sahar', 2100, 2, 3, 'wifi'),
    ('ITC Maratha', 2000, 2, 2, 'wifi'),
    ('The Leela Mumbai', 1900, 2, 4, 'wifi'),
    ('Aurika Mumbai', 1700, 2, 2, 'wifi'),
    ('Grand Hyatt', 1800, 2, 5, 'wifi'),
    ('Hotel Bawa Intl.', 800, 2, 3, 'wifi'),
    ('Hotel Midland', 700, 2, 4, 'wifi'),
    ('Lemon Tree Premier', 1000, 2, 4, 'wifi'),
    ('Holiday Inn', 1100, 2, 5, 'wifi'),
]

for name, price, duration, distance, amenities in hotel_data:
    # Replace data attributes for this specific hotel
    old_pattern = f'>{name}</div>'
    # Find the div containing this hotel name and replace its data attrs
    # We need to be careful - match the full div tag before the hotel name
    pass

# Actually, let's use a simpler approach - replace ALL data-duration="2" data-price="1200" data-distance="3" data-amenities="wifi"
# in premium hotel items
old_premium = 'data-duration="2" data-price="1200" data-distance="3" data-amenities="wifi" role="button" tabindex="0">The Orchid Hotel</div>'
new_premium = 'data-duration="2" data-price="1200" data-distance="3" data-amenities="wifi" role="button" tabindex="0">The Orchid Hotel</div>'

# Hmm this is too specific. Let me use a different strategy.
# I'll replace the entire line 200 by reconstructing it.

# Actually, the simplest approach: use regex to replace data attrs per hotel
# But since all hotels currently have identical data attrs, we need to do it carefully.

# Strategy: split content by lines, find line 200, and replace each hotel div individually.
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'The Orchid Hotel</div>' in line and 'hotel-item' in line:
        # This is the grid line with all hotels
        hotel_replacements = [
            (('The Orchid Hotel', 1200, 2, 3, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('Hotel Sahara Star', 1400, 2, 2, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('Taj Santacruz', 2200, 2, 4, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('JW Marriott Sahar', 2100, 2, 3, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('ITC Maratha', 2000, 2, 2, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('The Leela Mumbai', 1900, 2, 4, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('Aurika Mumbai', 1700, 2, 2, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('Grand Hyatt', 1800, 2, 5, 'wifi'), 'bg-primary/5 border border-primary/20 rounded text-[11px] font-medium text-on-surface'),
            (('Hotel Bawa Intl.', 800, 2, 3, 'wifi'), 'bg-surface border border-outline-variant rounded text-[11px] text-on-surface'),
            (('Hotel Midland', 700, 2, 4, 'wifi'), 'bg-surface border border-outline-variant rounded text-[11px] text-on-surface'),
            (('Lemon Tree Premier', 1000, 2, 4, 'wifi'), 'bg-surface border border-outline-variant rounded text-[11px] text-on-surface'),
            (('Holiday Inn', 1100, 2, 5, 'wifi'), 'bg-surface border border-outline-variant rounded text-[11px] text-on-surface'),
        ]
        for (name, price, duration, distance, amenities), extra_classes in hotel_replacements:
            old = f'<div class="hotel-item p-2 {extra_classes}" data-duration="2" data-price="1200" data-distance="3" data-amenities="wifi" role="button" tabindex="0">{name}</div>'
            new = f'<div class="hotel-item p-2 {extra_classes}" data-price="{price}" data-duration="{duration}" data-distance="{distance}" data-amenities="{amenities}" role="button" tabindex="0">{name}</div>'
            line = line.replace(old, new)
        lines[i] = line
        break

content = '\n'.join(lines)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('hotels updated')
