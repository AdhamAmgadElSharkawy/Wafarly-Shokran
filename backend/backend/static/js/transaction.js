const openBtn = document.getElementById("openModal");
const modal = document.getElementById("transactionModal");
const closeBtn = document.getElementById("closeModal");

const incomeBtn = document.getElementById("incomeBtn");
const expenseBtn = document.getElementById("expenseBtn");

// Open modal
openBtn.addEventListener("click", () => {
    modal.style.display = "flex";
    loadCategories("income");
});

// Close modal
closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

// Categories
const incomeCategories = ["Salary", "Bonus", "Investment"];
const expenseCategories = ["Food", "Transport", "Shopping", "Housing"];

const categorySelect = document.getElementById("categorySelect");

function loadCategories(type) {
    categorySelect.innerHTML = "";

    let list = type === "income" ? incomeCategories : expenseCategories;

    list.forEach(cat => {
        let option = document.createElement("option");
        option.textContent = cat;
        categorySelect.appendChild(option);
    });

    incomeBtn.classList.remove("active-type");
    expenseBtn.classList.remove("active-type");

    if (type === "income") {
        incomeBtn.classList.add("active-type");
    } else {
        expenseBtn.classList.add("active-type");
    }
}

incomeBtn.onclick = () => loadCategories("income");
expenseBtn.onclick = () => loadCategories("expense");