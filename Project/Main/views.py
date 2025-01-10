from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.conf import settings
from .models import *
from .forms import *
import os


def main(request):
    return render(request, 'main.html', {})

def machine(request):
    machine = Machine.objects.all()
    context = {
        "machines": machine
    }
    return render(request, 'machine.html', context)

def create_machine(request):
    if request.method == 'POST':
        form = MachineCreateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/machines/')
        else:
            print("Errors:", form.errors)
    else:
        form = MachineCreateForm()

    client_group = Group.objects.get(name='Client')
    clients = User.objects.filter(groups=client_group)
    service_company = Service_company.objects.all()
    equipment_model = Technical_handbook.objects.all()
    engine_model = Engine_handbook.objects.all()
    transmission_model = Transmission_handbook.objects.all()
    drive_axle_model = Drive_axle_handbook.objects.all()
    steerable_axle_model = Steerable_axle_handbook.objects.all()

    context = {
        'form': form,
        'equipment_models': equipment_model,
        'engine_models': engine_model,
        'transmission_models': transmission_model,
        'drive_axle_models': drive_axle_model,
        'steerable_axle_models': steerable_axle_model,
        'services_company': service_company,
        'clients': clients
    }
    return render(request, 'machine_create.html', context)

def maintenance(request):
    maintenance = Maintenance.objects.all()
    context = {
        "maintenances": maintenance
    }
    return render(request, 'maintenance.html', context)

def create_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceCreateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/maintenance/')
        else:
            print("Errors:", form.errors)
    else:
        form = MaintenanceCreateForm()

    machine = Machine.objects.all()
    maintenance_type = Maintenance_handbook.objects.all()
    service_company = Service_company.objects.all()

    context = {
        'form': form,
        'machines': machine,
        'maintenance_types': maintenance_type,
        'services_company': service_company,
    }
    return render(request, 'maintenance_create.html', context)

def сlaim(request):
    сlaimed = Claim.objects.all()
    context = {
        "сlaimed": сlaimed
    }
    return render(request, 'сlaim.html', context)

def create_claim(request):
    if request.method == 'POST':
        form = ClaimCreateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/maintenance/')
        else:
            print("Errors:", form.errors)
    else:
        form = ClaimCreateForm()

    machine = Machine.objects.all()
    service_company = Service_company.objects.all()
    failure_node = Fault_handbook.objects.all()
    recovery_method = Recovery_handbook.objects.all()

    context = {
        'form': form,
        'machines': machine,
        'failure_node': failure_node,
        'recovery_method': recovery_method,
        'services_company': service_company,
    }
    return render(request, 'claim_create.html', context)

def picture_view(filename):
    print(filename)
    image_path = os.path.join(settings.STATIC_URL, 'materials', filename)
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image')

def profile_logout(request):
    logout(request)
    return redirect('/accounts/login/')

def favicon_view():
    image_path = os.path.join(settings.STATIC_URL, 'materials', 'favicon.ico')
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image')

def profile_redirect(request):
    try:
        api_keys = ApiKey.objects.filter(user=request.user)
    except:
        api_keys = None

    groups = request.user.groups.all()
    context = {
        'groups': groups,
        'api_keys': api_keys
    }
    return render(request, 'profile.html', context=context)

def profile_table(request, table_name):
    print(request)
    try:
        api_keys = ApiKey.objects.filter(user=request.user, visible=True)
    except:
        api_keys = None

    groups = request.user.groups.all()
    context = {
        'groups': groups,
        'api_keys': api_keys
    }
    return render(request, 'profile.html', context=context)

def apikey_create(request):
    if request.method == 'POST':
        form = ApiKeyCreateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/')
    else:
        form = ApiKeyCreateForm()
    return render(request, 'apikey_create.html', {'form': form})

def apiket_delete(request, pk):
    ApiKey.objects.get(id=pk).delete()
    return redirect(profile_redirect)

def show_description(request):
    last_page = request.GET.get('last_page')
    table_title = request.GET.get('table_title')
    name = request.GET.get('name')
    description = request.GET.get('description')

    context = {
        'last_page': last_page,
        'table_title': table_title,
        'name': name,
        'description': description,
    }
    return render(request, 'description.html', {'data': context})
