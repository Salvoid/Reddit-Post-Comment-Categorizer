# [Imports]====================================================================================================
import os # Miscellaneous Operating System Interfaces
import sys # System-specific Parameters & Functions
from genericpath import exists

from prawcore.exceptions import NotFound
from prawcore.exceptions import Forbidden
from praw.exceptions import RedditAPIException

import nltk # Natural Language Toolkit for Natural Language Processing
from nltk.corpus import stopwords # Stopwords for removing them
from nltk.tokenize import word_tokenize # Tokenize string/sentences into word arrays

import gui_module as guiModule # Software GUI


# [Declarations & Initializations]====================================================================================================
english_stopWords = set(stopwords.words('english')) # Set English Stopwords Words for referencing
english_wholeWords = set(nltk.corpus.words.words()) # Set English Whole Words for referencing


# [Functions]====================================================================================================
# [Defines the relative path from the absolute path of local files.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def define_relativepath(in_toCreate, in_path_relative):
    try:
        # path_base = sys._MEIPASS
        # path_base = getattr(sys, '_MEIPASS', os.getcwd())
        path_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        path_base = os.path.abspath(".")
    
    return path_base + in_path_relative

# [Check Reddit Post URL Format and Retrieve Reddit Post if Valid.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def verifyfetch_url(in_windowWidget, in_inputUrl, in_object_reddit):
    # https[0]:/[1]/www.reddit.com[2]/r[3]/<subreddit name>[4]/comments[5]/<post id>[6]/<post title>[7]/
    if in_inputUrl == "": # Return if the 'Reddit Post Link' Field is empty
        guiModule.print_console(in_windowWidget, True, False, "Reddit Post URL Status: ", 'textTag_task')
        guiModule.print_console(in_windowWidget, False, True, "URL Field is Empty.", 'textTag_process')
        return None

    guiModule.print_console(in_windowWidget, True, False, "Reddit Post URL Input: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, in_inputUrl, 'textTag_normalboldtext')

    guiModule.print_console(in_windowWidget, True, False, "Reddit Post URL Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "Validating URL Link Format...", 'textTag_process')

    inputUrl_parts = in_inputUrl.split('/')
    
    if (len(inputUrl_parts)==7) or (len(inputUrl_parts)==8) or (len(inputUrl_parts)==9):
        if (
            ((inputUrl_parts[0]=="http:") or (inputUrl_parts[0]=="https:")) and 
            (inputUrl_parts[1]=="") and 
            ((inputUrl_parts[2]=="reddit.com") or (inputUrl_parts[2]=="www.reddit.com")) and 
            ((inputUrl_parts[3]=="r") or (inputUrl_parts[3]=="user") or (inputUrl_parts[3]=="u")) and 
            (inputUrl_parts[5]=="comments")
        ):
            guiModule.print_console(in_windowWidget, True, False, "Reddit Post URL Status: ", 'textTag_task')
            guiModule.print_console(in_windowWidget, False, True, "URL Link Format Accepted.", 'textTag_process')

            guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
            guiModule.print_console(in_windowWidget, False, True, "Fetching Post...", 'textTag_process')
            object_inputPost = in_object_reddit.submission(id=inputUrl_parts[6]) # Get post/submission using the Post ID
            try:
                isPostNotDeleted = object_inputPost.is_robot_indexable # 'NotFound' & 'Forbidden' exception trigger if applicable
                if isPostNotDeleted:
                    guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                    if inputUrl_parts[3]=="r":
                        guiModule.print_console(in_windowWidget, False, True, "Validating Subreddit Source...", 'textTag_process')
                        try:
                            source_subreddit = in_object_reddit.subreddits.search_by_name(inputUrl_parts[4], exact=True)[0] # 'IndexError' exception trigger if applicable
                            source_subreddit.subreddit_type # 'NotFound' & 'Forbidden' exception trigger if applicable

                            if (inputUrl_parts[4]).lower() == (object_inputPost.subreddit.display_name).lower():
                                guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                guiModule.print_console(in_windowWidget, False, True, "SUCCESS", 'textTag_finish')
                                return object_inputPost
                            else:
                                guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                guiModule.print_console(in_windowWidget, False, True, "ERROR... Reddit Post Link's Subreddit Source doesn't match the actual Reddit Post's Subreddit.", 'textTag_finish')
                                return None
                        # except prawcore.exceptions.NotFound:
                        except NotFound:
                            guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                            guiModule.print_console(in_windowWidget, False, True, "ERROR... Subreddit Source of Reddit Post Not Found/Doesn't Exist/Banned.", 'textTag_finish')
                            return None
                        # except prawcore.exceptions.Forbidden:
                        except Forbidden:
                            guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                            guiModule.print_console(in_windowWidget, False, True, "ERROR... Subreddit Source of Reddit Post is a Private Community.", 'textTag_finish')
                            return None
                        # except IndexError:
                        except IndexError:
                            guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                            guiModule.print_console(in_windowWidget, False, True, "ERROR... Subreddit Source of Reddit Post is Invalid.", 'textTag_finish')
                            return None
                    elif inputUrl_parts[3]=="user" or inputUrl_parts[3]=="u":
                        guiModule.print_console(in_windowWidget, False, True, "Validating Redditor Source...", 'textTag_process')
                        try:
                            source_redditor = in_object_reddit.redditor(inputUrl_parts[4])
                            # source_redditor.created # 'NotFound' exception trigger if applicable
                            if getattr(source_redditor, 'is_suspended', False): # 'NotFound' exception trigger if applicable
                                guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                guiModule.print_console(in_windowWidget, False, True, "ERROR... Redditor Source of Reddit Post is Suspended/Banned.", 'textTag_finish')
                                return None
                            else:
                                if (inputUrl_parts[4]).lower() == (object_inputPost.author.name).lower():
                                    guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                    guiModule.print_console(in_windowWidget, False, True, "SUCCESS", 'textTag_finish')
                                    return object_inputPost
                                else:
                                    guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                    guiModule.print_console(in_windowWidget, False, True, "ERROR... Reddit Post Link's Redditor Source doesn't match the actual Reddit Post's Subreddit.", 'textTag_finish')
                                    return None
                        # except prawcore.exceptions.NotFound:
                        except NotFound:
                            try:
                                if in_object_reddit.username_available(inputUrl_parts[4]): # 'RedditAPIException(error_type == 'BAD_USERNAME')' exception trigger if applicable
                                    guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                    guiModule.print_console(in_windowWidget, False, True, "ERROR... Redditor Source of Reddit Post Doesn't Exist.", 'textTag_finish')
                                    return None
                                else:
                                    guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                    guiModule.print_console(in_windowWidget, False, True, "ERROR... Redditor Source of Reddit Post is Deleted/Shadowbanned/Unavailable.", 'textTag_finish')
                                    return None
                            # except praw.exceptions.RedditAPIException:
                            # except RedditAPIException.error_type(ERROR_TYPE = u'BAD_USERNAME'):
                            except RedditAPIException as error_RedditAPIException:
                                # if error_RedditAPIException.error_type == 'BAD_USERNAME':
                                if error_RedditAPIException.items[0].error_type == 'BAD_USERNAME':
                                    guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                                    guiModule.print_console(in_windowWidget, False, True, "ERROR... Redditor Source Username of Reddit Post is Invalid.", 'textTag_finish')
                                    return None
                else:
                    guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                    guiModule.print_console(in_windowWidget, False, True, "ERROR... Reddit Post is Deleted.", 'textTag_finish')
                    return None
            # except prawcore.exceptions.NotFound:
            except NotFound:
                guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                guiModule.print_console(in_windowWidget, False, True, "ERROR... Reddit Post Not Found/Doesn't Exist.", 'textTag_finish')
                return None
            # except prawcore.exceptions.Forbidden:
            except Forbidden:
                guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
                guiModule.print_console(in_windowWidget, False, True, "ERROR... Reddit Post Forbidden.", 'textTag_finish')
                return None
        else:
            guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
            guiModule.print_console(in_windowWidget, False, True, "ERROR... Invalid Reddit Post Link Format.", 'textTag_finish')
            return None
    else:
        guiModule.print_console(in_windowWidget, True, False, "Reddit Post Fetch Status: ", 'textTag_task')
        guiModule.print_console(in_windowWidget, False, True, "ERROR... Invalid Reddit Post Link Format.", 'textTag_finish')
        return None

# [Tokenize and Clean Comments.(Process)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def tokenize_textCollection(sentenceCollection):
    newSentenceCollection = []
    
    for sentence in sentenceCollection:
        temp = []
        sentence = sentence.lower()
        wordTokens = word_tokenize(sentence)

        for word in wordTokens:
            if(word in english_stopWords) or (word not in english_wholeWords) or (not word.isalpha()):
                continue
            temp.append(word)
        
        newSentenceCollection.append(' '.join(temp))
    
    return newSentenceCollection

