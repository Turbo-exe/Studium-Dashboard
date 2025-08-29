document.addEventListener('DOMContentLoaded', function () {
    // Set up form handlers
    setupAddForm();
    setupEditForm();
    setupDeleteForm();

    // Set up add, edit and delete button click handlers
    setupAddButton();
    setupEditButtons();
    setupDeleteButtons();
});

/** Set up click handlers to show the add modal */
function setupAddButton() {
    const addButton = document.getElementById('add-enrollment-button');
    if (addButton) {
        addButton.addEventListener('click', function () {
            window.modalFunctions.showModal('add-enrollment-modal');
        });
    }
}

/** Set up click handlers to show the edit modal */
function setupEditButtons() {
    document.querySelectorAll('.edit-enrollment-button').forEach(button => {
        button.addEventListener('click', function () {
            const enrollmentId = this.getAttribute('data-enrollment-id');
            document.getElementById('edit-enrollment-id').value = enrollmentId;

            // Fetch enrollment data
            fetch(`/get-enrollment/${enrollmentId}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(async (response) => {
                const data = await response.json();
                if (response.status === 200) {
                    // Populate form fields
                    document.getElementById('id_status').value = data.status;
                    if (data.score !== null) {
                        document.getElementById('id_score').value = data.score;
                    } else {
                        document.getElementById('id_score').value = '';
                    }
                    // Show the modal
                    window.modalFunctions.showModal('edit-enrollment-modal');
                } else {
                    // Log error
                    console.error("Failed to fetch enrollment", data);
                    // Display error
                    alert("Failed to fetch enrollment. The dashboard will restart after you acknowledge this message.");
                    window.location.reload();
                }
            })
        });
    });
}

/** Set up click handlers to show the delete modal */
function setupDeleteButtons() {
    document.querySelectorAll('.delete-enrollment-button').forEach(button => {
        button.addEventListener('click', function () {
            document.getElementById('delete-enrollment-id').value = this.getAttribute('data-enrollment-id');
            window.modalFunctions.showModal('delete-enrollment-modal');
        });
    });
}


function setupAddForm() {
    const saveBtn = document.getElementById('add-enrollment-btn');
    if (!saveBtn) throw new Error('Save button not found!');

    saveBtn.addEventListener('click', function () {
        const form = document.getElementById('add-enrollment-form');
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(async (response) => {

            if (response.status === 201) {
                window.location.reload();
            } else if (response.status === 400) {
                const data = await response.json();
                // Log error
                console.error("Failed to add enrollment", data);

                // Display errors
                const errorsList = document.getElementById('add-enrollment-form-errors');
                errorsList.innerHTML = '';

                if (data.errors) {
                    for (const field in data.errors) {
                        const li = document.createElement('li');
                        li.textContent = `${field}: ${data.errors[field].join(' ')}`;
                        errorsList.appendChild(li);
                    }
                    document.querySelector('#add-enrollment-form .form-errors').style.display = 'block';
                }
            } else if (response.status === 500) {
                const data = await response.json();
                // Log error
                console.error("Failed to add enrollment", data);
                // Display error
                alert("Failed to add enrollment. The dashboard will restart after you acknowledge this message.");
                window.location.reload();
            }
        })
    });
}


function setupEditForm() {
    const saveBtn = document.getElementById('save-enrollment-btn');
    if (!saveBtn) throw new Error('Save button not found!');

    saveBtn.addEventListener('click', function () {
        const form = document.getElementById('edit-enrollment-form');
        const enrollmentId = document.getElementById('edit-enrollment-id').value;
        const formData = new FormData(form);

        fetch(`/edit-enrollment/${enrollmentId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(async (response) => {

            if (response.status === 204) {
                window.modalFunctions.hideModal('edit-enrollment-modal');
                window.location.reload();
            } else if (response.status === 400) {
                const data = await response.json();
                // Display errors
                const errorsList = document.getElementById('edit-form-errors');
                errorsList.innerHTML = '';

                if (data.errors) {
                    const errors = JSON.parse(data.errors);
                    for (const field in errors) {
                        const li = document.createElement('li');
                        li.textContent = `${field}: ${errors[field][0].message}`;
                        errorsList.appendChild(li);
                    }
                    document.querySelector('#edit-enrollment-form .form-errors').style.display = 'block';
                }
            } else if (response.status === 500) {
                const data = await response.json();
                // Log error
                console.error("Failed to edit enrollment", data);
                // Display error
                alert("Failed to edit enrollment. The dashboard will restart after you acknowledge this message.");
                window.location.reload();
            }
        })
    });
}

// Function to handle form submission for deleting an enrollment
function setupDeleteForm() {
    const deleteBtn = document.getElementById('confirm-enrollment-delete-btn');
    if (!deleteBtn) throw new Error('Confirm button not found!');

    deleteBtn.addEventListener('click', function () {
        const enrollmentId = document.getElementById("delete-enrollment-id").value;
        const form = document.getElementById("delete-enrollment-form");
        const formData = new FormData(form);

        fetch(`delete-enrollment/${enrollmentId}/`, {
            method: 'POST',
            body: formData,   // Although we don't need to send any business data, we require this for the CSRF cookie
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(async (response) => {
            if (response.status === 204) {
                window.location.reload();
            } else if (response.status === 500) {
                const data = await response.json();
                // Log error
                console.error("Failed to delete enrollment", data);
                // Display error
                alert("Failed to delete enrollment. The dashboard will restart after you acknowledge this message.");
                window.location.reload();
            }
        })
    });
}

