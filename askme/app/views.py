from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


QUESTIONS = []
for i in range(1,30):
  QUESTIONS.append({
    'title': 'title ' + str(i),
    'id': i,
    'text': 'text' + str(i),
    'tags': ['A' * (i % 5), 'AAA' * (i % 5), 'AAA' * (i % 5)],
  })



ANSWERS = []
for i in range(1,30):
  ANSWERS.append({
    'name': 'name ' + str(i),
    'text': 'text' + str(i)
  })


def paginate(objects_list, request, per_page=5):
  page_num = request.GET.get('page', 1)
  paginator = Paginator(objects_list, per_page)

  try:
    page = paginator.page(page_num)
  except PageNotAnInteger:
    page = paginator.page(1)
  except EmptyPage:
    page = paginator.page(paginator.num_pages)

  return page


def index(request):
  page = paginate(QUESTIONS, request)
  return render(request, 'index.html', {'question': page})


def questionitems(request, question_id):
  q = QUESTIONS[question_id]
  page = paginate(ANSWERS, request)
  return render(request, 'question.html',{'answers': page, 'question': q})

def tag(request,tag_name):
  questions = [q for q in QUESTIONS if tag_name in q.get("tags", [])]
  if not questions:
    raise Http404("No found")
  page = paginate(questions, request)
  return render(request, 'index.html', {'question': page})



def ask(request):
  return render(request, 'ask.html')

def login(request):
  return render(request, 'login.html')

def signup(request):
  return render(request, 'signup.html')

def red(request):
  return render(request, 'red.html')