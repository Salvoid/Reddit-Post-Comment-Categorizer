# [Imports]====================================================================================================
import tkinter as tkgui # Import tkinter for GUI
import tkinter.ttk as tkttk # Import tkinter themed widgets for GUI Themes
import tkinter.scrolledtext as tkst # Import tkinter scrolled textbox for adding Scroll Textbox

import other_module as otherModule # Other needed functions


# [Declarations & Initializations]====================================================================================================
color_redditOrange = '#ff4500'
color_redditBlue = '#5c97ce'
color_black = '#000000'
color_white = '#ffffff'
color_gray = '#828282'
color_lightGray = '#cfcfcf'
color_red = '#eb1313'
color_blue = '#1321eb'

font_title = 'helvetica'
font_label = 'helvetica'
font_content = 'consolas'

count_consoleLineNumber = 0 # Global Variable Declaration
tkgui_Entry_f1 = None # Global Variable Declaration
tkgui_ScrolledText_f2 = None # Global Variable Declaration
tkgui_ScrolledText_f3 = None # Global Variable Declaration
scrollableCanvasWidgetWidth = 0 # Global Variable Declaration


# [Functions]====================================================================================================
# [Display Main Window Frame and Components.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def display_widget_main(in_categorize_post_function, in_object_reddit):
    # [Initialize Widgets]--------------------------------------------------
    # [window(Tk)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # =============================
    tkgui_window = tkgui.Tk() #Create a window(GUI)
    tkgui_window.minsize(700,500)
    tkgui_window.title("Reddit Post Comment Categorizer")
    tkgui_window.iconbitmap(otherModule.define_relativepath(False,".\\assets\\images\\window_icon.ico"))
    tkgui_window.columnconfigure(0, weight=1)
    tkgui_window.rowconfigure(0, weight=1)

    # [Display Widgets]--------------------------------------------------
    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    tkgui_Frame_main = tkgui.Frame(tkgui_window)
    tkgui_Frame_main.grid(row=0, column=0, padx=5, pady=20, sticky='NSWE')
    tkgui_Frame_main.columnconfigure(0, weight=1)
    tkgui_Frame_main.rowconfigure(2, weight=1)
    tkgui_Frame_main.rowconfigure(3, weight=5)

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # title(Canvas)=============================
    tkgui_Canvas_title_height = 40
    tkgui_Canvas_title_width = 600
    tkgui_Canvas_title = tkgui.Canvas(tkgui_Frame_main)
    tkgui_Canvas_title.config(
        height=tkgui_Canvas_title_height, 
        width=tkgui_Canvas_title_width
    )
    tkgui_Canvas_title.create_text((tkgui_Canvas_title_width/2)-180, 20, anchor='c', text="Reddit", fill=color_redditOrange, font=(font_title,20,'bold'))
    tkgui_Canvas_title.create_text((tkgui_Canvas_title_width/2)+50, 20, text="Post Comment Categorizer", fill=color_redditBlue, font=(font_title,20,'bold'))
    tkgui_Canvas_title.grid(column=0, row=0, sticky='N')

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f1(Frame)=============================
    tkgui_Frame_f1 = tkgui.Frame(tkgui_Frame_main)
    tkgui_Frame_f1.grid(column=0, row=1, sticky='NSWE')
    tkgui_Frame_f1.columnconfigure(0, weight=1)
    tkgui_Frame_f1.columnconfigure(1, weight=1)
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f1(Label)=============================
    tkgui_Label_f1 = tkgui.Label(tkgui_Frame_f1)
    tkgui_Label_f1['text'] = "Reddit Post Link"
    tkgui_Label_f1.config(
        fg=color_black, 
        font=(font_label,15,'bold')
    )
    tkgui_Label_f1.grid(column=0, row=0, padx=20, pady=4, columnspan=2, sticky='W')
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f1(Entry)=============================
    global tkgui_Entry_f1 # Used to edit a variable's value
    tkgui_Entry_f1_height = 14
    tkgui_Entry_f1 = tkgui.Entry(tkgui_Frame_f1)
    tkgui_Entry_f1.config(
        fg=color_black, 
        bg=color_lightGray, 
        font=(font_content,tkgui_Entry_f1_height,''), 
        borderwidth=3, 
        relief=tkgui.SUNKEN, 
        state=tkgui.NORMAL
    )
    tkgui_Entry_f1.grid(column=0, row=1, padx=20, pady=4, columnspan=2, sticky='NSWE')
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # categorize(Button)=============================
    tkgui_Button_categorize = tkgui.Button(tkgui_Frame_f1)
    tkgui_Button_categorize['text'] = "CATEGORIZE"
    tkgui_Button_categorize['command'] = lambda: in_categorize_post_function(tkgui_window, in_object_reddit)
    tkgui_Button_categorize.config(
        fg=color_white, 
        bg=color_gray, 
        font=(font_label,12,'bold'), 
        borderwidth=5, 
        relief=tkgui.RAISED, 
        state=tkgui.NORMAL
    )
    tkgui_Button_categorize.grid(column=0, row=2, padx=20, pady=4, sticky='E')
    # [f1(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # clear(Button)=============================
    tkgui_Button_clear = tkgui.Button(tkgui_Frame_f1)
    tkgui_Button_clear['text'] = "CLEAR FIELDS"
    tkgui_Button_clear['command'] = lambda: clear_allfields()
    tkgui_Button_clear.config(
        fg=color_white, 
        bg=color_gray, 
        font=(font_label,12,'bold'), 
        borderwidth=5, 
        relief=tkgui.RAISED, 
        state=tkgui.NORMAL
    )
    tkgui_Button_clear.grid(column=1, row=2, padx=20, pady=4, sticky='W')

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f2(Frame)=============================
    tkgui_Frame_f2 = tkgui.Frame(tkgui_Frame_main)
    tkgui_Frame_f2.grid(column=0, row=2, sticky='NSWE')
    tkgui_Frame_f2.columnconfigure(0, weight=1)
    tkgui_Frame_f2.rowconfigure(1, weight=1)
    # [f2(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f2(Label)=============================
    tkgui_Label_f2 = tkgui.Label(tkgui_Frame_f2)
    tkgui_Label_f2['text'] = "Console"
    tkgui_Label_f2.config(
        fg=color_black, 
        font=(font_label,15,'bold')
    )
    tkgui_Label_f2.grid(column=0, row=0, padx=20, pady=4, sticky='W')
    # [f2(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f2(ScrolledText(Custom))=============================
    global tkgui_ScrolledText_f2 # Used to edit a variable's value
    tkgui_ScrolledText_f2_height = 5
    tkgui_ScrolledText_f2 = tkst.ScrolledText(tkgui_Frame_f2)
    tkgui_ScrolledText_f2.config(
        height=tkgui_ScrolledText_f2_height, 
        fg=color_black, 
        bg=color_lightGray, 
        font=(font_content,12,''), 
        undo=True, 
        wrap=tkgui.WORD, 
        borderwidth=3, 
        relief=tkgui.SUNKEN, 
        state=tkgui.DISABLED
    )
    tkgui_ScrolledText_f2.tag_config('textTag_normalboldtext', foreground=color_black, font=(font_content,12,'bold'))
    tkgui_ScrolledText_f2.tag_config('textTag_task', foreground=color_black, font=(font_content,12,'italic'))
    tkgui_ScrolledText_f2.tag_config('textTag_process', foreground=color_red, font=(font_content,12,))
    tkgui_ScrolledText_f2.tag_config('textTag_finish', foreground=color_blue, font=(font_content,12,))
    tkgui_ScrolledText_f2.grid(column=0, row=1, padx=20, pady=4, sticky='NSWE')

    # [main(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f3(Frame)=============================
    tkgui_Frame_f3 = tkgui.Frame(tkgui_Frame_main)
    tkgui_Frame_f3.grid(column=0, row=3, sticky='NSWE')
    tkgui_Frame_f3.columnconfigure(0, weight=1)
    tkgui_Frame_f3.rowconfigure(1, weight=1)
    # [f3(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f3(Label)=============================
    tkgui_Label_f3 = tkgui.Label(tkgui_Frame_f3)
    tkgui_Label_f3['text'] = "Categorized Comments"
    tkgui_Label_f3.config(
        fg=color_black, 
        font=(font_label,15,'bold')
    )
    tkgui_Label_f3.grid(column=0, row=0, padx=20, pady=4, sticky='W')
    # [f3(Frame)]~~~~~~~~~~~~~~~~~~~~~~~~~
    # f3(ScrolledText(Custom))=============================
    global tkgui_ScrolledText_f3 # Used to edit a variable's value
    tkgui_ScrolledText_f3_height = 10
    tkgui_ScrolledText_f3 = tkgui.Frame(tkgui_Frame_f3)
    tkgui_ScrolledText_f3.config(
        height=tkgui_ScrolledText_f3_height, 
        bg=color_lightGray, 
        borderwidth=3, 
        relief=tkgui.SUNKEN, 
    )
    tkgui_ScrolledText_f3.grid(column=0, row=1, padx=20, pady=4, sticky='NSWE')

    return tkgui_window

