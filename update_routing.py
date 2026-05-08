import re

# We will define a consistent routing function and inject it into marketplace, yourplan, and finalize_itinerary

routing_logic = r'''
window.calculateLegTravelTime = function(dist1, dist2) {
    if (dist1 === 0) return Math.round(window.calculateDynamicTravelMins(dist2) + 15);
    if (dist2 === 0) return Math.round(window.calculateDynamicTravelMins(dist1) + 15);
    
    // Mock realistic cross-city distance based on radial difference
    const mockCrossDist = Math.max(1.2, Math.abs(dist1 - dist2) * 1.5 + 2.5);
    return Math.round(window.calculateDynamicTravelMins(mockCrossDist) + 10);
};

window.calculateItineraryTravel = function(list) {
    if (!list || list.length === 0) return { totalTravelMins: 0, legs: [] };
    
    let total = 0;
    let legs = [];
    let currentDist = 0;
    
    list.forEach(item => {
        const itemDist = parseFloat(item.distance) || 0;
        const legTime = window.calculateLegTravelTime(currentDist, itemDist);
        legs.push(legTime);
        total += legTime;
        currentDist = itemDist;
    });
    
    // Return to airport
    const returnTime = window.calculateLegTravelTime(currentDist, 0);
    legs.push(returnTime);
    total += returnTime;
    
    return { totalTravelMins: total, legs: legs };
};
'''

# 1. Update marketplace.html
with open('marketplace.html', 'r', encoding='utf-8') as f:
    market_content = f.read()

# Insert the routing logic after calculateDynamicTravelMins
if 'window.calculateItineraryTravel' not in market_content:
    market_content = re.sub(
        r'(window\.calculateDynamicTravelMins = function[^\}]+};)',
        r'\1\n' + routing_logic,
        market_content
    )

# Update updateTimeCalculations
market_content = re.sub(
    r'if \(window\.layoverList\.length > 0\) \{\s*let maxDist = 0;\s*window\.layoverList\.forEach\(item => \{\s*expMins \+= window\.parseDurationToMins\(item\.duration\);\s*if \(item\.distance > maxDist\) maxDist = item\.distance;\s*\}\);\s*worstTravelMins = Math\.round\(window\.calculateDynamicTravelMins\(maxDist\) \* 2 \+ 30\);\s*\}',
    r'''if (window.layoverList.length > 0) {
        window.layoverList.forEach(item => {
            expMins += window.parseDurationToMins(item.duration);
        });
        const travelData = window.calculateItineraryTravel(window.layoverList);
        worstTravelMins = travelData.totalTravelMins;
    }''',
    market_content
)

# Update renderListDrawer inside marketplace.html
market_content = re.sub(
    r'const travelMins = window\.layoverList\.length > 0 \? Math\.round\(window\.calculateDynamicTravelMins\(maxDist\) \* 2 \+ 30\) : 0;',
    r'const travelMins = window.layoverList.length > 0 ? window.calculateItineraryTravel(window.layoverList).totalTravelMins : 0;',
    market_content
)

# Update the drawer item travel time to just be its distance from airport for the preview, or the leg time?
# The prompt says: "HOTEL MIDLAND / Hotel • 3 Hours • Travel 39m". Let's show the leg time from airport as an estimate for individual items.
# We'll leave the individual card's travel time as is (just the distance from T2 estimate) since it's just a generic estimate for that item, but the total uses the real sequence. Wait, "Travel 39m" in the drawer should probably be the leg time. 
# Actually, the user says "Each selected experience card should show: Name, Category, Editable duration, Estimated travel time, Remove button... Example: HOTEL MIDLAND Hotel • 3 Hours • Travel 39m".
market_content = re.sub(
    r'const travel = Math\.round\(window\.calculateDynamicTravelMins\(item\.distance\) \* 2 \+ 30\);',
    r'const travel = window.calculateLegTravelTime(0, item.distance);',
    market_content
)

with open('marketplace.html', 'w', encoding='utf-8') as f:
    f.write(market_content)

# 2. Update yourplan.html
with open('yourplan.html', 'r', encoding='utf-8') as f:
    plan_content = f.read()

if 'window.calculateItineraryTravel' not in plan_content:
    plan_content = re.sub(
        r'(window\.calculateDynamicTravelMins = function[^\}]+};)',
        r'\1\n' + routing_logic,
        plan_content
    )

# Replace the processedItems logic in yourplan.html
old_planner_state_regex = r'let processedItems = listToCalculate\.map.*?let remaining = totalLayoverMins > 0 \? \(totalLayoverMins - bufferMins - travelMins - expMins\) : 0;'
new_planner_state = r'''
        const travelData = window.calculateItineraryTravel(listToCalculate);
        travelMins = travelData.totalTravelMins;
        const legs = travelData.legs;

        let processedItems = listToCalculate.map((item, idx) => {
            let mins = window.parseDurationToMins(item.duration);
            expMins += mins;
            
            return {
                id: item.id || Date.now() + idx,
                category: item.category || 'Experience',
                title: item.name,
                selectedDurationMinutes: mins,
                transitOverheadMinutes: legs[idx], // unique leg travel time
                priority: idx + 1,
                originalItem: item
            };
        });
        
        let remaining = totalLayoverMins > 0 ? (totalLayoverMins - bufferMins - travelMins - expMins) : 0;
'''
plan_content = re.sub(old_planner_state_regex, new_planner_state, plan_content, flags=re.DOTALL)

with open('yourplan.html', 'w', encoding='utf-8') as f:
    f.write(plan_content)

# 3. Update finalize_itinerary.html
with open('finalize_itinerary.html', 'r', encoding='utf-8') as f:
    fin_content = f.read()

# We need to replace the legTravel logic inside finalize_itinerary.html
fin_content = re.sub(
    r'const legTravel = Math\.round\(\(item\.originalItem\.distance \* 3\) \+ 15\);',
    r'const legTravel = item.transitOverheadMinutes;',
    fin_content
)

# And the return travel logic
fin_content = re.sub(
    r'const returnTravel = Math\.round\(\(lastItem\.originalItem\.distance \* 3\) \+ 15\);',
    r'const returnTravel = state.totalTransitMinutes - state.selectedItems.reduce((acc, curr) => acc + curr.transitOverheadMinutes, 0);',
    fin_content
)

with open('finalize_itinerary.html', 'w', encoding='utf-8') as f:
    f.write(fin_content)

print("Routing logic updated across all files.")
