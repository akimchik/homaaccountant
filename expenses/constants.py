# Define choices for roles and frequencies to improve maintainability and reduce magic strings.

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
)

FREQUENCY_CHOICES = (
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('annually', 'Annually'),
)

CURRENCY_CHOICES = (
    ('EUR', 'Euro (€)'), # Default currency
    ('UAH', 'Ukrainian Hryvnia (₴)'),
    ('USD', 'US Dollar ($)'),
    ('GBP', 'British Pound (£)'),
    ('JPY', 'Japanese Yen (¥)'),
    ('CAD', 'Canadian Dollar (C$)'),
    ('AUD', 'Australian Dollar (A$)'),
)
