import os
import re
import codecs

def update_marketplace():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    summary_html = """
  <!-- Dynamic Planner Summary -->
  <section id="planner-summary-panel" class="bg-white border-2 border-primary/20 rounded-xl p-4 shadow-sm mb-4 transition-all duration-300 hidden">
      <h2 class="font-h3 text-sm font-semibold text-primary mb-3 uppercase tracking-widest">ITINERARY PLANNER</h2>
      <div class="grid grid-cols-3 gap-2 text-center">
          <div class="border border-outline-variant p-2 rounded bg-surface">
              <p class="text-[10px] text-secondary uppercase tracking-wider mb-1">Items</p>
              <p id="summary-items" class="font-bold text-lg text-primary">0</p>
          </div>
          <div class="border border-outline-variant p-2 rounded bg-surface">
              <p class="text-[10px] text-secondary uppercase tracking-wider mb-1">Experience</p>
              <p id="summary-exp-time" class="font-bold text-lg text-primary">0h</p>
          </div>
          <div class="border border-outline-variant p-2 rounded bg-surface">
              <p class="text-[10px] text-secondary uppercase tracking-wider mb-1">Transit</p>
              <p id="summary-transit-time" class="font-bold text-lg text-primary">0m</p>
          </div>
      </div>
  </section>
  <!-- Category Pills -->"""
    
    html = html.replace('<!-- Category Pills -->', summary_html)

    # Update updateListIndicator to also update the planner summary
    indicator_update = """
window.updateListIndicator = function() {
    let indicator = document.getElementById('global-list-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'global-list-indicator';
        indicator.className = 'fixed bottom-[75px] left-1/2 -translate-x-1/2 bg-white border border-outline-variant p-1.5 rounded-full shadow-lg z-[90] flex items-center gap-2 transition-all duration-300';
        document.body.appendChild(indicator);
    }

    const panel = document.getElementById('planner-summary-panel');
    if (window.layoverList.length > 0) {
        if (panel) {
            panel.classList.remove('hidden');
            let { expMins, worstTravelMins } = window.calculateTiming();
            const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';
            document.getElementById('summary-items').textContent = window.layoverList.length;
            document.getElementById('summary-exp-time').textContent = formatTime(expMins);
            document.getElementById('summary-transit-time').textContent = formatTime(worstTravelMins);
        }
    """
    
    html = re.sub(r'window\.updateListIndicator = function\(\) \{.*?if \(window\.layoverList\.length > 0\) \{', indicator_update, html, flags=re.DOTALL)
    
    # Hide the panel when empty
    html = html.replace('indicator.style.display = \'none\';', 'indicator.style.display = \'none\';\n        if(panel) panel.classList.add(\'hidden\');')

    # Update removeFromList to properly query dynamic buttons
    remove_logic = """window.removeFromList = function(itemName) {
      window.layoverList = window.layoverList.filter(i => i.name !== itemName);
      window.saveLayoverList();
      
      document.querySelectorAll('button[data-item-name]').forEach(btn => {
          if (btn.dataset.itemName === itemName && btn.dataset.originalClasses) {
              btn.className = btn.dataset.originalClasses;
              btn.innerHTML = btn.dataset.originalHtml;
              btn.disabled = false;
              // Reset duration dropdown if present
              const durSelect = btn.previousElementSibling;
              if (durSelect && durSelect.tagName === 'SELECT') {
                  durSelect.disabled = false;
              }
          }
      });
      
      // Also check standard generic query for fallback
      document.querySelectorAll('button').forEach(btn => {
          const onclickStr = btn.getAttribute('onclick') || '';
          if (onclickStr.includes(`'${itemName}'`) && btn.dataset.originalClasses) {
              btn.className = btn.dataset.originalClasses;
              btn.innerHTML = btn.dataset.originalHtml;
              btn.disabled = false;
          }
      });

      renderListDrawer();
      updateListIndicator();
      updateTimeCalculations();
  };"""
    html = re.sub(r'window\.removeFromList = function\(itemName\) \{.*?\};\n', remove_logic + '\n', html, flags=re.DOTALL)
    
    # Update addToList to disable duration selector
    add_logic = """window.addToList = function(btn, itemName, category, duration, distance, image) {
      if (!btn.dataset.originalClasses) {
          btn.dataset.originalClasses = btn.className;
          btn.dataset.originalHtml = btn.innerHTML;
      }
  
      const existing = window.layoverList.find(i => i.name === itemName);
      if (!existing) {
          window.layoverList.push({
              name: itemName,
              category: category || 'Experience',
              duration: duration || '',
              distance: parseFloat(distance) || 0,
              image: image || ''
          });
          window.saveLayoverList();
      }
  
      btn.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span> ADDED';
      btn.classList.remove('bg-primary', 'bg-secondary', 'text-white', 'hover:bg-indigo-700', 'bg-slate-900', 'hover:shadow-md');
      btn.classList.add('bg-emerald-50', 'text-emerald-700', 'border', 'border-emerald-200', 'cursor-default');
      btn.disabled = true;
      
      const durSelect = btn.previousElementSibling;
      if (durSelect && durSelect.tagName === 'SELECT') {
          durSelect.disabled = true;
      }
  
      updateListIndicator();
      updateTimeCalculations();
  };"""
    html = re.sub(r'window\.addToList = function\(btn, itemName.*?updateTimeCalculations\(\);\n\s*\};', add_logic, html, flags=re.DOTALL)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated {filepath}")

