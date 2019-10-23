from classifier import Classifier
import tensorflow as tf
from time import time
import tinder_api

if __name__ == "__main__":
    api = tinder_api.API()

    with tf.Session() as sess:
        classifier = Classifier(graph="./tf/training_output/retrained_graph.pb",
                                labels="./tf/training_output/retrained_labels.txt")

        end_time = time() + 60*60*2
        while time() < end_time:
            try:
                print('Getting nearby persons')
                persons = api.get_recs_v2('pt-br')
                pos_schools = [
                    "Universidade de Sao Paulo", "UFSCAR", "UZH"]

                for person in persons[:1]:
                    print('Calling the classifier')
                    score, ratings = person.predict_likeliness(
                        classifier, sess)

                    print('Some affinity calculation')
                    for school in pos_schools:
                        if school in person.schools:
                            score *= 1.2

                    print("-------------------------")
                    print("ID: ", person.id)
                    print("Name: ", person.name)
                    print("Schools: ", person.schools)
                    print("Images: ", person.images)
                    print('Ratings: %s' % ratings)
                    print('Score %f\n\n' % score)

                    if score > 0.85:
                        #res = person.like()
                        print("LIKE")
                    else:
                        #res = person.dislike()
                        print("DISLIKE")

            except Exception as e:
                print(e)
                pass
            #break
    classifier.close()
