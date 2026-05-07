import re
import codecs

def fix_file(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix main layout
    html = re.sub(
        r'<main class=".*?">',
        '<main class="flex-grow w-full max-w-4xl mx-auto p-4 flex flex-col items-center gap-6 relative pb-20 mt-4">',
        html
    )

    # 2. Fix level2 width
    html = re.sub(
        r'<div id="level2" class=".*?">',
        '<div id="level2" class="layout-transition hidden opacity-0 w-full max-w-4xl mx-auto flex-shrink-0 z-20 relative">',
        html,
        count=1
    )

    # 3. Fix button HTML to use id="add-list-btn" and default to "PLAN LAYOVER"
    html = re.sub(
        r'<button onclick="window\.location\.href=\'qr_upload_state\.html\'" class="(.*?)">\s*PLAN LAYOVER\s*</button>',
        r'<button id="add-list-btn" class="\1">\n                            PLAN LAYOVER\n                        </button>',
        html
    )
    html = re.sub(
        r'<button id="add-list-btn" class="(.*?)">\s*ADD TO LIST\s*</button>',
        r'<button id="add-list-btn" class="\1">\n                            PLAN LAYOVER\n                        </button>',
        html
    )

    # Determine item variable
    if 'items.find(h => h.id === id)' in html:
        item_var = 'item'
    elif 'hotels.find(h => h.id === id)' in html:
        item_var = 'hotel'
    else:
        item_var = 'item'

    if 'restaurants.html' in filepath:
        cat = 'Restaurant'
    elif 'spas.html' in filepath:
        cat = 'Spa'
    elif 'entertainment.html' in filepath:
        cat = 'Entertainment'
    else:
        cat = 'Hotel'

    # 4. Remove old JS block if it exists
    old_js_pattern = r"const btn = document\.getElementById\('add-list-btn'\);.*?l2\.classList\.remove\('hidden'\);"
    if re.search(old_js_pattern, html, flags=re.DOTALL):
        html = re.sub(old_js_pattern, "l2.classList.remove('hidden');", html, flags=re.DOTALL)

    # 5. Insert new dynamic JS block
    new_js = f"""
            const btn = document.getElementById('add-list-btn');
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
                            window.addToList(btn, {item_var}.name, '{cat}', '', {item_var}.distance, '');
                        }} else if (window.parent && window.parent.addToList) {{
                            window.parent.addToList(btn, {item_var}.name, '{cat}', '', {item_var}.distance, '');
                        }}
                    }};
                }} else {{
                    btn.innerHTML = 'PLAN LAYOVER';
                    btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
                    btn.onclick = function() {{
                        window.location.href = 'qr_upload_state.html';
                    }};
                }}
            }}
            
            l2.classList.remove('hidden');
    """

    html = re.sub(r'l2\.classList\.remove\(\'hidden\'\);', new_js, html, count=1)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

for page in ['hotel.html', 'restaurants.html', 'spas.html', 'entertainment.html']:
    try:
        fix_file(page)
        print(f"Fixed {page}")
    except Exception as e:
        print(f"Failed to fix {page}: {e}")
