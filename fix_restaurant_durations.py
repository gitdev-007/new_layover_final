import codecs
import re

def fix_restaurant_durations():
    filepath = 'restaurant.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Clear out the static options in item-duration
    html = re.sub(
        r'(<select id="item-duration"[^>]*>)\s*(<option[^>]*>.*?</option>\s*)*</select>',
        r'\1\n                        </select>',
        html,
        flags=re.DOTALL
    )

    # If there is a filter-duration in restaurant.html (there isn't, but just in case)
    html = re.sub(
        r'(<select id="filter-duration"[^>]*>)\s*<option[^>]*>.*?</option>\s*(<option[^>]*>.*?</option>\s*)*</select>',
        r'\1\n                                  <option value="any">Duration</option>\n                              </select>',
        html,
        flags=re.DOTALL
    )

    script_inject = """
        const restaurantDurations = [
            { valStr: '30m', label: '30 Min' },
            { valStr: '1h', label: '1 Hour' },
            { valStr: '1.5h', label: '1.5 Hours' },
            { valStr: '2h', label: '2 Hours' }
        ];

        function populateRestaurantDurations() {
            const filterDropdown = document.getElementById('filter-duration');
            if (filterDropdown && filterDropdown.options.length <= 1) {
                restaurantDurations.forEach(d => {
                    filterDropdown.add(new Option(d.label, d.valStr));
                });
            }

            const itemDropdown = document.getElementById('item-duration');
            if (itemDropdown && itemDropdown.options.length === 0) {
                restaurantDurations.forEach(d => {
                    itemDropdown.add(new Option(d.label, d.valStr));
                });
                itemDropdown.value = '1h'; // Set default to 1 Hour
            }
        }
        
        document.addEventListener('DOMContentLoaded', populateRestaurantDurations);
"""

    html = html.replace('const items = [', script_inject + '\n        const items = [')

    html = html.replace("const duration = durSelect ? durSelect.value : '2h';", "const duration = durSelect ? durSelect.value : '1h';")

    html = html.replace('document.addEventListener(\'DOMContentLoaded\', renderItems);', 
                       'populateRestaurantDurations();\n        document.addEventListener(\'DOMContentLoaded\', renderItems);\n        renderItems();')

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed restaurant.html duration dropdowns.")

fix_restaurant_durations()
