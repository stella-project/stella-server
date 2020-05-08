# stella-server

## todos

#### dashboard
- [ ] fill landing page with content
- [ ] explanation of metrics (dashboard)
- [ ] button for bulk-download (dashboard)

#### handling 
- [ ] register-ui: option `participant` (team-name, github-profiles,...)
- [ ] read and write permissions for users and participants
- [ ] automatic generation of docker-compose.yml for `stella-app`
- [ ] sync experimental systems &rarr; stella-server will write to config-file
- [ ] add meta-data about docker-containers/experimental systems (github-url, ...) to database
- [ ] cron-job that checks for updates in repos

#### misc
- [ ] unit tests

#### done 
- [x] authentication via jwt
- [x] production-ready (docker-compose + postgresql)
- [x] sequence diagram
- [x] tech-stack
- [x] dashboard

## dev-notes

run local postgres-db with:  
```
docker run -d -p 5432:5432 --name my-postgres -e POSTGRES_PASSWORD=change-me postgres
```

## Overview

The STELLA server provides the following services:

1. User administration (administration of admins, participants and sites)
2. Dashboard service
3. Automated generation of the STELLA app &rarr; `docker-compose.yml`  
4. Data storage (user feedback) for data analysis, training, etc.

## Setup

### Production-ready
1. Build app with Docker:  `docker-compose up -d`
2. Add toy data with the help of `util/simulate.py`

### Development
1. Change `app = create_app('postgres')` to `app = create_app('default')` in `stella-server.py`
2. Run `stella-server.py`
3. Change `PORT='80'` to `PORT='8000'` in `util/simulate.py` and run it
4. Login with user `participant_a@stella.org` and password `pass`
5. Visit `http://0.0.0.0:8000/dashboard`

## Tech stack
![tech-stack](doc/techstack.png)

