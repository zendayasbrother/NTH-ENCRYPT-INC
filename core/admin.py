from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tenant, User, Proposal, Project, Pod


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin to display Tenant and Role attributes."""

    fieldsets = UserAdmin.fieldsets + (
        ("Encrypt Workspace Info", {"fields": ("tenant", "role")}),
    )
    list_display = [
        "username",
        "email",
        "role",
        "tenant",
        "is_staff",
        "is_superuser",
    ]
    list_filter = ["role", "tenant", "is_staff"]


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ["name", "domain_restriction", "currency_default"]


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "tenant",
        "project_type",
        "genre",
        "submitted_by",
        "est_budget",
    ]
    list_filter = ["tenant", "project_type", "genre"]
    search_fields = ["title", "description"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "tenant", "status", "created_at"]
    list_filter = ["tenant", "status"]


@admin.register(Pod)
class PodAdmin(admin.ModelAdmin):
    list_display = ["name", "tenant", "created_at"]
# Register your models here.

