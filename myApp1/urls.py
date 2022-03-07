from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myApp1'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('about/', views.about, name='about'),
                  path('detail/<int:type_no>', views.detail, name='detail'),
                  path('movies/', views.movies, name='movies'),
                  path('movies/<str:movie_id>', views.movie_detail, name='movie_detail'),
                  path('movies/<str:movie_id>/similar', views.similar_movies, name='similar_movies'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