## Sequence diagram
[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgc2l0ZSAtPj4gc3RlbGxhX2FwcDogcXVlcnlcbiAgICBzdGVsbGFfYXBwIC0tPj4gc2l0ZTogPGl0ZW1zPlxuICAgIE5vdGUgbGVmdCBvZiBzaXRlOiBsb2dzIHVzZXIgZGF0YSA8YnI-IGFuZCBpbnRlcmFjdGlvbnNcbiAgICBsb29wIGZlZWRiYWNrXG4gICAgICAgIHNpdGUgLT4-IHN0ZWxsYV9hcHA6IHNlbmQgZmVlZGJhY2tcbiAgICAgICAgc3RlbGxhX2FwcCAtPj4gc3RlbGxhX3NlcnZlcjogR0VUIC9zaXRlcy88c3RyaW5nOm5hbWU-XG4gICAgICAgIHN0ZWxsYV9zZXJ2ZXIgLS0-PiBzdGVsbGFfYXBwOiA8c2l0ZV9pZD5cbiAgICAgICAgc3RlbGxhX2FwcCAtPj4gc3RlbGxhX3NlcnZlcjogUE9TVCAvc2l0ZXMvPGludDppZD4vc2Vzc2lvbnNcbiAgICAgICAgc3RlbGxhX3NlcnZlciAtLT4-IHN0ZWxsYV9hcHA6IDxzZXNzaW9uX2lkPlxuICAgICAgICBzdGVsbGFfYXBwIC0-PiBzdGVsbGFfc2VydmVyOiBQT1NUIC9zZXNzaW9ucy88aW50OmlkPi9mZWVkYmFja3NcbiAgICAgICAgc3RlbGxhX3NlcnZlciAtLT4-IHN0ZWxsYV9hcHAgOiA8ZmVlZGJhY2tfaWQ-XG4gICAgICAgIHN0ZWxsYV9hcHAgLT4-IHN0ZWxsYV9zZXJ2ZXIgOiBQT1NUIC9mZWVkYmFja3MvPGludDppZD4vcmFua2luZ3MgKGV4cGVyaW1lbnRhbClcbiAgICAgICAgc3RlbGxhX2FwcCAtPj4gc3RlbGxhX3NlcnZlciA6IFBPU1QgL2ZlZWRiYWNrcy88aW50OmlkPi9yYW5raW5ncyAoYmFzZWxpbmUpXG4gICAgZW5kXG4gICAgcGFydCAtPj4gc3RlbGxhX3NlcnZlciA6IEdFVCAvc2l0ZXMvPGludDppZD4vc2Vzc2lvbnNcbiAgICBzdGVsbGFfc2VydmVyIC0tPj4gcGFydCA6IHNlc3Npb25zIGRldGFpbHNcbiAgICBwYXJ0IC0-PiBzdGVsbGFfc2VydmVyIDogR0VUIC9zZXNzaW9ucy88aW50OmlkPi9mZWVkYmFja3NcbiAgICBzdGVsbGFfc2VydmVyIC0tPj4gcGFydCA6IGZlZWRiYWNrIGlkc1xuICAgIHBhcnQgLT4-IHN0ZWxsYV9zZXJ2ZXIgOiBHRVQgL2ZlZWRiYWNrcy88aW50OmlkPlxuICAgIHN0ZWxsYV9zZXJ2ZXIgLS0-PiBwYXJ0IDogZmVlZGJhY2sgZGV0YWlsc1xuICAgIHBhcnQgLT4-IHN0ZWxsYV9zZXJ2ZXIgOiBHRVQgL3JhbmtpbmdzLzxpbnQ6aWQ-XG4gICAgc3RlbGxhX3NlcnZlciAtLT4-IHBhcnQgOiByYW5raW5nIGRldGFpbHNcbiAgICBOb3RlIHJpZ2h0IG9mIHBhcnQgOiBvcHRpbWl6ZXMgaGVyIDxicj4gYWxnb3JpdGhtIHdpdGggdGhlIDxicj4gaGVscCBvZiBsb2cgZGF0YVxuICAgICIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgc2l0ZSAtPj4gc3RlbGxhX2FwcDogcXVlcnlcbiAgICBzdGVsbGFfYXBwIC0tPj4gc2l0ZTogPGl0ZW1zPlxuICAgIE5vdGUgbGVmdCBvZiBzaXRlOiBsb2dzIHVzZXIgZGF0YSA8YnI-IGFuZCBpbnRlcmFjdGlvbnNcbiAgICBsb29wIGZlZWRiYWNrXG4gICAgICAgIHNpdGUgLT4-IHN0ZWxsYV9hcHA6IHNlbmQgZmVlZGJhY2tcbiAgICAgICAgc3RlbGxhX2FwcCAtPj4gc3RlbGxhX3NlcnZlcjogR0VUIC9zaXRlcy88c3RyaW5nOm5hbWU-XG4gICAgICAgIHN0ZWxsYV9zZXJ2ZXIgLS0-PiBzdGVsbGFfYXBwOiA8c2l0ZV9pZD5cbiAgICAgICAgc3RlbGxhX2FwcCAtPj4gc3RlbGxhX3NlcnZlcjogUE9TVCAvc2l0ZXMvPGludDppZD4vc2Vzc2lvbnNcbiAgICAgICAgc3RlbGxhX3NlcnZlciAtLT4-IHN0ZWxsYV9hcHA6IDxzZXNzaW9uX2lkPlxuICAgICAgICBzdGVsbGFfYXBwIC0-PiBzdGVsbGFfc2VydmVyOiBQT1NUIC9zZXNzaW9ucy88aW50OmlkPi9mZWVkYmFja3NcbiAgICAgICAgc3RlbGxhX3NlcnZlciAtLT4-IHN0ZWxsYV9hcHAgOiA8ZmVlZGJhY2tfaWQ-XG4gICAgICAgIHN0ZWxsYV9hcHAgLT4-IHN0ZWxsYV9zZXJ2ZXIgOiBQT1NUIC9mZWVkYmFja3MvPGludDppZD4vcmFua2luZ3MgKGV4cGVyaW1lbnRhbClcbiAgICAgICAgc3RlbGxhX2FwcCAtPj4gc3RlbGxhX3NlcnZlciA6IFBPU1QgL2ZlZWRiYWNrcy88aW50OmlkPi9yYW5raW5ncyAoYmFzZWxpbmUpXG4gICAgZW5kXG4gICAgcGFydCAtPj4gc3RlbGxhX3NlcnZlciA6IEdFVCAvc2l0ZXMvPGludDppZD4vc2Vzc2lvbnNcbiAgICBzdGVsbGFfc2VydmVyIC0tPj4gcGFydCA6IHNlc3Npb25zIGRldGFpbHNcbiAgICBwYXJ0IC0-PiBzdGVsbGFfc2VydmVyIDogR0VUIC9zZXNzaW9ucy88aW50OmlkPi9mZWVkYmFja3NcbiAgICBzdGVsbGFfc2VydmVyIC0tPj4gcGFydCA6IGZlZWRiYWNrIGlkc1xuICAgIHBhcnQgLT4-IHN0ZWxsYV9zZXJ2ZXIgOiBHRVQgL2ZlZWRiYWNrcy88aW50OmlkPlxuICAgIHN0ZWxsYV9zZXJ2ZXIgLS0-PiBwYXJ0IDogZmVlZGJhY2sgZGV0YWlsc1xuICAgIHBhcnQgLT4-IHN0ZWxsYV9zZXJ2ZXIgOiBHRVQgL3JhbmtpbmdzLzxpbnQ6aWQ-XG4gICAgc3RlbGxhX3NlcnZlciAtLT4-IHBhcnQgOiByYW5raW5nIGRldGFpbHNcbiAgICBOb3RlIHJpZ2h0IG9mIHBhcnQgOiBvcHRpbWl6ZXMgaGVyIDxicj4gYWxnb3JpdGhtIHdpdGggdGhlIDxicj4gaGVscCBvZiBsb2cgZGF0YVxuICAgICIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

## API endpoints

### Feedback

GET details of all feedbacks (see also `util/GET_feedbacks.py`):  
`/feedbacks`

GET details of feedback with `id` (see also `util/GET_feedback.py`):  
`/feedbacks/<int:id>`

POST new feedback for session with `id` (see also `util/POST_feedback.py`):  
`/sessions/<int:id>/feedbacks`

The payload should be provided as follows:  

```json
{
    "start": "2019-11-04 00:06:23",
    "end": "2019-11-04 00:10:38",
    "interleave": "True",
    "clicks": [
               {"1": {"doc_id": "doc1", "clicked": "False", "date": "None", "system": "EXP"}},
               {"2": {"doc_id": "doc11", "clicked": "True", "date": "2019-11-04 00:08:15", "system": "BASE"}},
               {"3": {"doc_id": "doc2", "clicked": "False", "date": "None", "system": "EXP"}},
               {"4": {"doc_id": "doc12", "clicked": "True", "date": "2019-11-04 00:06:23", "system": "BASE"}},
               {"5": {"doc_id": "doc3", "clicked": "False", "date": "None", "system": "EXP"}},
               {"6": {"doc_id": "doc13", "clicked": "False", "date": "None", "system": "BASE"}},
               {"7": {"doc_id": "doc4", "clicked": "False", "date": "None", "system": "EXP"}},
               {"8": {"doc_id": "doc14", "clicked": "False", "date": "None", "system": "BASE"}},
               {"9": {"doc_id": "doc5", "clicked": "False", "date": "None", "system": "EXP"}},
               {"10": {"doc_id": "doc15", "clicked": "False", "date": "None", "system": "BASE"}}         
              ]
}
```

PUT details for feedback with `id` (see also `util/PUT_feedback.py`):  
`/feedbacks/<int:id>'`

The payload should be provided as follows:  

```json
{
    "start": "2019-11-04 00:06:23",
    "end": "2019-11-04 00:10:38",
    "interleave": "True",
    "clicks": [
               {"1": {"doc_id": "doc1", "clicked": "False", "date": "None", "system": "EXP"}},
               {"2": {"doc_id": "doc11", "clicked": "True", "date": "2019-11-04 00:08:15", "system": "BASE"}},
               {"3": {"doc_id": "doc2", "clicked": "False", "date": "None", "system": "EXP"}},
               {"4": {"doc_id": "doc12", "clicked": "True", "date": "2019-11-04 00:06:23", "system": "BASE"}},
               {"5": {"doc_id": "doc3", "clicked": "False", "date": "None", "system": "EXP"}},
               {"6": {"doc_id": "doc13", "clicked": "False", "date": "None", "system": "BASE"}},
               {"7": {"doc_id": "doc4", "clicked": "False", "date": "None", "system": "EXP"}},
               {"8": {"doc_id": "doc14", "clicked": "False", "date": "None", "system": "BASE"}},
               {"9": {"doc_id": "doc5", "clicked": "False", "date": "None", "system": "EXP"}},
               {"10": {"doc_id": "doc15", "clicked": "False", "date": "None", "system": "BASE"}}         
              ]
}
```

### Participant

GET all systems of participant with `id` (see also `util/GET_systems_of_participant.py`):  
`/participants/<int:id>/systems`

GET all sessions of participant with `id` (see also `util/GET_sessions_of_participant.py`):  
`/participants/<int:id>/sessions`

### Ranking

GET details of ranking with `id` (see also `util/GET_ranking.py`):  
`/rankings/<int:id>`

GET a list of all ranking `id`s (see also `util/GET_rankings.py`):  
`/rankings`

POST ranking for feedback with `id` (see also `util/POST_rankings.py`):  
`/feedbacks/<int:id>/rankings`

The payload should be provided as follows:  

```json
{
    "q": "this is the query text",
    "q_date": "2019-11-04 00:04:00",
    "q_time": 325,
    "num_found": 100,
    "page": 1,
    "rpp": 10,
    "items": [
              {"1": "doc1", "2": "doc2", "3": "doc3", "4": "doc4", "5": "doc5", 
               "6": "doc6", "7": "doc7", "8": "doc8", "9": "doc9", "10": "doc10"}
             ]
}
```

PUT ranking with `id` (see also `util/PUT_ranking.py`):  
`/rankings/<int:id>`

The payload should be provided as follows:  

```json
{
    "q": "this is the query text",
    "q_date": "2019-11-04 00:04:00",
    "q_time": 325,
    "num_found": 100,
    "page": 1,
    "rpp": 10,
    "items": [
              {"1": "doc1", "2": "doc2", "3": "doc3", "4": "doc4", "5": "doc5", 
               "6": "doc6", "7": "doc7", "8": "doc8", "9": "doc9", "10": "doc10"}
             ]
}
```

### Recommendation

GET details of recommendation with `id` (see also `util/GET_ranking.py` that works analogously):  
`/recommendations/<int:id>`

GET a list of all recommendation `id`s (see also `util/GET_rankings.py` that works analogously):  
`/recommendations`

POST recommendation for feedback with `id` (see also `util/POST_rankings.py` that works analogously):  
`/feedbacks/<int:id>/recommendations`

The payload should be provided as follows:  

```json
{
    "q": "docid",
    "q_date": "2019-11-04 00:04:00",
    "q_time": 325,
    "num_found": 100,
    "page": 1,
    "rpp": 10,
    "items": [
              {"1": "doc1", "2": "doc2", "3": "doc3", "4": "doc4", "5": "doc5", 
               "6": "doc6", "7": "doc7", "8": "doc8", "9": "doc9", "10": "doc10"}
             ]
}
```

PUT recommendation with `id` (see also `util/PUT_ranking.py` that works analogously):  
`/recommendations/<int:id>`

The payload should be provided as follows:  

```json
{
    "q": "docid",
    "q_date": "2019-11-04 00:04:00",
    "q_time": 325,
    "num_found": 100,
    "page": 1,
    "rpp": 10,
    "items": [
              {"1": "doc1", "2": "doc2", "3": "doc3", "4": "doc4", "5": "doc5", 
               "6": "doc6", "7": "doc7", "8": "doc8", "9": "doc9", "10": "doc10"}
             ]
}
```

### Session

GET session with `id` (see also `util/GET_session.py`):  
`/sessions/<int:id>`

GET feedback from session with `id` (see also `util/GET_feedbacks_of_session.py`):  
`/sessions/<int:id>/feedbacks` 

GET systems used in session with `id`:  
`/sessions/<int:id>/systems`

### Site

GET site details, e.g. `id`, with the help of the `name` (see also `util/GET_systems_at_site.py`):  
`/sites/<string:name>`

GET sessions at site with `id` (see also `util/GET_session_at_site.py`):  
`/sites/<int:id>/sessions`

GET systems deployed at site with `id` (see also `util/GET_systems_at_site.py`):  
`/sites/<int:id>/systems`

POST new session at site with `id` (see also `util/POST_sessions.py`):  
`/sites/<int:id>/sessions`

The payload should be provided as follows:  

```json
{
    "site_user": "123.123.123.123",
    "start": "2020-02-20 20:02:20",
    "end": "2020-02-20 20:02:20",
    "system_ranking": "rank_exp_a",
    "system_recommendation": "rec_exp_a"
}
```
