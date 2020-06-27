from django.urls import path
from . import views

urlpatterns =[
    path('', views.vendorview.as_view(), name='vendor'),
    path('request/', views.Requestview.as_view(), name='request_merge'),
    path('request/ajax/update/', views.UpdateRequest.as_view(), name='crud_ajax_update'),
    path('test1/', views.CrudView.as_view(), name='crud_ajax'),
    path('test1/ajax/crud/create/', views.CreateCrudRequest.as_view(), name='crud_ajax_create'), 
    # path('login/', views.login, name='login_t'),
    path('request/<int:pk>/delete', views.RequestDelete.as_view(), name='request_delete'),
]