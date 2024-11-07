from django.urls import path
from . import views, admin

urlpatterns = [
   path('', views.index, name='home'),
   path('question/<int:question_id>/', views.questionitems, name='question'),
   path('ask', views.ask, name='ask'),
   path('login', views.login, name='login'),
   path('signup', views.signup, name='signup'),
   path('tag/<str:tag_name>/', views.tag, name='tag'),
   #path('admin/', admin.site.urls),
]