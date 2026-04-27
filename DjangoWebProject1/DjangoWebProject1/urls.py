from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Buradaki 'app' uygulama klasörünüzün adýdýr. 
    # Eðer klasör adýnýz farklýysa (örneðin 'KulupApp'), 'app.urls' kýsmýný 'KulupApp.urls' yapýn.
    path('', include('app.urls')), 
]