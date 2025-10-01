from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model to extend Django's default User with a role field.
class User(AbstractUser):
    # Choices for the user's role.
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    # The role of the user, defaulting to 'user'.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

# Model to represent expense categories.
class Category(models.Model):
    # The name of the category (e.g., 'Food', 'Transportation').
    name = models.CharField(max_length=100)

    # String representation of the Category object.
    def __str__(self):
        return self.name

# Model to represent individual expenses.
class Expense(models.Model):
    # A brief description of the expense.
    description = models.CharField(max_length=255)
    # The amount of the expense, allowing for decimal values.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # The date when the expense occurred.
    date = models.DateField()
    # Foreign key to the Category model, indicating the category of the expense.
    # If a category is deleted, all associated expenses will also be deleted (CASCADE).
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Foreign key to the custom User model, linking the expense to a specific user.
    # If a user is deleted, all their expenses will also be deleted (CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # String representation of the Expense object.
    def __str__(self):
        return f'{self.description} - {self.amount}'

# Model to represent individual income entries.
class Income(models.Model):
    # A brief description of the income source.
    description = models.CharField(max_length=255)
    # The amount of the income, allowing for decimal values.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # The date when the income was received.
    date = models.DateField()
    # Foreign key to the custom User model, linking the income to a specific user.
    # If a user is deleted, all their incomes will also be deleted (CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # String representation of the Income object.
    def __str__(self):
        return f'{self.description} - {self.amount}'