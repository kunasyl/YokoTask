from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework import generics

from . import services, serializers, permissions, filters


class OrderView(APIView):
    order_services = services.OrderServices()
    customer_services = services.CustomerServices()
    store_services = services.StoreServices()
    filter_backends = [django_filters.DjangoFilterBackend, OrderingFilter]

    def get_permissions(self):
        if self.request.method in ('POST', 'PUT'):
            return [permissions.IsCustomer()]

    def get(self, request, *args, **kwargs):
        orders = self.order_services.get_orders()
        serializer = serializers.OrderSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        phone_num = request.query_params.get('phone_number')

        context = {
            'phone_number': phone_num
        }

        serializer = serializers.OrderSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"success": "Order created successfully"})

        return Response(serializer.errors)

    def put(self, request, *args, **kwargs):
        order = self.order_services.get_order(order_id=kwargs['pk'])
        serializer = serializers.OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitView(APIView):
    visit_services = services.VisitServices()
    filter_backends = [django_filters.DjangoFilterBackend, OrderingFilter]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsCustomer()]

    def get(self, request, *args, **kwargs):
        visits = self.visit_services.get_visits()
        serializer = serializers.VisitSerializer(visits, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        phone_num = request.query_params.get('phone_number')

        context = {
            'phone_number': phone_num
        }

        serializer = serializers.VisitSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"success": "Visit created successfully"})

        return Response(serializer.errors)


class StoreView(generics.ListAPIView):
    store_services = services.StoreServices()
    queryset = store_services.get_stores()
    serializer_class = serializers.StoreSerializer
    filter_class = filters.StoreFilter
    permission_classes = [permissions.IsAuthorized]
