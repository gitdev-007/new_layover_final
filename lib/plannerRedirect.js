// Centralized navigation for PLAN LAYOVER buttons
function redirectToExplorePlanner(category = '') {
    // Store category to restore state if needed after redirect
    if (category) {
        localStorage.setItem('pending_category', category);
    }
    // Set flag to show prompt on homepage
    localStorage.setItem('show_planner_prompt', 'true');
    // Redirect to main homepage (top of page)
    window.location.href = 'index.html';
}