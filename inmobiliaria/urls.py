from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("propiedades/", views.properties, name="properties"),
    path("propiedad/<int:pk>/", views.property_detail, name="property_detail"),
    path("favoritos/", views.favorites, name="favorites"),
    path("favorito/<int:pk>/", views.toggle_favorite, name="toggle_favorite"),
    path("nosotros/", views.about, name="about"),
    path("asistente/", views.assistant, name="assistant"),
    path("registro/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path(
        "propiedad/<int:pk>/contactar/",
        views.contact_property,
        name="contact_property"
    ),
    path("panel/", views.dashboard, name="dashboard"),
    path("panel/propiedades/agregar/", views.add_property, name="add_property"),
    path(
    "panel/propiedades/",
    views.manage_properties,
    name="manage_properties",
),
    path(
    "panel/solicitudes/",
    views.manage_contacts,
    name="manage_contacts",
),
    path(
    "panel/propiedades/<int:pk>/editar/",
    views.edit_property,
    name="edit_property",
),
    path(
    "panel/propiedades/<int:pk>/eliminar/",
    views.delete_property,
    name="delete_property",
),
    path("panel/usuarios/", views.manage_users, name="manage_users"),
    path("panel/usuarios/<int:pk>/permisos/", views.toggle_staff, name="toggle_staff"),
]