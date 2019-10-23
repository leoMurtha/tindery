import datetime
import requests
from time import sleep
from random import random
import numpy as np

LIKE = 1
DISLIKE = 0
IMAGE_FOLDER = './images'


class Person():

    def __init__(self, data, tinder_api, fast_match=False):
        self.tinder_api = tinder_api
        self.id = data['_id']
        self.name = data.get('name', 'unknown')
        self.bio = data.get('bio', '')
        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]

        self.images = list(
            map(lambda photo: photo["url"], data.get("photos", [])))

        self.jobs = list(
            map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")}, data.get("jobs", [])))
        self.schools = list(
            map(lambda school: school["name"], data.get("schools", [])))

        if not fast_match and data['spotify_connected']:
            if 'spotify_top_artists' in data:
                self.spotify_top_artists = data['spotify_top_artists']
            else:
                self.spotify_top_artists = None

            if 'spotify_theme_track' in data:
                self.spotify_theme_track = data['spotify_theme_track']
            else:
                self.spotify_theme_track = None

    def __repr__(self):
        return "{self.id}  -  {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"

    def like(self):
        #if self.tinder_api.like(self.id):
        self.save_images(LIKE)
            # self.download_images(LIKE)
        #    return True

        return False

    def dislike(self):
        #if self.tinder_api.dislike(self.id):
        self.save_images(DISLIKE)
        return True

        #return False

    def download_images(self, sleep_max_for=1):
        self.downloaded_images = []
        for image_url in self.images:
            req = requests.get(image_url, stream=True)

            if req.status_code == 200:
                self.downloaded_images.append(req.content)

            sleep(random()*sleep_max_for)

        print('User %s images downloaded.' % self.name)
        return self.downloaded_images

    def save_images(self, swipe):
        index = 0
        if swipe == LIKE:
            CLASS = 'like'
        else:
            CLASS = 'dislike'

        for image in self.downloaded_images:

            image_path = '%s/%s/%s_%d.jpeg' % (IMAGE_FOLDER,
                                               CLASS, self.id, index)

            print('Saving downloaded image to %s' % image_path)

            with open(image_path, "wb") as f:
                f.write(image)

            index += 1

    # def save_profile(self, swipe):
    #     profile = {'id': self.id, 'name': self.name,
    #                'bio': self.bio, 'birth_date': self.birth_date, ''}

    def predict_likeliness(self, classifier, sess):
        print('Likeliness')
        ratings = []
        for image in self.images:
            r = requests.get(image, stream=True)
            certainty = classifier.classify(r.content)
            print(certainty)
            pos = float(certainty["like"])
            ratings.append(pos)

        ratings = np.array(ratings)
        #ratings.sort(reverse=True)
        #ratings = ratings[:5]
        print('Ratings is over')
        if len(ratings) == 0:
            return 0.001, ratings

        #print(x)
        #print(y)
        print('SCORE: %f' % ratings.mean())
        #return ratings[0]*0.6 + sum(ratings[1:])/len(ratings[1:])*0.4, ratings
        return ratings.mean(), ratings