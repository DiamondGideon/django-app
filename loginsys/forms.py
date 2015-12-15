from django import forms
from django.contrib.auth.models import User
from horserace.models import UserProfile
from django.utils.translation import ugettext as _

class MyUserCreateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=(u"Пароль"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=(u"Подтверждение пароля"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "email", "is_staff",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
         class Meta:
            model = UserProfile
            fields =("balance",)