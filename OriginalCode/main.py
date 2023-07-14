# [Imports]========================================================================================================================================[Imports]
import os # Miscellaneous Operating System Interfaces
import praw
import csv

import run_NQTM as runNQTMModule # Main module to run model.
import preprocess_module as preprocessNQTMModule # Module to prepare data and create matrix and bag of words.
import gui_module as guiModule # Software GUI
import other_module as otherModule # Other needed functions


# [Declarations & Initializations]==========================================================================================[Declarations & Initializations]


# [Functions]====================================================================================================
# [Main.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    init_dirs() # Initialize needed directories.
    runNQTMModule.init_parser() # Initialize model.
    object_reddit = init_reddit() # Initialize Reddit API Requirements.

    tkgui_window = guiModule.display_widget_main(categorize_post, object_reddit)
    guiModule.set_widget_options(tkgui_window)

# [Initialize Needed Directories.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def init_dirs():
    os.makedirs(otherModule.define_relativepath(True,".\\d_input"), exist_ok=True)
    os.makedirs(otherModule.define_relativepath(True,".\\d_output"), exist_ok=True)
    os.makedirs(otherModule.define_relativepath(True,".\\d_raw"), exist_ok=True)
    os.makedirs(otherModule.define_relativepath(True,".\\d_results"), exist_ok=True)

# [Define and Initialize Reddit API Requirements.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def init_reddit():
    # Define Reddit API Requirements
    in_client_id = ""
    in_client_secret = ""
    in_username = ""
    in_password = ""
    in_user_agent = ""

    # Initiate Reddit API Requirements
    object_reddit = praw.Reddit(
        client_id = in_client_id, 
        client_secret = in_client_secret, 
        username = in_username, 
        password = in_password, 
        user_agent = in_user_agent,

        check_for_updates=False,
        comment_kind="t1",
        message_kind="t4",
        redditor_kind="t2",
        submission_kind="t3",
        subreddit_kind="t5",
        trophy_kind="t6",

        oauth_url="https://oauth.reddit.com",
        reddit_url="https://www.reddit.com",
        short_url="https://redd.it",

        ratelimit_seconds="5",
        timeout="16",
    )
    return object_reddit

