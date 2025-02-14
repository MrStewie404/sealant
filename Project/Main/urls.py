from .views import *
from django.urls import path

urlpatterns = [
    path('', main, name='main'),
    path('machines/', machine, name='machine_list'),
    path('create/machine/', create_machine, name='create_machine'),
    path('maintenance/', maintenance, name='maintenance_list'),
    path('create/maintenance/', create_maintenance, name='create_maintenance'),
    path('claim/', сlaim, name='сlaim_list'),
    path('create/claim/', create_claim, name='create_claim'),
    path('materials/<str:filename>', picture_view),
    path('<str:filename>', picture_view),
    path('accounts/logout/', profile_logout),
    path('accounts/profile/', profile_redirect),
    path('accounts/profile/<str:table_name>/', profile_table),
    path('apikey/create/', apikey_create),
    path('apikey/delete/<int:pk>', apiket_delete),
    path('handbook/<str:title>', handbooks, name='handbooks'),
    path('handbook/<str:model_name>/<int:pk>/edit', handbook_edit),
    path('handbook/<str:model_name>/create', handbook_create),
    path('handbook/<str:model_name>/<int:pk>/detail/', handbook_detail, name='handbook_detail'), # Добавлено
    path('description/', show_description)
]