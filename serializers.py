from rest_framework import serializers

from .models import Order, Refund


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

        
class RefundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Refund
        fields = '__all__'
