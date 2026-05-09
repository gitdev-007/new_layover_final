<!-- Auth Protection Modal -->
<div id="auth-modal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 opacity-0 pointer-events-none transition-all duration-300">
    <div class="absolute inset-0 bg-black/60 backdrop-blur-md transition-opacity" onclick="closeAuthModal()"></div>
    <div class="relative bg-neutral-900 border border-white/10 rounded-3xl p-8 max-w-sm w-full shadow-2xl scale-95 transition-transform duration-300">
        <h3 class="text-2xl font-bold text-white mb-3">Sign in required</h3>
        <p class="text-neutral-400 mb-8 leading-relaxed">Please sign in to continue exploring layover experiences.</p>
        <div class="flex flex-col gap-3">
            <button onclick="window.location.href='auth.html'" class="w-full bg-primary text-on-primary font-bold py-3.5 rounded-xl hover:scale-[1.02] active:scale-[0.98] transition-all">Sign In</button>
            <button onclick="closeAuthModal()" class="w-full bg-transparent border border-white/10 text-white font-bold py-3.5 rounded-xl hover:bg-white/5 transition-all">Cancel</button>
        </div>
    </div>
</div>

<script>
    function checkAuth(callback) {
        const session = localStorage.getItem('sb-yymnczb-auth-token');
        if (!session) {
            const modal = document.getElementById('auth-modal');
            modal.classList.remove('opacity-0', 'pointer-events-none');
            modal.querySelector('.scale-95').classList.remove('scale-95');
        } else {
            callback();
        }
    }
    
    function closeAuthModal() {
        const modal = document.getElementById('auth-modal');
        modal.classList.add('opacity-0', 'pointer-events-none');
        modal.querySelector('.bg-neutral-900').classList.add('scale-95');
    }
</script>