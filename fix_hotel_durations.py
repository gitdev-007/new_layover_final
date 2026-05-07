import codecs
import re

def fix_hotel_durations():
    filepath = 'hotel.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Clear out the static options in filter-duration
    html = re.sub(
        r'(<select id="filter-duration"[^>]*>)\s*<option[^>]*>.*?</option>\s*(<option[^>]*>.*?</option>\s*)*</select>',
        r'\1\n                                  <option value="any">Duration</option>\n                              </select>',
        html,
        flags=re.DOTALL
    )

    # 2. Clear out the static options in item-duration
    html = re.sub(
        r'(<select id="item-duration"[^>]*>)\s*(<option[^>]*>.*?</option>\s*)*</select>',
        r'\1\n                        </select>',
        html,
        flags=re.DOTALL
    )

    # 3. Add the javascript array and population logic at the top of the <script> block
    script_inject = """
        const hotelDurations = [
            { valNum: '3', valStr: '3h', label: '3 Hours' },
            { valNum: '4', valStr: '4h', label: '4 Hours' },
            { valNum: '6', valStr: '6h', label: '6 Hours' },
            { valNum: '8', valStr: '8h', label: '8 Hours' },
            { valNum: '10', valStr: '10h', label: '10 Hours' },
            { valNum: '12', valStr: '12h', label: '12 Hours' },
            { valNum: '16', valStr: '16h', label: '16 Hours' },
            { valNum: '24', valStr: '24h', label: '24 Hours' }
        ];

        function populateHotelDurations() {
            const filterDropdown = document.getElementById('filter-duration');
            if (filterDropdown && filterDropdown.options.length <= 1) {
                hotelDurations.forEach(d => {
                    filterDropdown.add(new Option(d.label, d.valNum));
                });
            }

            const itemDropdown = document.getElementById('item-duration');
            if (itemDropdown && itemDropdown.options.length === 0) {
                hotelDurations.forEach(d => {
                    itemDropdown.add(new Option(d.label, d.valStr));
                });
                itemDropdown.value = '3h'; // Set default to 3 Hours
            }
        }
        
        // Ensure duration is always set on load
        document.addEventListener('DOMContentLoaded', populateHotelDurations);
"""

    html = html.replace('const hotels = [', script_inject + '\n        const hotels = [')

    # Wait, the add-list-btn logic in hotel.html has a default of '2h' if not selected. Fix that.
    html = html.replace("const duration = durSelect ? durSelect.value : '2h';", "const duration = durSelect ? durSelect.value : '3h';")

    # Make sure we also call it inside renderHotels or openLevel2 just in case it was injected dynamically via innerHTML.
    # Actually, the selects are static in the HTML body of hotel.html, not generated in renderCard. So DOMContentLoaded is enough.
    # Wait, in marketplace.html, scripts are extracted and executed, so DOMContentLoaded might have already fired.
    # I should just call populateHotelDurations() directly in the script block.
    
    html = html.replace('document.addEventListener(\'DOMContentLoaded\', renderHotels);', 
                       'populateHotelDurations();\n        document.addEventListener(\'DOMContentLoaded\', renderHotels);\n        renderHotels();')

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed hotel.html duration dropdowns.")

fix_hotel_durations()
