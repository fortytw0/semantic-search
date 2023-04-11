# API Endpoints for Semantic Search 

This file gives the documentation for the different API endpoints in making the search happen. There are a finite number of endpoints, so it is best to check if your system can handle all of them. 

## General endpoint details 

The current URL for the backend server is : `http://198.59.83.83/` 

**This can change in the future. Make sure you don't hard code this!**

Prepend this URL to the routes provided in each individual section. 

## Login and Authentication 

### User Account Creation

`Route = auth/users/`

Expected Package : 

```
{
    "email": email,
    "username": username,
    "password": password,
    "re_password": password     
}
```

All users need to create an account to use the service. I know that the front-end already handles UA, but given the crunch for time - it is a little scary to decouple account creation right now. If you think this may cause problems in how you are graded - make sure you tell them this is "for another layer of security". Based on how fast we can integrate the backend, I can go ahead and try to remove the login logic. 

### User Login and Obtaining a Token

`Route = auth/token/login/`

Expected Package : 

```
{
    "username": username,
    "password": password,    
}
```

Returns : 

```
{"auth_token" : token_string}
```

Make sure you store the token_string in the Redux Store. You can reuse the login token as many times as you want. 

### Authentication Test Endpoint 

`Route = search/hw/v1/`

Expected Package : 

```
<No Package Expected>
```

Headers : 

```
{"Authorization" : "Token {token_string}"}
```
Returns : 

```
{"message" : "Hello World!"}
```

Use this endpoint to check if your authentication is working correctly. It is cheap, and does not trigger any search functions (which can take time to respond.)

### Search Endpoint 

`Route : search/reddit/v1/`

Expected Package : 

```
{
    'search_string' : search_string , 
    'subreddits' : subreddits, 
    'filter_keywords' : filter_keywords <comma separated, optional> , 
    'description' : description
    }
```

Headers : 

```
{"Authorization" : "Token {token_string}"}
```

Returns : 

```
{'status':'success','job_name' : search_job_name}

OR 

{'errors' : errors}
```

Hitting this proess will trigger the search. It takes approx 3-5 mins to get back your results, and it highly depends on how many concurrent users are searching. Definitely use this to test, but be prepared for a wait. 


### List User Jobs 

`Route = search/reddit/v1/list_jobs`

Expected Package : 

```
<No Expected Package>
```

Headers : 

```
{"Authorization" : "Token {token_string}"}
```

Returns : 

```
[{"model": "search.job", 
  "pk": <JobNumber>, 
  "fields": 
      {"user": <UserPK>, 
      "job_name": "<unique_job_name>", 
      "search_string": "<search_string>", 
      "filter_keywords": "", 
      "subreddits": "<comma separated subreddits WITHOUT the prefix r/> cuboulder,college", 
      "description": "<description>", 
      "time_submitted": "<time_stamp_of_submission> 2023-02-03T20:40:41.547Z"}
      }, 
  ]
```

You can use this to keep a track record of the searches submitted by a User. The `job_name` parameter is very important, as it is a unique identifier for a particular search. Similarly, you can use the `time_submitted` to indicate how long the search process has been going on. 


### Get Job Status 

`Route = search/reddit/v1/status/<job_name>/`

Expected Package : 

```
<No Expected Package>
```

Headers : 

```
{"Authorization" : "Token {token_string}"}
```

Returns : 

```
{'job_name' : <status>}
```

**Please note, I messed up : The `job_name` in the response should actually be `job_status`, but it was the end of the semester and my brain no work good. So keep in mind that you will NOT receive the `job_name` in response, just the status.**

The design pattern here is you check the job status every 1 second or so, and then when the job status hits `finished`, you can call the Get Finished Jobs API to retrieve your results. 

### Get Finished Jobs 

`Route = search/reddit/v1/finished/<job_name>/`


Expected Package : 

```
<No Expected Package>
```

Headers : 

```
{"Authorization" : "Token {token_string}"}
```

Returns : 

```
[
{'all_awardings': [], 
'archived': False, 
'associated_award': None, 
'author': 'ad1s6h', 
'author_cakeday': None, 
'author_created_utc': 1638782197, 
'author_flair_background_color': 'transparent', 
'author_flair_css_class': None, 
'author_flair_richtext': [[]], 
'author_flair_template_id': 'a8ad979e-7c07-11e9-b588-0e55aa3940a6', 
'author_flair_text': ':FC_Barcelona:', 
'author_flair_text_color': 'dark', 
'author_flair_type': 'richtext', 
'author_fullname': 't2_h9waggzn', 
'author_patreon_flair': False, 
'author_premium': False, 
'body': "", 
'can_gild': True, 
'collapsed': False, 
'collapsed_reason': None, 
'collapsed_reason_code': None, 
'comment_type': None, 
'controversiality': 0, 
'created_utc': 1655786526, 
'distinguished': None, 
'editable': None, 
'edited': 'false', 
'gilded': 0, 
'gildings': [None, None, None], 
'id': 'id5aicv', 
'is_submitter': False, 
'link_id': 't3_vglajm', 
'locked': False, 
'media_metadata': None, 
'name': 't1_id5aicv', 
'no_follow': False, 
'parent_id': 't1_id58zdy', 
'permalink': '/r/soccer/comments/vglajm/daily_discussion/id5aicv/', 
'retrieved_on': 1656884729, 
'score': 4, 
'score_hidden': False, 
'send_replies': True, 
'stickied': False, 
'subreddit': 'soccer', 
'subreddit_id': 't5_2qi58', 
'subreddit_name_prefixed': 'r/soccer', 
'subreddit_type': 'public', 
'total_awards_received': 0, 
'treatment_tags': [], 
'cosine_similarity': 0.4055141508579254}
]
```

This basically returns everything that is contained in the Reddit comment. The few things that I would like to draw your attention to is `body` , which contains the text in the comment, and `cosine_similarity` which contains the similarity score. The closer the `cosine_similarity` is to 1, the better. 











