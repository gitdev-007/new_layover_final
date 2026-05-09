// Centralized navigation for PLAN LAYOVER buttons
function redirectToExplorePlanner(category = '') {
    // Store category to restore state if needed after redirect
    if (category) {
        localStorage.setItem('pending_category', category);
    }
    // Redirect to main homepage (top of page)
    window.location.href = 'index.html';
}