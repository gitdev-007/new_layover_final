import codecs
import re

def fix_marketplace_timing():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_timing = """window.calculateTiming = function() {
      let expMins = 0;
      window.layoverList.forEach(item => {
          let mins = 0;
          const durStr = (item.duration || '').toLowerCase();
          if (durStr.includes('h')) {
              mins = parseFloat(durStr) * 60;
          } else if (durStr.includes('m')) {
              mins = parseFloat(durStr);
          }
          expMins += mins;
      });
  
      let worstTravelMins = 0;
      if (window.layoverList.length > 0) {
          let currentDist = 0;
          window.layoverList.forEach(item => {
              let legDistance = (currentDist === 0) ? item.distance : (currentDist + item.distance);
              worstTravelMins += Math.round((legDistance * 3) + 15);
              currentDist = item.distance;
          });
          worstTravelMins += Math.round((currentDist * 3) + 15);
      }
      return { expMins, worstTravelMins };
  };"""

    html = re.sub(r'window\.calculateTiming = function\(\) \{.*?return \{ expMins, worstTravelMins \};\n  \};', new_timing, html, flags=re.DOTALL)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated marketplace.html global calculateTiming.")

fix_marketplace_timing()
