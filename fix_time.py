import re

def fix_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add parseDurationToMins
    parse_logic = r'''window.parseDurationToMins = function(durStr) {
    if (!durStr) return 0;
    const lowerStr = String(durStr).toLowerCase();
    let totalMins = 0;
    const hMatch = lowerStr.match(/([\d\.]+)\s*(h|hour|hours)/);
    if (hMatch) totalMins += parseFloat(hMatch[1]) * 60;
    
    const mMatch = lowerStr.match(/([\d\.]+)\s*(m|min|mins|minute|minutes)/);
    if (mMatch) totalMins += parseFloat(mMatch[1]);
    
    if (!hMatch && !mMatch) {
        const val = parseFloat(lowerStr);
        if (!isNaN(val)) {
            if (val <= 24) totalMins += val * 60;
            else totalMins += val;
        }
    }
    return totalMins;
};

window.updateTimeCalculations'''
    
    if 'window.parseDurationToMins = function' not in content:
        content = content.replace('window.updateTimeCalculations', parse_logic)

    # 2. Replace flawed logic inside updateTimeCalculations (marketplace.html)
    content = re.sub(
        r'window\.layoverList\.forEach\(item => \{\s*let m = 0;\s*const dur = String\(item\.duration \|\| \'0\'\);\s*if \(dur\.includes\(\'h\'\)\) m = parseFloat\(dur\) \* 60;\s*else if \(dur\.includes\(\'m\'\)\) m = parseFloat\(dur\);\s*else m = parseFloat\(dur\) \* 60;\s*expMins \+= m;\s*if \(item\.distance > maxDist\) maxDist = item\.distance;\s*\}\);',
        r'window.layoverList.forEach(item => {\n            expMins += window.parseDurationToMins(item.duration);\n            if (item.distance > maxDist) maxDist = item.distance;\n        });',
        content
    )
    
    # 3. Replace flawed logic inside renderListDrawer (marketplace.html)
    content = re.sub(
        r'window\.layoverList\.forEach\(item => \{\s*const dur = String\(item\.duration \|\| \'0\'\);\s*if \(dur\.includes\(\'h\'\)\) expMins \+= parseFloat\(dur\) \* 60;\s*else if \(dur\.includes\(\'m\'\)\) expMins \+= parseFloat\(dur\);\s*else expMins \+= parseFloat\(dur\) \* 60;\s*if \(item\.distance > maxDist\) maxDist = item\.distance;\s*\}\);',
        r'window.layoverList.forEach(item => {\n            expMins += window.parseDurationToMins(item.duration);\n            if (item.distance > maxDist) maxDist = item.distance;\n        });',
        content
    )

    # 4. Replace flawed risk logic (marketplace.html)
    content = re.sub(
        r'if \(remainingMins < 0\) \{\s*window\.isRisk = true;\s*remEl\.textContent = \'Risk\';\s*remEl\.style\.color = \'#dc2626\';\s*remContainer\.style\.backgroundColor = \'#fef2f2\';\s*\} else \{\s*window\.isRisk = false;\s*remEl\.textContent = format\(remainingMins\);\s*remEl\.style\.color = \'#15803d\';\s*remContainer\.style\.backgroundColor = \'#ecfdf5\';\s*\}',
        r'''if (remainingMins < 15) {
            window.isRisk = true;
            remEl.textContent = remainingMins < 0 ? Math.abs(remainingMins) + 'm Over' : format(remainingMins);
            remEl.style.color = '#dc2626';
            remContainer.style.backgroundColor = '#fef2f2';
            remContainer.style.border = '1px solid #fee2e2';
        } else if (remainingMins <= 45) {
            window.isRisk = false;
            remEl.textContent = format(remainingMins);
            remEl.style.color = '#b45309';
            remContainer.style.backgroundColor = '#fffbeb';
            remContainer.style.border = '1px solid #fef3c7';
        } else {
            window.isRisk = false;
            remEl.textContent = format(remainingMins);
            remEl.style.color = '#15803d';
            remContainer.style.backgroundColor = '#ecfdf5';
            remContainer.style.border = '1px solid #d1fae5';
        }''',
        content
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('marketplace.html')

# Apply similar fixes to yourplan.html
with open('yourplan.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add parseDurationToMins
if 'window.parseDurationToMins' not in content:
    parse_logic = r'''window.parseDurationToMins = function(durStr) {
    if (!durStr) return 0;
    const lowerStr = String(durStr).toLowerCase();
    let totalMins = 0;
    const hMatch = lowerStr.match(/([\d\.]+)\s*(h|hour|hours)/);
    if (hMatch) totalMins += parseFloat(hMatch[1]) * 60;
    const mMatch = lowerStr.match(/([\d\.]+)\s*(m|min|mins|minute|minutes)/);
    if (mMatch) totalMins += parseFloat(mMatch[1]);
    if (!hMatch && !mMatch) {
        const val = parseFloat(lowerStr);
        if (!isNaN(val)) {
            if (val <= 24) totalMins += val * 60;
            else totalMins += val;
        }
    }
    return totalMins;
};

window.getPlannerState'''
    content = content.replace('window.getPlannerState', parse_logic)

# Replace flawed duration parsing
content = re.sub(
    r'let mins = 0;\s*const durStr = \(item\.duration \|\| \'\'\)\.toLowerCase\(\);\s*if \(durStr\.includes\(\'h\'\)\) mins \+= parseFloat\(durStr\) \* 60;\s*else if \(durStr\.includes\(\'m\'\)\) mins \+= parseFloat\(durStr\);',
    r'let mins = window.parseDurationToMins(item.duration);',
    content
)

# Fix risk status colors in yourplan
content = re.sub(
    r'if \(journeyMins < 0\) \{\s*remEl\.textContent = \'Risk\';\s*remEl\.style\.color = \'#dc2626\';\s*remContainer\.style\.backgroundColor = \'#fef2f2\';\s*remContainer\.style\.border = \'1px solid #fee2e2\';\s*\} else \{\s*remEl\.textContent = formatTime\(journeyMins\);\s*remEl\.style\.color = \'#15803d\';\s*remContainer\.style\.backgroundColor = \'#ecfdf5\';\s*remContainer\.style\.border = \'1px solid #d1fae5\';\s*\}',
    r'''if (journeyMins < 15) {
                remEl.textContent = journeyMins < 0 ? Math.abs(journeyMins) + 'm Over' : formatTime(journeyMins);
                remEl.style.color = '#dc2626';
                remContainer.style.backgroundColor = '#fef2f2';
                remContainer.style.border = '1px solid #fee2e2';
            } else if (journeyMins <= 45) {
                remEl.textContent = formatTime(journeyMins);
                remEl.style.color = '#b45309';
                remContainer.style.backgroundColor = '#fffbeb';
                remContainer.style.border = '1px solid #fef3c7';
            } else {
                remEl.textContent = formatTime(journeyMins);
                remEl.style.color = '#15803d';
                remContainer.style.backgroundColor = '#ecfdf5';
                remContainer.style.border = '1px solid #d1fae5';
            }''',
    content
)

with open('yourplan.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Time logic and risk states fixed.")
