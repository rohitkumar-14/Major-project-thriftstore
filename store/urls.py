from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home,about,contact,product_detail,sell_with_us,add_to_cart,add_to_wishlist,cart_view,wishlist_view,checkout_view,user_login,user_register,user_logout,create_order,CollectionView, MensCollectionView, WomensCollectionView, AccessoriesCollectionView,user_profile,delete_wishlist_item

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('collections/<str:category>/', CollectionView.as_view(), name='collection'),
    path('collections/mens/', MensCollectionView.as_view(), name='mens'),
    path('collections/womens/',WomensCollectionView.as_view(), name='womens'),
    path('collections/accessories/', AccessoriesCollectionView.as_view(), name='accessories'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('sell_with_us', sell_with_us, name='sell_with_us'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('cart/', cart_view, name='cart'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/delete/<int:item_id>/', delete_wishlist_item, name='delete_wishlist_item'),
    path('checkout/', checkout_view, name='checkout'),
    path('create_order/', create_order, name='create_order'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('user_profile/', user_profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)