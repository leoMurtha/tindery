from googletrans import Translator
import os
import pandas as pd

"""
I made this one from parsing tweets and their replies. It contains conversations (2 or more tweets),
each tweet is on a seperate line and there is three empty lines between each dialouge
,and they are sorted by length of dialogue.
"""

"""
Dataset will be

# Query  # Reply
"""

from googletrans import Translator
translator = Translator()


def main(filename):
    text = 'start'
    data = {'comment': [], 'reply': []}
    with open(filename, mode='r') as f:
        
        while(text != ''):
            text = f.readline()
        
            if(len(text.split(' ')) > 1):
                try:

                    comment = translator.translate(text, dest='pt').text
                    last_comment = f.tell()
                    reply = translator.translate(f.readline(), dest='pt').text
                    f.seek(last_comment)

                    if reply != '\n' or reply != '':
                        data['comment'].append(comment)
                        data['reply'].append(reply)
                except:
                    pass
                #print('[%s] -\n (%s)' % (comment, reply))
            else:
                # Jumping two \n
                f.readline()
                f.readline()
    
    df = pd.DataFrame.from_dict(data)

    print(df.head(10))

if __name__ == "__main__":
    main(os.sys.argv[1])
