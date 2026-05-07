import codecs
import re

def fix_yourplan_time_parsing():
    filepath = 'yourplan.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_parse_logic = """    const flightDepartureRaw = localStorage.getItem('flight_departure') || '';
    
    let depTimeStr = '--:--';
    let depDateStr = '';
    if (flightDepartureRaw) {
        if (flightDepartureRaw.includes(':') && flightDepartureRaw.length <= 5) {
            depTimeStr = flightDepartureRaw;
        } else {
            try {
                const depDate = new Date(flightDepartureRaw);
                if (!isNaN(depDate.getTime())) {
                    depTimeStr = depDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
                    depDateStr = depDate.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
                }
            } catch(e) {}
        }
    }"""

    html = re.sub(
        r"    const flightDepartureRaw = localStorage\.getItem\('flight_departure'\) \|\| '';\s*let depTimeStr = '--:--';\s*let depDateStr = '';\s*if \(flightDepartureRaw\) \{\s*try \{\s*const depDate = new Date\(flightDepartureRaw\);\s*if \(\!isNaN\(depDate\.getTime\(\)\)\) \{\s*depTimeStr = depDate\.toLocaleTimeString.*?\s*depDateStr = depDate\.toLocaleDateString.*?\s*\}\s*\} catch\(e\) \{\}\s*\}",
        new_parse_logic,
        html,
        flags=re.DOTALL
    )

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed yourplan.html time parsing.")

fix_yourplan_time_parsing()
