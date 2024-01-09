from django.urls import path
from cstoreapp import views
from cstore import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('viewcart',views.viewcart),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('removeorder/<pid>',views.removeorder),
    path('userlogin',views.userlogin),
    path('register',views.register),
    path('productview/<pid>',views.productview),
    path('myaccount', views.myaccount),
    path('userlogout',views.userlogout),
    path('byprice/<prc>',views.byprice),
    path('bycatagory/<ctg>',views.bycatagory),
    path('about',views.about),
    path('contact',views.contact),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
