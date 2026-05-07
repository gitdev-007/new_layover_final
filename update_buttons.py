import re
import codecs

def update_button(filepath, category_name):
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Change the button HTML
    html = re.sub(
        r'<button onclick="window\.location\.href=\'qr_upload_state\.html\'" class="(.*?)">\s*PLAN LAYOVER\s*</button>',
        r'<button id="add-list-btn" class="\1">\n                            ADD TO LIST\n                        </button>',
        html
    )

    # Insert Javascript to hook up the button inside openLevel2
    if category_name == 'Hotel':
        item_var = 'hotel'
    else:
        item_var = 'item'

    js_code = f"""
            const btn = document.getElementById('add-list-btn');
            if (btn) {{
                // Reset styling in case it was previously clicked
                if (btn.dataset.originalClasses) {{
                    btn.className = btn.dataset.originalClasses;
                    btn.innerHTML = btn.dataset.originalHtml;
                }} else {{
                    btn.innerHTML = 'ADD TO LIST';
                    btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
                }}
                
                btn.onclick = function() {{
                    if (window.addToList) {{
                        window.addToList(btn, {item_var}.name, '{category_name}', '', {item_var}.distance, '');
                    }} else if (window.parent && window.parent.addToList) {{
                        window.parent.addToList(btn, {item_var}.name, '{category_name}', '', {item_var}.distance, '');
                    }} else {{
                        alert('Added to list!');
                    }}
                }};
            }}
            
            l2.classList.remove('hidden');
    """

    html = re.sub(r'l2\.classList\.remove\(\'hidden\'\);', js_code, html, count=1)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

update_button('hotel.html', 'Hotel')
update_button('entertainment.html', 'Entertainment')
