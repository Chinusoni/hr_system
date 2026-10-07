from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import csv
from django.http import HttpResponse
from .models import AttendanceRequest 
from .forms import AttendanceRequestForm, EmployeeRegistrationForm

def index(request):
    # If the user is logged in, grab their leave history
    if request.user.is_authenticated:
        my_leaves = AttendanceRequest.objects.filter(employee=request.user).order_by('-start_date')
        return render(request, 'index.html', {'leaves': my_leaves})
    
    # If they are a public visitor, just show the plain home page
    else:
        return render(request, 'index.html')

@login_required
def submit_leave_request(request):
    # If they are submitting the form...
    if request.method == 'POST':
        form = AttendanceRequestForm(request.POST)
        if form.is_valid():
            # Pause saving to attach the logged-in user!
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            
            # Send them to the success page
            return redirect('leave_success')
            
    # If they are just viewing the page or the form is invalid...
    else:
        form = AttendanceRequestForm()
        
    return render(request, 'leave_form.html', {'form': form})

def leave_request_success(request):
    return render(request, 'success.html')

def register_employee(request):
    if request.method == 'POST':
        # Swapped to your custom HR form here
        form = EmployeeRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            # Log the employee in automatically right after they sign up!
            login(request, user)
            return redirect('index')
    else:
        # Swapped to your custom HR form here too
        form = EmployeeRegistrationForm() 
        
    return render(request, 'registration/register.html', {'form': form})

@login_required
def export_leaves_csv(request):
    # Security Check: Only let HR admins (staff) download the company data!
    if not request.user.is_staff:
        return HttpResponse("Unauthorized: Only HR can download this file.", status=401)

    # Tell the browser to expect a downloadable CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="HR_Leave_Report.csv"'

    writer = csv.writer(response)
    
    # Write the Header row for the spreadsheet
    writer.writerow(['Employee Name', 'Employee ID', 'Department', 'Leave Type', 'Start Date', 'End Date', 'Reason', 'Status'])

    # Get all leave requests, newest first
    all_leaves = AttendanceRequest.objects.all().order_by('-start_date')

    # Loop through the database and write each request as a row
    for leave in all_leaves:
        # Safely grab the extra HR profile data if it exists
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