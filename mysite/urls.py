from django.contrib import admin
from django.urls import path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.loginn,name="login"),
    path('index/',views.index,name="index"),
    path('addStudent/',views.addStudent,name="addStudent"),
    path('facultyEnroll/',views.facultyEnroll,name="facultyEnroll"),
    path('login/',views.loginn,name="login"),
    path('attendance/',views.attendance,name="attendance"),
    path('report/',views.report,name="report"),
    path('month_report/',views.month_report,name="month_report")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)