import os
import re
import codecs

def fix_errors():
    files = ['hotel.html', 'restaurant.html', 'restaurants.html', 'spa.html', 'spas.html', 'entertainment.html']
    for filepath in files:
        if not os.path.exists(filepath): continue
        with codecs.open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Fix syntax error } } l2.classList.remove -> } l2.classList.remove
        html = re.sub(r'\}\s*\}\s*l2\.classList\.remove', r'}\n            l2.classList.remove', html)
        
        # If it's hotel.html, fix item.name -> hotel.name
        if 'hotel' in filepath:
            # But only inside the openLevel2 function where btn is handled
            html = re.sub(r'btn\.dataset\.itemName = item\.name;', r'btn.dataset.itemName = hotel.name;', html)
            html = re.sub(r'i\.name === item\.name', r'i.name === hotel.name', html)
            html = re.sub(r'window\.addToList\(btn, item\.name, \'Hotel\', duration, item\.distance', r'window.addToList(btn, hotel.name, \'Hotel\', duration, hotel.distance', html)
            html = re.sub(r'window\.parent\.addToList\(btn, item\.name, \'Hotel\', duration, item\.distance', r'window.parent.addToList(btn, hotel.name, \'Hotel\', duration, hotel.distance', html)
            
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Fixed {filepath}")

fix_errors()
