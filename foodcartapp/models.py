from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum, F
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def total_amount(self):
        queryset = self.annotate(
            total_amount=Sum(
                F('ordered_items__quantity')*F('ordered_items__price'))
        )
        return queryset


class Order(models.Model):
    STATUS = (
        ('in_processing', 'В обработке'),
        ('on_assembly', 'На сборке'),
        ('in_delivery', 'В доставке'),
        ('delivered', 'Доставлен')
    )

    firstname = models.CharField(
        max_length=100,
        verbose_name='имя',
        default=''
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name='фамилия',
        default=''
    )
    phonenumber = PhoneNumberField(
        verbose_name='телефон',
        db_index=True,
        default=''
    )
    address = models.CharField(
        verbose_name='Адрес доставки',
        max_length=200,
        default=''
    )
    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=20,
        db_index=True,
        choices=STATUS,
        default='in_processing'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        max_length=1000,
        default=''
    )
    created_date = models.DateTimeField(
        verbose_name="Дата создания",
        default=timezone.now,
        db_index=True
    )
    called_date = models.DateTimeField(
        verbose_name="Дата звонка",
        null=True,
        blank=True
    )
    delivery_date = models.DateTimeField(
        verbose_name="Дата доставки",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):

        return f"{self.firstname} {self.lastname} - адрес({self.address})"

    objects = OrderQuerySet.as_manager()


class ProductOrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='ordered_items',
        on_delete=models.CASCADE,
        verbose_name='заказ',
        default=0
    )
    product = models.ForeignKey(
        Product,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='товар',
    )
    quantity = models.IntegerField(
        verbose_name='количество',
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказах'

    def __str__(self):
        return f"{self.product} - кол: {self.quantity}"
