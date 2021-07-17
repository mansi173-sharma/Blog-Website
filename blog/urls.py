from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/',views.post_details,name='post_details'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]