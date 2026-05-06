const openBtn = document.getElementById("openModal");
const modal = document.getElementById("transactionModal");
const closeBtn = document.getElementById("closeModal");

const incomeBtn = document.getElementById("incomeBtn");
const expenseBtn = document.getElementById("expenseBtn");

const form = document.getElementById("transactionForm");
const categorySelect = document.getElementById("categorySelect");

let editId = null;

// Open modal
openBtn.addEventListener("click", () => {
    editId = null;
    form.reset();// added
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


// CSRF
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Submit (Add / Edit)
form.addEventListener("submit", function (e) {
    e.preventDefault();

    const description = document.getElementById("descInput").value;
    const amount = document.getElementById("amountInput").value;
    const category = categorySelect.value;
    const type = incomeBtn.classList.contains("active-type") ? "i" : "e";

    let url = "/transactions/add/";
    if (editId) {
        url = `/transactions/edit/${editId}/`;
    }

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ description, amount, category, type })
    })
        .then(res => res.json())
        .then(() => location.reload());
});

// Delete
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("delete-btn")) {
        const row = e.target.closest("tr");
        const id = row.dataset.id;

        fetch(`/transactions/delete/${id}/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCSRFToken() }
        })
            .then(res => res.json())
            .then(() => row.remove());
    }
});

// Edit
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("edit-btn")) {
        const row = e.target.closest("tr");
        const id = row.dataset.id;

        fetch(`/transactions/edit/${id}/`)
            .then(res => res.json())
            .then(data => {
                modal.style.display = "flex"; //block

                document.getElementById("descInput").value = data.description;
                document.getElementById("amountInput").value = data.amount;

                loadCategories(data.type === "i" ? "income" : "expense");
                categorySelect.value = data.category;

                editId = id;
            });
    }
});

//for filter
const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");

function filterTransactions() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    const rows = document.querySelectorAll("#tableBody tr");

    rows.forEach(row => {
        const description = row.cells[1].textContent.toLowerCase();
        const category = row.cells[2].textContent;

        const matchesSearch = description.includes(searchTerm);
        const matchesCategory = (selectedCategory === "all" || category === selectedCategory);

        if (matchesSearch && matchesCategory) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

searchInput.addEventListener("input", filterTransactions);


categoryFilter.addEventListener("change", filterTransactions);