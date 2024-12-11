from django.db import models

class Machine(models.Model):
    serial_number = models.CharField(max_length=255, unique=True, verbose_name='Зав. № машины')
    equipment_model = models.CharField(max_length=255, verbose_name='Модель техники')
    engine_model = models.CharField(max_length=255, verbose_name='Модель двигателя')
    engine_serial_number = models.CharField(max_length=255, verbose_name='Зав. № двигателя')
    transmission_model = models.CharField(max_length=255, verbose_name='Модель трансмиссии')
    transmission_serial_number = models.CharField(max_length=255, verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.CharField(max_length=255, verbose_name='Модель ведущего моста')
    drive_axle_serial_number = models.CharField(max_length=255, verbose_name='Зав. № ведущего моста')
    steerable_axle_model = models.CharField(max_length=255, verbose_name='Модель управляемого моста')
    steerable_axle_serial_number = models.CharField(max_length=255, verbose_name='Зав. № управляемого моста')
    supply_contract_number = models.CharField(max_length=255, verbose_name='Договор поставки №, дата')
    shipment_date = models.DateField(verbose_name='Дата отгрузки с завода')
    consignee = models.CharField(max_length=255, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес поставки (эксплуатации)')
    configuration = models.TextField(verbose_name='Комплектация (доп. опции)')
    client = models.CharField(max_length=255, verbose_name='Клиент')
    service_company = models.CharField(max_length=255, verbose_name='Сервисная компания')

    def __str__(self):
        return self.serial_number

class Maintenance(models.Model):
    maintenance_type = models.CharField(max_length=255, verbose_name='Вид ТО')
    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')
    hours = models.FloatField(verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=255, verbose_name='№ заказ-наряда')
    order_date = models.DateField(verbose_name='Дата заказ-наряда')
    performing_organization = models.CharField(max_length=255, verbose_name='Организация, проводившая ТО')
    machine = models.ForeignKey(
        'Machine', 
        on_delete=models.CASCADE, 
        related_name='maintenances', 
        verbose_name='Машина'
    )
    service_company = models.CharField(max_length=255, verbose_name='Сервисная компания')

    def __str__(self):
        return f"{self.maintenance_type} - {self.machine.serial_number} on {self.maintenance_date}"
    
from django.db import models

class Claim(models.Model):
    failure_date = models.DateField(verbose_name='Дата отказа')
    operating_hours = models.FloatField(verbose_name='Наработка, м/час')
    failure_node = models.CharField(max_length=255, verbose_name='Узел отказа')
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.CharField(max_length=255, verbose_name='Способ восстановления')
    used_spare_parts = models.TextField(verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    downtime = models.FloatField(verbose_name='Время простоя техники', editable=False)
    machine = models.ForeignKey(
        'Machine', 
        on_delete=models.CASCADE, 
        related_name='claims', 
        verbose_name='Машина'
    )
    service_company = models.CharField(max_length=255, verbose_name='Сервисная компания')

    # def save(self, *args, **kwargs):
    #     if self.recovery_date and self.failure_date:
    #         self.downtime = (self.recovery_date - self.failure_date).days
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Claim for {self.machine.serial_number} on {self.failure_date}"
    
class Technical_handbook(models.Model):
    ...

class Engine_handbook(models.Model):
    ...

class Transmission_handbook(models.Model):
    ...

class Drive_axle_handbook(models.Model):
    ...

class Steerable_axle_handbook(models.Model):
    ...


class Maintenance_handbook(models.Model):
    ...

class Fault_handbook(models.Model):
    ...

class Recovery_handbook(models.Model):
    ...