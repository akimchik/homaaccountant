from django.contrib.auth.forms import UserCreationForm
from .models import User

# Custom form for user creation, extending Django's built-in UserCreationForm.
# This form is used to allow users to sign up with an additional 'role' field.
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Specifies the custom User model to be used for this form.
        model = User
        # Includes all default fields from UserCreationForm, plus the custom 'role' field.
        fields = UserCreationForm.Meta.fields + ('role',)