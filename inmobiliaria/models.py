from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    TYPE_CHOICES = [
        ("Casa", "Casa"),
        ("Apartamento", "Apartamento"),
        ("Lote", "Lote"),
        ("Comercial", "Comercial"),
    ]
    OPERATION_CHOICES = [
        ("Venta", "Venta"),
        ("Arriendo", "Arriendo"),
    ]
    title = models.CharField(max_length=150)
    city = models.CharField(max_length=80)
    neighborhood = models.CharField(max_length=100, blank=True)
    property_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES, default="Venta")
    price = models.DecimalField(max_digits=14, decimal_places=0)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    parking = models.PositiveIntegerField(default=0)
    area = models.PositiveIntegerField(default=0, help_text="Área en m²")
    description = models.TextField()
    image_url = models.URLField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def formatted_price(self):
        return f"${self.price:,.0f}".replace(",", ".")


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "property"], name="unique_user_property_favorite")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"
    
class ContactRequest(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="contact_requests"
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.property.title}"
   