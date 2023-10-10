
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product, Cart, Order
from django.urls import reverse
from django.db.models import Count

def index(request):
    #récupère tous les produits pour block content
    products = Product.objects.all().order_by('name')    
    # récupère les produits filtrés par nom
    products_filtered = Product.objects.values('name').annotate(count=Count('name')).order_by('name')
    context = {
         'products': products,
         'products_filtered': products_filtered  
    }
    return render(request, 'shop/index.html', context)

def author_filtered(request, name):    
    # récupère les produits filtrés par nom
    products_filtered = Product.objects.filter(name=name).order_by('name')
    context = {
         'products_filtered': products_filtered
    }
    return render(request, 'shop/author_filtered.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'shop/detail.html', context) 

def addToCart(request, slug):
    # recupère l'utilisateur connecté
    user = request.user
    # recupère le produit s'il existe, en lui passant le slug
    # si le produit n'existe pas, on renvoie une erreur 404
    product = get_object_or_404(Product, slug=slug)
    # recupère le panier de l'utilisateur dans cart, ou le crée s'il n'existe pas
    cart, _ = Cart.objects.get_or_create(user=user)
    # recupère la commande de l'utilisateur pour le produit dans order, ou la crée s'il n'existe pas
    order, created = Order.objects.get_or_create(user=user, product=product)
    # si le produit n'existait pas, on l'ajoute au panier et on sauvegarde
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        # sinon on augmente la quantité de 1 et on sauvegarde
        order.quantity += 1
        order.save()
    # on redirige vers la page du produit
    return redirect(reverse("product", kwargs={"slug": slug}))

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    sous_total = 0
    total_price = 0
    # récupère le nombre de ligne de commande
    nb_cmd = cart.orders.all().count()
    
    for n in range(nb_cmd):
        # récupère la quantité de chaque ligne de commande
        nb= cart.orders.all()[n].quantity
        # récupère le prix du produit de chaque ligne de commande
        sous_total = cart.orders.all()[n].product.price * nb
        # calcule le prix total
        total_price += sous_total

    context = {
        'orders': cart.orders.all(),
        'total_price': total_price
    }

    return render(request, 'shop/cart.html', context)

def deleteCart(request):
    cart = request.user.cart
    if cart:
        cart.orders.all().delete()
        cart.delete()

    return redirect('index')

