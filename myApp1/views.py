from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Type, Item
from http.client import HTTPSConnection as Connect
import json
from dotenv import load_dotenv
import os

load_dotenv()
MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')


def index(request):
    response = HttpResponse()
    heading1 = '<p>' + 'This is the main page of group#4 "Movies Django project"' + '</p>'
    contributions = '<p>' + 'Contributors: Abhay, Rahul, Sarab, Shruti' + '</p>'
    response.write(heading1)
    response.write(contributions)
    all_href = '<a href="{}">{}</a>'.format(build_uri(request, '/movies/'), 'Show All Movies')
    response.write(all_href)
    return response


def about(request):
    # return HttpResponse('This is the about page')
    return render(request, 'myApp1/about.html')


def detail(request, type_no):
    type_with_id = get_object_or_404(Type, pk=type_no)
    # type_with_id = Type.objects.get(id=type_no)
    items_with_type = Item.objects.filter(type=type_with_id)
    response = HttpResponse()
    heading1 = '<p>' + 'Different Items with type: ' + str(type_with_id) + '</p>'
    response.write(heading1)
    for item in items_with_type:
        para = '<p>' + str(item.price) + ': ' + str(item) + '</p>'
        response.write(para)
    return response


def build_uri(request, uri_endpoint):
    return request.build_absolute_uri(uri_endpoint)


# will return list of movie names
def fetch_movies(request) -> [str]:
    top_movies = list()
    top_movies.append({'name': 'Fight Club', 'url': build_uri(request, '/movies/550')})
    top_movies.append({'name': 'Poseidon', 'url': build_uri(request, '/movies/551')})
    top_movies.append({'name': 'Dogville', 'url': build_uri(request, '/movies/553')})
    connection = Connect("api.themoviedb.org")
    json_data = dict()
    try:
        api_key = '?api_key=' + MOVIE_API_KEY
        top_movies_endpoint = '/3/movie/top_rated' + api_key
        connection.request("GET", top_movies_endpoint)
        res = connection.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))
        for movie in json_data['results']:
            movie_url = build_uri(request, '/movies/' + str(movie['id']))
            movie_json = {'name': movie['title'], 'url': movie_url}
            top_movies.append(movie_json)
        print('Movies fetched from API:', len(top_movies))
    except TypeError as error:
        json_data['error'] = error
    if 'status_code' in json_data and json_data['status_code'] == 34:
        json_data['title'] = 'No such movie found'
        json_data['overview'] = 'Try other movies from below URL'
        json_data['vote_average'] = 0.0
        json_data['vote_count'] = 0
    return top_movies


def fetch_movie_detail(movie_id: str) -> dict:
    connection = Connect("api.themoviedb.org")
    headers = {}
    payload = ''
    json_data = dict()
    try:
        print(MOVIE_API_KEY)
        api_key = '?api_key=' + MOVIE_API_KEY
        movie_id_endpoint = "/3/movie/" + movie_id + api_key
        connection.request("GET", movie_id_endpoint, payload, headers)
        res = connection.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))
    except TypeError as error:
        json_data['error'] = error
    if 'status_code' in json_data and json_data['status_code'] == 34:
        json_data['title'] = 'No such movie found'
        json_data['overview'] = 'Try other movies from below URL'
        json_data['vote_average'] = 0.0
        json_data['vote_count'] = 0
    return json_data


def movies(request):
    response = HttpResponse()
    heading1 = '<p>' + 'Different movies fetched dynamically: ' + '</p>'
    response.write(heading1)
    list_items = ''
    for movie in fetch_movies(request):
        href = '<a href="{}">{}</a>'.format(movie['url'], movie['name'])
        list_items += '<li>' + href + '</li>'
    ul = '<ul>{}</ul>'.format(list_items)
    response.write(ul)
    return response


def get_movie_detail_in_html(request, movie_details):
    t = movie_details['title']
    va = str(movie_details["vote_average"])
    vc = str(movie_details["vote_count"])
    all_href = '<a href="{}">{}</a>'.format(build_uri(request, '/movies/'), 'Show All Movies')
    movie_details_html = '<p>' + 'Title:<strong> </br>' + t + '</strong></p>' \
                         + '<p>' + 'Overview: </br>' + movie_details['overview'] + '</p>' \
                         + '<p> Vote Average:</br>' + va + '</p>' \
                         + '<p> Vote Count:</br>' + vc + '</p>' \
                         + all_href
    return movie_details_html


def movie_detail(request, movie_id):
    response = HttpResponse()
    heading1 = '<p>' + 'Movie details: ' + '</p>'
    response.write(heading1)
    movie_details = fetch_movie_detail(movie_id)
    response.write(get_movie_detail_in_html(request, movie_details))
    return response
