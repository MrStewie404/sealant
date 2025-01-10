from django.contrib.auth.models import User
from django.db import models
import hashlib
import time

class Machine(models.Model):
    serial_number = models.CharField(max_length=255, unique=True, verbose_name='Зав. № машины')
    equipment_model = models.ForeignKey("Technical_handbook", verbose_name='Модель техники', on_delete=models.DO_NOTHING, null=True)
    engine_model = models.ForeignKey("Engine_handbook", verbose_name='Модель двигателя', on_delete=models.DO_NOTHING, null=True)
    engine_serial_number = models.CharField(max_length=255, verbose_name='Зав. № двигателя')
    transmission_model = models.ForeignKey("Transmission_handbook", verbose_name='Модель трансмиссии', on_delete=models.DO_NOTHING)
    transmission_serial_number = models.CharField(max_length=255, verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.ForeignKey("Drive_axle_handbook", verbose_name='Модель ведущего моста', on_delete=models.SET_NULL, null=True)
    drive_axle_serial_number = models.CharField(max_length=255, verbose_name='Зав. № ведущего моста')
    steerable_axle_model = models.ForeignKey("Steerable_axle_handbook", verbose_name='Модель управляемого моста', on_delete=models.SET_NULL, null=True)
    steerable_axle_serial_number = models.CharField(max_length=255, verbose_name='Зав. № управляемого моста')
    supply_contract_number = models.CharField(max_length=255, verbose_name='Договор поставки №, дата')
    shipment_date = models.DateField(verbose_name='Дата отгрузки с завода')
    consignee = models.CharField(max_length=255, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес поставки (эксплуатации)')
    configuration = models.TextField(verbose_name='Комплектация (доп. опции)')

    # Устанавливаем машину у клиента в нулевое значение в случае удаление машины 
    client = models.ForeignKey(User, verbose_name='Клиент', on_delete=models.SET_NULL, null=True)
    service_company = models.ForeignKey("Service_company", verbose_name='Сервисная компания', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.serial_number

class Maintenance(models.Model):
    machine = models.ForeignKey(
            'Machine', 
            on_delete=models.CASCADE, 
            related_name='maintenances', 
            verbose_name='Машина'
        )
    maintenance_type = models.ForeignKey("Maintenance_handbook", verbose_name='Вид ТО', on_delete=models.SET_NULL, null=True)
    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')
    hours = models.FloatField(verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=255, verbose_name='№ заказ-наряда')
    order_date = models.DateField(verbose_name='Дата заказ-наряда')
    service_company = models.ForeignKey("Service_company", verbose_name='Сервисная компания', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.maintenance_type} - {self.machine.serial_number} on {self.maintenance_date}"

from django.db import models

class Claim(models.Model):
    machine = models.ForeignKey(
        'Machine', 
        on_delete=models.CASCADE, 
        related_name='claims', 
        verbose_name='Машина'
    )
    service_company = models.ForeignKey("Service_company", verbose_name='Сервисная компания', on_delete=models.SET_NULL, null=True)
    failure_date = models.DateField(verbose_name='Дата отказа')
    operating_hours = models.FloatField(verbose_name='Наработка, м/час')
    failure_node = models.ForeignKey("Fault_handbook", verbose_name='Узел отказа', on_delete=models.SET_NULL, null=True)
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey("Recovery_handbook", verbose_name='Способ восстановления', on_delete=models.SET_NULL, null=True)
    used_spare_parts = models.TextField(verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    downtime = models.FloatField(verbose_name='Время простоя техники')

    def save(self, *args, **kwargs):
        if self.recovery_date and self.failure_date:
            self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"Claim for {self.machine.serial_number} on {self.failure_date}"
    
class Technical_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Engine_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Transmission_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Drive_axle_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Steerable_axle_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Service_company(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Maintenance_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Fault_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class Recovery_handbook(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"

class ApiKey(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    key = models.TextField(verbose_name="Ключ")
    name = models.TextField(verbose_name='Название', default='Новый ключ')
    description = models.TextField(verbose_name="Описание ключа")
    visible = models.BooleanField(verbose_name="Видимость ключа", default=True)
    user = models.ForeignKey(User, verbose_name="Владелец ключа", on_delete=models.CASCADE)

    def generate_key(self, secret_word):
        secret_word = str(secret_word).encode('utf-8')
        hash_object = hashlib.sha256(secret_word)
        self.key = hash_object.hexdigest()

        return self.key