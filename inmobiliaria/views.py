from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Property, Favorite, ContactRequest

def home(request):
    featured = Property.objects.filter(featured=True)[:6]
    if not featured.exists():
        featured = Property.objects.all()[:6]
    return render(request, "home.html", {"properties": featured})

def properties(request):
    qs = Property.objects.all()
    city = request.GET.get("city", "").strip()
    ptype = request.GET.get("type", "").strip()
    operation = request.GET.get("operation", "").strip()
    q = request.GET.get("q", "").strip()

    if city:
        qs = qs.filter(city__iexact=city)
    if ptype:
        qs = qs.filter(property_type=ptype)
    if operation:
        qs = qs.filter(operation=operation)
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(city__icontains=q) |
            Q(neighborhood__icontains=q)
        )

    return render(request, "properties.html", {
        "properties": qs,
        "cities": Property.objects.values_list("city", flat=True).distinct().order_by("city"),
        "selected_city": city,
        "selected_type": ptype,
        "selected_operation": operation,
        "query": q,
    })

def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(
        user=request.user, property=prop
    ).exists()
    return render(request, "property_detail.html", {"property": prop, "is_favorite": is_favorite})

@login_required
def toggle_favorite(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=prop)
    if not created:
        favorite.delete()
        messages.info(request, "Propiedad retirada de favoritos.")
    else:
        messages.success(request, "Propiedad guardada en favoritos.")
    return redirect(request.META.get("HTTP_REFERER", "properties"))

@login_required
def favorites(request):
    saved = Property.objects.filter(favorited_by__user=request.user).distinct()
    return render(request, "favorites.html", {"properties": saved})

def about(request):
    return render(request, "about.html")

def assistant(request):
    answer = None
    user_text = ""
    if request.method == "POST":
        user_text = request.POST.get("message", "").strip()
        text = user_text.lower()

        if any(x in text for x in ["hola", "buenas", "hey"]):
            answer = "¡Hola! Soy Vaji, tu asistente inmobiliario. Puedo ayudarte a buscar casas y apartamentos."
        elif "arriendo" in text or "alquiler" in text:
            answer = "Claro. En VajiSTech puedes filtrar las propiedades por operación y revisar sus detalles."
        elif "comprar" in text or "venta" in text:
            answer = "Perfecto. Te recomiendo entrar a Propiedades y filtrar por Venta, ciudad y tipo de inmueble."
        elif "bogotá" in text or "bogota" in text:
            answer = "Tenemos propiedades en diferentes ciudades. Prueba el filtro de Bogotá en Propiedades."
        elif "precio" in text or "presupuesto" in text:
            answer = "Puedes revisar el precio de cada inmueble y comparar varias opciones antes de tomar una decisión."
        else:
            answer = "Puedo orientarte sobre búsqueda, compra, venta y arriendo. Prueba escribiendo: 'busco un apartamento en Bogotá'."

    return render(request, "assistant.html", {"answer": answer, "user_text": user_text})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        if not username or not email or not password:
            messages.error(request, "Completa todos los campos.")
        elif password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Cuenta creada correctamente.")
            return redirect("home")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def contact_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(
                request,
                "Por favor completa tu nombre, correo y mensaje."
            )
        else:
            ContactRequest.objects.create(
                property=property_obj,
                name=name,
                email=email,
                phone=phone,
                message=message,
            )

            messages.success(
                request,
                "¡Tu solicitud fue enviada correctamente!"
            )

            return redirect("property_detail", pk=property_obj.pk)

    return render(
        request,
        "contact_property.html",
        {"property": property_obj}
    )
    
    # ================================
# PANEL DE GESTIÓN VAJISTECH
# ================================

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url="/login/")
def dashboard(request):
    properties_count = Property.objects.count()
    sale_count = Property.objects.filter(operation="Venta").count()
    rent_count = Property.objects.filter(operation="Arriendo").count()
    contact_count = ContactRequest.objects.count()

    recent_contacts = ContactRequest.objects.select_related(
        "property"
    ).order_by("-created_at")[:5]

    return render(
        request,
        "dashboard.html",
        {
            "properties_count": properties_count,
            "sale_count": sale_count,
            "rent_count": rent_count,
            "contact_count": contact_count,
            "recent_contacts": recent_contacts,
        },
    )
    
@login_required
def add_property(request):
    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":
        Property.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            operation=request.POST.get("operation"),
            property_type=request.POST.get("property_type"),
            city=request.POST.get("city"),
            neighborhood=request.POST.get("neighborhood"),
            address=request.POST.get("address"),
            bedrooms=request.POST.get("bedrooms"),
            bathrooms=request.POST.get("bathrooms"),
            parking=request.POST.get("parking"),
            area=request.POST.get("area"),
            image_url=request.POST.get("image_url"),
            featured=request.POST.get("featured") == "on",
        )

        return redirect("dashboard")

    return render(request, "add_property.html")

@login_required
def manage_properties(request):
    if not request.user.is_staff:
        return redirect("home")

    properties = Property.objects.all().order_by("-id")

    search = request.GET.get("q", "").strip()
    operation = request.GET.get("operation", "").strip()

    if search:
        properties = properties.filter(
            Q(title__icontains=search)
            | Q(city__icontains=search)
            | Q(neighborhood__icontains=search)
        )

    if operation:
        properties = properties.filter(operation=operation)

    return render(
        request,
        "manage_properties.html",
        {
            "properties": properties,
            "search": search,
            "operation": operation,
            "total_results": properties.count(),
        },
    )
    
@login_required
def manage_contacts(request):
    if not request.user.is_staff:
        return redirect("home")

    contacts = ContactRequest.objects.select_related(
        "property"
    ).order_by("-created_at")

    return render(
        request,
        "manage_contacts.html",
        {
            "contacts": contacts,
        },
    )
    
@login_required
def edit_property(request, pk):
    if not request.user.is_staff:
        return redirect("home")

    property = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        property.title = request.POST.get("title")
        property.description = request.POST.get("description")
        property.price = request.POST.get("price")
        property.operation = request.POST.get("operation")
        property.property_type = request.POST.get("property_type")
        property.city = request.POST.get("city")
        property.neighborhood = request.POST.get("neighborhood")
        property.address = request.POST.get("address")
        property.bedrooms = request.POST.get("bedrooms")
        property.bathrooms = request.POST.get("bathrooms")
        property.parking = request.POST.get("parking")
        property.area = request.POST.get("area")
        property.image_url = request.POST.get("image_url")
        property.featured = request.POST.get("featured") == "on"

        property.save()

        return redirect("manage_properties")

    return render(
        request,
        "edit_property.html",
        {
            "property": property,
        },
    )
    
@login_required
def delete_property(request, pk):
    if not request.user.is_staff:
        return redirect("home")

    property = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        property.delete()
        return redirect("manage_properties")

    return render(
        request,
        "delete_property.html",
        {
            "property": property,
        },
    )
@login_required
def manage_users(request):
    if not request.user.is_staff:
        return redirect("home")

    users = User.objects.all().order_by("-date_joined")

    return render(
        request,
        "manage_users.html",
        {"users": users},
    )
@login_required
def toggle_staff(request, pk):
    if not request.user.is_staff:
        return redirect("home")

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        if user != request.user:
            user.is_staff = not user.is_staff
            user.save()

        return redirect("manage_users")

    return redirect("manage_users")