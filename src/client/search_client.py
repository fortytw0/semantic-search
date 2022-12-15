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

def print_elipsis(s) : 

    for i in range(s) :
        print('...')
        time.sleep(1) 


print('Hello! This is a demo for our Reddit Semantic Search framework!')

username = 'mycoolusername'
password = 'mycoolpassword1234'
email = 'mycoolemail@123.com'

print_elipsis(3)

print('We begin by creating an account...')

print('Credentials are : ')
print('Username : ' , username)
print('Password : ' , password)
print('Email : ' , email)

response = create_account(username, password, email)

print('Reply from API endpoint: ' , response.json())
print('We have been successfully able to create an account...')

print_elipsis(3)

print('Now we are going to login using our new credentials.')

response = login(username, password)

token = response.json()['auth_token']

print('We have received the token {} as a response of our login request. Please keep it secret.'.format(token))

print_elipsis(3)

print('Now we are going to send a search query to the server...\n')
print('The details of our request are given below : \n')

print_elipsis(3)

print("search_string = 'I think Messi is way better than Ronaldo'")
print("subreddits = 'soccer'")
print("filter_keywords = ''")
print("description = 'I have an incredibly parochial view on soccer'")

print_elipsis(3)

print('Sending the actual request...')

search_string = 'I think Messi is way better than Ronaldo'
subreddits = 'soccer'
filter_keywords = ''
description = 'I have an incredibly parochial view on soccer'

response = reddit_search(token , search_string, subreddits , filter_keywords , description)

job_name = response.json()['job_name']

print('We have been assigned a job name :  ' , job_name)
print(response.json())

print_elipsis(3)
print('Let us take a look at all the jobs that I have submitted : ')
response = list_my_jobs(token)

print(response.json())

print_elipsis(3)
print('Let us monitor the status of my job : ')

job_finished = False 

while not job_finished : 

    response = get_job_status(token , job_name)
    status = response.json()['job_name']
    if status != 'finished' : 
        print('Current status : ' , status)
        print_elipsis(1)
    else : 
        print('The job has finished!')
        job_finished = True

print('Let us look at the results : ')

response = get_finished_results(token)

for result in response.json() : 

    if len(result) < 10 : 
        for r in result :
            print(r)
            print('\n') 

    else : 
        for r in result[:10] : 
            print(r)
            print('\n')





