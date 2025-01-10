import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from Main.models import *
from datetime import date


class APIMachines(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            serial_number = data.get('serial_number')
            
            if data.get('api_key'):
                if await self.check_key(data.get('api_key')):
                    response_data = await self.get_machine_data(serial_number, 17)
                else:
                    response_data = await self.get_machine_data(serial_number, 10)
            else:
                response_data = await self.get_machine_data(serial_number, 10)

            await self.send(text_data = json.dumps(response_data, ensure_ascii=False))

        except json.JSONDecodeError:
            await self.send(text_data = json.dumps({'error': 0, 'description': 'Неверный JSON формат'}, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data = json.dumps({'error': 3, 'description': f'Произошла ошибка: {str(e)}'}, ensure_ascii=False))


    async def disconnect(self, _):
        pass

    async def get_machine_data(self, serial_number, fields_len):
        machine_info = await self.machine(serial_number, fields_len)
        if machine_info != None:
            return {
                'fields':['serial_number', 'equipment_model', 
                        'engine_model', 'engine_serial_number', 
                        'transmission_model', 'transmission_serial_number', 
                        'drive_axle_model', 'drive_axle_serial_number', 
                        'steerable_axle_model', 'steerable_axle_serial_number',
                        'supply_contract_number', 'shipment_date',
                        'consignee', 'delivery_address',
                        'configuration', 'client',
                        'service_company',
                        ][:fields_len],
                'machine_info': machine_info
            }
        else:
            return {'error': 2, 'description': f'Машина с номером {serial_number} не найдена'}

    @sync_to_async
    def machine(self, serial_number, fields_len):
        if serial_number != '':
            machines = [Machine.objects.get(serial_number=serial_number)]
        else:
            machines = Machine.objects.all()

        data = []
        for machine in machines:
            data.append(dict(list({
                'id': machine.id,
                'serial_number': machine.serial_number,
                'equipment_model': {'name': machine.equipment_model.name, 'description': machine.equipment_model.description},
                'engine_model': {'name': machine.engine_model.name, 'description': machine.engine_model.description},
                'engine_serial_number': machine.engine_serial_number,
                'transmission_model': {'name': machine.transmission_model.name, 'description': machine.transmission_model.description},
                'transmission_serial_number': machine.transmission_serial_number,
                'drive_axle_model': {'name': machine.drive_axle_model.name, 'description': machine.drive_axle_model.description},
                'drive_axle_serial_number': machine.drive_axle_serial_number,
                'steerable_axle_model': {'name': machine.steerable_axle_model.name, 'description': machine.steerable_axle_model.description},
                'steerable_axle_serial_number': machine.steerable_axle_serial_number,
                'supply_contract_number': machine.supply_contract_number,
                'shipment_date': str(machine.shipment_date),
                'consignee': machine.consignee,
                'delivery_address': machine.delivery_address,
                'configuration': machine.configuration,
                'client': f"{machine.client.first_name} {machine.client.last_name} ({machine.client.id})",
                'service_company': {'name': machine.service_company.name, 'description': machine.service_company.description}
            }.items())[:fields_len+1]))
        return data
    
    @sync_to_async
    def check_key(self, api_key):
        api_keys = ApiKey.objects.all()
        api_keys = [api_key.key for api_key in api_keys]
        try_generate = ApiKey().generate_key(api_key)

        if str(api_key) in api_keys or try_generate in api_keys:
            return True
        
        return False
    

class APIMaintenance(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            serial_number = data.get('serial_number')
            
            if data.get('api_key'):
                if await self.check_key(data.get('api_key')):
                    response_data = await self.get_maintenances_data(serial_number)
                else:
                    response_data = {}
            else:
                response_data = {}

            await self.send(text_data = json.dumps(response_data, ensure_ascii=False))

        except json.JSONDecodeError:
            await self.send(text_data = json.dumps({'error': 0, 'description': 'Неверный JSON формат'}, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data = json.dumps({'error': 3, 'description': f'Произошла ошибка: {str(e)}'}, ensure_ascii=False))


    async def disconnect(self, _):
        pass

    async def get_maintenances_data(self, serial_number):
        maintenances_info = await self.maintenances(serial_number)
        if maintenances_info != None:
            return {
                'fields':['serial_number', 
                        'maintenance_type', 'maintenance_date', 
                        'hours', 'order_number', 
                        'order_date', 'service_company'
                        ],
                'maintenance_info': maintenances_info
            }
        else:
            return {'error': 2, 'description': f'Машина с номером {serial_number} не найдена'}

    @sync_to_async
    def maintenances(self, serial_number):
        if serial_number != '':
            machine = Machine.objects.get(serial_number=serial_number)
            maintenances = [Maintenance.objects.filter(machine=machine)]
        else:
            maintenances = Maintenance.objects.all()


        data = []
        for maintenance in maintenances:
            data.append({
                'id': maintenance.id,
                'serial_number': maintenance.machine.serial_number,
                'maintenance_type': {'name': maintenance.maintenance_type.name, 'description': maintenance.maintenance_type.description},
                'maintenance_date': str(maintenance.maintenance_date),
                'hours': maintenance.hours,
                'order_number': maintenance.order_number,
                'order_date': str(maintenance.order_date),
                'service_company': {'name': maintenance.service_company.name, 'description': maintenance.service_company.description}
            })
        return data
    
    @sync_to_async
    def check_key(self, api_key):
        api_keys = ApiKey.objects.all()
        api_keys = [api_key.key for api_key in api_keys]
        try_generate = ApiKey().generate_key(api_key)

        if str(api_key) in api_keys or try_generate in api_keys:
            return True
        
        return False
    
class APIClaim(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            serial_number = data.get('serial_number')
            
            if data.get('api_key'):
                if await self.check_key(data.get('api_key')):
                    response_data = await self.get_claims_data(serial_number)
                else:
                    response_data = {}
            
            else:
                response_data = {}

            await self.send(text_data = json.dumps(response_data, ensure_ascii=False))

        except json.JSONDecodeError:
            await self.send(text_data = json.dumps({'error': 0, 'description': 'Неверный JSON формат'}, ensure_ascii=False))
        except Exception as e:
            await self.send(text_data = json.dumps({'error': 3, 'description': f'Произошла ошибка: {str(e)}'}, ensure_ascii=False))


    async def disconnect(self, _):
        pass

    async def get_claims_data(self, serial_number):
        claims_info = await self.claims(serial_number)
        if claims_info != None:
            return {
                'fields':['serial_number', 
                        'service_company', 'failure_date', 
                        'operating_hours', 'failure_node', 
                        'failure_description', 'recovery_method',
                        'used_spare_parts', 'recovery_date',
                        'downtime'
                        ],
                'claim_info': claims_info
            }
        else:
            return {'error': 2, 'description': f'Машина с номером {serial_number} не найдена'}

    @sync_to_async
    def claims(self, serial_number):
        if serial_number != '':
            machine = Machine.objects.get(serial_number=serial_number)
            claims = [Claim.objects.filter(machine=machine)]
        else:
            claims = Claim.objects.all()

        data = []
        for claim in claims:
            data.append({
                'id': claim.id,
                'serial_number': claim.machine.serial_number,
                'service_company': {'name': claim.service_company.name, 'description': claim.service_company.description},
                'failure_date': str(claim.failure_date),
                'operating_hours': claim.operating_hours,
                'failure_node': {'name': claim.failure_node.name, 'description': claim.failure_node.description},
                'failure_description': claim.failure_description,
                'recovery_method': {'name': claim.recovery_method.name, 'description': claim.recovery_method.description},
                'used_spare_parts': claim.used_spare_parts,
                'recovery_date': str(claim.recovery_date),
                'downtime': claim.downtime
            })
        print(data[0])
        return data
    
    @sync_to_async
    def check_key(self, api_key):
        api_keys = ApiKey.objects.all()
        api_keys = [api_key.key for api_key in api_keys]
        try_generate = ApiKey().generate_key(api_key)

        if str(api_key) in api_keys or try_generate in api_keys:
            return True
        
        return False