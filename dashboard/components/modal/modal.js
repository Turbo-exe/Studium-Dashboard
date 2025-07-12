/** Initialize all modals on DOM startup */
document.addEventListener('DOMContentLoaded', function () {
    initModals();
});


function initModals() {
    /** Method to setup event listeners for modal features */
    // On close button click
    document.querySelectorAll('.close-modal').forEach(button => {
        button.addEventListener('click', function () {
            const modalId = this.getAttribute('data-modal-id');
            hideModal(modalId);
        });
    });

    // On backdrop click
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', function () {
            const modalId = this.getAttribute('data-modal-id');
            hideModal(modalId);
        });
    });

    // On ESC click
    document.addEventListener('keydown', function (event) {
        if (event.key !== "Escape") return;
        const visibleModal = document.querySelector('.modal.show');
        if (!visibleModal) return;
        const modalId = visibleModal.id;
        hideModal(modalId);
    });
}

/**
 * Show a modal by ID
 * @param {string} modalId - The ID of the modal to show
 */
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    const backdrop = document.getElementById(`${modalId}-backdrop`);

    if (!modal) throw new Error(`Failed to show modal. Could not find modal '${modalId}'!`);
    if (!backdrop) throw new Error(`Failed to show modal. Could not find backdrop for modal '${modalId}'!`);

    // Show modal (via classes)
    modal.classList.add('show');
    backdrop.classList.add('show');

    // Prevent scrolling in the outer most element 'body'
    document.body.style.overflow = 'hidden';

    // Set focus to first focusable element. This is the close button in this case.
    const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (focusableElements.length > 0) {
        focusableElements[0].focus();
    }
}

/**
 * Hide a modal by ID
 * @param {string} modalId - The ID of the modal to hide
 */
function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    const backdrop = document.getElementById(`${modalId}-backdrop`);

    if (!modal) throw new Error(`Failed to hide modal. Could not find modal '${modalId}'!`)
    if (!backdrop) throw new Error(`Failed to hide modal. Could not find backdrop for modal '${modalId}'!`)

    // Hide modal (via classes)
    modal.classList.remove('show');
    backdrop.classList.remove('show');

    // Restore body scrolling
    document.body.style.overflow = '';
}

// Export functions for use in other components
window.modalFunctions = {
    showModal: showModal,
    hideModal: hideModal
};
