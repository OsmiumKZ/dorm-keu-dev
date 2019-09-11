from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('auth/account/', views.auth_account),
    path('orphanage/', views.OrphanageAPIView.as_view()),
    path('guardian/', views.GuardianAPIView.as_view()),
    path('accounts/student/<int:pk>/', views.AccountStudentViewAPI.as_view()),
    path('reports/sort/', views.ReportsSortViewAPI.as_view()),
    path('requests/sort/', views.RequestsSortViewAPI.as_view()),
    path('reports/', views.ReportsViewAPI.as_view()),
    path('report/<int:pk>/', views.ReportViewAPI.as_view()),
    path('requests/', views.RequestsViewAPI.as_view()),
    path('request/<int:pk>/', views.RequestViewAPI.as_view()),
    path('db/', views.db_base),
    path('statistic/', views.statistic),
    path('floor/<int:pk>/rooms/', views.rooms_floor),
    path('doc/download/direction/<int:pk>/', views.send_direction_file),
    path('doc/download/request/<int:pk>/', views.send_request_file),

    path('auth/admin/', obtain_auth_token)
]
