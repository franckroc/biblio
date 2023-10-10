
from django.urls import path
from shop.views import index, product_detail, addToCart, cart, deleteCart, author_filtered
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import signup, logout_user, login_user

urlpatterns = [
    path('', index, name='index'),
    path('filter/<str:name>/', author_filtered, name='author_filtered'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('cart/', cart, name='cart'),
    path('cart/delete/', deleteCart, name='deleteCart'),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/addToCart/', addToCart, name="addToCart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


