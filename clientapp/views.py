from django.shortcuts import render
from .models import User, Tour, Slider, Day, TourInTimetable, Place, Hotel, Publications, Team, BookingTour
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404
from django.views.generic import View
from django.http import JsonResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from .forms import TourForm, UserForm
from datetime import datetime as dt
from django.db.models import Max
import datetime
from django.contrib import auth
from django.contrib.auth import authenticate, login
import hashlib

def registr(request):
    return render_to_response("registr.html")
def go_auth(request):
    return render_to_response("login.html")
@csrf_exempt
def log_in(request):

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user_id=request.session.get('user_id', 0)
        request.session["user_id"] = user.id
        user_id = request.session['user_id']
        return redirect ('../baikal')

    else:
        return render_to_response("login.html", {"wrong": "Введен неправильный логин или пароль."})

@csrf_exempt
def log_out(request):
    auth.logout(request)
    return redirect('../baikal/')

def forPage(request, listt = []):
    tours_list = listt
    paginator = Paginator(tours_list, 10)

    page = request.GET.get('page')
    try:
        tours = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tours = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tours = paginator.page(paginator.num_pages)
    return tours
def transfer(request):
    return render_to_response("transfer.html", {"user":auth.get_user(request)})



def getTours(request):
    base_url = ""
    placess = []
    tours = []
    toursResult = Tour.objects.filter(activity_status = True).reverse()
    tour_name = ""
    date_start = ""
    date_end = ""
    num_start = ""
    num_end = ""
    price_start = ""
    price_end = ""
    if request.method == 'GET':
        if 'name' in request.GET: tour_name = request.GET.get('name')
        if 'dateStart' in request.GET: date_start = request.GET.get('dateStart')
        if 'dateEnd' in request.GET: date_end = request.GET.get('dateEnd')
        if 'numStart' in request.GET: num_start = request.GET.get('numStart')
        if 'numEnd' in request.GET: num_end = request.GET.get('numEnd')
        if 'priceStart' in request.GET: price_start = request.GET.get('priceStart')
        if 'priceEnd' in request.GET: price_end = request.GET.get('priceEnd')
        if 'check' in request.GET: placess = request.GET.getlist('check')

        if len(placess)>0:
            newList = []

            for p in placess:
                base_url+="&check="+p

            for t in toursResult:
                    for p in t.places.all():
                        for pl in placess:
                            if p.name == pl and t not in newList : newList.append(t)
            toursResult = newList

        if tour_name!= "":
            base_url +="&name="+tour_name
            newList = []
            for result in toursResult:
                if result.name == tour_name and result not in newList: newList.append(result)
            toursResult = newList

        if date_start!="" and date_end == "":
            base_url += "&dateStart="+date_start
            listOfTours = []
            newList = []

            timetable = TourInTimetable.objects.filter(date__range=[date_start, "3000-01-31"])
            for tour in timetable:
                listOfTours.append(tour.tourID)

            for tour in toursResult:
                for tour2 in listOfTours:
                    if tour == tour2 and tour not in newList: newList.append(tour)
            toursResult = newList

        if date_start == "" and date_end != "":
            listOfTours = []
            newList = []
            base_url += "&dateEnd="+date_end
            timetable = TourInTimetable.objects.filter(date__range=["0001-01-01", date_end])
            for tour in timetable:
                listOfTours.append(tour.tourID)

            for tour in toursResult:
                for tour2 in listOfTours:
                    if tour == tour2 and tour not in newList: newList.append(tour)
            toursResult = newList

        if date_start != "" and date_end != "":
            listOfTours = []
            newList = []
            base_url += "&dateStart="+date_start+"&dateEnd="+date_end
            timetable = TourInTimetable.objects.filter(date__range=[date_start, date_end])
            for tour in timetable:
                listOfTours.append(tour.tourID)

            for tour in toursResult:
                for tour2 in listOfTours:
                    if tour == tour2 and tour not in newList: newList.append(tour)
            toursResult = newList

        if num_start!="":
            base_url +="&numStart="+num_start
            newList = []
            for result in toursResult:
                if result.number_of_days >= int(num_start) and result not in newList: newList.append(result)
            toursResult = newList

        if num_end!="":
            base_url +="&numStart="+num_end
            newList = []
            for result in toursResult:
                if result.number_of_days <= int(num_end) and result not in newList: newList.append(result)
            toursResult = newList

        if price_start!="":
            base_url +="&priceStart="+price_start
            newList = []
            for result in toursResult:
                if result.min_price >= int(price_start) and result not in newList: newList.append(result)
            toursResult = newList

        if price_end!="":
            base_url +="&priceEnd="+price_end
            newList = []
            for result in toursResult:
                if result.min_price <= int(price_end) and result not in newList: newList.append(result)
            toursResult = newList

    slider = Slider.objects.all()
    tours = forPage(request, toursResult)
    place = Place.objects.filter(activity_status = True)
    form = TourForm()
    return render_to_response('tours.html', {"user": auth.get_user(request), "form": form,"slider": slider, "tours": tours, "base_url": base_url, "filter_name":tour_name,"filter_date_start": date_start, "filter_date_end": date_end, "filter_num_start": num_start, "filter_num_end":num_end, "filter_places":placess, "place":place, "filter_price_start":price_start, "filter_price_end": price_end}, request)

def tourCard(request, tour_url):
    tour = Tour.objects.get(url = tour_url)
    day = Day.objects.filter(tourID = tour)
    tourInT = TourInTimetable.objects.filter(tourID = tour)

    dates = []
    for t in TourInTimetable.objects.filter(tourID = tour):
        d = t.date.strftime("%B")
        if (d == "January"): d = "января"
        if (d == "February"): d = "февраля"
        if (d == "March"): d = "марта"
        if (d == "April"): d = "апреля"
        if (d == "May"): d = "мая"
        if (d == "June"): d = "июня"
        if (d == "July"): d = "июля"
        if (d == "August"): d = "августа"
        if (d == "September"): d = "сентября"
        if (d == "October"): d = "октября"
        if (d == "November"): d = "ноября"
        if (d == "December"): d = "декабря"
        result = {"day": str(t.date.day), "month": str(d)}

        dates.append(result)
    return render_to_response('tour_card.html', {"tour":tour, "day": day, "dates": dates, "user": auth.get_user(request)})


