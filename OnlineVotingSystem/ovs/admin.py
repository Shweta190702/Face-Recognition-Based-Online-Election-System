from django.contrib import admin
from .models import UserProfile
# from .models import Vote
from .models import Party
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Party)
# admin.site.register(Vote)