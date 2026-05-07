import codecs
import re

def update_marketplace():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_js = """window.draftLayoverList = [];

  window.toggleListDrawer = function() {
      let drawer = document.getElementById('list-drawer');
      if (!drawer) {
          drawer = document.createElement('div');
          drawer.id = 'list-drawer';
          drawer.className = 'fixed bottom-[140px] left-1/2 -translate-x-1/2 w-[90%] max-w-[400px] bg-white rounded-xl shadow-2xl border border-outline-variant z-[100] transition-all duration-300 transform scale-95 opacity-0 pointer-events-none flex flex-col max-h-[400px]';
          document.body.appendChild(drawer);
      }
      
      if (drawer.classList.contains('opacity-0')) {
          // OPEN drawer -> create draft
          window.draftLayoverList = JSON.parse(JSON.stringify(window.layoverList));
          window.renderListDrawer();
          drawer.classList.remove('opacity-0', 'scale-95', 'pointer-events-none');
          drawer.classList.add('opacity-100', 'scale-100', 'pointer-events-auto');
      } else {
          // CLOSE drawer -> discard draft
          drawer.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
          drawer.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
      }
  };

  window.saveListEdits = function() {
      // Apply draft to main
      window.layoverList = JSON.parse(JSON.stringify(window.draftLayoverList));
      window.saveLayoverList();
      window.updateTimeCalculations();
      window.updateListIndicator();
      window.syncButtonStates();
      window.toggleListDrawer();
  };

  window.draftMoveUp = function(index) {
      if (index > 0) {
          const temp = window.draftLayoverList[index];
          window.draftLayoverList[index] = window.draftLayoverList[index - 1];
          window.draftLayoverList[index - 1] = temp;
          window.renderListDrawer();
      }
  };

  window.draftMoveDown = function(index) {
      if (index < window.draftLayoverList.length - 1) {
          const temp = window.draftLayoverList[index];
          window.draftLayoverList[index] = window.draftLayoverList[index + 1];
          window.draftLayoverList[index + 1] = temp;
          window.renderListDrawer();
      }
  };

  window.draftRemove = function(index) {
      window.draftLayoverList.splice(index, 1);
      window.renderListDrawer();
  };

  window.draftUpdateDuration = function(index, newDuration) {
      window.draftLayoverList[index].duration = newDuration;
      window.renderListDrawer();
  };

  window.draftUpdateStart = function(index, newTime) {
      window.draftLayoverList[index].startTime = newTime;
      window.renderListDrawer();
  };

  window.draftUpdateEnd = function(index, newTime) {
      window.draftLayoverList[index].endTime = newTime;
      window.renderListDrawer();
  };

  window.calculateTimingForDraft = function() {
      let expMins = 0;
      window.draftLayoverList.forEach(item => {
          let mins = 0;
          const durStr = item.duration.toLowerCase();
          if (durStr.includes('h')) {
              mins = parseFloat(durStr) * 60;
          } else if (durStr.includes('m')) {
              mins = parseFloat(durStr);
          }
          expMins += mins;
      });

      let worstTravelMins = 0;
      if (window.draftLayoverList.length > 0) {
          // No permutations! It's explicit routing!
          let currentDist = 0;
          window.draftLayoverList.forEach(item => {
              let legDistance = (currentDist === 0) ? item.distance : (currentDist + item.distance);
              worstTravelMins += Math.round((legDistance * 3) + 15);
              currentDist = item.distance;
          });
          worstTravelMins += Math.round((currentDist * 3) + 15);
      }
      return { expMins, worstTravelMins };
  };

  window.renderListDrawer = function() {
      let drawer = document.getElementById('list-drawer');
      if (!drawer) return;
      
      let html = `
          <div class="px-4 py-3 border-b border-outline-variant flex justify-between items-center bg-surface-container-lowest rounded-t-xl shrink-0">
              <h4 class="font-bold text-sm text-primary flex items-center gap-2"><span class="material-symbols-outlined text-[16px]">list_alt</span> Edit Experiences</h4>
              <button onclick="window.toggleListDrawer()" class="text-secondary hover:text-primary"><span class="material-symbols-outlined text-[18px]">close</span></button>
          </div>
          <div class="p-4 overflow-y-auto flex-1 space-y-3">
      `;
      
      if (window.draftLayoverList.length === 0) {
          html += `<p class="text-xs text-secondary text-center py-4">No items added yet.</p>`;
      } else {
          let { expMins, worstTravelMins } = window.calculateTimingForDraft();
          const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';
  
          window.draftLayoverList.forEach((item, index) => {
              let indTravel = Math.round((item.distance * 3) + 15); // Simplify individual travel estimate
              
              let optionsHTML = '';
              const cat = (item.category || '').toLowerCase();
              
              if (cat.includes('hotel')) {
                  const opts = ['3h', '4h', '6h', '8h', '10h', '12h', '16h', '24h'];
                  opts.forEach(o => {
                      const label = o.replace('h', ' Hours');
                      optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                  });
              } else if (cat.includes('restaurant')) {
                  const opts = ['30m', '1h', '1.5h', '2h'];
                  opts.forEach(o => {
                      const label = o === '30m' ? '30 Min' : o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
                      optionsHTML += `<option value="${o}" ${item.duration === o ? 'selected' : ''}>${label}</option>`;
                  });
              } else if (cat.includes('spa')) {
                  const opts = ['30m', '1h', '1.5h', '2h', '2.5h', '3h'];
                  opts.forEach(o => {
                      const label = o === '30m' ? '30 Min' : o.replace('h', ' Hours').replace('1 Hours', '1 Hour');
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
                  <div class="flex flex-col gap-2 bg-surface p-3 rounded-lg border border-outline-variant relative group">
                      <div class="flex items-center gap-3">
                          <span class="font-bold text-primary text-[14px] w-4 text-center">${index + 1}</span>
                          ${item.image ? `<img src="${item.image}" class="w-10 h-10 rounded object-cover">` : `<div class="w-10 h-10 rounded bg-secondary-container flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-on-secondary-container text-[16px]">image</span></div>`}
                          <div class="flex-1 min-w-0">
                              <p class="font-bold text-[11px] text-primary truncate">${item.name}</p>
                              <p class="text-[9px] text-secondary mt-0.5">${item.category} &bull; Est ${formatTime(indTravel)} travel</p>
                          </div>
                          <div class="flex flex-col gap-1 items-end">
                              <div class="flex gap-1">
                                  <button onclick="window.draftMoveUp(${index})" class="p-0.5 border rounded hover:bg-surface-container-high ${index === 0 ? 'opacity-30 pointer-events-none' : ''}"><span class="material-symbols-outlined text-[14px]">arrow_upward</span></button>
                                  <button onclick="window.draftMoveDown(${index})" class="p-0.5 border rounded hover:bg-surface-container-high ${index === window.draftLayoverList.length - 1 ? 'opacity-30 pointer-events-none' : ''}"><span class="material-symbols-outlined text-[14px]">arrow_downward</span></button>
                              </div>
                              <button onclick="window.draftRemove(${index})" class="text-error hover:bg-error-container p-0.5 rounded-md mt-1 transition-colors">
                                  <span class="material-symbols-outlined text-[14px]">delete</span>
                              </button>
                          </div>
                      </div>
                      <div class="flex gap-2 items-center mt-1 border-t border-outline-variant pt-2">
                          <div class="flex-1">
                              <span class="text-[9px] text-secondary block mb-0.5">Duration</span>
                              <div class="relative flex items-center">
                                  <select onchange="window.draftUpdateDuration(${index}, this.value)" class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-1.5 pr-4 py-1 text-[9px] font-bold text-primary outline-none cursor-pointer hover:bg-surface-container-low transition-colors appearance-none">
                                      ${optionsHTML}
                                  </select>
                                  <span class="material-symbols-outlined absolute right-1 text-[12px] pointer-events-none text-primary/70">arrow_drop_down</span>
                              </div>
                          </div>
                          <div class="flex-1">
                              <span class="text-[9px] text-secondary block mb-0.5">Start</span>
                              <input type="time" value="${item.startTime || ''}" onchange="window.draftUpdateStart(${index}, this.value)" class="w-full bg-surface-container-lowest border border-outline-variant rounded px-1.5 py-1 text-[9px] font-bold text-primary outline-none cursor-pointer">
                          </div>
                          <div class="flex-1">
                              <span class="text-[9px] text-secondary block mb-0.5">End</span>
                              <input type="time" value="${item.endTime || ''}" onchange="window.draftUpdateEnd(${index}, this.value)" class="w-full bg-surface-container-lowest border border-outline-variant rounded px-1.5 py-1 text-[9px] font-bold text-primary outline-none cursor-pointer">
                          </div>
                      </div>
                  </div>
              `;
          });
  
          html += `
              <div class="mt-2 pt-3 border-t border-outline-variant flex flex-col gap-1 text-[10px] text-secondary font-medium">
                  <div class="flex justify-between">
                      <span>Experience Time:</span>
                      <span class="font-bold text-primary">${formatTime(expMins)}</span>
                  </div>
                  <div class="flex justify-between">
                      <span>Est. Travel Overhead:</span>
                      <span class="font-bold text-primary">${formatTime(worstTravelMins)}</span>
                  </div>
              </div>
          `;
      }
      
      html += `</div>
          <div class="p-3 bg-surface-container-lowest border-t border-outline-variant flex justify-between gap-3 shrink-0 rounded-b-xl">
              <button onclick="window.toggleListDrawer()" class="flex-1 py-2 rounded-lg border border-outline-variant font-bold text-xs text-secondary hover:bg-surface-container-high transition-colors">Cancel</button>
              <button onclick="window.saveListEdits()" class="flex-1 py-2 rounded-lg bg-primary text-white font-bold text-xs shadow-md hover:bg-primary/90 transition-colors">Save Changes</button>
          </div>
      `;
      drawer.innerHTML = html;
  };"""

    # We need to replace toggleListDrawer up to the end of renderListDrawer.
    # I will split using toggleListDrawer = function() { and updateListIndicator = function() {
    parts = html.split('window.toggleListDrawer = function() {')
    part2 = parts[1].split('window.updateListIndicator = function() {')
    html = parts[0] + new_js + "\n\n  window.updateListIndicator = function() {" + part2[1]
    
    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated marketplace.html drawer logic.")

update_marketplace()
