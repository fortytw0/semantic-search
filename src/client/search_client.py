import requests
from urllib import parse

URL = 'http://198.59.83.83/'

def create_account(username, password, email) -> requests.Response : 

    endpoint = 'auth/users/'

    data = {
    "email": email,
    "username": username,
    "password": password,
    "re_password": password     
    }   
    

    return requests.post(parse.urljoin(URL , endpoint) , json=data)


def login(username, password) -> requests.Response : 

    endpoint = 'auth/token/login/'

    data = {
        "username": username,
        "password": password,
    }

    return requests.post(parse.urljoin(URL , endpoint) , json=data)


def hello_world(token) : 

    endpoint = 'search/hw/v1/'

    return requests.get(parse.urljoin(URL , endpoint) , headers={'Authorization' : 'Token {}'.format(token)})

def reddit_search(token , search_string, subreddits , filter_keywords , description) : 

    endpoint = 'search/reddit/v1/'

    data = {
        'search_string' : search_string , 
        'subreddits' : subreddits , 
        'filter_keywords' : filter_keywords , 
        'description' : description
    }

    return requests.post(parse.urljoin(URL , endpoint) , json=data, headers={'Authorization' : 'Token {}'.format(token)})

def list_my_jobs(token) : 

    endpoint = 'search/reddit/v1/list_jobs'

    return requests.get(parse.urljoin(URL , endpoint) , headers={'Authorization' : 'Token {}'.format(token)})


username = 'zhiyong'
password = 'kaka1234'
email = 'zw@123.com'

response = create_account(username, password, email)

print(response.content)
print(response.status_code)

response = login(username, password)

print(response.content)
print(response.status_code)
print(response.json())

token = response.json()['auth_token']

response = hello_world(token)

print(response.content)
print(response.status_code)
print(response.json())

search_string = 'I think Messi is way better than Ronaldo'
subreddits = 'soccer,nfl'
filter_keywords = 'messi,ronaldo'
description = 'I have an incredibly parochial view on soccer'

response = reddit_search(token , search_string, subreddits , filter_keywords , description)

print(response.content)
print(response.status_code)
print(response.json())

response = list_my_jobs(token)

print(response.content)
print(response.status_code)
