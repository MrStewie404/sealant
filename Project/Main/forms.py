from django import forms
from .models import ApiKey, Machine, Service_company, Maintenance, Claim
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ApiKeyCreateForm(forms.ModelForm):
    secret_word = forms.TextInput()
    class Meta:
        model = ApiKey
        fields = ['name', 'description']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'description': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if not name:
           self.add_error('name', "Имя ключа не может быть пустым.")
        elif len(name) > 255:
            self.add_error('name', "Длина имени не должна превышать 255 символов.")
        else:
           cleaned_data['name'] = name.strip()

        if not description:
            self.add_error('description', "Описание не может быть пустым.")
        else:
             cleaned_data['description'] = description.strip()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.key:
            instance.generate_key(self.secret_word)
        if commit:
            instance.save()
        return instance
    
class MachineCreateForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Выберите клиента")
    service_company = forms.ModelChoiceField(queryset=Service_company.objects.all(), empty_label="Выберите сервисную компанию")

    class Meta:
        model = Machine
        fields = ['serial_number', 'equipment_model', 
                    'engine_model', 'engine_serial_number', 
                    'transmission_model', 'transmission_serial_number', 
                    'drive_axle_model', 'drive_axle_serial_number', 
                    'steerable_axle_model', 'steerable_axle_serial_number',
                    'supply_contract_number', 'shipment_date',
                    'consignee', 'delivery_address',
                    'configuration', 'client',
                    'service_company']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=True)
        if commit:
            instance.save()
        return instance
    
class MaintenanceCreateForm(forms.ModelForm):
    service_company = forms.ModelChoiceField(queryset=Service_company.objects.all(), empty_label="Выберите сервисную компанию")

    class Meta:
        model = Maintenance
        fields = ['machine', 'maintenance_type', 
                'maintenance_date', 'hours', 
                'order_number', 'order_date',
                'service_company']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=True)
        if commit:
            instance.save()
        return instance

class ClaimCreateForm(forms.ModelForm):
    service_company = forms.ModelChoiceField(queryset=Service_company.objects.all(), empty_label="Выберите сервисную компанию")

    class Meta:
        model = Claim
        fields = ['machine', 'failure_date', 
                'operating_hours', 'failure_node', 
                'failure_description', 'recovery_method',
                'used_spare_parts', 'recovery_date',
                'downtime', 'service_company']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=True)
        if commit:
            instance.save()
        return instance