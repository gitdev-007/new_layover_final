<!-- Auth Protection Modal -->
<div id="auth-modal" class="fixed inset-0 bg-black/50 hidden z-[100] flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl p-8 max-w-sm w-full shadow-xl">
        <h3 class="text-xl font-bold mb-4">Sign in required</h3>
        <p class="text-gray-600 mb-6">Please sign in to continue with your layover planning.</p>
        <div class="flex gap-4">
            <button onclick="window.location.href='auth.html'" class="flex-1 bg-primary text-white py-3 rounded-lg font-bold">Sign In</button>
            <button onclick="closeAuthModal()" class="flex-1 bg-gray-100 text-gray-700 py-3 rounded-lg font-bold">Cancel</button>
        </div>
    </div>
</div>

<script>
    function checkAuth(callback) {
        const session = localStorage.getItem('sb-yymnczb-auth-token'); // Check local storage for session
        if (!session) {
            document.getElementById('auth-modal').classList.remove('hidden');
        } else {
            callback();
        }
    }
    
    function closeAuthModal() {
        document.getElementById('auth-modal').classList.add('hidden');
    }
</script>