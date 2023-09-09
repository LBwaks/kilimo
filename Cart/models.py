from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
# Create your models here.
class CartItem(models.Model):
    """Model definition for CartItem."""

    # TODO: Define fields here
    content_type = models.ForeignKey(ContentType, verbose_name=_(""), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    

    class Meta:
        """Meta definition for Cart Item."""

        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        """Unicode representation of CartItem."""
        f'{self.quantity} x {self.content_object}'

    # def save(self):
    #     """Save method for CartItem."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for CartItem."""
        return ('')

    # TODO: Define custom methods here
    def total_price(self):
        if hasattr(self.content_object, 'price'):
            return self.quantity * self.content_object.price
        return 0  # Adjust this based on how you handle service prices



class Cart(models.Model):
    """Model definition for Cart."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, verbose_name=_(""))

    class Meta:
        """Meta definition for Cart."""

        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        """Unicode representation of Cart."""
        return f'Cart for {self.user.username}'

    # def save(self):
    #     """Save method for Cart."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Cart."""
        return ('')

    # TODO: Define custom methods here
    def total_price(self):
        # Calculate the total price of all items in the cart
        return sum(item.total_price() for item in self.items.all())
    def add_item(self, content_object, quantity=1):
        # Add an item to the cart
        content_type = ContentType.objects.get_for_model(content_object)
        item, created = CartItem.objects.get_or_create(
            content_type=content_type,
            object_id=content_object.id,
            quantity=quantity
        )
        if not created:
            item.quantity += quantity
            item.save()
        self.items.add(item)
    def remove_item(self, content_object, quantity=1):
        # Remove an item from the cart
        content_type = ContentType.objects.get_for_model(content_object)
        try:
            item = CartItem.objects.get(
                content_type=content_type,
                object_id=content_object.id
            )
            if item.quantity <= quantity:
                self.items.remove(item)
            else:
                item.quantity -= quantity
                item.save()
        except CartItem.DoesNotExist:
            pass