# Tindery
Tinder bot that automates swiping using machine/deep learning using TensorFlow/Keras API.

## Pipeline

Steps to make the bot run smoothly.

1. Get your tinder token by running `sms_auth.py`, it will create token file that will be used in the next scripts.
2. Gather image data by running `tinder_gui.py` and gather A LOT of data before training.
3. If you have a lot of data (> 5000 examples) then you can already train the CNN by running:  
    `python3 src/retrain.py --bottleneck_dir=tf/training_data/bottlenecks --model_dir=tf/training_data/inception --summaries_dir=tf/training_data/summaries/basic --output_graph=tf/training_output/retrained_graph.pb --output_labels=tf/training_output/retrained_labels.txt --image_dir=./images/ --how_many_training_steps=50000 --testing_percentage=20 --learning_rate=0.001` 

Otherwise you can run `image_processing.py` that verifies the image and also do data augmentation.
4. Now run `tindery.py` and wait for matches.

## Swiping
The bot learns from your matches what kinda person you like and then decides if it will swipe right or left.

The main concept is using a CNN but we also can use a similarity score between musics and description to make the final bot decision.

swipe(user) = CNN*0.7 + Similarity*0.3  and if this result is greater than a certain **threshold** the bot makes a decision.
