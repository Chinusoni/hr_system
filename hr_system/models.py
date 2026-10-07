from django.db import models
from django.contrib.auth.models import User

# ---------------------------------------------------------
# 1. THE ATTENDANCE REQUEST MODEL
# ---------------------------------------------------------
class AttendanceRequest(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)

    LEAVE_CHOICES = [
        ('FULL', 'Full-day leave'),
        ('HALF', 'Half-day leave'),
        ('WFH', 'Work From Home'),
    ]
    leave_type = models.CharField(max_length=4, choices=LEAVE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"

# ---------------------------------------------------------
# 2. THE EMPLOYEE PROFILE MODEL
# ---------------------------------------------------------
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    
    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('SALES', 'Sales'),
        ('OPS', 'Operations'),
        ('FIN', 'Finance'),
    ]
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return f"{self.full_name} ({self.employee_id}) - {self.department}"