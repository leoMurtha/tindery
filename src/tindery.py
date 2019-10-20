import sys
import tinder_api
import json
from person import Person
import tinder_gui 


if __name__ == "__main__":
    
    with open('user_mock.json', mode='r') as f:
        recs = json.load(f)
    

    recs = recs['data']['results']
    for rec in recs:
        rec['user'].update(rec['spotify'])
        
    persons = [Person(rec['user']) for rec in recs]

    for person in persons[:2]:
       print(person.id, person.name, len(person.images))
       person.like()