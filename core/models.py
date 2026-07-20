from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from decimal import Decimal

class Tenant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    domain_restriction = models.CharField(max_length=100, help_text="e.g., encrypt.com")
    currency_default = models.CharField(max_length=3, default="GBP")

    def __str__(self):
        return self.name

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin / In-house Head'
        CREATOR = 'CREATOR', 'Talent / Creator'
        FREELANCER = 'FREELANCER', 'Talent / Freelancer'

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="users")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FREELANCER)
    is_ex_talent = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.role == self.Role.ADMIN and self.tenant and not self.email.endswith(self.tenant.domain_restriction):
            raise ValidationError(f"Admins for this tenant must use @{self.tenant.domain_restriction}")

class Project(models.Model):
    class Phase(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        PRODUCTION = 'PRODUCTION', 'Filming and Production'
        APPROVED = 'APPROVED', 'Approved / Complete'

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    project_type = models.CharField(max_length=50, default="tv")
    genre = models.CharField(max_length=50, blank=True)
    budget_cap = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('500000.00'))
    production_costs = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    gross_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    current_phase = models.CharField(max_length=50, choices=Phase.choices, default=Phase.NOT_STARTED)

    def __str__(self):
        return f"[{self.tenant.name}] {self.title}"

class Pod(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, limit_choices_to={'role': User.Role.ADMIN}, related_name="admin_pods")
    creators = models.ManyToManyField(User, limit_choices_to={'role': User.Role.CREATOR}, related_name="creator_pods")
    projects = models.ManyToManyField(Project, related_name="pod_assignments")

class Proposal(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="proposals")
    title = models.CharField(max_length=255)
    project_type = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Duration in months")
    description = models.TextField(max_length=250)
    est_budget = models.DecimalField(max_digits=12, decimal_places=2)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposals")
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)