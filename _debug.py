import re

path = r'c:\Users\Dev Tinker\Desktop\layoverX_dummy\hotel.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'<div class="hotel-item[^>]*>', content)
with open(r'c:\Users\Dev Tinker\Desktop\layoverX_dummy\_debug.txt', 'w') as f:
    f.write(f'Found {len(matches)} matches\n')
    for m in matches:
        f.write(m + '\n---\n')

print(f'Found {len(matches)} matches')
