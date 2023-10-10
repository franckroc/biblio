from django.db import models
from django.urls import reverse
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=60)
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60)
    price = models.FloatField(default = 0.0)
    quantity = models.IntegerField(default = 0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.title} ({self.quantity})'
    
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

class Order(models.Model):
    # relation many to one (plusieurs commandes pour un utilisateur)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # on_delete=models.CASCADE : si l'utilisateur est supprimé, on supprime aussi ses commandes
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
    
    
class Cart(models.Model):
    # l'utilisateur ne peut avoir qu'un seul panier
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