def getPlaces(request):

    pAll = Place.objects.filter(activity_status = True)
    places = forPage(request, pAll)
    return render_to_response('places.html', {"places":places,  "user":auth.get_user(request)})

def placeCard(request, place_id):
    idd = place_id
    placee = Place.objects.filter(id = place_id, activity_status = True)[0]
    tours = Tour.objects.filter(places = placee, activity_status = True)[:6]
    hotels = Hotel.objects.filter(place_id = idd, activity_status = True)
    return render_to_response('place_card.html', {"place":placee, "tours": tours, "hotels":hotels,  "user":auth.get_user(request)})

def index(request):
    tours = Tour.objects.filter(show_on_main_status = True, activity_status = True)
    places = Place.objects.filter(show_on_main_status = True, activity_status = True)
    sliders = Slider.objects.filter(show_on_main_status = True)
    return render_to_response('index.html', {"tours":tours, "places":places, "sliders": sliders, "user":auth.get_user(request)})
def getHotels(request):
    places = Place.objects.filter(activity_status = True)
    hotelsResult = Hotel.objects.filter(activity_status = True)

    base_url = ""
    placess = []
    hotel_name = ""
    price_start = ""
    price_end = ""

    if request.method == 'GET':
        if 'name' in request.GET: hotel_name = request.GET.get('name')
        if 'priceStart' in request.GET: price_start = request.GET.get('priceStart')
        if 'priceEnd' in request.GET: price_end = request.GET.get('priceEnd')
        if 'check' in request.GET: placess = request.GET.getlist('check')

        if len(placess)>0:
            newList = []
            for p in placess:
                base_url+="&check="+p

            for t in hotelsResult:
                        for pl in placess:
                            if t.place.name == pl and t not in newList : newList.append(t)
            hotelsResult = newList

        if hotel_name!= "":
            base_url +="&name="+hotel_name
            newList = []
            for result in hotelsResult:
                if result.name == hotel_name and result not in newList: newList.append(result)
            hotelsResult = newList

        if price_start!="":
            base_url +="&priceStart="+price_start
            newList = []
            for result in hotelsResult:
                if result.min_price >= int(price_start) and result not in newList: newList.append(result)
            hotelsResult = newList

        if price_end!="":
            base_url +="&priceEnd="+price_end
            newList = []
            for result in hotelsResult:
                if result.min_price <= int(price_end) and result not in newList: newList.append(result)
            hotelsResult = newList


    hotels = forPage(request, hotelsResult)
    return render_to_response('hotels.html', {"hotels": hotels, "user":auth.get_user(request), "places": places, "base_url": base_url, "filter_name":hotel_name,"filter_places":placess, "filter_price_start":price_start, "filter_price_end": price_end, "user": auth.get_user(request)})


def hotelCard(request, hotel_id):
    hotel = Hotel.objects.filter(id = hotel_id)[0]
    return render_to_response('hotel_card.html',  {"hotel": hotel, "user": auth.get_user(request) })


def articleCard(request, article_id):
    article = Publications.objects.filter(id = article_id, activity_status = True)[0]
    return render_to_response('article_card.html',  {"article": article, "user": auth.get_user(request) })

def getArticles(request):
    articles = Publications.objects.filter(activity_status = True)
    articles = forPage(request, articles)
    return render_to_response('blog.html',  {"articles": articles, "user": auth.get_user(request) })

def contacts(request):
    return render_to_response('contacts.html', {"user": auth.get_user(request)})


def rest(request):
    return render_to_response('rest.html', {"user": auth.get_user(request)})

def getTeam(request):
    team_list = Team.objects.all()
    return render_to_response('about.html', {"team":team_list, "user": auth.get_user(request)})








import json as simplejson
@csrf_exempt
def add(request):
    allTours = Tour.objects.all()
    maxID = allTours.aggregate(Max('id'))
    form = TourForm(request.POST, request.FILES)
    post = form.save(commit=False)

    post.save()
    placeList = []
    resultPlaceList = []
    for p in form.cleaned_data['places']:
        p.tour_set.add(post)
    for s in form.cleaned_data['slider']:
        s.tour_set.add(post)


    for p in Place.objects.all():
        if post in p.tour_set.all():
            placeList.append(p)

    for p in placeList:
        resultPlaceList.append({"name": p.name, "id": p.id})
    if len(Tour.objects.filter(url = post.url))>1:
        post.delete()
        return HttpResponse(simplejson.dumps({'response': 'Already exist', 'result': 'error'}))

    newTours = list(Tour.objects.values())

    return JsonResponse({'newTours': newTours, "resultPlaceList":resultPlaceList})





