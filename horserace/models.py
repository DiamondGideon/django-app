from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_(u"Пользователь"))
    balance = models.IntegerField(default=0, verbose_name=_(u"баланс"))

    def __str__(self):
        return "%s's profile" % self.user
    def get_balance(self):
        return self.balance
    def set_balance(self, new):
        self.balance = self.balance + new
        return self.balance


class Post(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name=_(u"Автор"))
    title = models.CharField(max_length=200, verbose_name=_(u"Титл"))
    text = models.TextField()
    win_coef = models.PositiveSmallIntegerField(default=0, verbose_name=_(u"Коэфициен на победу"))
    result = models.SmallIntegerField(null = True, verbose_name=_(u"результат"))
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True, verbose_name=_(u"дата публикации"))


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class RaceBet(models.Model):
        user = models.ForeignKey(User , verbose_name=_(u"пользователь"))
        bet = models.IntegerField(default=0, verbose_name=_(u"ставка"))
        result = models.CharField(max_length=20, verbose_name=_(u"результат"))
        race = models.ForeignKey(Post, verbose_name=_(u"забег"))

        def __str__(self):
            return str(self.user.username)
