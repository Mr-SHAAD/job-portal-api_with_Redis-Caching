from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    # Jobs
    path('jobs/', views.job_list),
    path('jobs/<int:pk>/', views.job_detail),
    path('jobs/search/', views.search_jobs),

    # Applications
    path('jobs/<int:pk>/apply/', views.apply_job),
    path('applications/my/', views.my_applications),

    # Companies
    path('companies/', views.company_list),
]