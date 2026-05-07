import codecs
import re

def fix_entertainment_durations():
    filepath = 'entertainment.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Clear out the static options in item-duration
    html = re.sub(
        r'(<select id="item-duration"[^>]*>)\s*(<option[^>]*>.*?</option>\s*)*</select>',
        r'\1\n                        </select>',
        html,
        flags=re.DOTALL
    )

    script_inject = """
        const entertainmentDurations = [
            { valStr: '30m', label: '30 Min' },
            { valStr: '1h', label: '1 Hour' },
            { valStr: '2h', label: '2 Hours' },
            { valStr: '3h', label: '3 Hours' },
            { valStr: '4h', label: '4 Hours' }
        ];

        function populateEntertainmentDurations() {
            const itemDropdown = document.getElementById('item-duration');
            if (itemDropdown && itemDropdown.options.length === 0) {
                entertainmentDurations.forEach(d => {
                    itemDropdown.add(new Option(d.label, d.valStr));
                });
                itemDropdown.value = '1h'; // Set default to 1 Hour
            }
        }
        
        document.addEventListener('DOMContentLoaded', populateEntertainmentDurations);
"""

    html = html.replace('const items = [', script_inject + '\n        const items = [')

    html = html.replace("const duration = durSelect ? durSelect.value : '2h';", "const duration = durSelect ? durSelect.value : '1h';")

    html = html.replace('document.addEventListener(\'DOMContentLoaded\', renderItems);', 
                       'populateEntertainmentDurations();\n        document.addEventListener(\'DOMContentLoaded\', renderItems);\n        renderItems();')

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed entertainment.html duration dropdowns.")

fix_entertainment_durations()
