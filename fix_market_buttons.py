import codecs
import re

def fix_file(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    cat = 'Restaurant' if 'restaurant' in filepath else 'Spa'
    
    js_code = f"""const btn = document.getElementById('add-list-btn');
            if (btn) {{
                // Reset styling
                if (btn.dataset.originalClasses) {{
                    btn.className = btn.dataset.originalClasses;
                    btn.innerHTML = btn.dataset.originalHtml;
                }}
                
                const isMarketplace = !!document.getElementById('marketplace-content') || window.location.pathname.includes('marketplace');
                if (isMarketplace) {{
                    btn.innerHTML = 'ADD TO LIST';
                    btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
                    btn.onclick = function() {{
                        if (window.addToList) {{
                            window.addToList(btn, item.name, '{cat}', '', item.distance, '');
                        }} else if (window.parent && window.parent.addToList) {{
                            window.parent.addToList(btn, item.name, '{cat}', '', item.distance, '');
                        }}
                    }};
                }} else {{
                    btn.innerHTML = 'PLAN LAYOVER';
                    btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
                    btn.onclick = function() {{
                        window.location.href = 'QR_Upload_State.html';
                    }};
                }}
            }}"""
    
    pattern = r"const btn = document\.getElementById\('add-list-btn'\);.*?btn\.onclick = function\(\) \{.*?window\.location\.href = 'QR_Upload_State\.html';.*?\};\s*\}"
    
    updated = re.sub(pattern, js_code, html, flags=re.DOTALL)
    
    if updated == html:
        print(f"No changes made to {filepath}. Pattern might not have matched.")
    else:
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"Fixed {filepath}")

for p in ['restaurant.html', 'restaurants.html', 'spa.html', 'spas.html']:
    try:
        fix_file(p)
    except Exception as e:
        print(f"Failed {p}: {e}")
