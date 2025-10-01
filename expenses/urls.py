from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DashboardView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView,
    IncomeListView, IncomeCreateView, IncomeUpdateView, IncomeDeleteView,
    SignUpView,
    ReportView
)

# Define URL patterns for the expenses application.
urlpatterns = [
    # Dashboard URL: The main landing page after login.
    path('', DashboardView.as_view(), name='dashboard'),

    # Account URLs: For user authentication.
    # Signup page.
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # Login page, using Django's built-in LoginView with a custom template.
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Logout functionality, using Django's built-in LogoutView with a custom confirmation template.
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout_confirm.html'), name='logout'),

    # Category URLs: For managing expense categories.
    # List all categories.
    path('categories/', CategoryListView.as_view(), name='category-list'),
    # Create a new category.
    path('categories/new/', CategoryCreateView.as_view(), name='category-create'),
    # Edit an existing category, identified by its primary key (pk).
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    # Delete an existing category, identified by its primary key (pk).
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # Expense URLs: For managing individual expenses.
    # List all expenses.
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    # Create a new expense.
    path('expenses/new/', ExpenseCreateView.as_view(), name='expense-create'),
    # Edit an existing expense, identified by its primary key (pk).
    path('expenses/<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense-update'),
    # Delete an existing expense, identified by its primary key (pk).
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),

    # Income URLs: For managing individual income entries.
    # List all incomes.
    path('incomes/', IncomeListView.as_view(), name='income-list'),
    # Create a new income.
    path('incomes/new/', IncomeCreateView.as_view(), name='income-create'),
    # Edit an existing income, identified by its primary key (pk).
    path('incomes/<int:pk>/edit/', IncomeUpdateView.as_view(), name='income-update'),
    # Delete an existing income, identified by its primary key (pk).
    path('incomes/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income-delete'),

    # Report URL: For viewing financial reports.
    path('reports/', ReportView.as_view(), name='report'),
]