# [Set Widget Options.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def set_widget_options(in_tkgui_window):
    style = tkttk.Style()
    style.theme_use('clam')

    in_tkgui_window.resizable(True, True) #Window resizability: Width = True; Height = True;
    in_tkgui_window.mainloop() #Keeps the window(GUI) active/displayed on screen

# [Print To Console(Process)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_console(in_windowWidget, in_addcount_consoleLineNumber, in_addNewline, in_insertText, in_textTag):
    global count_consoleLineNumber # Used to edit a variable's value
    tkgui_ScrolledText_f2.config(state=tkgui.NORMAL) # Enable Locked Text(Textarea)
    if in_addcount_consoleLineNumber:
        count_consoleLineNumber += 1
        tkgui_ScrolledText_f2.insert(tkgui.END, '[' + str(count_consoleLineNumber) + ']', 'textTag_normalboldtext') # Insert Console Line Number on Text(Textarea)
    
    if in_addNewline:
        tkgui_ScrolledText_f2.insert(tkgui.END, in_insertText + '\n', in_textTag) # Insert to End Text(Textarea) with newline
    else:
        tkgui_ScrolledText_f2.insert(tkgui.END, in_insertText, in_textTag) # Insert to End Text(Textarea)
    tkgui_ScrolledText_f2.config(state=tkgui.DISABLED) # Disable Locked Text(Textarea)
    tkgui_ScrolledText_f2.see(tkgui.END)
    
    in_windowWidget.update_idletasks() # Update widgets(?)

