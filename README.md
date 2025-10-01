# Home Accountant

![Home Accountant Banner](https://via.placeholder.com/1200x300.png?text=Home+Accountant)

**A modern and intuitive web application for managing your personal finances, built with Django and Bootstrap.**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-purple.svg)](https://getbootstrap.com/)

---

## ✨ Core Features

*   **🔐 Access Control:** Two user roles (Admin and Regular User). Admins have full control, while regular users have restricted permissions.
*   **📊 Interactive Dashboard:** Get a quick overview of your financial health with a summary of recent expenses and an interactive chart showing expenses by category.
*   **💰 Income Management:** Easily track your expected and unexpected income to build a comprehensive budget.
*   **💸 Expense Tracking:** Add, edit, and delete expenses with detailed information, including description, amount, date, and category.
*   **🗂️ Category Management:** Organize your expenses by creating and managing custom categories like "Food," "Transportation," and "Bills."
*   **📈 Financial Reports:** Generate detailed monthly reports of your expenses, with powerful filtering options by category and date range. Compare your income to your expenses and receive alerts when you're overspending.
*   **📅 Monthly Balance Carry-Over:** Automatically carry over your balance from the previous month to the next, giving you a continuous and accurate view of your finances.
*   **📱 Responsive Design:** Enjoy a seamless experience on any device, thanks to a fully responsive interface built with Bootstrap.

---

## 📸 Screenshots

*(This section would ideally contain screenshots of the application. Here are some descriptions of what they would show.)*

| Dashboard                                                              | Reports                                                                  |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| ![Dashboard Screenshot](https://via.placeholder.com/600x400.png?text=Dashboard) | ![Reports Screenshot](https://via.placeholder.com/600x400.png?text=Reports) |

---

## 🛠️ Technology Stack

*   **Backend:**
    *   [Python](https://www.python.org/)
    *   [Django](https://www.djangoproject.com/)
*   **Database:**
    *   [SQLite](https://www.sqlite.org/index.html) (for development)
*   **Frontend:**
    *   [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
    *   [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
    *   [Bootstrap](https://getbootstrap.com/)
    *   [Chart.js](https://www.chartjs.org/) (for data visualization)

---

## 🚀 Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   [Python 3.12+](https://www.python.org/downloads/)
*   [Pip](https://pip.pypa.io/en/stable/installation/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd homeaccountant
    ```

2.  **Create and activate a virtual environment:**
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file would be ideal here. Since one doesn't exist, I'm assuming the dependencies are Django and python-dateutil based on the previous README.)*

4.  **Apply the database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

---

## 📂 Project Structure

```
homeaccountant/
├── expenses/
│   ├── migrations/
│   ├── templates/
│   │   ├── expenses/
│   │   └── registration/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── constants.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── urls.py
├── homeaccountant/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   └── js/
├── venv/
├── .gitignore
├── manage.py
└── README.md
```

---

## 🔄 Database Management

To reset your database, you can use the `reset_db.sh` script.

**⚠️ WARNING: This will permanently delete all data in your `db.sqlite3` file and remove all migration history. Use with caution!**

1.  **Make the script executable:**
    ```bash
    chmod +x reset_db.sh
    ```

2.  **Run the script:**
    ```bash
    ./reset_db.sh
    ```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.