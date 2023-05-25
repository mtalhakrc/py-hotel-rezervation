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

Anasayfada slider şeklinde otel fotoğrafları olması lazım. Tasarım kısmı önemli bir yere sahip. OK
Altında odalar başlığı altında tıkladığımızda oda detay sayfasına girmeliyiz OK 
Oda detay sayfasında her odada  5-6 fotoğraf, OK odaların özellikleri, OK
Şuan rezerve için müsait olup olmadığı bilgileri verilmeli OK
Yukarıdaki navbar odalar,iletişim, hakkımızda olmalı ve sayfalara tıkladığımızda ilgili sayfanın template ine yönlendirmeli OK

 
sonra : Sistemdeki müşteriler belirlenen iki tarih arasında en çok tutulan yada en az tutulan odayı görmeli. Sitede şuan böyle bir şey karşımıza çıkmıyor.
sonra: Şuan müsait olan dolu olan odaları, ileriki bir tarihte müsait ve dolu olan odaları kullanıcılar arama yaptıkları takdirde görebilmeli
sonra : Adminler sitede toplam gelir ve en çok tutulan en az tutulan odalar için ciroyu görebilmeli

aynen QnaQa: Müşteriler üye oldukları takdirde yaptırdıkları rezervasyonları görebilmeli. siktir git reis 
aynenQnaq: Oda eğer müsait değilse takip et butonu olmalı. Rezervasyonlarım içinde takip ettikleri odaları da kullanıcılar görebilmeli. Oda boşaldığı zaman takibe alınan müşteriye istediğiniz oda şuan müsait diye mesaj gelmeli. siktir git reis 

"""
from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("about_us/",views.about_us),

    path("search_room", views.room_search),

    path("room_detail/<str:room_slug>/", views.room_detail, name="room-detail"),
]
