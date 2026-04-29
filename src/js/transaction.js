const openBtn = document.getElementById("openModal");
const modal = document.getElementById("transactionModal");
const closeBtn = document.getElementById("closeModal");

// Open modal
openBtn.addEventListener("click", () => {
    modal.style.display = "flex";
});

// Close modal
closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

// Close when clicking outside
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});