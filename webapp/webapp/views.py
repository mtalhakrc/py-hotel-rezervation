import time

import datetime as datetime
from django.http.response import HttpResponse
from django.shortcuts import render
from webapp.models import Room


def index(request):
    results = Room.objects.filter(is_active=True)
    return render(request, "index.html", {"rooms": results})


def room_search(request):
    # iki tarih arasında rezerve edilmiş en çok ciro yapan odalar
    start_date = request.POST.get("start_date", "")
    end_date = request.POST.get("end_date", "")
    print(start_date, end_date)
    if start_date == "" or end_date == "":
        return HttpResponse("Lütfen tarihleri giriniz.")

    results = Room.objects.raw("SELECT webapp_room.id, webapp_room.name, SUM(webapp_roomreservation.paid_amount) AS total_revenue FROM webapp_room INNER JOIN webapp_roomreservation ON webapp_room.id = webapp_roomreservation.room_id_id WHERE (webapp_roomreservation.start_date >= %s and webapp_roomreservation.end_date <= %s)   GROUP BY webapp_room.id ORDER BY total_revenue DESC;", [start_date, end_date])
    print(results)
    return render(request, "index.html", {"rooms": results})


def room_detail(request, room_slug):
    room = Room.objects.get(slug=room_slug)
    images = room.image_ids.all()
    print('images', images)
    features = room.features.split(',')
    return render(request, "room_detail.html", {"room": room, "images" : images, "features": features})