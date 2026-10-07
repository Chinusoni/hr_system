import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import AttendanceRequest, EmployeeProfile

# Register the Employee Profile so HR can edit user details
admin.site.register(EmployeeProfile)

# Create the CSV Export Action
@admin.action(description="Export selected requests to CSV")
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="HR_Leave_Report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee Name', 'Employee ID', 'Department', 'Leave Type', 'Start Date', 'End Date', 'Reason', 'Status'])
    
    # Notice we use 'queryset' here instead of all records. 
    # This allows HR to check specific boxes and only export those!
    for leave in queryset:
        emp_name = "N/A"
        emp_id = "N/A"
        dept = "N/A"
        if hasattr(leave.employee, 'employeeprofile'):
            emp_name = leave.employee.employeeprofile.full_name
            emp_id = leave.employee.employeeprofile.employee_id
            dept = leave.employee.employeeprofile.department
            
        writer.writerow([
            emp_name, 
            emp_id, 
            dept, 
            leave.get_leave_type_display(), 
            leave.start_date, 
            leave.end_date, 
            leave.reason, 
            leave.status
        ])
    return response

# Attach the Action and create a beautiful Admin view
class AttendanceRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'leave_type') # 🌟 Bonus: Adds a filter sidebar for HR!
    actions = [export_as_csv]

# Register the Attendance Request with our new custom Admin class
admin.site.register(AttendanceRequest, AttendanceRequestAdmin)