from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


ORDER_STATUSES = (
    ('started', 'started'),
    ('ended', 'ended'),
    ('in process', 'in process'),
    ('awaiting', 'awaiting'),
    ('canceled', 'canceled'),
)


class Employee(models.Model):
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True)
    store_id = models.ForeignKey(
        to='Store',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='store_employees',
        verbose_name=_('Торговая точка')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _('Работник')
        verbose_name_plural = _('Работники')

    def __str__(self):
        return f"{self.name}"


class Store(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.ForeignKey(
        to=Employee,
        on_delete=models.CASCADE,
        related_name='employee_stores',
        verbose_name=_('Работник')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _('Торговая точка')
        verbose_name_plural = _('Торговые точки')

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True)
    store_id = models.ForeignKey(
        to=Store,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='store_customers',
        verbose_name=_('Торговая точка')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _('Заказчик')
        verbose_name_plural = _('Заказчики')

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    store_id = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='store_orders',
        verbose_name=_('Торговая точка')
    )
    customer_id = models.ForeignKey(
        to=Customer,
        on_delete=models.CASCADE,
        related_name='customer_orders',
        verbose_name=_('Заказчик')
    )
    status = models.CharField(choices=ORDER_STATUSES, max_length=100)
    employee_id = models.ForeignKey(
        to=Employee,
        on_delete=models.CASCADE,
        related_name='employee_orders',
        verbose_name=_('Работник')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("start_date",)
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказ')

    def __str__(self):
        return f"{self.employee_id}, {self.store_id} для {self.customer_id}- {self.status}"


class Visit(models.Model):
    start_date = models.DateTimeField()
    employee_id = models.ForeignKey(
        to=Employee,
        on_delete=models.CASCADE,
        related_name='employee_visits',
        verbose_name=_('Работник')
    )
    order_id = models.OneToOneField(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_visit',
        verbose_name=_('Заказ')
    )
    customer_id = models.ForeignKey(
        to=Customer,
        on_delete=models.CASCADE,
        related_name='customer_visits',
        verbose_name=_('Заказчик')
    )
    store_id = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='store_visits',
        verbose_name=_('Торговая точка')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("start_date",)
        verbose_name = _('Посещение')
        verbose_name_plural = _('Посещения')

    def __str__(self):
        return f"{self.start_date} - {self.order_id}"

