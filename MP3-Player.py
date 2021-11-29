import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
import pygame
from tkinter import ttk


class MP3:
    """The main part of program, that contain all methods and variables to work"""

    def __init__(self):
        # WINDOW CREATING
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.root = Tk()
        self.root.title('MP3-Player')
        self.root.iconphoto(False, PhotoImage(file='icon.png'))
        self.w = (self.root.winfo_screenwidth() // 2) - 200
        self.h = (self.root.winfo_screenheight() // 2) - 200
        self.root.geometry('450x300+{}+{}'.format(self.w, self.h))
        self.root.configure(bg='#38383C')
        self.root.resizable(False, False)

        # Style for ttk creating
        self.style = ttk.Style(self.root)
        self.style.theme_names()
        self.style.theme_use('alt')
        self.style.configure('TScale', background='#38383C', fg='#38383C', troughcolor='#5D5D65')

        # BUTTONS AND FRAMES CREATING
        self.btns_frame = Frame(self.root, height=100, bg='#38383C', borderwidth=1)
        self.btns_frame.pack(side=BOTTOM, fill=BOTH)

        self.prev_png = PhotoImage(file='prev.png').subsample(5)
        self.prev_btn = Button(master=self.btns_frame, image=self.prev_png, bg='#38383C', borderwidth=0,
                               activebackground='#5D5D65',
                               command=self.reach_for_begining)
        self.prev_btn.bind('<Double-Button-1>', self.prev)
        self.prev_btn.place(relx=0.35, rely=0.5, anchor=CENTER)

        self.start_png = PhotoImage(file='start.png').subsample(4)
        self.pause_png = PhotoImage(file='pause.png').subsample(4)
        self.start_or_pause_btn = Button(master=self.btns_frame, image=self.start_png, bg='#38383C', borderwidth=0,
                                         activebackground='#5D5D65',
                                         command=self.pause)
        self.start_or_pause_btn.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.stop_png = PhotoImage(file='stop.png').subsample(11)
        self.stop_btn = Button(master=self.btns_frame, image=self.stop_png, bg='#38383C', borderwidth=0,
                               activebackground='#5D5D65',
                               command=self.stop)
        self.stop_btn.place(relx=0.1, rely=0.5, anchor=CENTER)

        self.next_png = PhotoImage(file='next.png').subsample(5)
        self.next_btn = Button(master=self.btns_frame, image=self.next_png, bg='#38383C', borderwidth=0,
                               activebackground='#5D5D65',
                               command=self.next_track)
        self.next_btn.place(relx=0.65, rely=0.5, anchor=CENTER)

        self.replay_off_png = PhotoImage(file='replay_off.png').subsample(17)
        self.replay_on_png = PhotoImage(file='replay_on.png').subsample(17)
        self.replay_playlist_png = PhotoImage(file='replay_playlist.png').subsample(17)
        self.replay_btn = Button(master=self.btns_frame, image=self.replay_off_png, bg='#38383C', borderwidth=0,
                                 activebackground='#5D5D65',
                                 command=self.replay_on)
        self.replay_btn.place(relx=0.9, rely=0.5, anchor=CENTER)

        # Load_button and track_name out the frame
        self.load_png = PhotoImage(file='load.png').subsample(10)
        self.load_btn = Button(master=self.root, image=self.load_png, bg='#38383C', borderwidth=0,
                               activebackground='#5D5D65',
                               command=self.load)
        self.load_btn.place(relx=0.1, rely=0.175, anchor=CENTER)

        self.track_name_on_screen = Label(master=self.root, bg='#38383C', fg='#D8C3C3',
                                          text='', font=('Cambria Math', 12),
                                          justify=LEFT, width=30)
        self.track_name_on_screen.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.playlist_png = PhotoImage(file='playlist.png').subsample(8)
        self.playlist_btn = Button(master=self.root, image=self.playlist_png, bg='#38383C', borderwidth=0,
                                   activebackground='#5D5D65',
                                   command=self.playlist_open)
        self.playlist_btn.place(relx=0.9, rely=0.2, anchor=CENTER)

        self.list_of_songs_names = list()
        self.list_of_songs = list()

        # Height of volume
        self.scale_volume_mute_png = PhotoImage(file='mute.png').subsample(18)
        self.scale_volume_png = PhotoImage(file='volume.png').subsample(18)
        self.scale_volume_100_png = PhotoImage(file='volume_100.png').subsample(18)

        self.button_mute = Button(master=self.root, image=self.scale_volume_mute_png, bg='#38383C', borderwidth=0,
                                  activebackground='#5D5D65',
                                  command=self.volume_mute)
        self.button_mute.place(relx=0.045, rely=0.65, anchor=CENTER)

        self.button_average = Button(master=self.root, image=self.scale_volume_png, bg='#38383C', borderwidth=0,
                                     activebackground='#5D5D65',
                                     command=self.volume_average)
        self.button_average.place(relx=0.05, rely=0.5, anchor=CENTER)

        self.button_100 = Button(master=self.root, image=self.scale_volume_100_png, bg='#38383C', borderwidth=0,
                                 activebackground='#5D5D65',
                                 command=self.volume_100)
        self.button_100.place(relx=0.05, rely=0.35, anchor=CENTER)

        self.scale = ttk.Scale(self.root, from_=100, to=0, orient="vertical", style='TScale',
                               command=self.scale_volume_height, value=100)
        self.scale.place(relx=0.11, rely=0.5, anchor=CENTER)

        # Track playing
        self.scale_of_track = ttk.Scale(self.root, from_=0, to=0, orient='horizontal', length=200,
                                        style='TScale',
                                        command=self.track_playing)
        self.scale_of_track.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.time_playing = Label(master=self.root, bg='#38383C', fg='#D8C3C3',
                                  text=0, font=('Cambria Math', 12),
                                  justify=LEFT)
        self.time_playing.place(relx=0.25, rely=0.70, anchor=CENTER)
        # self.time_playing_update()
        self.length_track = 0
        self.time_all = Label(master=self.root, bg='#38383C', fg='#D8C3C3',
                              text=self.length_track, font=('Cambria Math', 12),
                              justify=LEFT)
        self.time_all.place(relx=0.75, rely=0.70, anchor=CENTER)
        self.time_all.configure(text=self.length_track)

        # Temporaries
        self.val = 0
        self.temp_st = ''

        self.playing = 0
        self.length = 0

        self.root.mainloop()

    def find_length_of_track(self):
        self.length_track = int(self.length)
        if self.length_track < 10:
            self.length_track = str('0.0' + str(self.length_track))
        else:
            self.length_track = str(self.length_track // 60) + '.' + str(self.length_track % 60)
        self.time_all.configure(text=self.length_track)
        self.scale_of_track.configure(to=self.length_track)

    def load(self):
        # self.tracks_length = list()
        track_name = askopenfilename()
        self.list_of_songs.append(track_name)
        # self.tracks_length = list()
        # self.tracks_length.append(pygame.mixer.Sound(track_name).get_length())
        # print(self.tracks_length)
        self.list_of_songs_names.append(((track_name.split("/")[-1]).split('.'))[0])
        if len(self.list_of_songs_names) == 1:
            try:
                pygame.mixer.music.load(self.list_of_songs[0])
                pygame.mixer.music.play()
                self.track_name_on_screen.configure(text=self.list_of_songs_names[0])
                self.playing = 1
                self.length = pygame.mixer.Sound(self.list_of_songs[0]).get_length()
                self.find_length_of_track()
            except:
                del self.list_of_songs_names[len(self.list_of_songs_names) - 1]
                del self.list_of_songs[len(self.list_of_songs) - 1]
        elif len(self.list_of_songs_names) == 2:
            try:
                pygame.mixer.Sound(track_name)
                if pygame.mixer.music.get_busy():
                    def check_event():
                        """ Function check events in pygame.event list(?), and if the events was already done, will
                        start to do some command you have ever code """
                        for event in pygame.event.get():
                            if event.type == MUSIC_END and len(self.list_of_songs) == 2:
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load(self.list_of_songs[1])
                                self.playing = 2
                                self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                                self.find_length_of_track()
                                pygame.mixer.music.play()
                                self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                                pygame.mixer.music.set_endevent(0)
                            if event.type == MUSIC_END and len(self.list_of_songs) == 1:
                                pygame.mixer.music.unload()
                                self.track_name_on_screen.configure(text='')
                        self.root.after(100, check_event)

                    MUSIC_END = pygame.USEREVENT + 1
                    pygame.mixer.music.set_endevent(MUSIC_END)

                    check_event()
                else:
                    pygame.mixer.music.load(self.list_of_songs[1])
                    self.playing = 2
                    self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                    self.find_length_of_track()
                    pygame.mixer.music.play(0)
                    self.track_name_on_screen.configure(text=self.list_of_songs_names[1])

            except:
                del self.list_of_songs_names[len(self.list_of_songs_names) - 1]
                del self.list_of_songs[len(self.list_of_songs) - 1]
        elif len(self.list_of_songs_names) == 3:
            try:
                pygame.mixer.Sound(track_name)
                if pygame.mixer.music.get_busy():
                    def check_event():
                        """ Function check events in pygame.event list(?), and if the events was already done, will
                        start to do some command you have ever code """
                        for event in pygame.event.get():
                            if event.type == MUSIC_END:
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load(self.list_of_songs[1])
                                pygame.mixer.music.play()
                                self.playing = 2
                                self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                                self.find_length_of_track()
                                self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                                pygame.mixer.music.set_endevent(MUSIC_END_2)
                            if event.type == MUSIC_END_2:
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load(self.list_of_songs[2])
                                pygame.mixer.music.play()
                                self.playing = 3
                                self.length = pygame.mixer.Sound(self.list_of_songs[2]).get_length()
                                self.find_length_of_track()
                                self.track_name_on_screen.configure(text=self.list_of_songs_names[2])
                                pygame.mixer.music.set_endevent(0)
                        self.root.after(100, check_event)

                    MUSIC_END = pygame.USEREVENT + 1
                    MUSIC_END_2 = pygame.USEREVENT + 2

                    check_event()
                else:
                    pygame.mixer.music.load(self.list_of_songs[2])
                    self.playing = 2
                    self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                    self.find_length_of_track()
                    pygame.mixer.music.play(0)
                    self.track_name_on_screen.configure(text=self.list_of_songs_names[2])
            except:
                del self.list_of_songs_names[len(self.list_of_songs_names) - 1]
                del self.list_of_songs[len(self.list_of_songs) - 1]

        if len(self.list_of_songs_names) == 4:
            try:
                pygame.mixer.Sound(track_name)
            except:
                pass
            else:
                answer = tkinter.messagebox.askyesno('Playlist',
                                                     'Playlists can contain only 3 tracks!\nYou want to remove '
                                                     'first track?')
                if answer:
                    del self.list_of_songs_names[0]
                    del self.list_of_songs[0]
                    pygame.mixer.music.load(self.list_of_songs[0])
                    pygame.mixer.music.play()
                    self.playing = 1
                    self.length = pygame.mixer.Sound(self.list_of_songs[0]).get_length()
                    self.find_length_of_track()
                    self.track_name_on_screen.configure(text=self.list_of_songs_names[0])

                    def check_event():
                        """ Function check events in pygame.event list(?), and if the events was already done, will
                        start to do some command you have ever code """
                        for event in pygame.event.get():
                            if event.type == MUSIC_END:
                                if len(self.list_of_songs) == 1 and self.playing == 1:
                                    pygame.mixer.music.set_endevent(0)
                                else:
                                    pygame.mixer.music.unload()
                                    pygame.mixer.music.load(self.list_of_songs[1])
                                    pygame.mixer.music.play()
                                    self.playing = 2
                                    self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                                    self.find_length_of_track()
                                    self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                                    pygame.mixer.music.set_endevent(MUSIC_END_2)
                            if event.type == MUSIC_END_2:
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load(self.list_of_songs[2])
                                pygame.mixer.music.play()
                                self.playing = 3
                                self.length = pygame.mixer.Sound(self.list_of_songs[2]).get_length()
                                self.find_length_of_track()
                                self.track_name_on_screen.configure(text=self.list_of_songs_names[2])
                                pygame.mixer.music.set_endevent(0)
                        self.root.after(100, check_event)

                    MUSIC_END = pygame.USEREVENT + 1
                    MUSIC_END_2 = pygame.USEREVENT + 2

                    pygame.mixer.music.set_endevent(MUSIC_END)

                    check_event()

                else:
                    del self.list_of_songs_names[3]

        self.start_or_pause_btn.config(image=self.pause_png, command=self.pause)

    def stop(self):
        try:
            self.replay_off()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.list_of_songs.clear()
            self.list_of_songs_names.clear()
            self.track_name_on_screen['text'] = ''
            self.time_all.configure(text=0)
        except:
            pass

    def time_playing_update(self):
        while pygame.mixer.music.get_busy():
            self.val += pygame.mixer.music.get_pos()
            self.time_playing.configure(text=self.val)
            self.root.after(100, self.time_playing_update)

    def pause(self):
        pygame.mixer.music.pause()
        self.start_or_pause_btn.config(image=self.start_png, command=self.play)

    def play(self):
        pygame.mixer.music.unpause()
        self.start_or_pause_btn.config(image=self.pause_png, command=self.pause)

    def replay_on(self):
        try:
            self.val += pygame.mixer.music.get_pos()
            pygame.mixer.music.play(-1, start=self.val / 1000)
        except:
            pass
        else:
            self.start_or_pause_btn.config(image=self.pause_png, command=self.pause)
            self.replay_btn.config(image=self.replay_on_png, command=self.replay_playlist)

    def replay_playlist(self):
        self.val += pygame.mixer.music.get_pos()
        try:
            if self.playing == 1:
                pygame.mixer.music.load(self.list_of_songs[0])
                pygame.mixer.music.play(0, start=self.val / 1000)
                pygame.mixer.music.set_endevent(0)
            elif self.playing == 2:
                pygame.mixer.music.load(self.list_of_songs[1])
                pygame.mixer.music.play(0, start=self.val / 1000)
                pygame.mixer.music.set_endevent(0)
            else:
                pygame.mixer.music.load(self.list_of_songs[2])
                pygame.mixer.music.play(0, start=self.val / 1000)
                pygame.mixer.music.set_endevent(0)

            if len(self.list_of_songs) == 1:
                self.replay_on()
                self.replay_btn.configure(image=self.replay_playlist_png)
            elif len(self.list_of_songs) == 2:
                MUSIC_END_1 = pygame.USEREVENT + 1
                MUSIC_END_2 = pygame.USEREVENT + 2

                def check_event():
                    for event in pygame.event.get():
                        if event.type == MUSIC_END_1:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[1])
                            pygame.mixer.music.play()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                            self.playing = 2
                            self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                            self.find_length_of_track()
                            pygame.mixer.music.set_endevent(MUSIC_END_2)

                        if event.type == MUSIC_END_2:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[0])
                            pygame.mixer.music.play()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[0])
                            self.playing = 1
                            self.length = pygame.mixer.Sound(self.list_of_songs[0]).get_length()
                            self.find_length_of_track()
                            pygame.mixer.music.set_endevent(MUSIC_END_1)
                    self.root.after(100, check_event)

                if self.playing == 1:
                    pygame.mixer.music.set_endevent(MUSIC_END_1)
                elif self.playing == 2:
                    pygame.mixer.music.set_endevent(MUSIC_END_2)

                check_event()
            else:
                MUSIC_END_1 = pygame.USEREVENT + 1
                MUSIC_END_2 = pygame.USEREVENT + 2
                MUSIC_END_3 = pygame.USEREVENT + 3

                def check_event():
                    for event in pygame.event.get():
                        if event.type == MUSIC_END_1:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[1])
                            pygame.mixer.music.play()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                            self.playing = 2
                            self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                            self.find_length_of_track()
                            pygame.mixer.music.set_endevent(MUSIC_END_2)

                        if event.type == MUSIC_END_2:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[2])
                            pygame.mixer.music.play()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[2])
                            self.playing = 3
                            self.length = pygame.mixer.Sound(self.list_of_songs[2]).get_length()
                            self.find_length_of_track()
                            pygame.mixer.music.set_endevent(MUSIC_END_3)

                        if event.type == MUSIC_END_3:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[0])
                            pygame.mixer.music.play()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[0])
                            self.playing = 1
                            self.length = pygame.mixer.Sound(self.list_of_songs[0]).get_length()
                            self.find_length_of_track()
                            pygame.mixer.music.set_endevent(MUSIC_END_1)
                    self.root.after(100, check_event)

                if self.playing == 1:
                    pygame.mixer.music.set_endevent(MUSIC_END_1)
                elif self.playing == 2:
                    pygame.mixer.music.set_endevent(MUSIC_END_2)
                elif self.playing == 3:
                    pygame.mixer.music.set_endevent(MUSIC_END_3)

                check_event()
        except:
            pass

        self.start_or_pause_btn.config(image=self.pause_png, command=self.pause)
        self.replay_btn.config(image=self.replay_playlist_png, command=self.replay_off)

    def replay_off(self):
        try:
            if self.playing == 1:
                pygame.mixer.music.load(self.list_of_songs[0])
                pygame.mixer.music.play(0, start=self.val / 1000)
                pygame.mixer.music.set_endevent(0)
            elif self.playing == 2:
                if len(self.list_of_songs) == 2:
                    pygame.mixer.music.load(self.list_of_songs[1])
                    pygame.mixer.music.play(0, start=self.val / 1000)
                    pygame.mixer.music.set_endevent(0)
                elif len(self.list_of_songs) == 3:
                    pygame.mixer.music.load(self.list_of_songs[1])
                    pygame.mixer.music.play(0, start=self.val / 1000)

                    def check_event():
                        for event in pygame.event.get():
                            if event.type == MUSIC_END:
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load(self.list_of_songs[2])
                                pygame.mixer.music.play()
                                self.playing = 3
                                self.length = pygame.mixer.Sound(self.list_of_songs[2]).get_length()
                                self.find_length_of_track()
                                self.track_name_on_screen.configure(text=self.list_of_songs_names[2])
                        self.root.after(100, check_event)

                    MUSIC_END = pygame.USEREVENT + 1
                    pygame.mixer.music.set_endevent(MUSIC_END)

                    check_event()
            else:
                pygame.mixer.music.load(self.list_of_songs[2])
                pygame.mixer.music.play(0, start=self.val / 1000)
                pygame.mixer.music.set_endevent(0)
        except:
            pass
        else:
            self.start_or_pause_btn.config(image=self.pause_png, command=self.pause)
            self.replay_btn.config(image=self.replay_off_png, command=self.replay_on)

    def scale_volume_height(self, val):
        try:
            pygame.mixer.music.set_volume(float(val) / 100)
        except:
            pass

    def volume_mute(self):
        try:
            pygame.mixer.music.set_volume(0.0)
            self.scale.configure(value=0)
        except:
            pass

    def volume_average(self):
        try:
            pygame.mixer.music.set_volume(0.5)
            self.scale.configure(value=50)
        except:
            pass

    def volume_100(self):
        try:
            pygame.mixer.music.set_volume(1.0)
            self.scale.configure(value=100)
        except:
            pass

    def track_playing(self):
        

    def playlist_open(self):
        """ Говноед не ленись и создай отдельный children-класс для создания окна поверх существующего
        edit: не работает ниче уже написано говняно"""

        # Creating window filled with playlist_of_tracks
        self.window = Toplevel()
        self.window.title('Playlist')
        self.window.iconphoto(False, PhotoImage(file='icon.png'))
        self.window.configure(bg='#38383C')
        self.window.geometry('450x150+{}+{}'.format(self.w, self.h))
        self.window.resizable(False, False)
        self.window.update()

        # Creating buttons with NAME=track_name(DOUBLE CLICK=PLAY CURRENT TRACK; RIGHT SIDE = DELETE FROM PLAYLIST)
        # NEED TO CREATE TRY-EXCEPT METHODS
        try:

            self.delete_png = PhotoImage(file='cancel.png').subsample(18)
            # 1
            self.btn_first = Button(master=self.window, bg='#38383C', borderwidth=1,
                                    text=self.list_of_songs_names[0], font=('Algerian', 14), justify=CENTER,
                                    activebackground='#5D5D65',
                                    command=self.play_first)
            self.btn_first.place(relx=0.5, rely=0.1, anchor=CENTER)

            self.btn_first_cancel = Button(master=self.window, bg='#38383C', borderwidth=0, image=self.delete_png,
                                           activebackground='#5D5D65',
                                           command=self.delete_first_track_from_playlist)
            self.btn_first_cancel.place(relx=0.9, rely=0.1, anchor=CENTER)

            # 2
            self.btn_second = Button(master=self.window, bg='#38383C', borderwidth=1,
                                     text=self.list_of_songs_names[1], font=('Algerian', 14), justify=CENTER,
                                     activebackground='#5D5D65',
                                     command=self.play_second)
            self.btn_second.place(relx=0.5, rely=0.5, anchor=CENTER)

            self.btn_second_cancel = Button(master=self.window, bg='#38383C', borderwidth=0, image=self.delete_png,
                                            activebackground='#5D5D65',
                                            command=self.delete_second_from_playlist)
            self.btn_second_cancel.place(relx=0.9, rely=0.5, anchor=CENTER)

            # 3
            self.btn_third = Button(master=self.window, bg='#38383C', borderwidth=1,
                                    text=self.list_of_songs_names[2], font=('Algerian', 14), justify=CENTER,
                                    activebackground='#5D5D65',
                                    command=self.play_third)
            self.btn_third.place(relx=0.5, rely=0.9, anchor=CENTER)

            self.btn_third_cancel = Button(master=self.window, bg='#38383C', borderwidth=0, image=self.delete_png,
                                           activebackground='#5D5D65',
                                           command=self.delete_third_from_playlist)
            self.btn_third_cancel.place(relx=0.9, rely=0.9, anchor=CENTER)
        except:
            pass

    def delete_first_track_from_playlist(self):
        try:
            self.replay_off()
            if len(self.list_of_songs) == 1:
                pygame.mixer.music.unload()
                self.track_name_on_screen.configure(text='')
                del self.list_of_songs[0]
                del self.list_of_songs_names[0]
                self.btn_first.place_forget()
                self.btn_first_cancel.place_forget()
                self.window.update_idletasks()
                self.stop()
            if len(self.list_of_songs) > 1:
                pygame.mixer.music.unload()
                del self.list_of_songs[0]
                del self.list_of_songs_names[0]
                self.track_name_on_screen.configure(text=self.list_of_songs_names[0])
                self.btn_first.place_forget()
                self.btn_first_cancel.place_forget()
                if self.playing == 1:
                    if len(self.list_of_songs) == 1:
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load(self.list_of_songs[0])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(self.list_of_songs[0])
                        pygame.mixer.music.play()
                        self.playing = 1
                        self.length = pygame.mixer.Sound(self.list_of_songs[0]).get_length()
                        self.find_length_of_track()

                        def check_event():
                            """ Function check events in pygame.event list(?), and if the events was already done, will
                            start to do some command you have ever code """
                            for event in pygame.event.get():
                                if event.type == MUSIC_END:
                                    pygame.mixer.music.unload()
                                    pygame.mixer.music.load(self.list_of_songs[1])
                                    pygame.mixer.music.play()
                                    self.playing = 2
                                    self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                                    self.find_length_of_track()
                                    self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                                    pygame.mixer.music.set_endevent(0)
                            self.root.after(100, check_event)

                        MUSIC_END = pygame.USEREVENT + 1

                        pygame.mixer.music.set_endevent(MUSIC_END)

                        check_event()

            if len(self.list_of_songs) == 0:
                self.stop()
        except:
            pass

    def delete_second_from_playlist(self):
        try:
            self.replay_off()
            if len(self.list_of_songs) == 1:
                del self.list_of_songs[0]
                del self.list_of_songs_names[0]
                self.btn_second.place_forget()
                self.btn_second_cancel.place_forget()
                self.track_name_on_screen.configure(text='')
                self.window.update_idletasks()
                self.stop()
            elif len(self.list_of_songs) > 1:
                del self.list_of_songs[1]
                del self.list_of_songs_names[1]
                self.btn_second.place_forget()
                self.btn_second_cancel.place_forget()
                self.window.update_idletasks()
                if self.playing == 2:
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(self.list_of_songs[1])
                    pygame.mixer.music.play()
                    self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                if len(self.list_of_songs) == 0:
                    self.stop()
        except:
            pass

    def delete_third_from_playlist(self):
        try:
            self.replay_off()
            if len(self.list_of_songs) == 1:
                del self.list_of_songs[0]
                del self.list_of_songs_names[0]
                self.btn_third.place_forget()
                self.btn_third_cancel.place_forget()
                self.track_name_on_screen.configure(text='')
                self.stop()
            elif len(self.list_of_songs) > 1:
                del self.list_of_songs[2]
                del self.list_of_songs_names[2]
                self.btn_third.place_forget()
                self.btn_third_cancel.place_forget()
                self.window.update_idletasks()
                if self.playing == 3:
                    pygame.mixer.music.unload()
                if len(self.list_of_songs) == 0:
                    self.stop()

        except:
            pass

    # PREVIOUS BUTTON
    def prev(self, event):
        try:
            if self.playing <= 1:
                pass
            elif self.playing == 2:
                self.play_first()
            else:
                self.play_second()
        except:
            pass

    def reach_for_begining(self):
        try:
            pygame.mixer.music.set_pos(0)
        except:
            pass

    # NEXT BUTTON
    def next_track(self):
        try:
            pygame.mixer.music.set_pos(self.length)
        except:
            pass

    # PLAYING TRACK FROM PLAYLIST WINDOW
    def play_first(self):
        try:
            if len(self.list_of_songs) == 1:
                pygame.mixer.music.load(self.list_of_songs[0])
                pygame.mixer.music.play()
                self.track_name_on_screen.configure(text=self.list_of_songs_names[0])

                self.replay_btn.config(image=self.replay_off_png, command=self.replay_on)
                self.window.update_idletasks()
            if len(self.list_of_songs) == 2:
                self.track_name_on_screen.configure(text=self.list_of_songs_names[0])
                pygame.mixer.music.load(self.list_of_songs[0])
                pygame.mixer.music.play()
                self.playing = 1
                self.length = pygame.mixer.Sound(self.list_of_songs[0]).get_length()
                self.find_length_of_track()

                def check_event():
                    """ Function check events in pygame.event list(?), and if the events was already done, will
                    start to do some command you have ever code """
                    for event in pygame.event.get():
                        if event.type == MUSIC_END:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[1])
                            pygame.mixer.music.play()
                            self.playing = 2
                            self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                            self.find_length_of_track()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                            pygame.mixer.music.set_endevent(0)
                    self.root.after(100, check_event)

                MUSIC_END = pygame.USEREVENT + 1

                pygame.mixer.music.set_endevent(MUSIC_END)

                check_event()
                self.replay_btn.config(image=self.replay_off_png, command=self.replay_on)
                self.window.update_idletasks()
            if len(self.list_of_songs) == 3:
                pygame.mixer.music.load(self.list_of_songs[0])
                pygame.mixer.music.play()
                self.playing = 1
                self.length = pygame.mixer.Sound(self.list_of_songs[0]).get_length()
                self.find_length_of_track()
                self.track_name_on_screen.configure(text=self.list_of_songs_names[0])
                self.window.update_idletasks()

                def check_event():
                    """ Function check events in pygame.event list(?), and if the events was already done, will
                    start to do some command you have ever code """
                    for event in pygame.event.get():
                        if event.type == MUSIC_END:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[1])
                            pygame.mixer.music.play()
                            self.playing = 2
                            self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                            self.find_length_of_track()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                            pygame.mixer.music.set_endevent(MUSIC_END_2)
                        if event.type == MUSIC_END_2:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[2])
                            pygame.mixer.music.play()
                            self.playing = 3
                            self.length = pygame.mixer.Sound(self.list_of_songs[2]).get_length()
                            self.find_length_of_track()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[2])
                            pygame.mixer.music.set_endevent(0)
                    self.root.after(100, check_event)

                MUSIC_END = pygame.USEREVENT + 1
                MUSIC_END_2 = pygame.USEREVENT + 2

                pygame.mixer.music.set_endevent(MUSIC_END)

                check_event()
                self.replay_btn.config(image=self.replay_off_png, command=self.replay_on)
                self.window.update_idletasks()
        except:
            pass

    def play_second(self):
        try:
            if len(self.list_of_songs) == 2:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(self.list_of_songs[1])
                pygame.mixer.music.play()
                self.playing = 2
                self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                self.find_length_of_track()
                self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                self.window.update_idletasks()
            if len(self.list_of_songs) == 3:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(self.list_of_songs[1])
                pygame.mixer.music.play()
                self.playing = 2
                self.length = pygame.mixer.Sound(self.list_of_songs[1]).get_length()
                self.find_length_of_track()
                self.track_name_on_screen.configure(text=self.list_of_songs_names[1])

                def check_event():
                    for event in pygame.event.get():
                        if event.type == MUSIC_END:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(self.list_of_songs[2])
                            pygame.mixer.music.play()
                            self.playing = 3
                            self.length = pygame.mixer.Sound(self.list_of_songs[2]).get_length()
                            self.find_length_of_track()
                            self.track_name_on_screen.configure(text=self.list_of_songs_names[2])
                            pygame.mixer.music.set_endevent(0)
                    self.root.after(100, check_event)

                MUSIC_END = pygame.USEREVENT + 1
                pygame.mixer.music.set_endevent(MUSIC_END)

                check_event()
                self.track_name_on_screen.configure(text=self.list_of_songs_names[1])
                self.replay_btn.config(image=self.replay_off_png, command=self.replay_on)
        except:
            pass

    def play_third(self):
        try:
            self.replay_off()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.list_of_songs[2])
            pygame.mixer.music.play()
            self.playing = 3
            self.length = pygame.mixer.Sound(self.list_of_songs[2]).get_length()
            self.find_length_of_track()
            self.track_name_on_screen.configure(text=self.list_of_songs_names[2])

            def check_event():
                for event in pygame.event.get():
                    if event.type == MUSIC_END:
                        pygame.mixer.music.pause()
                self.root.after(100, check_event)

            MUSIC_END = pygame.USEREVENT + 1
            pygame.mixer.music.set_endevent(MUSIC_END)

            check_event()
            self.window.update_idletasks()
            self.replay_btn.config(image=self.replay_off_png, command=self.replay_on)

        except:
            pass


''' Нужно доделать:
1. Реплей плейлиста - СДЕЛАНО 
2. Полоска момента времени в треке
3. Фронтить
4. Кнопка возврата из окна плейлиста
5. Не работает удаление 1 --> 2.  '''

MP3()
