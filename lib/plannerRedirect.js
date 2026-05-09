// Global utility for PLAN LAYOVER redirection
function redirectToPlanner(category = '') {
    const categoryParam = category ? `?type=${encodeURIComponent(category.toLowerCase())}` : '';
    window.location.href = `index.html${categoryParam}#how-it-works`;
}