# coding=utf-8
import json
import requests
from person import Person


class API():
    headers = {
        'app_version': '6.9.4',
        'platform': 'ios',
        "content-type": "application/json",
        "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
        "X-Auth-Token": '',
    }

    host = 'https://api.gotinder.com'

    def __init__(self, tinder_token=None):
        if not tinder_token:
            with open('tinder_token.txt', mode='r') as f:
                tinder_token = f.readline()
                tinder_token.strip()
                f.close()

        self.headers['X-Auth-Token'] = tinder_token

    def get_recommendations(self):
        '''
        Returns a list of users that you can swipe on
        '''
        try:
            r = requests.get(
                'https://api.gotinder.com/user/recs', headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting recomendations:", e)

    def get_updates(self, last_activity_date=""):
        '''
        Returns all updates since the given activity date.
        The last activity date is defaulted at the beginning of time.
        Format for last_activity_date: "2017-07-09T10:28:13.392Z"
        '''
        try:
            url = self.host + '/updates'
            r = requests.post(url,
                              headers=self.headers,
                              data=json.dumps({"last_activity_date": last_activity_date}))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting updates:", e)

    def get_self(self):
        '''
        Returns your own profile data
        '''
        try:
            url = self.host + '/profile'
            r = requests.get(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your data:", e)

    def change_preferences(self, **kwargs):
        '''
        ex: change_preferences(age_filter_min=30, gender=0)
        kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
        age_filter_min: 18..46
        age_filter_max: 22..55
        age_filter_min <= age_filter_max - 4
        gender: 0 == seeking males, 1 == seeking females
        distance_filter: 1..100
        discoverable: true | false
        {"photo_optimizer_enabled":false}
        '''
        try:
            url = self.host + '/profile'
            r = requests.post(url, headers=self.headers,
                              data=json.dumps(kwargs))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not change your preferences:", e)

    def get_meta(self):
        '''
        Returns meta data on yourself. Including the following keys:
        ['globals', 'client_resources', 'versions', 'purchases',
        'status', 'groups', 'products', 'rating', 'tutorials',
        'travel', 'notifications', 'user']
        '''
        try:
            url = self.host + '/meta'
            r = requests.get(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your metadata:", e)

    def update_location(self, lat, lon):
        '''
        Updates your location to the given float inputs
        Note: Requires a passport / Tinder Plus
        '''
        try:
            url = self.host + '/passport/user/travel'
            r = requests.post(url, headers=self.headers,
                              data=json.dumps({"lat": lat, "lon": lon}))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not update your location:", e)

    def reset_real_location(self):
        try:
            url = self.host + '/passport/user/reset'
            r = requests.post(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not update your location:", e)

    def get_recs_v2(self, locale):
        '''
        This works more consistently then the normal get_recommendations becuase it seeems to check new location
        '''
        try:
            url = self.host + '/v2/recs/core?locale=%s' % locale
            r = requests.get(url, headers=self.headers)
            recs = r.json()['data']['results']

            for rec in recs:
                rec['user'].update(rec['spotify'])
            recs = [Person(rec['user'], self) for rec in recs]
            return recs
        except Exception as e:
            print('excepted %s' % e)

    def get_person(self, id):
        '''
        Gets a user's profile via their id
        '''
        try:
            url = self.host + '/user/%s' % id
            r = requests.get(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get that person:", e)

    def send_msg(self, match_id, msg):
        try:
            url = self.host + '/user/matches/%s' % match_id
            r = requests.post(url, headers=self.headers,
                              data=json.dumps({"message": msg}))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not send your message:", e)

    def superlike(self, person_id):
        try:
            url = self.host + '/like/%s/super' % person_id
            r = requests.post(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not superlike:", e)

    def like(self, person_id):
        try:
            url = self.host + '/like/%s' % person_id
            r = requests.get(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not like:", e)
            return False

    def dislike(self, person_id):
        try:
            url = self.host + '/pass/%s' % person_id
            r = requests.get(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not dislike:", e)
            return False

    def report(self, person_id, cause, explanation=''):
        '''
        There are three options for cause:
            0 : Other and requires an explanation
            1 : Feels like spam and no explanation
            4 : Inappropriate Photos and no explanation
        '''
        try:
            url = self.host + '/report/%s' % person_id
            r = requests.post(url, headers=self.headers, data={
                              "cause": cause, "text": explanation})
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not report:", e)

    def match_info(self, match_id):
        try:
            url = self.host + '/matches/%s' % match_id
            r = requests.get(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your match info:", e)

    def all_matches(self):
        try:
            url = self.host + '/v2/matches'
            r = requests.get(url, headers=self.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your match info:", e)

    def get_fast_match(self):
        try:
            url = self.host + '/v2/fast-match/teasers'
            r = requests.get(url, headers=self.headers)
            
            recs = r.json()['data']['results']
            print(recs[0]['user']['_id'])
            
            #print(recs[0]['user'])
            recs = [Person(rec['user'], self, fast_match=True) for rec in recs]
            return recs
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your match info:", e)