# [Print To Categorized Comments(Output)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_comments(in_parentWidget, in_addNewline, in_insertText, in_textTag):
    in_parentWidget.config(state=tkgui.NORMAL) # Enable Locked Text(Textarea)
    if in_addNewline:
        in_parentWidget.insert(tkgui.END, in_insertText + '\n', in_textTag) # Insert to End Text(Textarea) with newline
    else:
        in_parentWidget.insert(tkgui.END, in_insertText, in_textTag) # Insert to End Text(Textarea)
    in_parentWidget.config(state=tkgui.DISABLED) # Disable Locked Text(Textarea)
    in_parentWidget.see(tkgui.END)

# [Clear All Fields.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def clear_allfields():
    tkgui_Entry_f1.delete("0", tkgui.END) # (For Entry)Clear start to end of input

    tkgui_ScrolledText_f2.config(state=tkgui.NORMAL) # Enable Locked Text(Textarea)
    tkgui_ScrolledText_f2.delete("1.0", tkgui.END) # (For Text(Textarea))Clear start to end of input
    tkgui_ScrolledText_f2.config(state=tkgui.DISABLED) # Disable Locked Text(Textarea)

    for tkgui_ScrolledText_f3_child in tkgui_ScrolledText_f3.winfo_children():
        tkgui_ScrolledText_f3_child.destroy() # (For Result)Delete Comment Results

    global count_consoleLineNumber # Used to edit a variable's value
    count_consoleLineNumber = 0

# [Clear 'Categorized Comments' Display to provide space for new content/results.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def init_clear_comments(in_windowWidget):
    if len(tkgui_ScrolledText_f3.winfo_children()) > 0: # Automatically clears the content/results on the 'Categorized Comments' Display to provide space for new content/results, if it currently has any content/results in it
        print_console(in_windowWidget, True, False, "CONSOLE: ", 'textTag_task')
        print_console(in_windowWidget, False, True, "Clearing Results...", 'textTag_process')

        for tkgui_ScrolledText_f3_child in tkgui_ScrolledText_f3.winfo_children():
            tkgui_ScrolledText_f3_child.destroy() # (For Result)Delete Comment Results

        print_console(in_windowWidget, True, False, "CONSOLE: ", 'textTag_task')
        print_console(in_windowWidget, False, True, "Cleared Results Display.", 'textTag_finish')

# [Set Togglable Frame Widget(Widget)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def toggle_widget(in_parentWidget, in_topic_comment_category, in_raw_categorized_comments):
    toggleFrame_tf1 = ToggledFrame(in_parentWidget, text=f"\tTopic: {str(in_topic_comment_category[0])}", relief="raised", borderwidth=1)
    toggleFrame_tf1_text = tkst.ScrolledText(toggleFrame_tf1.sub_frame, height=20)
    toggleFrame_tf1_text.tag_config('textTag_normalboldtext', foreground=color_black, font=(font_content,12,'bold'))
    toggleFrame_tf1_text.tag_config('textTag_normaltext', foreground=color_black, font=(font_content,12,))
    toggleFrame_tf1.pack(fill="x", expand=True, pady=2, padx=2, anchor="n")

    # Expand all Toggle Frame to fit the Scrollbar
    toggleFrame_tf1.show.set(1)
    toggleFrame_tf1.sub_frame.pack(fill="x", expand=True)
    toggleFrame_tf1.toggle_button.configure(text='-')

    print_comments(toggleFrame_tf1_text, False, "Topic: ", 'textTag_normalboldtext')
    print_comments(toggleFrame_tf1_text, True, str(in_topic_comment_category[0]), 'textTag_normaltext')
    print_comments(toggleFrame_tf1_text, False, "Number of Comments: ", 'textTag_normalboldtext')
    print_comments(toggleFrame_tf1_text, True, str(len(in_topic_comment_category[1])), 'textTag_normaltext')

    count_comment_category = 0
    for count_comment in in_topic_comment_category[1]:
        char_list = [in_raw_categorized_comments[count_comment][j] for j in range(len(in_raw_categorized_comments[count_comment])) if ord(in_raw_categorized_comments[count_comment][j]) in range(65536)]
        in_raw_categorized_comments[count_comment]=''
        for j in char_list:
            in_raw_categorized_comments[count_comment]=in_raw_categorized_comments[count_comment]+j
        
        count_comment_category += 1
        print_comments(toggleFrame_tf1_text, False, "Comment #"+str(count_comment_category)+": ", 'textTag_normalboldtext')
        print_comments(toggleFrame_tf1_text, True, in_raw_categorized_comments[count_comment], 'textTag_comment')

    toggleFrame_tf1_text.pack(side="left", fill="x", expand=True)

