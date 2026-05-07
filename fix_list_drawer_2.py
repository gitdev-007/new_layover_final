import codecs
import re

def fix_renderListDrawer():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_render_func = """window.updateItemDuration = function(itemName, newDuration) {
      const item = window.layoverList.find(i => i.name === itemName);
      if (item) {
          item.duration = newDuration;
          window.saveLayoverList();
          window.updateTimeCalculations();
          window.renderListDrawer();
          window.updateListIndicator();
      }
  };

  window.renderListDrawer = function() {
      let drawer = document.getElementById('list-drawer');
      if (!drawer) return;
      
      let html = `
          <div class="px-4 py-3 border-b border-outline-variant flex justify-between items-center bg-surface-container-lowest rounded-t-xl">
              <h4 class="font-bold text-sm text-primary flex items-center gap-2"><span class="material-symbols-outlined text-[16px]">list_alt</span> Selected Experiences</h4>
              <button onclick="window.toggleListDrawer()" class="text-secondary hover:text-primary"><span class="material-symbols-outlined text-[18px]">close</span></button>
          </div>
          <div class="p-4 overflow-y-auto flex-1 space-y-3">
      `;
      
      if (window.layoverList.length === 0) {
          html += `<p class="text-xs text-secondary text-center py-4">No items added yet.</p>`;
      } else {
          let { expMins, worstTravelMins } = window.calculateTiming();
          const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';
  
          window.layoverList.forEach(item => {
              let indTravel = Math.round(window.calculateDynamicTravelMins(item.distance) * 2 + 30);
              
              let optionsHTML = '';
              const cat = (item.category || '').toLowerCase();
              
              if (cat.includes('hotel')) {
                  const opts = ['1h', '2h', '3h', '4h', '6h', '8h'];
                  opts.forEach(o => {
                      const label = o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                      optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                  });
              } else if (cat.includes('restaurant')) {
                  const opts = ['30m', '1h', '2h', '3h'];
                  opts.forEach(o => {
                      const label = o === '30m' ? '30 Min' : o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                      optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                  });
              } else if (cat.includes('spa')) {
                  const opts = ['1h', '2h', '3h', '4h'];
                  opts.forEach(o => {
                      const label = o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                      optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                  });
              } else {
                  const opts = ['30m', '1h', '2h', '3h', '4h'];
                  opts.forEach(o => {
                      const label = o === '30m' ? '30 Min' : o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                      optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                  });
              }

              const safeItemName = item.name.replace(/'/g, "\\\\'");
              
              html += `
                  <div class="flex gap-3 items-center bg-surface p-2 rounded-lg border border-outline-variant relative">
                      ${item.image ? `<img src="${item.image}" class="w-10 h-10 rounded object-cover">` : `<div class="w-10 h-10 rounded bg-secondary-container flex items-center justify-center"><span class="material-symbols-outlined text-on-secondary-container text-[16px]">image</span></div>`}
                      <div class="flex-1 min-w-0">
                          <p class="font-bold text-[11px] text-primary truncate">${item.name}</p>
                          <div class="text-[9px] text-secondary flex gap-1.5 items-center mt-1 flex-wrap">
                              <span>${item.category}</span>
                              &bull;
                              <div class="relative flex items-center">
                                  <select onchange="window.updateItemDuration('${safeItemName}', this.value)" class="bg-surface-container-lowest border border-outline-variant rounded-md pl-1.5 pr-4 py-0.5 text-[9px] font-bold text-primary outline-none cursor-pointer hover:bg-surface-container-low hover:border-primary/30 transition-colors appearance-none">
                                      ${optionsHTML}
                                  </select>
                                  <span class="material-symbols-outlined absolute right-1 text-[12px] pointer-events-none text-primary/70">arrow_drop_down</span>
                              </div>
                              &bull; 
                              <span>Est ${formatTime(indTravel)} overhead</span>
                          </div>
                      </div>
                      <button onclick="window.removeFromList('${safeItemName}')" class="p-1.5 text-secondary hover:text-error transition-colors rounded-md hover:bg-error-container">
                          <span class="material-symbols-outlined text-[16px]">delete</span>
                      </button>
                  </div>
              `;
          });
  
          html += `
              <div class="mt-4 pt-3 border-t border-outline-variant flex flex-col gap-1 text-[10px] text-secondary font-medium">
                  <div class="flex justify-between">
                      <span>Total Experience Time:</span>
                      <span class="font-bold text-primary">${formatTime(expMins)}</span>
                  </div>
                  <div class="flex justify-between">
                      <span>Est. Worst-Case Travel Overhead:</span>
                      <span class="font-bold text-primary">${formatTime(worstTravelMins)}</span>
                  </div>
              </div>
          `;
      }
      
      html += `</div>`;
      drawer.innerHTML = html;
  };

"""

    parts = html.split('window.renderListDrawer = function() {')
    if len(parts) == 2:
        part2 = parts[1].split('window.updateListIndicator = function() {')
        html = parts[0] + new_render_func + "window.updateListIndicator = function() {" + part2[1]
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated marketplace.html drawer edit logic via split method.")
    else:
        print("Failed to find split point.")

fix_renderListDrawer()
