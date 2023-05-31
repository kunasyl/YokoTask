from rest_framework.permissions import DjangoObjectPermissions

from . import models, services


class IsCustomer(DjangoObjectPermissions):
    customer_services = services.CustomerServices()

    def has_permission(self, request, view):
        phone_num = self.get_phone_number(request)
        if not phone_num:
            return False
        return self.customer_services.customer_exists(phone_number=phone_num)

    @staticmethod
    def get_phone_number(request):
        phone_num = request.query_params.get('phone_number')
        return f"+{phone_num}"


class IsAuthorized(DjangoObjectPermissions):
    customer_services = services.CustomerServices()
    employee_services = services.EmployeeServices()

    def has_permission(self, request, view):
        phone_num = self.get_phone_number(request)
        if not phone_num:
            return False

        return bool(
            self.customer_services.customer_exists(phone_number=phone_num)
            or self.employee_services.employee_exists(phone_number=phone_num)
        )

    @staticmethod
    def get_phone_number(request):
        phone_num = request.query_params.get('phone_number')
        return f"+{phone_num}"
