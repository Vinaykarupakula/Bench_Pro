from django.shortcuts import render, redirect
from app.models import Employee, Blog
from app.forms import BlogForm
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db import connection
import subprocess, shlex
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    return render(request, "app/index.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "New user created! Please sign in.")
            return redirect('app:index')
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form":form})



@login_required
def home(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        emp_name = request.POST.get("emp_name")
        emp_status = request.POST.get("emp_status")
        emp_type = request.POST.get("emp_type")
        skill_set = request.POST.get("skill_set")
        department = request.POST.get("department")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        customer_name = request.POST.get("customer_name")

        # Saving to DB using Django ORM - the best way
        Employee.objects.create(emp_id=emp_id, emp_name=emp_name,
        emp_status=emp_status, emp_type=emp_type,skill_set= skill_set,department=department,start_date=start_date,end_date=end_date, customer_name=customer_name)

        # # Direct SQL Queries - the wrong way
        # cursor = connection.cursor()
        # query = "INSERT INTO app_employee (emp_id, first_name, last_name, age, sex, department, designation) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (emp_id, first_name, last_name, age, sex, department, designation)
        # cursor.execute(query)

        # # Direct SQL Queries - the correct way
        # cursor = connection.cursor()
        # cursor.execute("INSERT INTO app_employee (emp_id, first_name, last_name, age, sex, department, designation) VALUES (%s, %s, %s, %s, %s, %s, %s)", [emp_id, first_name, last_name, age, sex, department, designation])

        return redirect("app:employees")
    else:
        # Fetch all employees using Django ORM
        employees = Employee.objects.all()

        return render(request, 'app/employees.html',
        {"employees":employees})

@login_required
def employees(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        emp_name = request.POST.get("emp_name")
        emp_status = request.POST.get("emp_status")
        emp_type = request.POST.get("emp_type")
        skill_set = request.POST.get("skill_set")
        department = request.POST.get("department")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        customer_name = request.POST.get("customer_name")

        # Saving to DB using Django ORM - the best way
        Employee.objects.create(emp_id=emp_id, emp_name=emp_name,
        emp_status=emp_status, emp_type=emp_type,skill_set= skill_set,department=department,start_date=start_date,end_date=end_date, customer_name=customer_name)

        # # Direct SQL Queries - the wrong way
        # cursor = connection.cursor()
        # query = "INSERT INTO app_employee (emp_id, first_name, last_name, age, sex, department, designation) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (emp_id, first_name, last_name, age, sex, department, designation)
        # cursor.execute(query)

        # # Direct SQL Queries - the correct way
        # cursor = connection.cursor()
        # cursor.execute("INSERT INTO app_employee (emp_id, first_name, last_name, age, sex, department, designation) VALUES (%s, %s, %s, %s, %s, %s, %s)", [emp_id, first_name, last_name, age, sex, department, designation])

        return redirect("app:employees")
    else:
        # Fetch all employees using Django ORM
        employees = Employee.objects.all()

        return render(request, 'app/employees.html',
        {"employees":employees})

@login_required
@csrf_exempt
def search_employees(request):
    if request.is_ajax():
        search_term = request.POST.get('searchTerm')

        # Searching employees using Django ORM - the best way
        employees = Employee.objects.filter(first_name__icontains=search_term)

        # # Searching employees using raw() - the wrong way
        # query = "SELECT * FROM app_employee WHERE first_name ILIKE '%s';" % search_term
        # employees = Employee.objects.raw(query)

        # # Searching employees using raw() - the correct way
        # employees = Employee.objects.raw('SELECT * FROM app_employee WHERE first_name ILIKE %s;',[search_term])

        # # Searching employees using extra() - the wrong way
        # employees = Employee.objects.extra(where=["first_name ILIKE '%s'" % search_term])

        # # Searching employees using extra() - the correct way
        # employees = Employee.objects.extra(where=['first_name ILIKE %s'], params=[search_term])

        html = render_to_string('app/search_employees.html',
        {'employees':employees})

        return HttpResponse(html)

# @login_required
# def dns_lookup(request):
#     if request.method == "POST":
#         domain_name = request.POST.get("domain_name")

        # # DNS Lookup - the wrong way
        # command = "nslookup {}".format(domain_name)
        # output = subprocess.check_output(command, shell=True, encoding='UTF-8')
        # return render(request, 'app/dns_lookup.html', {'output':output,
        # 'domain_name':domain_name})

        # # DNS Lookup - the better way
        # try:
        #     safe_domain_name = shlex.quote(domain_name)
        #     command = "nslookup {}".format(safe_domain_name)
        #     output = subprocess.check_output(command, shell=True, encoding='UTF-8')
        #
        #     return render(request, 'app/dns_lookup.html', {'output':output,
        #     'domain_name':domain_name})
        # except subprocess.CalledProcessError:
        #     return render(request, 'app/dns_lookup.html', {'output':"Invalid Input",
        #     'domain_name':domain_name})


        # DNS Lookup - the best way - without shell=True
        # try:
        #     raw_command = "nslookup {}".format(domain_name)
        #     safe_command = shlex.split(raw_command)
        #     print(safe_command)
        #     output = subprocess.check_output(safe_command, encoding='UTF-8')

        #     return render(request, 'app/dns_lookup.html', {'output':output,
        #     'domain_name':domain_name})
        # except subprocess.CalledProcessError:
        #     return render(request, 'app/dns_lookup.html', {'output':"Invalid Input",
        #     'domain_name':domain_name})

        ## Note - Avoid using the deprecated os module

    # else:
    #     return render(request, "app/dns_lookup.html")


@login_required
def filter_by_date(request):
    if request.method == 'GET':
        start_date= request.GET.get('start_date')
        print('sd',start_date)
        end_date= request.GET.get('end_date')

        submitbutton= request.GET.get('submit')
        if start_date and end_date:
            results= Employee.objects.filter(start_date__gte = start_date,end_date__lte=end_date)
            context={'results': results,
                     'submitbutton': submitbutton,
                    }

            return render(request, 'app/search_employees.html', context)

        else:
            return render(request, 'app/search_employees.html')

    else:
        return render(request, 'app/search_employees.html')


@login_required
def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(emp_name__icontains=query) | Q(department__icontains=query)

            results= Employee.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'app/search_employees.html', context)

        else:
            return render(request, 'app/search_employees.html')

    else:
        return render(request, 'app/search_employees.html')
