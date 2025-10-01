from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Expense, Category, Income, RecurringExpense
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
import json
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone # Import timezone
from dateutil.relativedelta import relativedelta # For easier month calculations

# View for user registration.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm  # Uses the custom form to include the 'role' field.
    template_name = 'registration/signup.html'  # Template for the signup form.
    success_url = reverse_lazy('login')  # Redirects to the login page upon successful registration.

# Dashboard view, accessible only to logged-in users.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/dashboard.html'  # Template for the dashboard.

    # Provides context data to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetches the 5 most recent expenses for the logged-in user.
        context['recent_expenses'] = Expense.objects.filter(user=user).order_by('-date')[:5]
        # Fetches the 5 most recent incomes for the logged-in user.
        context['recent_incomes'] = Income.objects.filter(user=user).order_by('-date')[:5]

        # Calculate current month's budget summary
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1)) - timedelta(days=1)

        monthly_expenses = Expense.objects.filter(
            user=user,
            date__gte=start_of_month,
            date__lte=end_of_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        monthly_incomes = Income.objects.filter(
            user=user,
            date__gte=start_of_month,
            date__lte=end_of_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        context['monthly_expenses'] = monthly_expenses
        context['monthly_incomes'] = monthly_incomes
        context['money_left'] = monthly_incomes - monthly_expenses

        # Calculate next month's prognosis
        next_month_start = start_of_month + relativedelta(months=1)
        next_month_end = (next_month_start + relativedelta(months=1)) - timedelta(days=1)

        # Projected recurring expenses for next month
        projected_recurring_expenses = 0
        recurring_expenses = RecurringExpense.objects.filter(user=user)
        for re in recurring_expenses:
            # Simple projection: if recurring expense is active in next month
            # This logic can be made more sophisticated for daily/weekly frequencies
            if re.start_date <= next_month_end and (re.end_date is None or re.end_date >= next_month_start):
                if re.frequency == 'monthly':
                    projected_recurring_expenses += re.amount
                elif re.frequency == 'annually':
                    projected_recurring_expenses += re.amount / 12 # Prorate annually to monthly
                # For daily/weekly, a more complex calculation would be needed
                # For simplicity, we'll only consider monthly and annually for now

        context['projected_recurring_expenses'] = projected_recurring_expenses
        context['prognosis_next_month'] = monthly_incomes - projected_recurring_expenses # Assuming income is stable

        # Calculates expenses grouped by category for charting.
        expenses_by_category = Expense.objects.filter(user=user)\
                                .values('category__name')\
                                .annotate(total_amount=Sum('amount'))\
                                .order_by('category__name')

        # Extracts labels (category names) and data (total amounts) for the chart.
        chart_labels = [item['category__name'] for item in expenses_by_category]
        chart_data = [float(item['total_amount']) for item in expenses_by_category]

        # Dumps chart data to JSON for use in JavaScript.
        context['chart_labels_json'] = json.dumps(chart_labels)
        context['chart_data_json'] = json.dumps(chart_data)

        return context

# Category Views
# List view for categories, accessible only to logged-in users.
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category  # Specifies the model to use.
    template_name = 'expenses/category_list.html'  # Template for displaying the list of categories.
    context_object_name = 'categories'  # Name of the context variable containing the list.

    # Returns all categories (admin can see all, regular users can only add).
    def get_queryset(self):
        return Category.objects.all()

# Create view for categories, accessible only to logged-in users.
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category  # Specifies the model to use.
    fields = ['name']  # Fields to be displayed in the form.
    template_name = 'expenses/category_form.html'  # Template for the category creation form.
    success_url = reverse_lazy('category-list')  # Redirects to the category list upon successful creation.

# Update view for categories, accessible only to admin users.
class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category  # Specifies the model to use.
    fields = ['name']  # Fields to be displayed in the form.
    template_name = 'expenses/category_form.html'  # Template for the category update form.
    success_url = reverse_lazy('category-list')  # Redirects to the category list upon successful update.

    # Checks if the logged-in user is an admin.
    def test_func(self):
        return self.request.user.role == 'admin'

# Delete view for categories, accessible only to admin users.
class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category  # Specifies the model to use.
    template_name = 'expenses/category_confirm_delete.html'  # Template for confirming category deletion.
    success_url = reverse_lazy('category-list')  # Redirects to the category list upon successful deletion.

    # Checks if the logged-in user is an admin.
    def test_func(self):
        return self.request.user.role == 'admin'

# Expense Views
# List view for expenses, accessible only to logged-in users.
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense  # Specifies the model to use.
    template_name = 'expenses/expense_list.html'  # Template for displaying the list of expenses.
    context_object_name = 'expenses'  # Name of the context variable containing the list.

    # Returns expenses filtered by the logged-in user.
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

# Create view for expenses, accessible only to logged-in users.
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense  # Specifies the model to use.
    fields = ['description', 'amount', 'date', 'category']  # Fields to be displayed in the form.
    template_name = 'expenses/expense_form.html'  # Template for the expense creation form.
    success_url = reverse_lazy('expense-list')  # Redirects to the expense list upon successful creation.

    # Associates the new expense with the logged-in user.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Update view for expenses, accessible only to the owner of the expense.
class ExpenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Expense  # Specifies the model to use.
    fields = ['description', 'amount', 'date', 'category']  # Fields to be displayed in the form.
    template_name = 'expenses/expense_form.html'  # Template for the expense update form.
    success_url = reverse_lazy('expense-list')  # Redirects to the expense list upon successful update.

    # Checks if the logged-in user is the owner of the expense.
    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user

# Delete view for expenses, accessible only to the owner of the expense.
class ExpenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Expense  # Specifies the model to use.
    template_name = 'expenses/expense_confirm_delete.html'  # Template for confirming expense deletion.
    success_url = reverse_lazy('expense-list')  # Redirects to the expense list upon successful deletion.

    # Checks if the logged-in user is the owner of the expense.
    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user

# Income Views
# List view for incomes, accessible only to logged-in users.
class IncomeListView(LoginRequiredMixin, ListView):
    model = Income  # Specifies the model to use.
    template_name = 'expenses/income_list.html'  # Template for displaying the list of incomes.
    context_object_name = 'incomes'  # Name of the context variable containing the list.

    # Returns incomes filtered by the logged-in user.
    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

# Create view for incomes, accessible only to logged-in users.
class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income  # Specifies the model to use.
    fields = ['description', 'amount', 'date']  # Fields to be displayed in the form.
    template_name = 'expenses/income_form.html'  # Template for the income creation form.
    success_url = reverse_lazy('income-list')  # Redirects to the income list upon successful creation.

    # Associates the new income with the logged-in user.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Update view for incomes, accessible only to the owner of the income.
class IncomeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Income  # Specifies the model to use.
    fields = ['description', 'amount', 'date']  # Fields to be displayed in the form.
    template_name = 'expenses/income_form.html'  # Template for the income update form.
    success_url = reverse_lazy('income-list')  # Redirects to the income list upon successful update.

    # Checks if the logged-in user is the owner of the income.
    def test_func(self):
        income = self.get_object()
        return self.request.user == income.user

# Delete view for incomes, accessible only to admin users.
class IncomeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Income  # Specifies the model to use.
    template_name = 'expenses/income_confirm_delete.html'  # Template for confirming income deletion.
    success_url = reverse_lazy('income-list')  # Redirects to the income list upon successful deletion.

    # Checks if the logged-in user is an admin.
    def test_func(self):
        return self.request.user.role == 'admin'

# Recurring Expense Views
# List view for recurring expenses, accessible only to logged-in users.
class RecurringExpenseListView(LoginRequiredMixin, ListView):
    model = RecurringExpense
    template_name = 'expenses/recurringexpense_list.html'
    context_object_name = 'recurring_expenses'

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)

# Create view for recurring expenses, accessible only to logged-in users.
class RecurringExpenseCreateView(LoginRequiredMixin, CreateView):
    model = RecurringExpense
    fields = ['description', 'amount', 'frequency', 'start_date', 'end_date']
    template_name = 'expenses/recurringexpense_form.html'
    success_url = reverse_lazy('recurringexpense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Update view for recurring expenses, accessible only to the owner.
class RecurringExpenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RecurringExpense
    fields = ['description', 'amount', 'frequency', 'start_date', 'end_date']
    template_name = 'expenses/recurringexpense_form.html'
    success_url = reverse_lazy('recurringexpense-list')

    def test_func(self):
        recurring_expense = self.get_object()
        return self.request.user == recurring_expense.user

# Delete view for recurring expenses, accessible only to the owner.
class RecurringExpenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RecurringExpense
    template_name = 'expenses/recurringexpense_confirm_delete.html'
    success_url = reverse_lazy('recurringexpense-list')

    def test_func(self):
        recurring_expense = self.get_object()
        return self.request.user == recurring_expense.user

# Report view, accessible only to logged-in users.
class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/report.html'  # Template for displaying financial reports.

    # Provides context data to the template, including filtered expenses, incomes, and financial summaries.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Retrieves filtering parameters from the GET request.
        category_id = self.request.GET.get('category')
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        # Initializes querysets for expenses and incomes for the current user.
        expenses = Expense.objects.filter(user=user)
        incomes = Income.objects.filter(user=user)

        # Filters expenses by category if a category is selected.
        if category_id:
            expenses = expenses.filter(category__id=category_id)
        
        # Filters by start date. Defaults to the last 30 days if no start date is provided.
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            expenses = expenses.filter(date__gte=start_date)
            incomes = incomes.filter(date__gte=start_date)
        else:
            start_date = datetime.now().date() - timedelta(days=30)
            expenses = expenses.filter(date__gte=start_date)
            incomes = incomes.filter(date__gte=start_date)

        # Filters by end date. Defaults to today if no end date is provided.
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            expenses = expenses.filter(date__lte=end_date)
            incomes = incomes.filter(date__lte=end_date)
        else:
            end_date = datetime.now().date()

        # Calculates total expenses and incomes for the filtered period.
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_incomes = incomes.aggregate(Sum('amount'))['amount__sum'] or 0

        # Adds data to the context for rendering in the template.
        context['expenses'] = expenses
        context['incomes'] = incomes
        context['total_expenses'] = total_expenses
        context['total_incomes'] = total_incomes
        context['balance'] = total_incomes - total_expenses
        context['categories'] = Category.objects.all()  # All categories for the filter dropdown.
        context['selected_category'] = int(category_id) if category_id else ''  # Retains selected category in filter.
        context['start_date'] = start_date_str if start_date_str else start_date.strftime('%Y-%m-%d')  # Retains start date.
        context['end_date'] = end_date_str if end_date_str else end_date.strftime('%Y-%m-%d')  # Retains end date.

        # Generates an alert if expenses exceed income.
        if total_expenses > total_incomes:
            context['alert'] = 'Your expenses exceed your income for this period!'
        
        return context