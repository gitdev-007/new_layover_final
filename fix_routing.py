import codecs
import re

def fix_index():
    filepath = 'index.html'
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    modal_html = """
  <!-- Verification Persistence Modal -->
  <div id="verified-modal" class="fixed inset-0 z-[100] hidden items-center justify-center opacity-0 transition-opacity duration-300">
    <div class="absolute inset-0 bg-black/60 backdrop-blur-md"></div>
    <div class="relative z-10 w-[90%] max-w-[400px] bg-surface rounded-2xl p-6 shadow-2xl border border-outline-variant text-center">
      <h3 class="font-h3 text-xl font-bold text-primary mb-2">Continue With Existing Travel Details?</h3>
      <p class="text-sm text-secondary mb-8">We found an existing verified layover session for your upcoming journey.</p>
      <div class="flex flex-col gap-3">
        <button id="modal-continue-btn" onclick="window.location.href='transportation.html'" class="w-full bg-primary-container text-on-primary-container font-bold py-3 rounded-full hover:scale-[1.02] transition-transform text-sm">
          Use Existing Details
        </button>
        <button id="modal-update-btn" onclick="window.location.href='QR_Upload_State.html'" class="w-full bg-transparent border border-outline-variant text-secondary font-bold py-3 rounded-full hover:bg-surface-container-low transition-colors text-sm">
          Update Travel Information
        </button>
      </div>
    </div>
  </div>
"""
    if 'verified-modal' not in html:
        html = html.replace('</body>', modal_html + '\n</body>')

    pageshow_js = """
        // Prevent "Routing..." stuck state on Back button navigation
        window.addEventListener('pageshow', function(e) {
            const exploreBtn = document.getElementById('exploreBtn');
            if (exploreBtn && exploreBtn.innerHTML.includes('Routing...')) {
                exploreBtn.innerHTML = 'Explore Experiences <span class="material-symbols-outlined text-[18px]">arrow_forward</span>';
                exploreBtn.style.pointerEvents = 'auto';
                exploreBtn.classList.remove('opacity-90');
                
                // Re-validate to see if it should be fully enabled or disabled
                const durationVal = document.getElementById('layover-duration')?.value;
                const departureVal = document.getElementById('flight-departure')?.value;
                if (!durationVal || !departureVal) {
                    exploreBtn.classList.add('text-white/40', 'bg-white/[0.04]', 'opacity-50', 'cursor-not-allowed', 'pointer-events-none');
                    exploreBtn.classList.remove('bg-primary-container', 'text-on-primary-container', 'hover:scale-[1.02]', 'cursor-pointer', 'pointer-events-auto');
                }
            }
        });
    """
    
    if "window.addEventListener('pageshow'" not in html:
        html = html.replace('function initializeApp() {', pageshow_js + '\n        function initializeApp() {')

    update_ui_addition = """
            const isVerified = localStorage.getItem('qr_verified') === 'true';
            const planBtn = document.getElementById('plan-layover-btn');
            const mobilePlanBtn = document.getElementById('plan-layover-btn-mobile');
            const exploreBtn = document.getElementById('exploreBtn');
            
            if (user && isVerified) {
                if (planBtn) planBtn.textContent = 'Continue Planning';
                if (mobilePlanBtn) mobilePlanBtn.textContent = 'Continue Planning';
                if (exploreBtn) {
                    exploreBtn.innerHTML = 'Continue Planning <span class="material-symbols-outlined text-[18px]">arrow_forward</span>';
                    exploreBtn.classList.remove('text-white/40', 'bg-white/[0.04]', 'opacity-50', 'cursor-not-allowed', 'pointer-events-none');
                    exploreBtn.classList.add('bg-primary-container', 'text-on-primary-container', 'hover:scale-[1.02]', 'cursor-pointer', 'pointer-events-auto');
                }
            } else {
                if (planBtn) planBtn.textContent = 'Plan Layover';
                if (mobilePlanBtn) mobilePlanBtn.textContent = 'Plan Layover';
                if (exploreBtn && !exploreBtn.innerHTML.includes('Routing...')) {
                    exploreBtn.innerHTML = 'Explore Experiences <span class="material-symbols-outlined text-[18px]">arrow_forward</span>';
                }
            }
        }"""
        
    html = re.sub(r'updateAuthUI\(user\) \{.*?\}\s*\}', lambda m: m.group(0)[:-1] + update_ui_addition, html, flags=re.DOTALL)

    setup_explore_replacement = """        // Explore Experiences button and validation flow
        function setupExploreButton() {
            const exploreBtn = document.getElementById('exploreBtn');
            const durationInput = document.getElementById('layover-duration');
            const departureInput = document.getElementById('flight-departure');
            const validationMsg = document.getElementById('form-validation-msg');
            
            if (!exploreBtn || !durationInput || !departureInput) {
                console.error('Explore button or inputs not found');
                return;
            }

            const validateForm = () => {
                const isVerified = localStorage.getItem('qr_verified') === 'true';
                if (isVerified && (supabaseClient && supabaseClient.auth)) {
                    // Let async auth check override it via updateAuthUI
                    return true; 
                }

                const durationVal = durationInput.value;
                const departureVal = departureInput.value;
                const isValid = durationVal && departureVal;

                if (isValid) {
                    exploreBtn.classList.remove('text-white/40', 'bg-white/[0.04]', 'opacity-50', 'cursor-not-allowed', 'pointer-events-none');
                    exploreBtn.classList.add('bg-primary-container', 'text-on-primary-container', 'hover:scale-[1.02]', 'cursor-pointer', 'pointer-events-auto');
                    if(validationMsg) validationMsg.classList.add('hidden');
                } else {
                    exploreBtn.classList.add('text-white/40', 'bg-white/[0.04]', 'opacity-50', 'cursor-not-allowed', 'pointer-events-none');
                    exploreBtn.classList.remove('bg-primary-container', 'text-on-primary-container', 'hover:scale-[1.02]', 'cursor-pointer', 'pointer-events-auto');
                }
                return isValid;
            };

            durationInput.addEventListener('change', validateForm);
            departureInput.addEventListener('input', validateForm);
            departureInput.addEventListener('change', validateForm);
            
            validateForm(); // Initial state check
            
            exploreBtn.addEventListener('click', async function(e) {
                e.preventDefault();
                
                const isVerified = localStorage.getItem('qr_verified') === 'true';
                let isSessionValid = false;
                if (window.supabaseClient) {
                    const { data: { session } } = await supabaseClient.auth.getSession();
                    isSessionValid = !!session;
                }

                if (isSessionValid && isVerified) {
                    const modal = document.getElementById('verified-modal');
                    if (modal) {
                        modal.classList.remove('hidden');
                        // Small timeout to allow display:block to apply before animating opacity
                        setTimeout(() => modal.classList.remove('opacity-0'), 10);
                    }
                    return;
                }

                // Normal flow
                const durationVal = durationInput.value;
                const departureVal = departureInput.value;

                if (!durationVal || !departureVal) {
                    if(validationMsg) {
                        validationMsg.textContent = !durationVal ? "Please select your layover duration" : "Please choose your departure date & time";
                        validationMsg.classList.remove('hidden');
                        validationMsg.classList.add('animate-pulse');
                        setTimeout(() => validationMsg.classList.remove('animate-pulse'), 500);
                    }
                    return;
                }
                
                // Store values for downstream components
                localStorage.setItem('layover_duration', durationVal);
                localStorage.setItem('flight_departure', departureVal);
                
                exploreBtn.innerHTML = '<span class="material-symbols-outlined animate-spin text-[18px]">refresh</span> Routing...';
                exploreBtn.style.pointerEvents = 'none';
                exploreBtn.classList.add('opacity-90');
                
                console.log('Form validated - redirecting to QR Upload...');
                setTimeout(() => {
                    window.location.href = 'QR_Upload_State.html';
                }, 400);
            });
            
            console.log('Explore validation handler attached');
        }"""
        
    html = re.sub(r'// Explore Experiences button and validation flow.*?console\.log\([^)]*Explore validation handler attached[^)]*\);\n\s*\}', setup_explore_replacement, html, flags=re.DOTALL)
    
    plan_layover_top_btn = """        // Plan Layover button click handler - clean auth flow with no alerts
        document.getElementById("plan-layover-btn").addEventListener("click", async function (e) {
            e.preventDefault();
            console.log("Plan Layover button clicked");

            const { data: { session }, error } = await supabaseClient.auth.getSession();
            const isVerified = localStorage.getItem('qr_verified') === 'true';

            if (!session) {
                console.log("User not logged in -> redirecting");
                window.location.href = "/auth.html";
                return;
            }

            if (isVerified) {
                const modal = document.getElementById('verified-modal');
                if (modal) {
                    modal.classList.remove('hidden');
                    setTimeout(() => modal.classList.remove('opacity-0'), 10);
                }
            } else {
                window.location.href = "/plan.html";
            }
        });"""
    html = re.sub(r'// Plan Layover button click handler - clean auth flow with no alerts.*?window\.location\.href = "/plan\.html";\n\s*\}\);', plan_layover_top_btn, html, flags=re.DOTALL)

    plan_layover_mobile_btn = """        // Mobile Plan Layover button - same logic
        const mobileBtn = document.getElementById("plan-layover-btn-mobile");
        if (mobileBtn) {
            mobileBtn.addEventListener("click", async function (e) {
                e.preventDefault();
                console.log("Plan Layover button clicked (mobile)");

                const { data: { session }, error } = await supabaseClient.auth.getSession();
                const isVerified = localStorage.getItem('qr_verified') === 'true';

                if (!session) {
                    console.log("User not logged in -> redirecting");
                    window.location.href = "/auth.html";
                    return;
                }

                if (isVerified) {
                    const modal = document.getElementById('verified-modal');
                    if (modal) {
                        modal.classList.remove('hidden');
                        setTimeout(() => modal.classList.remove('opacity-0'), 10);
                    }
                } else {
                    window.location.href = "/plan.html";
                }
            });
        }"""
    html = re.sub(r'// Mobile Plan Layover button - same logic.*?\}\);\n\s*\}', plan_layover_mobile_btn, html, flags=re.DOTALL)


    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        print("Updated index.html")

fix_index()
