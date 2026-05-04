/* shared-layout.js */
const mainLayout = document.querySelector('.main-layout');
const level2 = document.querySelector('.level2');
const filterFields = document.querySelectorAll('[data-filter-field]');
const items = document.querySelectorAll('.listing-item');

function applyFilters(dataDetails) {
    const filterState = {};
    filterFields.forEach(field => {
        filterState[field.dataset.filterField] = field.value;
    });

    items.forEach((item) => {
        let isVisible = true;
        
        // Filter logic: Duration, Price, Distance, Category/Type
        if (filterState.duration && item.dataset.duration !== filterState.duration) isVisible = false;
        if (filterState.priceRange && item.dataset.priceRange !== filterState.priceRange) isVisible = false;
        if (filterState.distance && parseInt(item.dataset.distance) > parseInt(filterState.distance)) isVisible = false;
        if (filterState.type && item.dataset.type !== filterState.type) isVisible = false;

        item.style.display = isVisible ? 'block' : 'none';
    });
}

function initItems(dataDetails) {
    items.forEach((item) => {
        item.addEventListener('click', () => {
            const itemName = item.textContent.trim();
            const detail = dataDetails[itemName];
            if (detail) {
                renderDetails(detail);
                mainLayout.classList.add('active');
                level2.style.display = 'block';
            }
        });
    });
}

function renderDetails(detail) {
    // Basic dynamic update logic
    level2.querySelector('[data-detail-field="name"]').textContent = detail.name;
    level2.querySelector('[data-detail-field="rating"]').textContent = detail.rating || '';
    level2.querySelector('[data-detail-field="location"]').textContent = detail.location;
    // ... add more field mapping here
}
