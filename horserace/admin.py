from django.contrib import admin
from .models import Post
from .models import UserProfile
from .models import RaceBet

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(RaceBet)
