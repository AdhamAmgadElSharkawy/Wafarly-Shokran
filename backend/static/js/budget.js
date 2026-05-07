let modal = document.getElementById("budget_modal");
let openModalBtn = document.getElementById("open_budget_modal_btn");
let closeModalBtn = document.getElementById("close_budget_modal_btn");
let cancelBtn = document.getElementById("cancel_budget_btn");

openModalBtn.addEventListener('click', () => {
    modal.classList.add('active');
});

closeModalBtn.addEventListener('click', () => {
    modal.classList.remove('active');
});

cancelBtn.addEventListener('click', () => {
    modal.classList.remove('active');
});

// Edit modal
function openEditModal(pk, categoryId, limit, period, alertEnabled) {
    document.getElementById('edit_budget_form').action = `/budget/edit/${pk}/`;
    document.getElementById('edit_budget_category').value = categoryId;
    document.getElementById('edit_budget_amount').value = limit;
    document.getElementById('edit_budget_period').value = period;
    document.getElementById('edit_budget_alert').checked = alertEnabled;
    document.getElementById('edit_budget_modal').classList.add('active');
}

document.getElementById('close_edit_budget_modal_btn').addEventListener('click', () => {
    document.getElementById('edit_budget_modal').classList.remove('active');
});

document.getElementById('cancel_edit_budget_btn').addEventListener('click', () => {
    document.getElementById('edit_budget_modal').classList.remove('active');
});