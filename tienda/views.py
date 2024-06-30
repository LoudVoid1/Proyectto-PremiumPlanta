from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto,Categoria
from .forms import ProductoForm
from django.contrib import messages
from django.db.models import Q


def inicio(request):
    productos_destacados = Producto.objects.filter(destacado=True)[:4]
    herramientas = Producto.objects.filter(categoria__nombre="Herramientas de Jardineria")[:4]
    macetas = Producto.objects.filter(categoria__nombre="Macetas y Contenedores")[:4]
    
    context = {
        'productos_destacados': productos_destacados,
        'herramientas': herramientas,
        'macetas': macetas,
    }
    
    return render(request, 'tienda/inicio.html', context)


def lista_productos(request):
    categoria_ids = request.GET.getlist('categoria')
    if categoria_ids:
        productos = Producto.objects.filter(categoria_id__in=categoria_ids)
    else:
        productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'tienda/lista_productos.html', {'productos': productos, 'categorias': categorias})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        return redirect('carrito:agregar_al_carrito', producto_id=producto.pk, cantidad=cantidad)

    return render(request, 'tienda/detalle_producto.html', {'producto': producto})

def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tienda:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'tienda/agregar_producto.html', {'form': form})

def buscar(request):
    query = request.GET.get('q')
    resultados = Producto.objects.filter(nombre__icontains=query)
    return render(request, 'tienda/resultados_busqueda.html', {'resultados': resultados, 'query': query})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('tienda:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/editar_producto.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('tienda:lista_productos')
    return render(request, 'tienda/eliminar_producto.html', {'producto': producto})

def buscar(request):
    query = request.GET.get('q')
    productos = Producto.objects.filter(nombre__icontains=query)
    return render(request, 'tienda/buscar.html', {'productos': productos})