def bookingsList(request):
    base_url = ""
    user = auth.get_user(request)
    if user.is_staff==True:
        client = ""
        tourInT=""
        date=""
        status=""
        tourBasic=""
        tour = ""
        tourInTimetable = ""
        payment = ""
        bookingResult = BookingTour.objects.all()
        if request.method == 'GET':
            if 'date' in request.GET: date = request.GET.get('date')
            if 'client' in request.GET: client = request.GET.get('client')
            if 'tourInT' in request.GET: tourInT = request.GET.get('tourInT')
            if 'status' in request.GET: status = request.GET.get('status')
            if 'tourBasic' in request.GET: tourBasic = request.GET.get('tourBasic')
            if 'payment' in request.GET: payment = request.GET.get('payment')

        if status !="":
            base_url +="&status="+status
            newList = []
            for result in bookingResult:
                if result.status == status and result not in newList: newList.append(result)
            bookingResult = newList

        if tourBasic!="":
            base_url +="&tourBasic="+tourBasic
            newList = []
            for result in bookingResult:
                if result.tourInT.tourID.id == int(tourBasic) and result not in newList: newList.append(result)
            bookingResult = newList
            tour = Tour.objects.get(id = int(tourBasic))


        if tourInT!="":
            base_url +="&tourInT="+tourInT
            newList = []
            for result in bookingResult:
                if result.tourInT.id == tourInT and result not in newList: newList.append(result)
            bookingResult = newList
            tourInTimetable = TourInTimetable.objects.get(id = int(tourInT))

        if date!="":
            base_url +="&date="+date
            newList = []
            date1 = date.split('-')
            date1 = datetime.date(int(date1[2]), int(date1[1]), int(date1[0]))
            for result in bookingResult:
                if result.date_of_booking == date1 and result not in newList: newList.append(result)
            bookingResult = newList

        if client!="":
            base_url +="&client="+client
            newList = []
            for result in bookingResult:
                if result.user.id == int(client) and result not in newList: newList.append(result)
            bookingResult = newList
            client = User.objects.get(id = int(client))

        if payment!="":
            base_url +="&payment="+payment
            newList=[]
            if payment=="Оплачено":
                for result in bookingResult:
                    if (result.number_of_people*result.tourInT.price-result.payment)  ==0 and result not in newList: newList.append(result)
                bookingResult = newList

            if payment=="Оплачено частично":
                for result in bookingResult:
                    if result.number_of_people*result.tourInT.price-result.payment > 0 and result not in newList: newList.append(result)
                bookingResult = newList

            if payment=="Не оплачено":
                for result in bookingResult:
                    if result.payment == 0 and result not in newList: newList.append(result)
                bookingResult = newList

            if payment=="Переплата":
                for result in bookingResult:
                    if result.number_of_people*result.tourInT.price-result.payment < 0 and result not in newList: newList.append(result)
                bookingResult = newList



        bookingsList = forPage(request, bookingResult)
        return render_to_response('adm_bookings_list.html', {"bookingsList":bookingsList, "user": user, "base_url": base_url, "filter_basicTour": tourBasic, "filter_tourInT": tourInTimetable,
        "filter_client": client, "filter_status":status, "filter_date":date, "tour":tour,  "filter_payment":payment})
    else: return HttpResponse("Доступ в данный раздел ограничен.")

