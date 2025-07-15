

document.addEventListener('DOMContentLoaded', function() {
    // Set up edit button click handlers
    setupEditButtons();

    // Set up save button click handler
    document.getElementById('save-course-btn').addEventListener('click', saveEnrollment);
});

/**
 * Set up click handlers for edit buttons
 */
function setupEditButtons() {
    console.log(document.querySelectorAll('.edit-course-button'))
    document.querySelectorAll('.edit-course-button').forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.getAttribute('data-course-id');
            openEditModal(courseId);
        });
    });
}

/**
 * Open the edit modal and load enrollment data
 * @param {string} courseId - The ID of the enrollment to edit
 */
function openEditModal(courseId) {
    // Set the course ID in the hidden field
    document.getElementById('edit-course-id').value = courseId;

    // Clear previous form errors
    document.querySelector('.form-errors').style.display = 'none';

    // Fetch enrollment data
    fetch(`/edit-course/${courseId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Populate form fields
            const enrollment = data.enrollment;
            document.getElementById('id_score').value = enrollment.score || '';
            document.getElementById('id_status').value = enrollment.status;

            // Show the modal
            window.modalFunctions.showModal('edit-course-modal');
        } else {
            alert('Error loading enrollment data: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while loading enrollment data.');
    });
}

/**
 * Save the enrollment data
 */
function saveEnrollment() {
    const courseId = document.getElementById('edit-course-id').value;
    const form = document.getElementById('edit-course-form');
    const formData = new FormData(form);

    // Send the form data
    fetch(`/edit-course/${courseId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Hide the modal
            window.modalFunctions.hideModal('edit-course-modal');

            // Refresh the table
            location.reload();
        } else {
            // Display form errors
            displayFormErrors(data.errors);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving the enrollment.');
    });
}

/**
 * Display form errors
 * @param {string} errorsJson - JSON string of form errors
 */
function displayFormErrors(errorsJson) {
    const errors = JSON.parse(errorsJson);
    const errorsList = document.getElementById('edit-form-errors');
    errorsList.innerHTML = '';

    // Display general form errors
    document.querySelector('.form-errors').style.display = 'block';

    // Process each field's errors
    for (const field in errors) {
        const fieldErrors = errors[field];
        const errorElement = document.getElementById(`${field}-error`);

        if (errorElement) {
            errorElement.textContent = fieldErrors[0].message;
        }

        // Add to the general errors list
        const errorItem = document.createElement('li');
        errorItem.textContent = `${field}: ${fieldErrors[0].message}`;
        errorsList.appendChild(errorItem);
    }
}