# [Create Scrollable Frame Widget(Widget)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def scrollable_widget(in_windowWidget, in_topic_comment_categories, in_raw_categorized_comments):
    tkgui_Canvas_scrollable = tkgui.Canvas(tkgui_ScrolledText_f3)
    tkgui_Scrollbar_scrolly = tkgui.Scrollbar(tkgui_ScrolledText_f3, orient="vertical", command=tkgui_Canvas_scrollable.yview)

    tkgui_Frame_contentcontainer = tkgui.Frame(tkgui_Canvas_scrollable)
    
    # Place content on frame container
    for topic_comment_category in in_topic_comment_categories:
        toggle_widget(tkgui_Frame_contentcontainer, topic_comment_category, in_raw_categorized_comments)
    
    # Place frame container to canvas container
    tkgui_Window_scrollable = tkgui_Canvas_scrollable.create_window(0, 0, anchor='nw', window=tkgui_Frame_contentcontainer)

    # Verify display before configuring scrollregion
    tkgui_Canvas_scrollable.update_idletasks()

    # Configure scrollregion
    tkgui_Canvas_scrollable.configure(scrollregion=tkgui_Canvas_scrollable.bbox('all'), yscrollcommand=tkgui_Scrollbar_scrolly.set)
                    
    tkgui_Canvas_scrollable.pack(fill='both', expand=True, side='left')
    tkgui_Scrollbar_scrolly.pack(fill='y', side='right')

    tkgui_Canvas_scrollable.bind("<Configure>", lambda event:onWindowWidthChange(in_windowWidget, tkgui_Canvas_scrollable, tkgui_Window_scrollable)) # Bind canvas container children width updater
    onWindowWidthChange(in_windowWidget, tkgui_Canvas_scrollable, tkgui_Window_scrollable) # Trigger canvas container children width updater

# [Bind To Detect Main Window Width Size Change(Process)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def onWindowWidthChange(in_windowWidget, in_scrollableCanvasWidget, in_scrollableWindowWidget): # Trigger when main window size changed
    global scrollableCanvasWidgetWidth
    if not (scrollableCanvasWidgetWidth == in_scrollableCanvasWidget.winfo_width()): # Trigger when main window width changed
        in_windowWidget.after(500, lambda:update_scrollableWidth(in_windowWidget, in_scrollableCanvasWidget, in_scrollableWindowWidget)) # Delay 1/2 a second before calling function to update canvas container children width
        scrollableCanvasWidgetWidth = in_scrollableCanvasWidget.winfo_width()

# [Update Canvas Container Children Width(Process)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def update_scrollableWidth(in_windowWidget, in_scrollableCanvasWidget, in_scrollableWindowWidget):
    in_scrollableCanvasWidget.itemconfigure(in_scrollableWindowWidget, width=in_scrollableCanvasWidget.winfo_width())
    in_windowWidget.update_idletasks() # Update widgets(?)

# [Create Togglable Frame Widget(Widget)]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToggledFrame(tkgui.Frame):
    def __init__(self, parent, text="", *args, **options):
        tkgui.Frame.__init__(self, parent, *args, **options)

        self.show = tkgui.IntVar()
        self.show.set(0)

        self.title_frame = tkgui.Frame(self)
        self.title_frame.pack(fill="x", expand=True)

        tkgui.Label(self.title_frame, text=text, width=90).pack(side="left", fill="x", expand=True)

        self.toggle_button = tkttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle, variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tkgui.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=True)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')

# [Get User Input URL.]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_url():
    return tkgui_Entry_f1.get() # (For Entry)Get start to end of input excluding last character(*?)

