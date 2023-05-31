from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from datetime import datetime

from . import models, services

customer_services = services.CustomerServices()
employee_services = services.EmployeeServices()
order_services = services.OrderServices()


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'

    def create(self, validated_data):
        phone_num = self.context.get('phone_number')
        phone_num = self.convert_phone_number(phone_num)

        store_id = validated_data['store_id'].id
        employee_id = validated_data['employee_id'].id
        customer_id = validated_data['customer_id'].id

        # Sent customer id is valid by phone number
        is_valid_id = customer_services.validate_customer(phone_number=phone_num, customer_id=customer_id)

        # Is store is customer's
        is_customer_store = customer_services.is_customer_store(store_id=store_id, phone_number=phone_num)

        # Does employee work in this store
        is_employee_store = employee_services.is_employee_store(store_id=store_id, employee_id=employee_id)

        if is_valid_id:
            if is_customer_store and is_employee_store:
                order = models.Order.objects.create(**validated_data)
                return order

        raise ValidationError('Object is not valid.')

    @staticmethod
    def convert_phone_number(phone_number):
        return f"+{phone_number}"


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Visit
        fields = '__all__'

    def create(self, validated_data):
        phone_num = self.context.get('phone_number')
        phone_num = self.convert_phone_number(phone_num)

        order_id = validated_data['order_id'].id
        store_id = validated_data['store_id'].id
        customer_id = validated_data['customer_id'].id
        employee_id = validated_data['employee_id'].id

        # Sent customer id is valid by phone number
        is_valid_id = customer_services.validate_customer(phone_number=phone_num, customer_id=customer_id)

        # Is store is customer's
        is_customer_store = customer_services.is_customer_store(store_id=store_id, phone_number=phone_num)

        # Check deadline od the order
        is_not_deadline = order_services.validate_order_deadline(order_id=order_id, validate_date=datetime.now())

        # Validate employee
        is_valid_employee = order_services.get_order_employee(order_id=order_id).id == employee_id

        if is_valid_id:
            if is_customer_store:
                if is_not_deadline:
                    print('todo - check time')
                    if is_valid_employee:
                        visit = models.Visit.objects.create(**validated_data)
                        return visit

        raise ValidationError('Object is not valid.')

    @staticmethod
    def convert_phone_number(phone_number):
        return f"+{phone_number}"


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Store
        fields = '__all__'
