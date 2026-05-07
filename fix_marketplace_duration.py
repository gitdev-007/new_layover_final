import codecs
import re

def fix_duration_logic():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_add_logic = """window.addToList = function(btn, itemName, category, duration, distance, image) {
      if (!btn.dataset.originalClasses) {
          btn.dataset.originalClasses = btn.className;
          btn.dataset.originalHtml = btn.innerHTML;
      }

      let finalDuration = duration;
      
      // 1. Prioritize category-level duration filter if present
      const catFilter = document.getElementById('filter-duration');
      if (catFilter && catFilter.value !== 'any') {
          finalDuration = catFilter.value + 'h';
      } else {
          // 2. Fallback to the detail-level duration selector
          const itemFilter = document.getElementById('item-duration');
          if (itemFilter && itemFilter.value) {
              finalDuration = itemFilter.value;
          }
      }
      
      // Safety format normalization
      if (!finalDuration) finalDuration = '2h';
      if (!finalDuration.includes('h') && !finalDuration.includes('m')) {
          finalDuration += 'h';
      }

      const existing = window.layoverList.find(i => i.name === itemName);
      if (!existing) {
          window.layoverList.push({
              name: itemName,
              category: category || 'Experience',
              duration: finalDuration,
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

    html = re.sub(r'window\.addToList = function\(btn, itemName.*?updateTimeCalculations\(\);\n\s*\};', new_add_logic, html, flags=re.DOTALL)
    
    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated marketplace.html duration logic.")

fix_duration_logic()
