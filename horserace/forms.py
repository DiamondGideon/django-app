from django import forms
from .models import Post
from .models import RaceBet
from django.utils.translation import ugettext as _

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'win_coef')

class BetForm(forms.ModelForm):

    error_messages = {
        'bet_mismatch': ("U dont have enoth cash."),
    }

    def __init__(self,*args,**kwargs):
            self.balance = kwargs.pop('balance')
            super(BetForm,self).__init__(*args,**kwargs)

    class Meta:
        model = RaceBet
        fields = ('result',)


    bet = forms.IntegerField(label=_(u"ставка"),
        help_text=("Make a bet."))
    def cleaned_bet(self):
        bet = self.cleaned_data.get("bet")
        if bet > self.balance :
            raise forms.ValidationError(
                self.error_messages['bet_mismatch'],
                code='bet_mismatch',
            )
        return bet

    def save(self, commit=True):
        betf = super(BetForm, self).save(commit=False)
        betf.bet = (self.cleaned_data["bet"])
        if commit:
            betf.save()
        return betf

class ResultForm(forms.ModelForm):
    class Meta:
         model = Post
         fields = ('result',)

    # RESULT = (
    #    (1, ("Survive")),
    #    (2, ("Die")),
    #      )
    # pick = forms.ChoiceField(choices = RESULT)