# [Main Process in Categorizing Reddit Post Comments.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def categorize_post(in_windowWidget, in_object_reddit):
    inputUrl = guiModule.get_url()

    guiModule.init_clear_comments(in_windowWidget)

    object_inputPost = otherModule.verifyfetch_url(in_windowWidget, inputUrl, in_object_reddit)

    if object_inputPost == None: # If no Reddit Post was fetched successfully
        return
    
    object_inputPost.comments.replace_more(limit=None)
    inputPost_retrievedcomments = object_inputPost.comments.list()
    inputPost_totalComments = object_inputPost.num_comments
    inputPost_totalRetrievedComments = len(inputPost_retrievedcomments)
    raw_comments = [inputPost_comment.body for inputPost_comment in inputPost_retrievedcomments]

    guiModule.print_console(in_windowWidget, True, False, "Categorizing Comments Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "Text cleansing comments...", 'textTag_process')

    clean_comments = otherModule.tokenize_textCollection(raw_comments)

    raw_categorized_comments = []
    clean_categorized_comments = []
    raw_uncategorized_comments = []
    clean_uncategorized_comments = []

    count_comment = 0
    for comment in clean_comments:
        if(comment == "") or (comment.count(' ') < 1):
            raw_uncategorized_comments.append(raw_comments[count_comment])
            clean_uncategorized_comments.append(clean_comments[count_comment])
        else:
            raw_categorized_comments.append(raw_comments[count_comment])
            clean_categorized_comments.append(clean_comments[count_comment])

        count_comment += 1

    with open(otherModule.define_relativepath(True,".\\d_raw\\texts.txt"), 'w') as f:
        for term in clean_categorized_comments:
            f.write("%s\n" % term)

    guiModule.print_console(in_windowWidget, True, False, "Categorizing Comments Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "Preprocessing comments...", 'textTag_process')

    preprocessNQTMModule.preprocess_data() # Prepare data. Create matrix and bag of words.

    guiModule.print_console(in_windowWidget, True, False, "Categorizing Comments Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "Running comment categorizer...", 'textTag_process')

    runNQTMModule.run_main() # Run the model.

    # raw_comments = list()
    # with open(otherModule.define_relativepath(False,".\\d_raw\\texts.txt")) as topics_file:
    #     for line in topics_file:
    #         raw_comments.append(line.strip())

    topics = list()
    with open(otherModule.define_relativepath(False,".\\d_output\\topic_words_T1_K10_1th.txt")) as topics_file:
        for line in topics_file:
            topics.append(line.strip())
    
    topic_comment_categories = list()
    used_comment_indices = list()
    count_topic = 0
    while count_topic < len(topics):
        if not (used_comment_indices) or not (count_topic in used_comment_indices):
            comment_indices = [i for i, x in enumerate(topics) if x == topics[count_topic]] # Find all occurrences of a topic in the topic list
            topic_comment_categories.append([str(topics[count_topic]),comment_indices])
            used_comment_indices.extend(comment_indices)
        count_topic += 1

    guiModule.print_console(in_windowWidget, True, False, "Categorizing Comments Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "SUCCESS", 'textTag_finish')

    guiModule.print_console(in_windowWidget, True, False, "Printing Categorized Comments Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "Sorting Comments in Ascending Order...", 'textTag_process')

    topic_comment_categories.sort(key=len) # Sort from least to most comments
    topic_comment_categories.reverse() # Reverse list to ascending order

    guiModule.print_console(in_windowWidget, True, False, "Printing Categorized Comments Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "Printing comments...", 'textTag_process')
    
    guiModule.scrollable_widget(in_windowWidget, topic_comment_categories, raw_categorized_comments)

    guiModule.print_console(in_windowWidget, True, False, "Printing Categorized Comments Status: ", 'textTag_task')
    guiModule.print_console(in_windowWidget, False, True, "SUCCESS", 'textTag_finish')
    
    process_saveResults(topics, topic_comment_categories, raw_categorized_comments, clean_categorized_comments, raw_uncategorized_comments, clean_uncategorized_comments)

    # Clean used Variables
    inputUrl = None
    object_inputPost = None
    inputPost_retrievedcomments.clear()
    inputPost_totalComments = 0
    inputPost_totalRetrievedComments = 0
    raw_comments.clear()
    clean_comments.clear()
    raw_categorized_comments.clear()
    clean_categorized_comments.clear()
    raw_uncategorized_comments.clear()
    clean_uncategorized_comments.clear()
    topics.clear()
    topic_comment_categories.clear()
    used_comment_indices.clear()
    count_topic = 0
    count_comment = 0

# [Save Results for Topic Coherence Evaluation(Separate Process).]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_saveResults(in_topics, in_topic_comment_categories, in_raw_categorized_comments, in_clean_categorized_comments, in_raw_uncategorized_comments, in_clean_uncategorized_comments):
    with open(otherModule.define_relativepath(True,".\\d_results\\data.csv"), 'w', newline='', encoding='utf-8') as csv_file:
        columnNames = ["raw", "cleaned", "topic", "topic count", "categorized comments count", "uncategorized comments count"]
        write = csv.DictWriter(csv_file, fieldnames=columnNames)
        write.writeheader()
        # write.writerow("Topic Count: {}".format(len(topics)))
        # write.writerow("Categorized Comments Count: {}".format(len(raw_categorized_comments)))
        # write.writerow("Uncategorized Comments Count: {}".format(len(raw_uncategorized_comments)))
        write.writerow({"topic count": len(in_topic_comment_categories), "categorized comments count": len(in_raw_categorized_comments), "uncategorized comments count": len(in_raw_uncategorized_comments)})
        print("Topic Count: {}".format(len(in_topic_comment_categories)))
        print("Topic Count(Total Topics Assigned): {}".format(len(in_topics)))
        print("Raw Categorized Comments Count: {}".format(len(in_raw_categorized_comments)))
        print("Clean Categorized Comments Count: {}".format(len(in_clean_categorized_comments)))
        print("Raw Uncategorized Comments Count: {}".format(len(in_raw_uncategorized_comments)))
        print("Clean Uncategorized Comments Count: {}".format(len(in_clean_uncategorized_comments)))

        count_comment = 0
        while count_comment < len(in_raw_categorized_comments):
            write.writerow({"raw": in_raw_categorized_comments[count_comment], "cleaned": in_clean_categorized_comments[count_comment], "topic": in_topics[count_comment]})
            count_comment += 1
        
        count_comment = 0
        while count_comment < len(in_raw_uncategorized_comments):
            write.writerow({"raw": in_raw_uncategorized_comments[count_comment], "cleaned": in_clean_uncategorized_comments[count_comment], "topic": "*No Topic Category*"})
            count_comment += 1


# [Main]====================================================================================================
# [Main.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    main()

