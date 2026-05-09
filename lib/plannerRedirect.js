// Centralized navigation for PLAN LAYOVER buttons
function redirectToExplorePlanner(category = '') {
    // Store category to restore state if needed after redirect
    if (category) {
        localStorage.setItem('pending_category', category);
    }
    // Redirect to homepage planning/booking section
    window.location.href = 'index.html#planning-section';
}