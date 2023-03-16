from django.urls import path
from . import views

urlpatterns = [
    path('', views.GroupsListView.as_view(), name='home'),
    path('groups/<slug>', views.GroupsDetailView.as_view(), name='group'),
    path('groups/<slug>/<slug_app>', views.AppsDetailView.as_view(), name='app'),
    path('groups/', views.groups, name='groups'),
]