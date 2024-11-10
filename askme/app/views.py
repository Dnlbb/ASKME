from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import User, Question, Answer, Tag, QuestionLike, AnswerLike



def paginate(objects_list, request, per_page=3):
  page_num = request.GET.get('page', 1)
  paginator = Paginator(objects_list, per_page)
  try:
    page = paginator.page(page_num)
  except PageNotAnInteger:
    page = paginator.page(1)
  except EmptyPage:
    page = paginator.page(paginator.num_pages)
  return page



def hot(request):
    hot_questions = Question.objects.best_questions()
    page = paginate(hot_questions, request)
    return render(request, 'hot.html', {'question': page})


def index(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request)
    return render(request, 'index.html', {'question': page})


def questionitems(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    page = paginate(answers, request)
    return render(request, 'question.html', {'question': question, 'answers': page})


def tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    page = paginate(questions, request)
    return render(request, 'index.html', {'questions': page, 'tag_name': tag_name})


def ask(request):
  return render(request, 'ask.html')

def login(request):
  return render(request, 'login.html')

def signup(request):
  return render(request, 'signup.html')

def red(request):
  return render(request, 'red.html')