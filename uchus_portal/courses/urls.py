from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.dashboard, name='dashboard'),
    path('apply/', views.create_application, name='apply'),
    path('review/<int:application_id>/', views.add_review, name='add_review'),
    path('panel/', views.admin_panel, name='admin_panel'),
    path('panel/applications/create/', views.admin_application_create, name='admin_application_create'),
    path('panel/applications/<int:application_id>/edit/', views.admin_application_edit, name='admin_application_edit'),
    path('panel/applications/<int:application_id>/delete/', views.admin_application_delete, name='admin_application_delete'),
    path('panel/login/', views.admin_login, name='admin_login'),
    path('panel/logout/', views.admin_logout, name='admin_logout'),
]
