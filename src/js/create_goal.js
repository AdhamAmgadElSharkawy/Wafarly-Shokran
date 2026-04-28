let modal = document.getElementById("goal_modal");
let openModelBtn = document.getElementById("open_modal_btn");
let closeModelBtn = document.getElementById("close_modal_btn");
let submitBtn = document.getElementById("submit_btn");
let cancelBtn = document.getElementById("cancel_btn");

openModelBtn.addEventListener('click', () => {
    modal.classList.add('active');
});

closeModelBtn.addEventListener('click', () => {
    modal.classList.remove('active');
});

cancelBtn.addEventListener('click', () => {
    modal.classList.remove('active');
});