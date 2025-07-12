const QUICKLINK_WIDTH = 150;
const GAP = 8;

// Function to open the delete quicklink modal
function openDeleteQuicklinkModal(quicklinkId) {
    document.getElementById('delete-quicklink-id').value = quicklinkId;
    window.modalFunctions.showModal('delete-quicklink-modal');
}

// Function to handle form submission for adding a quicklink
function setupAddQuicklinkForm() {
    const saveBtn = document.getElementById('save-quicklink-btn');
    if (!saveBtn) return;

    saveBtn.addEventListener('click', function() {
        const form = document.getElementById('add-quicklink-form');
        const formData = new FormData(form);

        fetch(form.action || window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                // Display errors
                const errorsList = document.getElementById('add-form-errors');
                errorsList.innerHTML = '';

                if (data.errors) {
                    for (const field in data.errors) {
                        const li = document.createElement('li');
                        li.textContent = `${field}: ${data.errors[field].join(' ')}`;
                        errorsList.appendChild(li);
                    }
                    document.querySelector('#add-quicklink-form .form-errors').style.display = 'block';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

// Function to handle form submission for deleting a quicklink
function setupDeleteQuicklinkForm() {
    const deleteBtn = document.getElementById('confirm-delete-btn');
    if (!deleteBtn) return;

    deleteBtn.addEventListener('click', function() {
        const form = document.getElementById('delete-quicklink-form');
        const formData = new FormData(form);

        fetch(form.action || window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                // Display errors
                const errorsList = document.getElementById('delete-form-errors');
                errorsList.innerHTML = '';

                if (data.errors) {
                    for (const field in data.errors) {
                        const li = document.createElement('li');
                        li.textContent = `${field}: ${data.errors[field].join(' ')}`;
                        errorsList.appendChild(li);
                    }
                    document.querySelector('#delete-quicklink-form .form-errors').style.display = 'block';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

function setWrapperPosition(pos) {
    const wrapper = document.getElementById('quicklinksWrapperInner');
    wrapper.style.transform = `translateX(${pos}px)`;
}

function getActiveDotIndex() {
    let activeIndex = 0;
    const pagination = document.getElementById('quicklinksPagination');
    const activeDot = pagination.querySelector('.pagination-dot.active');
    if (activeDot) {
        const dots = Array.from(pagination.querySelectorAll('.pagination-dot'));
        activeIndex = dots.indexOf(activeDot);
    }
    return activeIndex
}


function deletePaginationDots() {
    const pagination = document.getElementById('quicklinksPagination');
    pagination.innerHTML = '';
    pagination.style.display = 'none';
}

function getItemCountPerPage() {
    const wrapper = document.getElementById('quicklinksWrapperInner');
    let itemCountPerPage = Math.floor(wrapper.clientWidth / (QUICKLINK_WIDTH + GAP));
    if (itemCountPerPage < 1) itemCountPerPage = 1;
    return itemCountPerPage;
}


function determinePageCount() {
    const wrapper = document.getElementById('quicklinksWrapperInner');
    const quickLinks = wrapper.querySelectorAll('.quicklink');
    const itemsPerPage = getItemCountPerPage()
    return Math.ceil(quickLinks.length / itemsPerPage);
}

function hasQuickLinks() {
    const wrapper = document.getElementById('quicklinksWrapperInner');
    const quickLinks = wrapper.querySelectorAll('.quicklink');
    return quickLinks.length > 0;
}

function createPaginationDots(amount) {
    const pagination = document.getElementById('quicklinksPagination');
    pagination.style.display = 'flex';
    for (let i = 0; i < amount; i++) {
        const dot = document.createElement('div');
        dot.classList.add('pagination-dot');
        dot.addEventListener('click', function () {
            onPaginationDotClick(i);
        });
        pagination.appendChild(dot);
    }
}

function setActiveDotByIndex(index) {
    const pagination = document.getElementById('quicklinksPagination');
    const dots = Array.from(pagination.querySelectorAll('.pagination-dot'));
    dots.forEach(dot => dot.classList.remove('active'));
    if (index >= dots.length) {
        index = dots.length - 1;
    }
    dots[index].classList.add('active');
}

function onPaginationDotClick(index) {
    const itemsPerPage = getItemCountPerPage();
    const movePos = index * itemsPerPage * (QUICKLINK_WIDTH + GAP);
    setWrapperPosition(movePos * -1);
    setActiveDotByIndex(index);
}

function updatePaginationDots() {
    if (!hasQuickLinks()) return;

    // Reset the pagination wrapper and remove all dots.
    setWrapperPosition(0);
    deletePaginationDots()

    // Check if we have enough quicklinks to show pagination
    const pageCount = determinePageCount()
    if (pageCount <= 1) return;

    // Setup pagination dots
    let activeDotIndex = getActiveDotIndex();
    createPaginationDots(pageCount)
    setActiveDotByIndex(activeDotIndex);
}

// Update pagination dots when window resizes
window.addEventListener('resize', function () {
    updatePaginationDots();
});

// Update pagination dots when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    updatePaginationDots();
    setupAddQuicklinkForm();
    setupDeleteQuicklinkForm();
});

// Update pagination dots when wrapper is resized
if (typeof ResizeObserver !== 'undefined') {
    const wrapper = document.getElementById('quicklinksWrapperInner');
    const resizeObserver = new ResizeObserver(function () {
        updatePaginationDots();
    });

    resizeObserver.observe(wrapper);
}
