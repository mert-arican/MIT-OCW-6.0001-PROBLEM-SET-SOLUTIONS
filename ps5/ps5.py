# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid ; self.title = title 
        self.description = description
        self.link = link ; self.pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate
    
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    
    def __init__(self,phrase):
        self.phrase = phrase.lower()       
   
    def is_phrase_in(self,text):
        a = [] ; punc = string.punctuation; low_text = text.lower() ; index_list = []
        for p in punc:
            if p in low_text:
                a = low_text.split(p)
                low_text = " ".join(a)
        a = low_text.split()
        for word in self.phrase.split():
            if word not in a:
                return False
            index_list.append(a.index(word)) ; 
        for index in range(len(index_list) - 1):
            if index_list[index+1] - index_list[index] != 1:
                return False
        return True
    

# Problem 3

class TitleTrigger(PhraseTrigger):
    def __init__(self,phrase):
        super().__init__(phrase)
    
    def evaluate(self,story):
        return self.is_phrase_in(story.get_title())
    

# Problem 4

class DescriptionTrigger(PhraseTrigger):
    def __init__(self,phrase):
        super().__init__(phrase)
        
    def evaluate(self,story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
        
class TimeTrigger(Trigger):
    def __init__(self,time):
        datetime_object = datetime.strptime(time, '%d %b %Y %H:%M:%S')
        self.time = datetime_object

# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6

class BeforeTrigger(TimeTrigger):
    def __init__(self,time):
        super().__init__(time)
    
    def evaluate(self,story):
        self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
        return self.time >= story.get_pubdate()
    
class AfterTrigger(TimeTrigger):
    def __init__(self,time):
        super().__init__(time)
    
    def evaluate(self,story):
        self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
        return self.time <= story.get_pubdate()
        
# COMPOSITE TRIGGERS

# Problem 7
        
class NotTrigger(Trigger):
    def __init__(self,other):
        self.other = other
        
    def evaluate(self,story):
        return not self.other.evaluate(story)
# Problem 8

class AndTrigger(Trigger):
    def __init__(self,other,further):
        self.other = other
        self.further = further
        
    def evaluate(self,story):
        return self.other.evaluate(story) and self.further.evaluate(story)
# Problem 9

class OrTrigger(Trigger):
    def __init__(self, other, further):
        self.other = other
        self.further = further
    
    def evaluate(self, story):
        return self.other.evaluate(story) or self.further.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # (we're just returning all the stories, with no filtering)
    story_dict = {} ; return_list = []
    for story in stories:
        for trigger in triggerlist:
            if story not in story_dict:
                story_dict[story] = [str(trigger.evaluate(story))]
            else:
                story_dict[story] += [str(trigger.evaluate(story))]
    for story in story_dict:
        if "True" in story_dict[story]:
            return_list.append(story)
    return return_list



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    dirty_lines = [] ; clean_lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            dirty_lines.append(line)
    for line in dirty_lines:
        clean_lines.append(line.split(","))
    triggerList = []
    triggerDict = {}
    for line in clean_lines:
        if line[1] == "TITLE":
            t1 = TitleTrigger(line[2])
            triggerDict[line[0]] = t1
        if line[1] == "DESCRIPTION":
            t2 = DescriptionTrigger(line[2])
            triggerDict[line[0]] = t2
        if line[1] == "AFTER":
            t3 = AfterTrigger(line[2])
            triggerDict[line[0]] = t3
        if line[1] == "BEFORE":
            t4 = AfterTrigger(line[2])
            triggerDict[line[0]] = t4
        if line[1] == "NOT":
            t5 = NotTrigger(line[2])
            triggerDict[line[0]] = t5
        if line[1] == "AND":
            t6 = AndTrigger(line[2], line[3])
            triggerDict[line[0]] = t6
        if line[1] == "OR":
            t7 = OrTrigger(line[2], line[3])
            triggerDict[line[0]] = t7
        if line[0] == "ADD":
            triggerList += [triggerDict[line[1]], triggerDict[line[2]]]
    return triggerList



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("trump")
        t2 = DescriptionTrigger("saudi")
        t3 = DescriptionTrigger("Europe")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # After implementing read_trigger_config, uncomment this line 

        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

