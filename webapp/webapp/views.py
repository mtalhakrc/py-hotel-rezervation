from django.http.response import HttpResponse
from django.shortcuts import render
from webapp.models import Room
from webapp.models import Images
from django.http import JsonResponse


def index(request):
    rooms = Room.objects.filter(is_active=True)
    dashboardimages = Images.objects.all().order_by("-priority")[:5]
    room_images = []

    roomsWithImages = []

    class roomswithimage:
        room: Room
        image: Images

    for room in rooms:
        roomswithimage = roomswithimage()
        roomswithimage.room = room
        roomswithimage.image = room.image_ids.all().order_by("-priority")[0] # thumbnail
        roomsWithImages.append(roomswithimage)

    ctx = {
        "rooms": roomsWithImages,
        "images": dashboardimages,
    }
    return render(request, "index.html", {"ctx": ctx})

def about_us(request):
    return render(request, "about_us.html")


def room_search(request):
    # iki tarih arasında rezerve edilmiş en çok ciro yapan odalar
    # start_date = request.POST.get("start_date", "")
    # end_date = request.POST.get("end_date", "")
    # print(start_date, end_date)
    # if start_date == "" or end_date == "":
    #     return HttpResponse("Lütfen tarihleri giriniz.")
    #
    # results = Room.objects.raw(
    #     "SELECT webapp_room.id, webapp_room.name, SUM(webapp_roomreservation.paid_amount) AS total_revenue FROM webapp_room INNER JOIN webapp_roomreservation ON webapp_room.id = webapp_roomreservation.room_id_id WHERE (webapp_roomreservation.start_date >= %s and webapp_roomreservation.end_date <= %s)   GROUP BY webapp_room.id ORDER BY total_revenue DESC;",
    #     [start_date, end_date])
    # print(results)

    global rooms
    q = request.GET.get('q', None)
    if q == "turnover": # sırası ile en çok ciro yapan odalar
        rooms = Room.objects.raw("select * from webapp_room order by ((select  SUM(paid_amount) as revenue from webapp_roomreservation where webapp_room.id  = webapp_roomreservation.room_id_id )) desc;")
    elif q == "preferred": # sırası ile en çok tercih edilen odalar
        rooms = Room.objects.raw("select *  from webapp_room order by (select  COUNT(*)  from webapp_roomreservation where webapp_room.id  = webapp_roomreservation.room_id_id) desc;")
    elif q == "available": # müsait odalar
        rooms = Room.objects.filter(is_active=True, reservation_id=None)
    else:
        rooms = Room.objects.filter(is_active=True)

    ctx ={
        "rooms": rooms,
    }
    return render(request, "search_room.html", {"ctx": ctx})


def room_detail(request, room_slug):
    room = Room.objects.get(slug=room_slug)
    images = room.image_ids.all()
    features = room.features.split(',')
    return render(request, "room_detail.html", {"room": room, "images": images, "features": features})
