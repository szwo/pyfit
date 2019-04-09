import requests
import json
import urllib3

API_KEY = 'Token 8eb4e02b8a4eac66f3709d545fbbb8713e1fbb08'
ACCEPT_HEADER = 'application/json'
DATA = '{"key": "value"}'
HEADERS = {'Accept': ACCEPT_HEADER, 'Authorization': API_KEY}
BASE_PATH = 'https://wger.de/api/v2/'
ROUTES = {
    'profile': 'userprofile/',
    'exercises': 'exercise/',
    'categories': 'exercisecategory/'
}

urllib3.disable_warnings()


# HTTP REST Helper Functions

def get(route, params=''):
    url = BASE_PATH + ROUTES[route] + params
    # TODO: Verify HTTPS request
    r = requests.get(url=url, data=DATA, headers=HEADERS, verify=False)
    r
    return json.loads(r.content)


def post(route, payload, params):
    body = json.dumps(payload)
    url = BASE_PATH + ROUTES[route] + params
    # TODO: Verify HTTPS request
    r = requests.post(url=url, data=body, headers=HEADERS, verify=False)
    r
    return json.loads(r.content)


# API Calls

def get_exercises_by_category(categoryId):
    route = '?muscles=' + str(categoryId)
    return get('exercises', route)


def get_exercise_categories():
    results = get('categories')
    return results['results']
