from django.shortcuts import render,HttpResponse
from .models import Employee,Department,Role
from django.db.models import Q
# index views function
def index(request):
    return render(request,'index.html')

#view function to display all employees
def all_emp(request):
    
    emps=Employee.objects.all()  #retrieve employee from database
    context={
        'emps':emps #json format
    }
    print(context)
    return render(request,'all_emp.html',context)


#view function to display add employees
def add_emp(request):
    if request.method == 'POST': #post method used
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        salary=request.POST['salary']
        bonus=request.POST['bonus']
        phone=request.POST['phone']
        hire_date=request.POST['hire_date']
        dept_name=request.POST['dept']
        role_name=request.POST['role']
        
        
         # Get or create Role or department
        dept_instance, created = Department.objects.get_or_create(name=dept_name)
        
       
        role_instance, created = Role.objects.get_or_create(name=role_name)

        # Create the Employee instance with the Department and Role instances
        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            role=role_instance,
            dept=dept_instance,
            hire_date=hire_date
        )
        new_emp.save()

        return render(request, 'add_emp.html', {'message': 'Employee added successfully'})

    elif request.method == 'GET':
        return render(request, 'add_emp.html')

    else:
        return HttpResponse("An exception occurred")

def remove_emp(request, emp_id=0): #first argument request ligeko 2nd argument emp_id=0 default value ligeko
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Please enter a valid employee id")

    emps = Employee.objects.all()
    context = {     #queryset operation 
        'emps': emps
    }  
    return render(request, 'remove_emp.html', context)



def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')

        # Start with the full queryset
        emps = Employee.objects.all()

        # Applying filters based on user input
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name)) # for cases
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {
            'emps': emps
        }

        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    
    else:
        return HttpResponse("Exception occurred")

    return render(request, 'filter_emp.html')