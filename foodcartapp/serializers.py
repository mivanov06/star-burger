from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.transaction import atomic
from rest_framework import serializers

from foodcartapp.models import ProductOrderItem, Order, Product


class OrderedItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Product.objects.available()
    )
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(500)],
        required=True
    )

    class Meta:
        model = ProductOrderItem
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    products = OrderedItemSerializer(many=True, required=True, source="ordered_items", allow_empty=False)
    status_display = serializers.CharField(
        source='get_status_display'
    )
    payment_display = serializers.CharField(
        source='get_payment_display'
    )
    firstname = serializers.CharField(
        required=True
    )
    lastname = serializers.CharField(
        required=True
    )
    phonenumber = serializers.CharField(
        required=True
    )
    address = serializers.CharField(
        required=True)
    total_amount = serializers.FloatField(
        read_only=True
    )
    comment = serializers.CharField(
    )

    class Meta:
        model = Order
        fields = ("products", "status_display", "firstname", "lastname", "phonenumber", "address",
                  "comment", "id", "total_amount", "payment_display")
        read_only_fields = ("id", *fields)

    @atomic
    def create(self, validated_data):
        ordered_items_data = validated_data.pop("ordered_items")
        order = Order.objects.create(**validated_data)
        for entity in ordered_items_data:
            ProductOrderItem.objects.create(**entity, order=order)
        return order
