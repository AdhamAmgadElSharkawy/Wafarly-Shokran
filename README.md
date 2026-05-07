# Wafarly Shokran 💰

Wafarly Shokran is a comprehensive personal finance management web application built using **Python** and the **Django Framework**.  
It empowers users to track their income, monitor expenses, set financial goals, and visualize their budget through an intuitive dashboard and interactive charts.

This project highlights a robust MVT (Model-View-Template) architecture, demonstrating proficiency in backend web development, relational database management, and interactive frontend data visualization.

## Table of Contents
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Build & Run](#build--run)
- [Contributors](#Contributors)



## Demo



---

## Prerequisites

To build and run this project, you need:

- **Python 3.x**
- **pip** (Python package installer)
- **Git**

---

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AdhamAmgadElSharkawy/Wafarly-Shokran.git
    cd Wafarly-Shokran/backend
    ```

2. **Create and activate a virtual environment:**

    - **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    - **Linux/Mac:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

    *(Optional)* **Load mock data to test the dashboard:**
    ```bash
    python manage.py loaddata mock_data.json
    ```

---

## Technology Stack

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Data Visualization:** Chart.js
- **Database:** SQLite3

---

## Features

### Interactive Dashboard
- **Total Income & Expenses overview**
- **Savings Rate calculation**
- **Spending by Category (Pie Chart)**
- **Income vs Budget comparison (Bar Chart)**
- **Recent activity feed**

### Transaction Management
- **Add, edit, and delete Income/Expenses**
- **Categorize transactions** (Food, Housing, Transportation, etc.)

### Goal & Budget Tracking
- **Set monthly budgets**
- **Create financial goals**
- **Track progress towards goals**

### User Authentication & Profile
- **Secure Sign Up / Login**
- **User-specific data isolation**

---

## Build & Run

1. **Ensure your virtual environment is activated.**
2. **Run the Django development server:**

    ```bash
    python manage.py runserver
    ```

3. **Open your web browser and navigate to:**
    `http://127.0.0.1:8000/`

---

## Contributors

- **Adham Amgad Eid** – [GitHub Profile](https://github.com/AdhamAmgadElSharkawy)  
- **Mohammed Atef** – [GitHub Profile](https://github.com/MohmmedAtef)  
- **Adham Mohamed Megahed** – [GitHub Profile](https://github.com/Adham-Mohamed-Megahed)
- **Amir Mostafa** – [GitHub Profile](https://github.com/am16ir)
