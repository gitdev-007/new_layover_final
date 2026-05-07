import re
import glob
import codecs

for f in ['hotel.html', 'restaurant.html', 'spa.html', 'entertainment.html']:
    with codecs.open(f, 'r', encoding='utf-8') as file:
        html = file.read()
    selects = re.findall(r'<select[^>]*id="([^"]+)"', html)
    print(f"{f}: {selects}")
