from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.vendorview.as_view(), name='vendor'),
    path('request/', views.Requestview.as_view(), name='request_merge'),
    path('test1/', views.CrudView.as_view(), name='crud_ajax'),
    path('test1/ajax/crud/create/', views.CreateCrudRequest.as_view(), name='crud_ajax_create'), 
    path('test1/ajax/update/', views.UpdateCrudRequest.as_view(), name='crud_ajax_update'),
    path('test1/ajax/delete/', views.DeletCrudRequest.as_view(), name='crud_ajax_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]