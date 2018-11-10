from Tix import *
import tkFileDialog
from ttk import Progressbar, Style
from PIL import Image, ImageTk
import xml.etree.cElementTree as ET
import os


class Program(Tk):

    def __init__(self):
        Tk.__init__(self)

        aa = {
            # Application Attributes
            'main_bg': 'deepskyblue4',
            'sub_bg': 'deepskyblue2'
        }
        self.fs = False
        self.title('Field View Searcher')
        self.geometry(str(int(self.winfo_screenwidth()*0.8)) + 'x' + str(int(self.winfo_screenheight()*0.8)))
        self.attributes('-fullscreen', self.fs)  # Fullscreen the program
        # self.state('zoomed')  # Maximize the program
        self.config(bg=aa['sub_bg'])

        self.directory_location = None
        self.tree = None
        self.root = None
        self.total_wb_count = 0
        self.wb_count = 0
        self.total_wb_start = 0
        self.wb_start = 0

        # Frames
        self.left_frame = Frame(self, bg=aa['main_bg'])
        self.left_frame.pack(side=LEFT, fill=Y)
        self.left_top_frame = Frame(self.left_frame, bg=aa['main_bg'])
        self.left_top_frame.pack(side=TOP, fill=BOTH)
        self.left_bottom_frame = Frame(self.left_frame, bg=aa['main_bg'])
        self.left_bottom_frame.pack(side=BOTTOM, fill=BOTH)

        self.right_frame = Frame(self, bg=aa['sub_bg'], relief=SUNKEN)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.right_left_frame = Frame(self.right_frame, bg=aa['sub_bg'])
        self.right_left_frame.pack(side=LEFT, fill=BOTH)
        self.right_left_frame_1 = Frame(self.right_frame, bg=aa['sub_bg'])
        self.right_left_frame_1.pack(side=LEFT, fill=BOTH)
        self.right_left_frame_2 = Frame(self.right_frame, bg=aa['sub_bg'])
        self.right_left_frame_2.pack(side=LEFT, fill=BOTH)


        ba = {
            # Button Attributes
            'padx': 2,
            'pady': 4,
            'font': 'none 12 bold',
            'bg_color': 'white',
            'fg_color': 'deepskyblue4'
        }
        ta = {
            # Text Attributes
            'padx': 2,
            'pady': 4,
            'font': 'none 12',
            'bg_color': 'white',
            'fg_color': 'black'
        }
        la = {
            # Label Attributes
            'padx': 2,
            'pady': 4,
            'font': 'none 26 bold',
            'bg_color': aa['sub_bg'],
            'fg_color': aa['main_bg']
        }
        # Images
        image_width, image_height = 30, 30
        dir_image = Image.open('Images/blue_folder.png')
        dir_image = dir_image.resize((image_width, image_height), Image.ANTIALIAS)
        self.directory_image = ImageTk.PhotoImage(dir_image)
        s_image = Image.open('Images/search.png')
        s_image = s_image.resize((image_width, image_height), Image.ANTIALIAS)
        self.search_image = ImageTk.PhotoImage(s_image)
        fs_image = Image.open('Images/fullscreen.png')
        fs_image = fs_image.resize((image_width, image_height), Image.ANTIALIAS)
        self.fullscreen_image = ImageTk.PhotoImage(fs_image)
        q_image = Image.open('Images/quit.png')
        q_image = q_image.resize((image_width, image_height), Image.ANTIALIAS)
        self.quit_image = ImageTk.PhotoImage(q_image)

        # Buttons
        self.locate_directory_button = Button(self.left_top_frame, image=self.directory_image, command=self.view_directory_locator, fg=ba['fg_color'], bg=ba['bg_color'], font=ba['font'])
        self.locate_directory_button.pack(side=LEFT, padx=ba['padx'], pady=ba['pady'])
        self.toggle_fs_button = Button(self.left_bottom_frame, image=self.fullscreen_image, command=self.toggle_fullscreen, fg=ba['fg_color'], bg=ba['bg_color'], font=ba['font'])
        self.toggle_fs_button.pack(side=LEFT, padx=ba['padx'], pady=ba['pady'])
        self.exit_button = Button(self.left_bottom_frame, image=self.quit_image, command=quit, fg=ba['fg_color'], bg=ba['bg_color'], font=ba['font'])
        self.exit_button.pack(side=LEFT, padx=ba['padx'], pady=ba['pady'])
        # Search bar & button
        self.search_bar = Entry(self.left_top_frame, fg=ta['fg_color'], bg=ta['bg_color'], font=ta['font'], relief=SUNKEN)
        self.search_bar.pack(side=LEFT, fill=BOTH, expand=True, padx=ta['padx'], pady=ta['pady'])
        self.search_button = Button(self.left_top_frame, image=self.search_image, command=self.search_views, fg=ba['fg_color'], bg=ba['bg_color'], font=ba['font'])
        self.search_button.pack(side=RIGHT, padx=ba['padx'], pady=ba['pady'])

        # Label Text
        self.wb_count_text = StringVar()
        self.wb_count_text.set('')
        self.wb_desc_text = StringVar()
        self.wb_desc_text.set('')
        self.total_wb_count_text = StringVar()
        self.total_wb_count_text.set('')
        self.total_wb_desc_text = StringVar()
        self.total_wb_desc_text.set('')

        # Labels
        self.total_wb_desc_label = Label(self.right_left_frame, textvariable=self.total_wb_desc_text, fg=la['fg_color'], bg=la['bg_color'], font=la['font'], anchor=NE)
        self.total_wb_desc_label.pack(side=TOP, fill=BOTH, padx=la['padx'], pady=la['pady'])
        self.total_wb_count_label = Label(self.right_left_frame_2, textvariable=self.total_wb_count_text, fg=la['fg_color'], bg=la['bg_color'], font=la['font'], anchor=NW)
        self.total_wb_count_label.pack(side=TOP, fill=BOTH, padx=la['padx'], pady=la['pady'])

        self.wb_desc_label = Label(self.right_left_frame, textvariable=self.wb_desc_text, fg=la['fg_color'], bg=la['bg_color'], font=la['font'], anchor=NE)
        self.wb_desc_label.pack(side=TOP, fill=BOTH, padx=la['padx'], pady=la['pady'])
        self.wb_count_label = Label(self.right_left_frame_2, textvariable=self.wb_count_text, fg=la['fg_color'], bg=la['bg_color'], font=la['font'], anchor=NW)
        self.wb_count_label.pack(side=TOP, fill=BOTH, padx=la['padx'], pady=la['pady'])

        # Progress Bars
        self.s = Style()
        self.s.theme_use('classic')
        self.s.configure('blue.Horizontal.TProgressbar', troughcolor=aa['sub_bg'], background=aa['main_bg'], thickness=45)

        self.wb_total_progressbar = Progressbar(self.right_left_frame_1, style='blue.Horizontal.TProgressbar', length=400)
        self.wb_progressbar = Progressbar(self.right_left_frame_1, style='blue.Horizontal.TProgressbar', length=400)

        # Tooltips
        self.tooltips = Balloon(self)
        for sub in self.tooltips.subwidgets_all():  # Makes the tooltip background a specified color
            sub.config(bg='white')
        self.tooltips.subwidget('label')['image'] = BitmapImage()  # Removes arrow in the top left corner
        self.tooltips.bind_widget(self.toggle_fs_button, balloonmsg='Fullscreen')
        self.tooltips.bind_widget(self.exit_button, balloonmsg='Exit')
        self.tooltips.bind_widget(self.locate_directory_button, balloonmsg='Locate views directory')
        self.tooltips.bind_widget(self.search_button, balloonmsg='Search')

    def view_directory_locator(self):
        self.directory_location = tkFileDialog.askdirectory(title='Locate the folder that contains the views you would like to search')

    def search_views(self):
        """ Will be used to search the directory's workbooks for the field written in the search bar.

        :return: Will probably run other functions that do things like count the views with that field, count the workbooks, etc.
        """
        self.reset_metrics()

        if self.directory_location != None and self.search_bar.get() != '':
            for the_file in os.listdir(self.directory_location):
                if the_file.split('.')[1] == 'twb':
                    # set the path to the file
                    path = self.directory_location + '/' + the_file
                    # set the tree and root
                    self.tree = ET.parse(path)
                    self.root = self.tree.getroot()
                    self.total_wb_count += 1
                    self.wb_count += 1

        if self.search_bar.get() != '':
            self.wb_desc_text.set('Workbooks Using ' + self.search_bar.get() + ': ')
            self.total_wb_desc_text.set('Workbooks Total: ')

            self.wb_total_progressbar['maximum'] = self.total_wb_count
            self.wb_progressbar['maximum'] = self.total_wb_count
            self.wb_total_progressbar.pack(side=TOP, fill=BOTH)
            self.wb_progressbar.pack(side=TOP, fill=BOTH)
            self.total_wb_progress_start()
            self.wb_progress_start()

    def total_wb_progress_start(self):
        if self.total_wb_start < self.total_wb_count:
            self.total_wb_start += (self.total_wb_count * 0.02)
            self.wb_total_progressbar['value'] = self.total_wb_start
            self.after(1, self.total_wb_progress_start)
        else:
            self.total_wb_count_text.set(str(self.total_wb_count))

    def wb_progress_start(self):
        if self.wb_start < self.wb_count:
            self.wb_start += (self.wb_count * 0.02)
            self.wb_progressbar['value'] = self.wb_start
            self.after(1, self.wb_progress_start)
        else:
            self.wb_count_text.set(str(self.wb_count))

    def reset_metrics(self):
        self.total_wb_count = 0
        self.wb_count = 0
        self.total_wb_start = 0
        self.wb_start = 0
        self.wb_desc_text.set('')
        self.total_wb_desc_text.set('')
        self.wb_count_text.set('')
        self.total_wb_count_text.set('')

    def toggle_fullscreen(self):
        if self.fs:
            self.fs = False
        else:
            self.fs = True
        self.attributes('-fullscreen', self.fs)


app = Program()
app.mainloop()

# flask