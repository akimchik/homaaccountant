# Personal Expense Tracker

A simple and intuitive web application for managing personal finances, built with Django and Bootstrap.

## Core Features:

*   **Access Control:** Two categories of users (admin and regular user). Admins can remove categories and incomes, while regular users can only add.
*   **Dashboard:** A summary view of recent expenses and a chart showing expenses by category.
*   **Income Setup:** Manage expected and unexpected incomes that form your budget.
*   **Expense Management:** Add, edit, and delete expenses with description, amount, date, and category.
*   **Category Management:** Create and manage expense categories (e.g., "Food", "Transportation", "Bills").
*   **Reporting:** View monthly reports of expenses, filterable by category and date range, with comparison to income and alerts for overspending.

## Technology Stack:

*   **Backend:** Django (Python)
*   **Database:** SQLite (for simplicity and ease of setup)
*   **Frontend:** Bootstrap (for a clean and responsive user interface), Chart.js (for data visualization)

## Setup Instructions:

Follow these steps to get the project up and running on your local machine.

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd homeaccountant
    ```

2.  **Create a Virtual Environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install Django
    ```

5.  **Apply Database Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Collect Static Files:**
    ```bash
    python manage.py collectstatic --noinput
    ```

8.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

## Database Management:

To reset your database (e.g., for development or to clear all data), you can use the `reset_db.sh` script.

**WARNING: This script will permanently delete all data in your `db.sqlite3` file and remove all migration history. Use with caution!**

1.  **Make the script executable (if you haven't already):**
    ```bash
    chmod +x reset_db.sh
    ```

2.  **Run the script:**
    ```bash
    ./reset_db.sh
    ```

    This script will:
    *   Delete the `db.sqlite3` file.
    *   Remove all migration files (except `__init__.py`).
    *   Recreate the virtual environment and reinstall Django.
    *   Reapply all migrations.
    *   Collect static files.

    After running the script, a development superuser with username 'admin' and password 'admin' will be created automatically.

## Project Structure:

*   `homeaccountant/`: Main Django project directory.
    *   `settings.py`: Project settings, including database configuration, installed apps, and static files setup.
    *   `urls.py`: Main URL routing for the project.
*   `expenses/`: Django app for managing expenses, incomes, and categories.
    *   `models.py`: Defines the database models (`User`, `Category`, `Expense`, `Income`).
    *   `views.py`: Contains the logic for handling web requests and returning responses (CRUD operations, dashboard, reports).
    *   `urls.py`: URL routing specific to the `expenses` app.
    *   `forms.py`: Custom forms, such as `CustomUserCreationForm`.
    *   `templates/expenses/`: HTML templates for the `expenses` app.
        *   `base.html`: Base template extending Bootstrap, used by other templates.
        *   `dashboard.html`: Dashboard view with recent expenses and expense chart.
        *   `category_list.html`, `category_form.html`, `category_confirm_delete.html`: Templates for category management.
        *   `expense_list.html`, `expense_form.html`, `expense_confirm_delete.html`: Templates for expense management.
        *   `income_list.html`, `income_form.html`, `income_confirm_delete.html`: Templates for income management.
        *   `report.html`: Template for financial reports with filtering options.
    *   `templates/registration/`: Templates for user authentication.
        *   `signup.html`: User registration form.
        *   `login.html`: User login form.
*   `static/`: Directory for static assets (CSS, JavaScript, images) collected from apps.
    *   `css/`: Contains `bootstrap.min.css` and `style.css` (custom styles).
    *   `js/`: Contains `bootstrap.bundle.min.js` and `chart.min.js`.
*   `staticfiles/`: Directory where `collectstatic` gathers all static files for deployment.
*   `venv/`: Python virtual environment directory.

## Usage:

1.  **Access the Application:** Once the server is running, open your web browser and go to `http://127.0.0.1:8000/`.
2.  **Register/Login:** Create a new user account via the "Sign Up" link on the login page, or log in with an existing account (including the superuser you created).
3.  **Logout:** To log out, click the "Logout" button in the navigation bar. You will be prompted to confirm your logout. After logging out, you will be redirected to the login page, where you can choose to log in again or sign up for a new account.
3.  **Manage Categories:** Navigate to the "Categories" section to add, edit, or delete expense categories. Only admin users can delete categories.
4.  **Manage Expenses:** Go to the "Expenses" section to record your spending. You can add new expenses, specifying description, amount, date, and category.
5.  **Manage Incomes:** Visit the "Incomes" section to add your income sources. Only admin users can delete incomes.
6.  **View Dashboard:** The dashboard provides a quick overview of your recent expenses and a pie chart visualizing expenses by category.
7.  **Generate Reports:** Use the "Reports" section to generate financial reports. You can filter by category and date range to see your total expenses, total income, and balance for a specific period. Alerts will be shown if expenses exceed income.
