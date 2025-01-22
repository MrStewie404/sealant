from django.contrib.auth.decorators import user_passes_test

def is_manager(user):
   return user.groups.filter(name='Manager').exists()

def is_service_organization(user):
   return user.groups.filter(name='Service organization').exists()

def is_client(user):
   return user.groups.filter(name='Client').exists()

def group_required(groups):
    """
    Декоратор для проверки принадлежности пользователя к хотя бы одной из указанных групп.
    """
    def check_group(user):
        if user.is_authenticated:
            return user.groups.filter(name__in=groups).exists()
        return False # или redirect на страницу авторизации

    def decorator(view_func):
        return user_passes_test(check_group, login_url='/accounts/login/')(view_func)
    return decorator