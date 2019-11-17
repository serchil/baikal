from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator



class User(AbstractUser):
    name =  models.CharField(max_length=200, blank=True, null = True)
    second_name =  models.CharField(max_length=200, blank=True, null = True)
    surname =  models.CharField(max_length=200, blank=True, null = True)
    email = models.EmailField(_('email address'), unique=True, blank=True, null = True )
    phone_number = models.CharField(max_length=200, blank=True, null = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




def booking_tour_page(request, TourInTimetableID):
    tourInT = TourInTimetable.objects.get(id = TourInTimetableID)
    tour = Tour.objects.get(id = tourInT.tourID.id)
    form = UserForm()
    return render_to_response('booking_tour.html', {"tourInT":tourInT, "tour": tour, "form": form})



@csrf_exempt
def addUser(request):
    allTours = Tour.objects.all()
    maxID = allTours.aggregate(Max('id'))
    form = UserForm(request.POST)
    post = form.save(commit=False)
    post.save()

    return HttpResponse("ok");
<script>

		$( document ).ready(function() {
			var Selected = document.querySelector(".selected-wrapper");
			Selected.innerHTML = '<div class="header">Выбранные</div>';
{% for h in tour_t.hotels.all %}
Selected.innerHTML+=  '<a tabindex="0" class="item selected" role="button" data-value="{{h.name}}" multi-index="0">{{h.name}}</a>';
{% endfor %}


var notSelected = document.querySelector(".non-selected-wrapper");
var newContent = "";
for (var i = 1; i < notSelected.childNodes.length; i++) {
content = notSelected.childNodes[i].outerHTML;

content = content.toString().replace("item","item selected");

newContent+=content;

	}
notSelected.innerHTML = newContent;
		});



</script>-->

from .models import Choice, Question, User1
, Сумма<= Максимальная_сумма, Сумма >= Минимальная_сумма, Процентная_ставка <=Процентная_ставка, Возраст >=Минимальный_возраст, Возраст<=Максимальный_возраст, Срок >= Минимальный_срок, Срок <= Максимальный_срок
@csrf_exempt
def addTour(request):
    name1 = str(request.POST['name'])
    description1 = str(request.POST['description'])
    number_of_days1 = int(request.POST['numOfDays'])
    min_price1 = int(request.POST['minPrice'])
    placeID = int((request.POST['place']))
    places1 = Place.objects.filter(id = placeID)[0]
    sliderID = int((request.POST['slider']))
    slider1 = Slider.objects.filter(id = sliderID)[0]
    preview_descr1 = str((request.POST['previewDescr']))
    activity_status = True

    u = Tour.objects.create(name = name1, description=description1, number_of_days = number_of_days1, min_price =  min_price1, preview_descr = preview_descr1, activity_status = True, show_on_main_status = False )
    places1.tour_set.add(u)
    slider1.tour_set.add(u)
    return HttpResponse("ok")
def addTour(request):
    name1 = str(request.POST['name'])
    description1 = str(request.POST['description'])
    number_of_days1 = int(request.POST['numOfDays'])
    min_price1 = int(request.POST['minPrice'])
    placeID = int((request.POST['place']))
    places1 = Place.objects.filter(id = placeID)[0]
    sliderID = int((request.POST['slider']))
    slider1 = Slider.objects.filter(id = sliderID)[0]
    preview_descr1 = int((request.POST['previewDescr']))
    activity_status = True
    files = request.FILES
    u = User.objects.create(name = name1, description=description1, number_of_days = number_of_days1, min_price =  min_price1, places = places1, slider = slider1, preview_descr = preview_descr1,preview_img = files, activity_status = True, show_on_main_status = False )

    return HttpResponse("ok")

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})



def getClients(request, page_num):

    number = (page_num-1)*5
    user = User1.objects.all()[number:number+5]

    return render(request, "users1.html", {"user":user, "page_num": page_num})

def create(request):
    if request.method == "POST":
        tom = User1()
        tom.user1_name = request.POST.get("name")
        tom.user1_surname = request.POST.get("age")
        tom.save()
    return HttpResponseRedirect("http://127.0.0.1:8000/polls/meow/")

#def addClient(request, page_num):
#    if request.method == 'GET':
#        thisname = request.GET['name']
#        thissurname = request.GET['text']
#        newUser = User1(user1_name = thisname, user1_surname = thissurname)
#        newUser.save()

def meow(request):
    people = User1.objects.all()
    return render(request, "meow.html", {"people":people})

def home(request, page_number=1):

   articles = User1.objects.all()

   current_page = Paginator(articles,1)  # создаим переменную, которая будет содержать 2 статьи из всего обьекта

   articles_list = current_page.page(page_number)


   context = {"articles": articles_list}

   return render(request,  'home.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
