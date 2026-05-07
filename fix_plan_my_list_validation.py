import codecs
import re

def fix_plan_my_list_validation():
    filepath = 'marketplace.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    validation_script = """
window.updateListIndicator = function() {
    let indicator = document.getElementById('global-list-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'global-list-indicator';
        indicator.className = 'fixed bottom-[75px] left-1/2 -translate-x-1/2 bg-white border border-outline-variant p-1.5 rounded-full shadow-lg z-[90] flex items-center gap-2 transition-all duration-300';
        document.body.appendChild(indicator);
    }

    const panel = document.getElementById('planner-summary-panel');
    let state = window.getPlannerState(window.layoverList);
    
    if (window.layoverList.length > 0) {
        if (panel) {
            panel.classList.remove('hidden');
            const formatTime = (m) => m > 0 ? (m >= 60 ? Math.floor(m/60) + 'h ' + (m%60 > 0 ? (m%60)+'m' : '') : m + 'm') : '0m';
            document.getElementById('summary-items').textContent = window.layoverList.length;
            document.getElementById('summary-exp-time').textContent = formatTime(state.totalExperienceMinutes);
            document.getElementById('summary-transit-time').textContent = formatTime(state.totalTransitMinutes);
        }
        
        let isInvalid = state.remainingMinutes < 0;
    
        indicator.innerHTML = `
            <button onclick="window.toggleListDrawer(event)" class="flex items-center gap-2 bg-surface-container-low hover:bg-surface-container-highest text-primary px-4 py-2 rounded-full font-label-sm transition-colors border border-outline-variant/50">
                <span class="bg-primary text-white w-4 h-4 flex items-center justify-center rounded-full font-bold text-[9px]">${window.layoverList.length}</span>
                <span class="font-semibold tracking-wide text-xs">View List</span>
            </button>
            <button id="btn-plan-my-list" onclick="window.proceedToPlan(this)" class="flex items-center gap-1.5 px-5 py-2 rounded-full font-label-sm transition-all shadow-sm ${isInvalid ? 'bg-error-container text-error border border-error/50 cursor-pointer opacity-90' : 'bg-primary hover:bg-primary/90 text-white'}">
                <span class="font-semibold tracking-wide text-xs">Plan My List</span>
                <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
            </button>
        `;
        indicator.style.display = 'flex';
    } else {
        indicator.style.display = 'none';
        if(panel) panel.classList.add('hidden');
        if(window.viewListModal) window.viewListModal.close();
    }
};

window.showRiskWarningModal = function() {
    let warningModal = document.getElementById('risk-warning-modal');
    if (!warningModal) {
        warningModal = document.createElement('div');
        warningModal.id = 'risk-warning-modal';
        warningModal.className = 'fixed inset-0 z-[200] flex items-center justify-center px-4 transition-opacity duration-300 opacity-0 pointer-events-none';
        
        const overlay = document.createElement('div');
        overlay.className = 'absolute inset-0 bg-black/60 backdrop-blur-sm';
        overlay.onclick = () => window.closeRiskWarningModal();
        warningModal.appendChild(overlay);
        
        const content = document.createElement('div');
        content.className = 'relative bg-surface-container-lowest w-full max-w-sm rounded-2xl shadow-2xl overflow-hidden border border-error/20 flex flex-col scale-95 transition-transform duration-300';
        
        content.innerHTML = `
            <div class="bg-error/10 p-5 flex flex-col items-center border-b border-error/10">
                <div class="w-12 h-12 rounded-full bg-error/20 flex items-center justify-center mb-3">
                    <span class="material-symbols-outlined text-error text-2xl">warning</span>
                </div>
                <h3 class="font-display text-h2 text-on-surface text-center font-bold">Not Enough Layover Time</h3>
            </div>
            <div class="p-5 flex flex-col gap-4">
                <p class="text-body-md text-secondary text-center">Your selected experiences exceed your available layover duration.</p>
                <div class="bg-surface-container-low rounded-lg p-3 border border-outline-variant/50 text-sm text-on-surface-variant font-medium">
                    <p class="mb-2 text-xs font-bold uppercase tracking-wider text-secondary">Please do one of the following:</p>
                    <ul class="list-disc pl-5 space-y-1">
                        <li>Reduce experience durations</li>
                        <li>Remove some activities</li>
                        <li>Increase layover duration</li>
                    </ul>
                </div>
                <button onclick="window.closeRiskWarningModal()" class="w-full bg-error text-white font-bold py-3 rounded-xl mt-2 hover:bg-error/90 transition-colors shadow-md active:scale-[0.98]">Review Itinerary</button>
            </div>
        `;
        
        warningModal.appendChild(content);
        document.body.appendChild(warningModal);
    }
    
    warningModal.classList.remove('opacity-0', 'pointer-events-none');
    warningModal.classList.add('opacity-100', 'pointer-events-auto');
    warningModal.querySelector('.relative').classList.remove('scale-95');
    warningModal.querySelector('.relative').classList.add('scale-100');
};

window.closeRiskWarningModal = function() {
    const warningModal = document.getElementById('risk-warning-modal');
    if (warningModal) {
        warningModal.classList.remove('opacity-100', 'pointer-events-auto');
        warningModal.classList.add('opacity-0', 'pointer-events-none');
        warningModal.querySelector('.relative').classList.remove('scale-100');
        warningModal.querySelector('.relative').classList.add('scale-95');
    }
};

window.proceedToPlan = function(btn) {
    if (window.layoverList.length === 0) return;
    
    let state = window.getPlannerState(window.layoverList);
    
    if (state.remainingMinutes < 0 || window.isRisk) {
        window.showRiskWarningModal();
        return;
    }
    
    localStorage.setItem("tripPlanActivated", "true");
    btn.classList.add('opacity-90', 'cursor-wait');
    
    setTimeout(() => {
        window.location.href = 'yourplan.html';
    }, 400);
};
"""

    html = re.sub(r'window\.updateListIndicator = function\(\) \{.*?(?=// Initialize modal DOM structures immediately)', validation_script, html, flags=re.DOTALL)

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed Plan My List validation in marketplace.html.")

fix_plan_my_list_validation()
