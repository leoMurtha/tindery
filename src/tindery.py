from classifier import Classifier
import tensorflow as tf
from time import time
import tinder_api
from cv2 import cv2
from skimage import io
import numpy as np


def show_images(images, swipe):
    W, H = (300, 300)
    images = [cv2.resize(io.imread(image), (W, H)) for image in images]
    final_image = images[0]

    for i in range(1, len(images)):
        final_image = np.hstack((final_image, images[i]))

    cv2.imshow('%s' % swipe, cv2.cvtColor(final_image, code=cv2.COLOR_BGR2RGB))
    cv2.waitKey(0)

    return True


if __name__ == "__main__":
    api = tinder_api.API()

    with tf.Session() as sess:
        classifier = Classifier(graph="./tf/training_output/retrained_graph.pb",
                                labels="./tf/training_output/retrained_labels.txt")

        end_time = time() + 60*60*2
        while time() < end_time:
            try:
                print('Getting nearby persons')
                persons = api.get_recs_v2('en-us')
                pos_schools = [
                    "Universidade de São Paulo", "UFSCAR"]

                total_persons = len(persons)
                for i, person in enumerate(persons):
                    print('Calling the classifier')
                    score, ratings = person.predict_likeliness(
                        classifier, sess)

                    print('Some affinity calculation')
                    for school in pos_schools:
                        if school in person.schools:
                            score *= 1.2

                    print("-------------------------")
                    print('Person %d out of %d' % (i + 1, total_persons))
                    print("ID: ", person.id)
                    print("Name: ", person.name)
                    print("Schools: ", person.schools)
                    print("Images: ", person.images)
                    print('Ratings: %s' % ratings)
                    print('Score %f\n\n' % score)

                    if score > 0.83:
                        person.like(training=False)
                        print("You might like this person")
                        #show_images(person.images, 'Liked')
                    elif score < 0.7:
                        person.dislike(training=False)
                        print("DISLIKE")
                        #show_images(person.images, 'Disliked')

            except Exception as e:
                print(e)
                pass
            # break
    classifier.close()