def timetableList(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        base_url = ""
        client = ""
        date=""
        date_end=""
        tourBasic=""
        maxPrice = ""
        freeSpace = ""
        freeSpaceMin = ""
        timetableResult = TourInTimetable.objects.all()
        if request.method == 'GET':
            if 'date' in request.GET: date = request.GET.get('date')
            if 'date_end' in request.GET: date_end = request.GET.get('date_end')
            if 'client' in request.GET: client = request.GET.get('client')
            if 'tourBasic' in request.GET: tourBasic = request.GET.get('tourBasic')
            if 'maxPrice' in request.GET: maxPrice = request.GET.get('maxPrice')
            if 'freeSpace' in request.GET: freeSpace = request.GET.get('freeSpace')
            if 'freeSpaceMin' in request.GET: freeSpaceMin = request.GET.get('freeSpaceMin')

        if tourBasic!="":
            base_url +="&tourBasic="+tourBasic
            newList = []
            for result in timetableResult:
                if result.tourID.id == int(tourBasic) and result not in newList: newList.append(result)
            timetableResult = newList
            tourBasic = Tour.objects.get(id = int(tourBasic))
        if client!="":
            base_url +="&client="+client
            newList = []
            try:
                client = User.objects.get(id = client)
                bookings=BookingTour.objects.filter(user = client)[0]

                for result in timetableResult:
                    if result.id ==  bookings.tourInT.id  and result not in newList: newList.append(result)
                timetableResult = newList
            except IndexError: timetableResult = newList

        if date!="" and date_end == "":
            base_url += "&date="+date
            listOfTours = []
            newList = []
            date1 = date.split('-')
            date1 = datetime.date(int(date1[2]), int(date1[1]), int(date1[0]))
            timetable = TourInTimetable.objects.filter(date__range=[date1, "3000-01-31"])
            for tour in timetableResult:
                for tour2 in timetable:
                    if tour == tour2 and tour not in newList: newList.append(tour)
            timetableResult = newList

        if date == "" and date_end != "":
            newList = []
            date1 = date_end.split('-')
            date1 = datetime.date(int(date1[2]), int(date1[1]), int(date1[0]))
            base_url += "&dateEnd="+date_end
            timetable = TourInTimetable.objects.filter(date__range=["0001-01-01", date1])

            for tour in timetableResult:
                for tour2 in timetable:
                    if tour == tour2 and tour not in newList: newList.append(tour)
            timetableResult = newList

        if date != "" and date_end != "":
            newList = []
            date1 = date.split('-')
            date1 = datetime.date(int(date1[2]), int(date1[1]), int(date1[0]))
            date2 = date_end.split('-')
            date2 = datetime.date(int(date2[2]), int(date2[1]), int(date2[0]))

            base_url += "&dateEnd="+date_end+"&date="+date
            timetable = TourInTimetable.objects.filter(date__range=[date1, date2])

            for tour in timetableResult:
                for tour2 in timetable:
                    if tour == tour2 and tour not in newList: newList.append(tour)
            timetableResult = newList

        if freeSpaceMin!="" and freeSpace=="":
            base_url +="&freeSpaceMin="+freeSpaceMin
            newList = []
            for result in timetableResult:
                freeS = getFrS(result.id)
                if freeS >= int(freeSpaceMin) and result not in newList: newList.append(result)
            timetableResult = newList


        if freeSpaceMin=="" and freeSpace!="":
            base_url +="&freeSpace="+freeSpace
            newList = []
            for result in timetableResult:
                freeS = getFrS(result.id)
                if freeS <= int(freeSpace) and result not in newList: newList.append(result)
            timetableResult = newList

        if freeSpaceMin!="" and freeSpace!="":
            base_url +="&freeSpaceMin="+freeSpaceMin+"&freeSpace="+freeSpace
            newList = []
            for result in timetableResult:
                freeS = getFrS(result.id)
                if freeS <= int(freeSpace) and freeS >= int(freeSpaceMin) and freeS  and result not in newList: newList.append(result)
            timetableResult = newList

        if maxPrice!="":
            base_url +="&maxPrice="+maxPrice
            newList = []
            for result in timetableResult:
                if result.price <= int(maxPrice) and result not in newList: newList.append(result)
            timetableResult = newList

        timetableResult = forPage(request, timetableResult)
        bookings = BookingTour.objects.all()


        return render_to_response('adm_timetable_list.html', {"timetable":timetableResult, "user": user, "bookings":bookings,
        "filter_basicTour":tourBasic, "filter_client": client, "filter_date":date, "filter_dateEnd":date_end, "filter_freeSpace":freeSpace, "filter_freeSpaceMin":freeSpaceMin, "filter_maxPrice":maxPrice})
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def addingToTimetabelCard(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        hotels = Hotel.objects.all()
        tours = Tour.objects.all()
        return render_to_response('tourInTimetableAdd.html', {"hotels":hotels, "tours": tours, "user":user})
    else: return HttpResponse("Доступ в данный раздел ограничен.")
@csrf_exempt
def addTimetable(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        tourID = ""
        price = ""
        date = ""
        name = ""
        num_of_people = ""
        hotels = []
        t = ""
        if request.method == 'POST':
            if 'name' in request.POST: name = request.POST.get('name')
            if 'selectedTour' in request.POST: tourID = request.POST.get('selectedTour')
            if 'price' in request.POST: price = request.POST.get('price')
            if 'date' in request.POST:
                date = request.POST.get('date')
                date1 = date.split('/')
                date1 = datetime.date(int(date1[2]), int(date1[0]), int(date1[1]))
                date = date1
            if 'num' in request.POST: num_of_people = request.POST.get('num')
            if 'hotels' in request.POST: hotels = request.POST.getlist('hotels')

            t = Tour.objects.filter(name = tourID)[0]
            newTimetable = TourInTimetable.objects.create(name = name, tourID = t, price = int(price), date = date, capacity= int(num_of_people))
            newTimetable.save()
            for h in  hotels:
                hotel = Hotel.objects.filter(name = h)[0]
                hotel.tourintimetable_set.add(newTimetable)
        hotels = Hotel.objects.all()
        tours = Tour.objects.all()
        return redirect('../timetable/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")




def getTourInTimetable(request, t_id):
    user = auth.get_user(request)
    bookingsResult =[]
    if user.is_staff==True:
        t = TourInTimetable.objects.filter(id = t_id)[0]
        date = t.date.strftime("%d-%m-%Y")
        bookings = BookingTour.objects.filter(tourInT=t)

        num = 0
        for b in bookings:

            if b.status=="Подтверждено":
                bookingsResult.append(b)
                num+=b.number_of_people

        freeS = getFrS(t_id)
        return render_to_response("tourintimetableCard.html", {"tour_t": t, "date": date, "user":user, "bookings": bookingsResult, "num":num, "freeS":freeS})
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def getTimetableCardToEdit(request, t_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        t = TourInTimetable.objects.filter(id = t_id)[0]
        date = t.date.strftime("%m/%d/%Y")
        hotels = Hotel.objects.all()
        tours = Tour.objects.all()
        return render_to_response("tourInTimetableEdit.html", {"tour_t": t, "date": date, "hotels":hotels, "tours":tours, "user":user})
    else: return HttpResponse("Доступ в данный раздел ограничен.")

@csrf_exempt
def editTimetable(request, t_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        if request.method == "POST":
            name = request.POST.get("name")
            tour = request.POST.get("selectedTour")
            price = request.POST.get("price")
            date = request.POST.get("date")
            num = request.POST.get("num")
            hotels = request.POST.getlist("hotels")
            t = Tour.objects.get(name = tour)
            tour_t = TourInTimetable.objects.get(id=t_id)
            tour_t.tourID=t
            tour_t.name = name
            tour_t.price = int(price)
            date = datetime.strptime(date, "%m/%d/%Y")
            date = date.strftime("%Y-%m-%d")
            tour_t.date = date
            tour_t.capacity = int(num)
            tour_t.save()
            for h in tour_t.hotels.all():
                h.tourintimetable_set.remove(tour_t)

            for h in hotels:
                h = Hotel.objects.get(name = h)
                h.tourintimetable_set.add(tour_t)
        return redirect('../../timetable/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")

def del_t(request, t_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        TourInTimetable.objects.filter(id=t_id).delete()
        return redirect('../../timetable/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")


@csrf_exempt
def getTourToEdit(request, tour_url):
    user = auth.get_user(request)
    if user.is_staff==True:
        t = Tour.objects.get(url = tour_url)
        days = Day.objects.filter(tourID = t).order_by("number")

        slider = Slider.objects.all()
        places = Place.objects.filter(activity_status = True)
        form = TourForm()
        return render_to_response("tourCardEdit.html", {"form": TourForm, "tour": t, "days":days, "slider":slider, "places": places, "user":user})
    else: return HttpResponse("Доступ в данный раздел ограничен.")




@csrf_exempt
def editTour1(request, tour_url):
    user = auth.get_user(request)
    if user.is_staff==True:
        tour = Tour.objects.get(url = tour_url)
        places = request.POST.getlist("places")
        slider = request.POST.getlist("slider")
        if len(places)>0:
            for p in tour.places.all():
                p.tour_set.remove(tour)
        if len(slider)>0:
            for p in tour.slider.all():
                p.tour_set.remove(tour)
        form = TourForm(request.POST, request.FILES, instance = tour)
        post = form.save(commit=False)
        post.save()
        for p in form.cleaned_data['places']:
            p.tour_set.add(post)
        for s in form.cleaned_data['slider']:
            s.tour_set.add(post)
        return redirect('../../tourCard/'+str(tour_url)+'/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def del_tour(request, tour_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        Tour.objects.get(id=tour_id).delete()
        return redirect('../../tours/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")



def get_tours_info(request, tour_url):
    tour = Tour.objects.get(url=tour_url)
    dates = []
    for t in TourInTimetable.objects.filter(tourID = tour.id):
        d = t.date.strftime("%B")
        if (d == "January"): d = "января"
        if (d == "February"): d = "февраля"
        if (d == "March"): d = "марта"
        if (d == "April"): d = "апреля"
        if (d == "May"): d = "мая"
        if (d == "June"): d = "июня"
        if (d == "July"): d = "июля"
        if (d == "August"): d = "августа"
        if (d == "September"): d = "сентября"
        if (d == "October"): d = "октября"
        if (d == "November"): d = "ноября"
        if (d == "December"): d = "декабря"
        result = {"day": str(t.date.day), "month": str(d)}

        dates.append(result)
    firstTour = TourInTimetable.objects.all()[0]

    bookings = BookingTour.objects.all()



    return render_to_response('tours_info.html', {"dates":dates, "user": auth.get_user(request), "bookings":bookings, "tour":tour, "tour_in_timetable": TourInTimetable.objects.filter(tourID = tour.id), "firstTour":firstTour})


def booking_tour_page(request, TourInTimetableID):
    user = auth.get_user(request)
    tourInT = TourInTimetable.objects.get(id = TourInTimetableID)
    tour = Tour.objects.get(id = tourInT.tourID.id)
    freeSpace = getFrS(TourInTimetableID)
    form = UserForm()
    if user.is_anonymous:
        return render_to_response('booking_tour.html', {"tourInT":tourInT, "tour": tour, "form": form, "freeSpace":freeSpace})
    else:
        return render_to_response('booking_tour.html', {"tourInT":tourInT, "user":user, "tour": tour, "form": form, "freeSpace":freeSpace})

import random

@csrf_exempt
def addNewBooking(request, TourInTimetableID, number_of_people):
    allTours = Tour.objects.all()
    maxID = allTours.aggregate(Max('id'))
    try:
        form = UserForm(request.POST)
        newUser = form.save(commit=False)
        username = random.random()*100
        newUser.username = username
        newUser.save()
        newUser.set_password(newUser.password)
        newUser.username = newUser.id
        newUser.save()
    except Exception:
        newUser = auth.get_user(request)
    newTourInT = TourInTimetable.objects.get(id = TourInTimetableID)
    newBooking = BookingTour.objects.create(tourInT = newTourInT, user = newUser, status = "На рассмотрении", payment = 0, number_of_people = number_of_people, date_of_booking = dt.today())
    newBooking.save()
    return HttpResponse(TourInTimetableID);

@csrf_exempt
def addNewBookingByM(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        t_id = request.POST.get('tourInTID')
        tourInTinBooking = TourInTimetable.objects.get(id = t_id)
        user_id = request.POST.get('userID')
        userInBooking = User.objects.get(id = user_id)
        numberOfPeople = request.POST.get('numberOfPeople')
        payment = request.POST.get('payment')
        status = request.POST.get('status')
        newBooking = BookingTour.objects.create(tourInT = tourInTinBooking, user= userInBooking, status = status, payment = payment, number_of_people=numberOfPeople, date_of_booking = dt.today() )
    #    return redirect ('../timetable/')
        return HttpResponseRedirect('../bookings_list/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")

def getBookingCardToEdit(request, booking_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        booking = BookingTour.objects.get(id = booking_id)
        freeSpace = getFrS(booking.tourInT.id)
        return render_to_response("adm_bookingCard_edit.html", {"booking": booking, "user":user, "freeSpace":freeSpace})
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def editBookingCard(request, booking_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        booking = BookingTour.objects.get(id = booking_id)
        userInBooking = User.objects.get(id = request.POST.get('userID'))
        tourInTinBooking = TourInTimetable.objects.get(id = request.POST.get('tourInTID'))
        booking.user=userInBooking
        booking.tourInT = tourInTinBooking
        booking.status = request.POST.get('status')
        booking.number_of_people = request.POST.get('numberOfPeople')
        booking.payment = request.POST.get('payment')
        booking.save()
        return HttpResponseRedirect('../../bookings_list/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def del_booking(request, booking_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        BookingTour.objects.filter(id=booking_id).delete()
        return redirect('../../bookings_list/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")

# def getTours(request):
#     base_url = ""
#     placess = []
#     tours = []
#     toursResult = Tour.objects.filter(activity_status = True).reverse()
#     tour_name = ""
#     date_start = ""
#     date_end = ""
#     num_start = ""
#     num_end = ""
#     price_start = ""
#     price_end = ""
#     if request.method == 'GET':
#         if 'name' in request.GET: tour_name = request.GET.get('name')
#         if 'dateStart' in request.GET: date_start = request.GET.get('dateStart')
#         if 'dateEnd' in request.GET: date_end = request.GET.get('dateEnd')
#         if 'numStart' in request.GET: num_start = request.GET.get('numStart')
#         if 'numEnd' in request.GET: num_end = request.GET.get('numEnd')
#         if 'priceStart' in request.GET: price_start = request.GET.get('priceStart')
#         if 'priceEnd' in request.GET: price_end = request.GET.get('priceEnd')
#         if 'check' in request.GET: placess = request.GET.getlist('check')
#
#         if len(placess)>0:
#             newList = []
#
#             for p in placess:
#                 base_url+="&check="+p
#
#             for t in toursResult:
#                     for p in t.places.all():
#                         for pl in placess:
#                             if p.name == pl and t not in newList : newList.append(t)
#             toursResult = newList
#
#         if tour_name!= "":
#             base_url +="&name="+tour_name
#             newList = []
#             for result in toursResult:
#                 if result.name == tour_name and result not in newList: newList.append(result)
#             toursResult = newList
#
#         if date_start!="" and date_end == "":
#             base_url += "&dateStart="+date_start
#             listOfTours = []
#             newList = []
#
#             timetable = TourInTimetable.objects.filter(date__range=[date_start, "3000-01-31"])
#             for tour in timetable:
#                 listOfTours.append(tour.tourID)
#
#             for tour in toursResult:
#                 for tour2 in listOfTours:
#                     if tour == tour2 and tour not in newList: newList.append(tour)
#             toursResult = newList
#
#         if date_start == "" and date_end != "":
#             listOfTours = []
#             newList = []
#             base_url += "&dateEnd="+date_end
#             timetable = TourInTimetable.objects.filter(date__range=["0001-01-01", date_end])
#             for tour in timetable:
#                 listOfTours.append(tour.tourID)
#
#             for tour in toursResult:
#                 for tour2 in listOfTours:
#                     if tour == tour2 and tour not in newList: newList.append(tour)
#             toursResult = newList
#
#         if date_start != "" and date_end != "":
#             listOfTours = []
#             newList = []
#             base_url += "&dateStart="+date_start+"&dateEnd="+date_end
#             timetable = TourInTimetable.objects.filter(date__range=[date_start, date_end])
#             for tour in timetable:
#                 listOfTours.append(tour.tourID)
#
#             for tour in toursResult:
#                 for tour2 in listOfTours:
#                     if tour == tour2 and tour not in newList: newList.append(tour)
#             toursResult = newList
#
#         if num_start!="":
#             base_url +="&numStart="+num_start
#             newList = []
#             for result in toursResult:
#                 if result.number_of_days >= int(num_start) and result not in newList: newList.append(result)
#             toursResult = newList
#
#         if num_end!="":
#             base_url +="&numStart="+num_end
#             newList = []
#             for result in toursResult:
#                 if result.number_of_days <= int(num_end) and result not in newList: newList.append(result)
#             toursResult = newList
#
#         if price_start!="":
#             base_url +="&priceStart="+price_start
#             newList = []
#             for result in toursResult:
#                 if result.min_price >= int(price_start) and result not in newList: newList.append(result)
#             toursResult = newList
#
#         if price_end!="":
#             base_url +="&priceEnd="+price_end
#             newList = []
#             for result in toursResult:
#                 if result.min_price <= int(price_end) and result not in newList: newList.append(result)
#             toursResult = newList
#
#     slider = Slider.objects.all()
#     tours = forPage(request, toursResult)
#     place = Place.objects.filter(activity_status = True)
#     form = TourForm()
#     return render_to_response('tours.html', {"user": auth.get_user(request), "form": form,"slider": slider, "tours": tours, "base_url": base_url, "filter_name":tour_name,"filter_date_start": date_start, "filter_date_end": date_end, "filter_num_start": num_start, "filter_num_end":num_end, "filter_places":placess, "place":place, "filter_price_start":price_start, "filter_price_end": price_end}, request)
#


def bookingsList(request):
    base_url = ""
    user = auth.get_user(request)
    if user.is_staff==True:
        client = ""
        tourInT=""
        date=""
        status=""
        tourBasic=""
        tour = ""
        tourInTimetable = ""
        payment = ""
        bookingResult = BookingTour.objects.all()
        if request.method == 'GET':
            if 'date' in request.GET: date = request.GET.get('date')
            if 'client' in request.GET: client = request.GET.get('client')
            if 'tourInT' in request.GET: tourInT = request.GET.get('tourInT')
            if 'status' in request.GET: status = request.GET.get('status')
            if 'tourBasic' in request.GET: tourBasic = request.GET.get('tourBasic')
            if 'payment' in request.GET: payment = request.GET.get('payment')

        if status !="":
            base_url +="&status="+status
            newList = []
            for result in bookingResult:
                if result.status == status and result not in newList: newList.append(result)
            bookingResult = newList

        if tourBasic!="":
            base_url +="&tourBasic="+tourBasic
            newList = []
            for result in bookingResult:
                if result.tourInT.tourID.id == int(tourBasic) and result not in newList: newList.append(result)
            bookingResult = newList
            tour = Tour.objects.get(id = int(tourBasic))


        if tourInT!="":
            base_url +="&tourInT="+tourInT
            newList = []
            for result in bookingResult:
                if result.tourInT.id == tourInT and result not in newList: newList.append(result)
            bookingResult = newList
            tourInTimetable = TourInTimetable.objects.get(id = int(tourInT))

        if date!="":
            base_url +="&date="+date
            newList = []
            date1 = date.split('-')
            date1 = datetime.date(int(date1[2]), int(date1[1]), int(date1[0]))
            for result in bookingResult:
                if result.date_of_booking == date1 and result not in newList: newList.append(result)
            bookingResult = newList

        if client!="":
            base_url +="&client="+client
            newList = []
            for result in bookingResult:
                if result.user.id == int(client) and result not in newList: newList.append(result)
            bookingResult = newList
            client = User.objects.get(id = int(client))

        if payment!="":
            base_url +="&payment="+payment
            newList=[]
            if payment=="Оплачено":
                for result in bookingResult:
                    if (result.number_of_people*result.tourInT.price-result.payment)  ==0 and result not in newList: newList.append(result)
                bookingResult = newList

            if payment=="Оплачено частично":
                for result in bookingResult:
                    if result.number_of_people*result.tourInT.price-result.payment > 0 and result not in newList: newList.append(result)
                bookingResult = newList

            if payment=="Не оплачено":
                for result in bookingResult:
                    if result.payment == 0 and result not in newList: newList.append(result)
                bookingResult = newList

            if payment=="Переплата":
                for result in bookingResult:
                    if result.number_of_people*result.tourInT.price-result.payment < 0 and result not in newList: newList.append(result)
                bookingResult = newList



        bookingsList = forPage(request, bookingResult)
        return render_to_response('adm_bookings_list.html', {"bookingsList":bookingsList, "user": user, "base_url": base_url, "filter_basicTour": tourBasic, "filter_tourInT": tourInTimetable,
        "filter_client": client, "filter_status":status, "filter_date":date, "tour":tour,  "filter_payment":payment})
    else: return HttpResponse("Доступ в данный раздел ограничен.")



def addingToBookingCard(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        tourInT = TourInTimetable.objects.filter(date__gt = dt.today())
        users = User.objects.filter(is_staff = False)
        userInBooking = None
        tour = None
        if request.method == 'GET':
            if 'user' in request.GET:
                userInBooking = request.GET.get('user')
                userInBooking = User.objects.get(id=userInBooking)
            if 'tour' in request.GET:
                tour = request.GET.get('tour')
                tour = Tour.objects.get(id=tour)
        return render_to_response('adm_bookingCard_add.html', {"user":user, "tour":tour, "userInBooking": userInBooking, "tourInBooking": tour})
    else: return HttpResponse("Доступ в данный раздел ограничен.")



@csrf_exempt
def getTourInTById(request, t_id):
    tourInT = TourInTimetable.objects.get(id = t_id)
    tours_price = tourInT.price
    return JsonResponse({'id': tourInT.id, "tourInT_name":tourInT.name, "tours_price":tours_price})

def getFreeSpace(request, t_id):
    freeSpace = getFrS(t_id)
    return JsonResponse({'freeSpace': freeSpace})

def getFrS(t_id):
    tourInT = TourInTimetable.objects.get(id=t_id)
    bookings=BookingTour.objects.filter(tourInT = tourInT)
    booked = 0
    for b in bookings:
        booked= booked+b.number_of_people
    freeSpace = tourInT.capacity - booked
    return freeSpace

def basicTourChoosing(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        tours = Tour.objects.all()
        tours = forPage(request, tours)
        return render_to_response('adm_basicTourChooser.html', {"tours":tours, "user": user})
    else: return HttpResponse("Доступ в данный раздел ограничен.")
@csrf_exempt
def getTourById(request, t_id):
    tour = Tour.objects.get(id = t_id)
    return JsonResponse({'id': tour.id, "tour_name":tour.name, "tour_url": tour.url})

def tourChoosing(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        timetable = TourInTimetable.objects.all()
        timetable = forPage(request, timetable)
        bookings = BookingTour.objects.all()
        return render_to_response('adm_toursListChooser.html', {"timetable":timetable, "user": user, "bookings":bookings})
    else: return HttpResponse("Доступ в данный раздел ограничен.")

def userChoosing(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        users = User.objects.filter(is_staff=False)
        users = forPage(request, users)
        return render_to_response('adm_userListChooser.html', {"users":users, "user": user})
    else: return HttpResponse("Доступ в данный раздел ограничен.")
#
#
# def bookingsList(request):
#     base_url = ""
#     user = auth.get_user(request)
#     if user.is_staff==True:
#         client = ""
#         tourInT=""
#         date=""
#         status=""
#         tourBasic=""
#         tour = ""
#         tourInTimetable = ""
#         payment = ""
#         bookingResult = BookingTour.objects.all()
#         if request.method == 'GET':
#             if 'date' in request.GET: date = request.GET.get('date')
#             if 'client' in request.GET: client = request.GET.get('client')
#             if 'tourInT' in request.GET: tourInT = request.GET.get('tourInT')
#             if 'status' in request.GET: status = request.GET.get('status')
#             if 'tourBasic' in request.GET: tourBasic = request.GET.get('tourBasic')
#             if 'payment' in request.GET: payment = request.GET.get('payment')
#
#         if status !="":
#             base_url +="&status="+status
#             newList = []
#             for result in bookingResult:
#                 if result.status == status and result not in newList: newList.append(result)
#             bookingResult = newList
#
#         if tourBasic!="":
#             base_url +="&tourBasic="+tourBasic
#             newList = []
#             for result in bookingResult:
#                 if result.tourInT.tourID.id == int(tourBasic) and result not in newList: newList.append(result)
#             bookingResult = newList
#             tour = Tour.objects.get(id = int(tourBasic))
#
#
#         if tourInT!="":
#             base_url +="&tourInT="+tourInT
#             newList = []
#             for result in bookingResult:
#                 if result.tourInT.id == tourInT and result not in newList: newList.append(result)
#             bookingResult = newList
#             tourInTimetable = TourInTimetable.objects.get(id = int(tourInT))
#
#         if date!="":
#             base_url +="&date="+date
#             newList = []
#             date1 = date.split('-')
#             date1 = datetime.date(int(date1[2]), int(date1[1]), int(date1[0]))
#             for result in bookingResult:
#                 if result.date_of_booking == date1 and result not in newList: newList.append(result)
#             bookingResult = newList
#
#         if client!="":
#             base_url +="&client="+client
#             newList = []
#             for result in bookingResult:
#                 if result.user.id == int(client) and result not in newList: newList.append(result)
#             bookingResult = newList
#             client = User.objects.get(id = int(client))
#
#         if payment!="":
#             base_url +="&payment="+payment
#             newList=[]
#             if payment=="Оплачено":
#                 for result in bookingResult:
#                     if (result.number_of_people*result.tourInT.price-result.payment)  ==0 and result not in newList: newList.append(result)
#                 bookingResult = newList
#
#             if payment=="Оплачено частично":
#                 for result in bookingResult:
#                     if result.number_of_people*result.tourInT.price-result.payment > 0 and result not in newList: newList.append(result)
#                 bookingResult = newList
#
#             if payment=="Не оплачено":
#                 for result in bookingResult:
#                     if result.payment == 0 and result not in newList: newList.append(result)
#                 bookingResult = newList
#
#             if payment=="Переплата":
#                 for result in bookingResult:
#                     if result.number_of_people*result.tourInT.price-result.payment < 0 and result not in newList: newList.append(result)
#                 bookingResult = newList
#
#
#
#         bookingsList = forPage(request, bookingResult)
#         return render_to_response('adm_bookings_list.html', {"bookingsList":bookingsList, "user": user, "base_url": base_url, "filter_basicTour": tourBasic, "filter_tourInT": tourInTimetable,
#         "filter_client": client, "filter_status":status, "filter_date":date, "tour":tour,  "filter_payment":payment})
#     else: return HttpResponse("Доступ в данный раздел ограничен.")





def userList(request):
    user = auth.get_user(request)

    if user.is_staff==True:
        base_url = ""
        surname = ""
        name = ""
        email=""
        phone=""
        users_group =""
        usersList = User.objects.all().order_by('date_joined').reverse()

        if request.method == 'GET':
            if 'surname' in request.GET: surname = request.GET.get('surname')
            if 'name' in request.GET: name = request.GET.get('name')
            if 'email' in request.GET: email = request.GET.get('email')
            if 'users_group' in request.GET: users_group = request.GET.get('users_group')
            if 'phone' in request.GET: phone = request.GET.get('phone')

        if surname !="":
            base_url +="&surname="+surname
            newList = []
            for result in usersList:
                if result.surname == surname and result not in newList: newList.append(result)
            usersList = newList
        if name !="":
            base_url +="&name="+name
            newList = []
            for result in usersList:
                if result.name == name and result not in newList: newList.append(result)
            usersList = newList
        if email !="":
            base_url +="&email="+email
            newList = []
            for result in usersList:
                if result.email == email and result not in newList: newList.append(result)
            usersList = newList
        if phone !="":
            base_url +="&phone="+phone
            newList = []
            for result in usersList:
                if result.phone_number == phone and result not in newList: newList.append(result)
            usersList = newList
        if users_group !="":
            base_url +="&users_group="+users_group
            newList = []
            if users_group=="Клиент":
                for result in usersList:
                    if result.is_staff ==False and result not in newList: newList.append(result)
                usersList = newList
            if users_group=="Сотрудник":
                for result in usersList:
                    if result.is_staff == True and result not in newList: newList.append(result)
                usersList = newList

        users = forPage(request, usersList)
        return render_to_response('adm_user_list.html', {"users":users, "user": user, "base_url": base_url, "filter_surname":surname, "filter_name":name, "filter_email":email, "filter_phone":phone, "filter_users_group":users_group})

    else: return HttpResponse("Доступ в данный раздел ограничен.")








def getUserCard(request, user_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        userCard = User.objects.get(id = user_id)
        return render_to_response("adm_user_card.html", {"userCard": userCard, "user":user})
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def getUserCardToEdit(request, user_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        userCard = User.objects.get(id = user_id)
        return render_to_response("adm_userCard_edit.html", {"userCard": userCard})
    else: return HttpResponse("Доступ в данный раздел ограничен.")

def addUserCard(request):
    user = auth.get_user(request)
    try:
        if user.is_staff==True:
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            if (request.POST.get('password')!=""):
                password = request.POST.get('password')
            if request.POST.get('type')=="Клиент":
                is_staff = False
            else: is_staff = True
            users = User.objects.all()
            max = users[len(users)-1].id
            newUser = User.objects.create(name = name, surname = surname, email = email, phone_number = phone_number, is_staff= is_staff, username=max)
            newUser.set_password(password)
            newUser.save()
            return HttpResponse("ок")
        else: return HttpResponse("Доступ в данный раздел ограничен.")
    except:  return HttpResponse("Пользователь с таким email уже зарегестрирован")


def addingNewUser(request):
    user = auth.get_user(request)
    if user.is_staff==True:
        return render_to_response("adm_userCard_add.html", {"user":user})
    else: return HttpResponse("Доступ в данный раздел ограничен.")





@csrf_exempt
def getUserById(request, user_id):
    user = User.objects.get(id = user_id)
    return JsonResponse({'user_id': user.id, "user_name":user.name, "user_surname": user.surname})


def ediUserCard(request, user_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        userCard = User.objects.get(id = user_id)
        userCard.name = request.POST.get('name')
        userCard.surname = request.POST.get('surname')
        userCard.phone_number = request.POST.get('phone_number')
        userCard.email = request.POST.get('email')
        if (request.POST.get('password')!=""):
            userCard.password = request.POST.get('password')
            userCard.set_password(userCard.password)
        if request.POST.get('type')=="Клиент":
            userCard.is_staff = False
        else: userCard.is_staff = True
        userCard.save()
        return HttpResponse("ок")
    else: return HttpResponse("Доступ в данный раздел ограничен.")



def addNewUser(request):
    user = auth.get_user(request)
    if user.is_anonymous==True:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        users = User.objects.all()
        max = users[len(users)-1].id
        userCard = User.objects.create(name = name, surname = surname, phone_number = phone_number, email = email, is_staff=False, username = max+1)

        if (request.POST.get('password')!=""):
            userCard.password = request.POST.get('password')
            userCard.set_password(userCard.password)

        userCard.save()
        return HttpResponse("ок")
    else: return HttpResponse("Вы уже зарегестрированы")






def editUserCardSelf(request, user_id):
    user = auth.get_user(request)
    if user.id==user_id:
        userCard = User.objects.get(id = user_id)
        userCard.name = request.POST.get('name')
        userCard.surname = request.POST.get('surname')
        userCard.phone_number = request.POST.get('phone_number')
        userCard.email = request.POST.get('email')
        if (request.POST.get('password')!=""):
            userCard.password = request.POST.get('password')
            userCard.set_password(userCard.password)
        if request.POST.get('type')=="Клиент":
            userCard.is_staff = False
        else: userCard.is_staff = True
        userCard.save()
        return HttpResponse("ок")
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def del_user(request, user_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        User.objects.filter(id=user_id).delete()
        return redirect('../../userList/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")


def personal_account_show(request):
    user = auth.get_user(request)
    if user.is_anonymous:
        return HttpResponse("Для доступа в личный кабинет Вам необходимо зарегестрироваться на сайте или войти")
    else:
        bookings = BookingTour.objects.filter(user = user).order_by('date_of_booking').reverse()
        bookings = forPage(request, bookings)
        return render_to_response("account.html", {"bookings":bookings, "user": user})

def cancel_booking(request, booking_id):
    user = auth.get_user(request)
    booking = BookingTour.objects.get(id = booking_id)
    if user==booking.user:
        booking.status = "Отменено"
        booking.save()
        return redirect ('../../personal_account/')
    else: return HttpResponse("Доступ ограничен.")


def editUserInAccount(request, user_id):
    user = auth.get_user(request)
    if user.is_staff==True:
        userCard = User.objects.get(id = user_id)
        userCard.name = request.POST.get('name')
        userCard.surname = request.POST.get('surname')
        userCard.phone_number = request.POST.get('phone_number')
        userCard.email = request.POST.get('email')
        userCard.password = request.POST.get('password')
        userCard.set_password(userCard.password)
        if request.POST.get('type')=="Клиент":
            userCard.is_staff = False
        else: userCard.is_staff = True
        userCard.save()
        return HttpResponseRedirect('../personal_account/')
    else: return HttpResponse("Доступ в данный раздел ограничен.")




def sign_up(request):
    user = auth.get_user(request)
    if user.is_anonymous==True:
        return render_to_response ("sign_up.html", {"user":user})
    else: return HttpResponse("Вы уже зарегестрированы")

def account_settings(request):
    user_info = auth.get_user(request)
    if user_info.is_anonymous:
        return HttpResponse("Для доступа в личный кабинет Вам необходимо зарегестрироваться на сайте")
    else:
        return render_to_response("personal_account_settings.html", {"user_info":user_info, "user":user_info})
