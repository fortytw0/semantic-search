import requests
from urllib import parse
import time

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

def get_job_status(token, job_name) : 

    endpoint = 'search/reddit/v1/status/{}/'.format(job_name)
    return requests.get(parse.urljoin(URL , endpoint) , headers={'Authorization' : 'Token {}'.format(token)})

def get_finished_results(token) : 

    endpoint = 'search/reddit/v1/finished/'
    return requests.get(parse.urljoin(URL , endpoint) , headers={'Authorization' : 'Token {}'.format(token)})


print('Hello! This is a demo for our Reddit Semantic Search framework!')

username = 'mycoolusername'
password = 'mycoolpassword1234'
email = 'mycoolemail@123.com'

time.sleep(3)

print('We begin by creating an account...')

print('Credentials are : ')
print('Username : ' , username)
print('Password : ' , password)
print('Email : ' , email)

response = create_account(username, password, email)

print('Json Response after account creation request: ' , response.json())
print('We have been successfully able to create an account...')

time.sleep(3)

print('Now we are going to login using our new credentials.')

response = login(username, password)

token = response.json()['auth_token']

print('We have received the token {} as a response of our login request. Please keep it secret.'.format(token))

time.sleep(3)

print('Now we are going to send a search query to the server...')

print('The details of our request are given below : ')

print("search_string = 'I think Messi is way better than Ronaldo'")
print("subreddits = 'soccer'")
print("filter_keywords = ''")
print("description = 'I have an incredibly parochial view on soccer'")

search_string = 'I think Messi is way better than Ronaldo'
subreddits = 'soccer'
filter_keywords = ''
description = 'I have an incredibly parochial view on soccer'

response = reddit_search(token , search_string, subreddits , filter_keywords , description)

print('The response to our search request is : ')
print(response.json())

time.sleep(3)
print('Listing all my jobs : ')
response = list_my_jobs(token)

print('Response to our request is : ')
print(response.json())


