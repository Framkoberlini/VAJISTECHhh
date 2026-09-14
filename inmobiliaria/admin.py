from django.contrib import admin

from .models import Property, Favorite, ContactRequest


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "property_type",
        "operation",
        "price",
        "featured",
    )

    list_filter = (
        "city",
        "property_type",
        "operation",
        "featured",
    )

    search_fields = (
        "title",
        "city",
        "neighborhood",
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "property",
        "created_at",
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "property",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "property__title",
    )

    readonly_fields = (
        "created_at",
    )