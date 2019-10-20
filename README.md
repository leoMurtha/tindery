# Tindery
Tinder bot that automates everything using machine/deep learning.


## Pipeline
### Swiping
The bot learns from your matches what kinda person you like and then decides if it will swipe right or left.

The main concept is using a CNN but we also can use a similarity score between musics and description to make the final bot decision.

$$swipe(user) = CNN*0.7 + Similarity*0.3$$  and if this result is greater than a certain **threshold** the bot makes a decision.


#### TO-DO(Swiping)
* Choose the CNN archictecture.
* Choose a similarity function.
* Gather matches info.
* Code the swipe routine

### Talking
...