"""baikal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from clientapp import views
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from clientapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientapp/', include('clientapp.urls')),
    path('tours/', views.getTours, name = "getTours"),

    #клиентская часть
        path('baikal/', views.index, name = "index"),
        path('tours/', views.getTours, name = "getTours"),
        path('places/', views.getPlaces, name = "getPlaces"),
        path('hotels/', views.getHotels, name = "getHotels"),
        path('blog/', views.getArticles, name = "getArticles"),
        path('contacts/', views.contacts, name = "contacts"),
        path('rest/', views.rest, name = "rest"),
        path('about/', views.getTeam, name = "getTeam"),
        path('hotelCard/<int:hotel_id>/', views.hotelCard, name = "hotelCard"),
        path('placeCard/<int:place_id>/', views.placeCard, name = "placeCard"),
        path('sign_up/', views.sign_up, name = "sign_up"),
        path('transfer/', views.transfer, name = "transfer"),

    #разное
        path('articleCard/<int:article_id>/', views.articleCard, name = "articleCard"),


    #расписание
        path('timetable/', views.timetableList, name = "timetableList"),
        path('addTimetable/', views.addTimetable, name = "addTimetable"),
        path('addtotimetabel/', views.addingToTimetabelCard, name = "addingToTimetabelCard"),
        path('timetable-card-edit/<int:t_id>/', views.getTimetableCardToEdit, name = "timetableCardEdit"),
        path('edittimetable/<int:t_id>/', views.editTimetable, name = "editTimetable"),
        path('timetable-card/<int:t_id>/', views.getTourInTimetable, name = "timetableCard"),
        path('getFreeSpace/<int:t_id>/', views.getFreeSpace, name = "getFreeSpace"),
        path('getTourInTById/<int:t_id>/', views.getTourInTById, name = "getTourInTById"),
        path('tourChoosing/', views.tourChoosing, name = "tourChoosing"),


    #туры
        path('add/', views.add, name = "add"),
        path('tourCard/<str:tour_url>/', views.tourCard, name = "tourCard"),
        path('del_t/<int:t_id>/', views.del_t, name = "del_t"),
        path('edit-tour/<str:tour_url>/', views.getTourToEdit, name = "getTourToEdit"),
        path('edit-tour-save/<str:tour_url>/', views.editTour1, name = "editTour1"),
        path('del_tour/<int:tour_id>/', views.del_tour, name = "del_tour"),
        path('tours_info/<str:tour_url>', views.get_tours_info, name = "get_tours_info"),
        path('basicTourChoosing/', views.basicTourChoosing, name = "basicTourChoosing"),
        path('getTourById/<int:t_id>/', views.getTourById, name = "getTourById"),

    #авторизация и регистрация
        path('auth/', views.go_auth, name = "go_auth"),
        path('login/', views.log_in, name = "log_in"),
        path('logout/', views.log_out, name = "log_out"),
        path('registration/', views.registr, name = "registr"),

    #Бронирования
        path('booking-tour/<int:TourInTimetableID>', views.booking_tour_page, name = "booking_tour_page"),
        path('addNewBooking/<int:TourInTimetableID>/<int:number_of_people>/', views.addNewBooking, name = "addNewBooking"),
        path('addNewBookingByM/', views.addNewBookingByM, name = "addNewBookingByM"),
        path('bookings_list/', views.bookingsList, name = "bookingsList"),
        path('newBookingByM/', views.addingToBookingCard, name = "addingToBookingCard"),
        path('userChoosing/', views.userChoosing, name = "userChoosing"),
        path('booking-card-edit/<int:booking_id>/', views.getBookingCardToEdit, name = "getBookingCardToEdit"),
        path('editBookingCard/<int:booking_id>/', views.editBookingCard, name = "editBookingCard"),
        path('del_booking/<int:booking_id>/', views.del_booking, name = "del_booking"),

    #Пользователи
        path('getUserById/<int:user_id>/', views.getUserById, name = "getUserById"),
        path('userList/', views.userList, name = "userList"),
        path('userCard/<int:user_id>', views.getUserCard, name = "getUserCard"),
        path('user-card-edit/<int:user_id>', views.getUserCardToEdit, name = "getUserCardToEdit"),
        path('editUserCard/<int:user_id>', views.ediUserCard, name = "ediUserCard"),
        path('editUserCardSelf/<int:user_id>', views.editUserCardSelf, name = "editUserCardSelf"),
        path('addNewUser/', views.addNewUser, name = "addNewUser"),

        path('del_user/<int:user_id>/', views.del_user, name = "del_user"),
        path('addUserCard/', views.addUserCard, name = "addUserCard"),
        path('addingNewUser/', views.addingNewUser, name = "addingNewUser"),

        #Личный кабинет
        path('personal_account/', views.personal_account_show, name = "personal_account_show"),
        path('account_settings/', views.account_settings, name = "account_settings"),
        path('editUserInAccount/<int:user_id>/', views.editUserInAccount, name = "editUserInAccount"),
        path('cancel_booking/<int:booking_id>/', views.cancel_booking, name = "cancel_booking"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
