from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Carrito, ItemCarrito
from tienda.models import Producto
from django.contrib.auth import logout


def obtener_carrito(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        carrito, created = Carrito.objects.get_or_create(session_key=request.session.session_key, activo=True)
    return carrito

def ver_carrito(request):
    carrito = obtener_carrito(request)
    return render(request, 'carrito/ver_carrito.html', {'carrito': carrito})

def agregar_al_carrito(request, producto_id, cantidad):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito(request)
    
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    if not created:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad
    item.save()

    messages.success(request, 'Producto agregado al carrito.')
    return redirect('tienda:detalle_producto', pk=producto_id)

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito:ver_carrito')

def logout_view(request):
    carrito = Carrito.objects.filter(session_key=request.session.session_key, activo=True)
    carrito.delete()
    logout(request)
    messages.info(request, 'Has cerrado sesión con éxito.')
    return redirect('inicio')
