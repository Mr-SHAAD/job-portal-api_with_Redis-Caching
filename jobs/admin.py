from django.contrib import admin

from .models import Company, Job, Application

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'owner', 'created_at']
    search_fields = ['name', 'location']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'salary', 'is_active']
    search_fields = ['title', 'skills_required']
    list_filter = ['job_type', 'is_active']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status']
# Register your models here.
