from django.http.response import HttpResponse
from django.shortcuts import render
from webapp.models import Room
from webapp.models import Images
from django.http import JsonResponse


def index(request):
    rooms = Room.objects.filter(is_active=True)
    dashboardimages = Images.objects.all().order_by("-priority")[:5]
    roomsWithImages = []

    class roomswithimage:
        room: Room
        image: Images

    for room in rooms:
        roomswithimagex = roomswithimage()
        roomswithimagex.room = room
        roomswithimagex.image = room.image_ids.all().order_by("-priority")[:1]  # thumbnail
        roomsWithImages.append(roomswithimagex)

    ctx = {
        "rooms": roomsWithImages,
        "images": dashboardimages,
    }
    return render(request, "index.html", {"ctx": ctx})


def about_us(request):
    return render(request, "about_us.html")


def room_search(request):
    q = request.GET.get('q', None)

    class roomswithimage:
        room: Room
        image: Images

    roomsWithImages = []
    global rooms

    if q == "turnover":  # sırası ile en çok ciro yapan odalar
        rooms = Room.objects.raw(
            "select * from webapp_room order by ((select  SUM(paid_amount) as revenue from webapp_roomreservation where webapp_room.id  = webapp_roomreservation.room_id_id )) desc;")
    elif q == "preferred":  # sırası ile en çok tercih edilen odalar
        rooms = Room.objects.raw(
            "select *  from webapp_room order by (select  COUNT(*)  from webapp_roomreservation where webapp_room.id  = webapp_roomreservation.room_id_id) desc;")
    elif q == "available":  # müsait odalar
        rooms = Room.objects.filter(is_active=True, reservation_id=None)
    else:
        rooms = []
    for room in rooms:
        roomswithimagex = roomswithimage()
        roomswithimagex.room = room
        roomswithimagex.image = room.image_ids.all().order_by("-priority")[:1]  # thumbnail
        roomsWithImages.append(roomswithimagex)

    ctx = {
        "rooms": roomsWithImages,
    }
    return render(request, "search_room.html", {"ctx": ctx})


def room_search_by_date(request):
    global roomswithimagex
    start_date = request.GET.get('start_date', "")
    end_date = request.GET.get('end_date', "")
    pref = request.GET.get('pref', "")
    # 2023-05-04 2023-05-06

    if start_date == "" or end_date == "":
        ctx = {
            "err": "Lütfen tarihleri giriniz."
        }
        return render(request, "search_room.html", {"ctx": ctx})

    if pref == "":
        ctx = {
            "err": "Lütfen tercihinizi giriniz."
        }
        return render(request, "search_room.html", {"ctx": ctx})

    # todo:  BUNU SAKIN KAYBETME current time localtime in unixtimestamp : strftime('%s', datetime(2023-05-22, 'localtime'))
    # bus sqlite ve python'dan nefret ettim, uğraşmıcam artık sokarlar.
    if pref == "turnover":
        results = Room.objects.raw(
            "SELECT * FROM webapp_room r LEFT JOIN webapp_roomreservation rr ON r.id = rr.room_id_id WHERE (r.reservation_id_id IS NULL) OR (rr.end_date < strftime('%s', datetime(\"%s\", 'localtime')) AND rr.start_date > strftime('%s', datetime(\"%s\", 'localtime'))) GROUP BY r.id order by ((select  SUM(paid_amount) as revenue from webapp_roomreservation where r.id  = webapp_roomreservation.room_id_id )) desc;", [start_date, end_date])
    elif pref == "preferred":
        results = Room.objects.raw(
            "SELECT r.* FROM webapp_room r LEFT JOIN webapp_roomreservation rr ON r.id = rr.room_id_id WHERE (r.reservation_id_id IS NULL) OR (rr.end_date < strftime('%s', datetime({start_date}, 'localtime')) AND rr.start_date > strftime('%s', datetime({end_date}, 'localtime'))) GROUP BY r.id  order by (select  COUNT(*)  from webapp_roomreservation where webapp_room.id  = webapp_roomreservation.room_id_id) desc ;",
            [start_date, end_date])
    elif pref == "available":
        results = Room.objects.raw(
            "SELECT r.* FROM webapp_room r LEFT JOIN webapp_roomreservation rr ON r.id = rr.room_id_id WHERE (r.reservation_id_id IS NULL) OR (rr.end_date < strftime('%s', datetime({start_date}, 'localtime')) AND rr.start_date > strftime('%s', datetime({end_date}, 'localtime'))) GROUP BY r.id ")
    elif pref == "notavailable":
        results = Room.objects.raw(
            "SELECT r.* FROM webapp_room r LEFT JOIN webapp_roomreservation rr ON r.id = rr.room_id_id WHERE (r.reservation_id_id IS NOT NULL) OR NOT (rr.end_date < strftime('%s', datetime({start_date}, 'localtime')) AND rr.start_date > strftime('%s', datetime({end_date}, 'localtime'))) GROUP BY r.id order by ((select  SUM(paid_amount) as revenue from webapp_roomreservation where webapp_room.id  = webapp_roomreservation.room_id_id )) desc ;")
    else:
        results = []

    class roomswithimage:
        room: Room
        image: Images

    roomsWithImages = []
    for room in results:
        roomswithimagex = roomswithimage()
        roomswithimagex.room = room
        roomswithimagex.image = room.image_ids.all().order_by("-priority")[:1]

    roomsWithImages.append(roomswithimagex)
    ctx = {
        "rooms": roomsWithImages,
    }
    return render(request, "search_room.html", {"ctx": ctx})


def room_detail(request, room_slug):
    room = Room.objects.get(slug=room_slug)
    images = room.image_ids.all()
    features = room.features.split(',')
    return render(request, "room_detail.html", {"room": room, "images": images, "features": features})
