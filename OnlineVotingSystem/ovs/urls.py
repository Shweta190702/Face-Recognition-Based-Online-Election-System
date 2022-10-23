from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('profile', views.profile, name="profile"),
    path('vote', views.vote, name="vote"),
    path('adminPanel', views.adminPanel, name="adminPanel"),
    path('adminSignin', views.adminSignin, name="adminSignin"),
    path('adminlogout', views.adminlogout, name="adminlogout"),
    path('adminTable', views.adminTable, name="adminTable"),
    path('giveVote', views.giveVote, name="giveVote"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)