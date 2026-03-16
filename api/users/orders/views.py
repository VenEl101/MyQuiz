from rest_framework import viewsets, mixins

from apps.order.models import Order
from common.serializers.order.serializer import OrderCreateSerializer, OrderListSerializer


class OrderViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    queryset = Order.objects.select_related('course', 'user')
    http_method_names = ['get', 'post']


    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderListSerializer








