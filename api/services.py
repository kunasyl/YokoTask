import pytz
import datetime

from . import repos


class OrderServices:
    repos = repos.APIRepos()

    def get_orders(self):
        return self.repos.get_orders()

    def validate_order_deadline(self, order_id, validate_date):
        order = self.repos.get_order(order_id=order_id)
        return validate_date.replace(tzinfo=pytz.UTC) < order.end_date

    def get_order(self, order_id):
        return self.repos.get_order(order_id=order_id)

    def get_order_employee(self, order_id):
        order = self.repos.get_order(order_id=order_id)
        return order.employee_id


class StoreServices:
    repos = repos.APIRepos()

    def get_store_employees(self, store_id):
        store = self.repos.get_store(store_id=store_id)
        employees = store.store_employees.all()
        return employees

    def get_store_customers(self, store_id):
        store = self.repos.get_store(store_id=store_id)
        customers = store.store_customers.all()
        return customers

    def get_stores(self):
        return self.repos.get_stores()


class EmployeeServices:
    repos = repos.APIRepos()
    store_services = StoreServices()

    def get_employee(self, phone_number):
        return self.repos.get_employee(phone_number=phone_number)

    def is_employee_store(self, store_id, employee_id):
        # Check if the employee works in this store.
        employee = self.repos.get_employee_by_id(employee_id=employee_id)
        employees = self.store_services.get_store_employees(store_id=store_id)
        return True if employee in employees else False

    def employee_exists(self, phone_number):
        employee = self.get_employee(phone_number=phone_number)
        return True if employee else False


class CustomerServices:
    repos = repos.APIRepos()
    store_services = StoreServices()

    def get_customer(self, phone_number):
        return self.repos.get_customer(phone_number=phone_number)

    def validate_customer(self, phone_number, customer_id):
        """
        Validate customer by id and phone number.
        """
        customer = self.get_customer(phone_number=phone_number)
        return customer.id == customer_id

    def customer_exists(self, phone_number):
        customer = self.get_customer(phone_number=phone_number)
        return True if customer else False

    def is_customer_store(self, store_id, phone_number):
        # Check if the store is customer's.
        customer = self.get_customer(phone_number=phone_number)
        customers = self.store_services.get_store_customers(store_id=store_id)
        return True if customer in customers else False


class VisitServices:
    repos = repos.APIRepos()

    def get_visits(self):
        return self.repos.get_visits()