def update_categories():
    files = ['hotel.html', 'restaurant.html', 'restaurants.html', 'spa.html', 'spas.html', 'entertainment.html']
    for filepath in files:
        if not os.path.exists(filepath): continue
        with codecs.open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        cat = 'Hotel'
        if 'restaurant' in filepath: cat = 'Restaurant'
        elif 'spa' in filepath: cat = 'Spa'
        elif 'entertainment' in filepath: cat = 'Entertainment'
        
        # Inject duration dropdown before add-list-btn if it doesn't exist
        duration_select = """
                      <select id="item-duration" class="w-full mb-3 bg-white border border-outline-variant px-2 py-2 text-[11px] text-on-surface font-medium outline-none cursor-pointer">
                          <option value="1h">1 Hour</option>
                          <option value="2h">2 Hours</option>
                          <option value="3h">3 Hours</option>
                          <option value="4h">4 Hours</option>
                      </select>
                      <button id="add-list-btn\""""
                      
        if 'id="item-duration"' not in html:
            html = html.replace('<button id="add-list-btn"', duration_select)
        
        # Update the javascript dynamic attachment
        js_code = f"""const btn = document.getElementById('add-list-btn');
            if (btn) {{
                // Reset styling
                if (btn.dataset.originalClasses) {{
                    btn.className = btn.dataset.originalClasses;
                    btn.innerHTML = btn.dataset.originalHtml;
                    btn.disabled = false;
                }}
                btn.dataset.itemName = item.name;
                
                const isMarketplace = !!document.getElementById('marketplace-content') || window.location.pathname.includes('marketplace');
                if (isMarketplace) {{
                    // Check if already in list
                    const existingListStr = localStorage.getItem('layoverList') || '[]';
                    let alreadyAdded = false;
                    try {{
                        const existingList = JSON.parse(existingListStr);
                        alreadyAdded = existingList.some(i => i.name === item.name);
                    }} catch(e) {{}}
                    
                    if (alreadyAdded) {{
                        btn.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span> ADDED';
                        btn.className = 'w-full py-2 text-sm tracking-widest uppercase transition-colors bg-emerald-50 text-emerald-700 border border-emerald-200 cursor-default';
                        btn.disabled = true;
                        if(document.getElementById('item-duration')) document.getElementById('item-duration').disabled = true;
                    }} else {{
                        btn.innerHTML = 'ADD TO LIST';
                        btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
                        btn.disabled = false;
                        if(document.getElementById('item-duration')) document.getElementById('item-duration').disabled = false;
                        btn.onclick = function() {{
                            const durSelect = document.getElementById('item-duration');
                            const duration = durSelect ? durSelect.value : '2h';
                            if (window.addToList) {{
                                window.addToList(btn, item.name, '{cat}', duration, item.distance, '');
                            }} else if (window.parent && window.parent.addToList) {{
                                window.parent.addToList(btn, item.name, '{cat}', duration, item.distance, '');
                            }}
                        }};
                    }}
                }} else {{
                    btn.innerHTML = 'PLAN LAYOVER';
                    btn.className = 'w-full bg-secondary text-white font-bold py-2 text-sm tracking-widest uppercase hover:bg-orange-700 transition-colors';
                    btn.disabled = false;
                    if(document.getElementById('item-duration')) document.getElementById('item-duration').disabled = false;
                    btn.onclick = function() {{
                        window.location.href = 'QR_Upload_State.html';
                    }};
                }}
            }}"""
            
        pattern = r"const btn = document\.getElementById\('add-list-btn'\);.*?btn\.onclick = function\(\) \{.*?window\.location\.href = 'QR_Upload_State\.html';.*?\};\s*\}"
        html = re.sub(pattern, js_code, html, flags=re.DOTALL)
        
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated {filepath}")

update_marketplace()
update_categories()
