from django.core.exceptions import ObjectDoesNotExist

from . import models


class APIRepos:
    def get_orders(self) -> models.Order:
        return models.Order.objects.all()

    def get_employee(self, phone_number) -> models.Employee:
        try:
            return models.Employee.objects.get(phone_number=phone_number)
        except models.Employee.DoesNotExist:
            raise ObjectDoesNotExist(f'Такого работника с номером {phone_number} не существует')

    def get_customer(self, phone_number) -> models.Customer:
        try:
            return models.Customer.objects.get(phone_number=phone_number)
        except models.Customer.DoesNotExist:
            raise ObjectDoesNotExist(f'Такого заказчика с номером {phone_number} не существует')

    def get_employee_by_id(self, employee_id) -> models.Customer:
        return models.Employee.objects.get(id=employee_id)

    def get_customer_by_id(self, employer_id) -> models.Customer:
        return models.Customer.objects.get(id=employer_id)

    def get_customer_stores(self, employer_id) -> models.Store:
        return models.Store.objects.filter()

    def get_store(self, store_id) -> models.Store:
        return models.Store.objects.get(id=store_id)

    def get_visits(self) -> models.Visit:
        return models.Visit.objects.all()

    def get_order(self, order_id):
        return models.Order.objects.get(id=order_id)

    def get_stores(self):
        return models.Store.objects.all()