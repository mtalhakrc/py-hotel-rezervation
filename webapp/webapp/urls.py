"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
oldu paşam hemen yapalım: 

Anasayfada slider şeklinde otel fotoğrafları olması lazım. Tasarım kısmı önemli bir yere sahip.
Altında odalar başlığı altında tıkladığımızda oda detay sayfasına girmeliyiz 
Oda detay sayfasında her odada 
5-6 fotoğraf,
odaların özellikleri,
Şuan rezerve için müsait olup olmadığı bilgileri verilmeli 
Yukarıdaki navbar odalar,iletişim, hakkımızda olmalı ve sayfalara tıkladığımızda ilgili sayfanın template ine yönlendirmeli 
sonra : Sistemdeki müşteriler belirlenen iki tarih arasında en çok tutulan yada en az tutulan odayı görmeli. Sitede şuan böyle bir şey karşımıza çıkmıyor.
aynen QnaQa: Müşteriler üye oldukları takdirde yaptırdıkları rezervasyonları görebilmeli.
sonra: Şuan müsait olan dolu olan odaları, ileriki bir tarihte müsait ve dolu olan odaları kullanıcılar arama yaptıkları takdirde görebilmeli 
aynenQnaq: Oda eğer müsait değilse takip et butonu olmalı. Rezervasyonlarım içinde takip ettikleri odaları da kullanıcılar görebilmeli. Oda boşaldığı zaman takibe alınan müşteriye istediğiniz oda şuan müsait diye mesaj gelmeli. 
sonra : Adminler sitede toplam gelir ve en çok tutulan en az tutulan odalar için ciroyu görebilmeli

"""
from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),

    #  path("room_detail/search", views.room_search),

    path("room_detail/<str:room_slug>/", views.room_detail, name="room-detail"),
]
