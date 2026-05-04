import re

path = r'c:\Users\Dev Tinker\Desktop\layoverX_dummy\hotel.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add data attributes before the closing > of each hotel-item div opening tag
content = re.sub(
    r'(<div class="hotel-item[^"]*"[^>]*?)(>)',
    r'\1 data-duration="2" data-price="1200" data-distance="3" data-amenities="wifi">',
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('modified')
