import datetime
import requests
from time import sleep
from random import random

LIKE = 1
DISLIKE = 0
IMAGE_FOLDER = './images'


class Person():

    def __init__(self, data, tinder_api):
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

        if data['spotify_connected']:
            if 'spotify_top_artists' in data:
                self.spotify_top_artists = data['spotify_top_artists']
            if 'spotify_theme_track' in data:
                self.spotify_theme_track = data['spotify_theme_track']

    def __repr__(self):
        return "{self.id}  -  {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"

    def like(self):
        if self.tinder_api.like(self.id):
            self.download_images(LIKE)
            return True

        return False

    def dislike(self):
        if self.tinder_api.dislike(self.id):
            self.download_images(DISLIKE)
            return True
        return False

    def download_images(self, swipe, sleep_max_for=3):
        index = 0
        if swipe == LIKE:
            CLASS = 'like'
        else:
            CLASS = 'dislike'

        for image_url in self.images:
            req = requests.get(image_url, stream=True)

            image_path = '%s/%s/%s_%d.jpeg' % (IMAGE_FOLDER, CLASS, self.id, index)

            print('Saving downloaded image to %s' % image_path)
            
            if req.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(req.content)
            
            sleep(random()*sleep_max_for)
            index += 1
