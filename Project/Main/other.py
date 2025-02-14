from django.contrib.auth.decorators import user_passes_test

def is_manager(user):
   return user.groups.filter(name='Manager').exists()

def is_service_organization(user):
   return user.groups.filter(name='Service organization').exists()

def is_client(user):
   return user.groups.filter(name='Client').exists()

def group_required(groups):
    """
    Декоратор для проверки принадлежности пользователя одной из указанных групп.
    """
    def check_group(user):
        if user.is_authenticated:
            return user.groups.filter(name__in=groups).exists()
        return False

    def decorator(view_func):
        return user_passes_test(check_group, login_url='/accounts/login/')(view_func)
    return decorator

# def get_data_from_model(model_class, data):
#     """
#     Сохраняет данные в модель, используя переданное имя модели и данные.

#     Args:
#         model_name (str): Название модели.
#         model_class (models.Model): Класс модели Django.
#         data (dict): Словарь с данными для сохранения. Ключи должны соответствовать
#                      именам полей модели.

#     Returns:
#         models.Model: Экземпляр созданной или обновленной модели.
#     """
#     instance_id = data.get('id')

#     try:
#         instance = model_class.objects.get(pk=instance_id)
#     except model_class.DoesNotExist:
#         return None
    
#     return instance

def save_data_to_model(model_class, data):
    """
    Сохраняет данные в модель, используя переданное имя модели и данные.

    Args:
        model_class (models.Model): Класс модели Django.
        data (dict): Словарь с данными для сохранения. Ключи должны соответствовать
                     именам полей модели.

    Returns:
        models.Model: Экземпляр созданной или обновленной модели.
    """
    instance_id = data.get('id')
    try:
        instance = model_class.objects.get(pk=instance_id)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
    except model_class.DoesNotExist:
        instance = model_class(**data)
        instance.save()

    return instance