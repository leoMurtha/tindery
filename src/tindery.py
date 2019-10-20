import sys
import tinder_api
import json
from person import Person


if __name__ == "__main__":
    
    # with open('user_mock.json', mode='r') as f:
    #     recs = json.load(f)
    api = tinder_api.API()
    
    recs = api.get_recs_v2('pt-br')
    
        
    persons = [Person(rec, api) for rec in recs[:3]]

    for person in persons[:2]:
       print(person.id, person.name, len(person.images))
       person.like()