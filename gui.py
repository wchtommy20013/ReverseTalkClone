from Tkinter import *
from main import *
from datetime import datetime
from pydub.playback import play

recording = False
recorder = Recorder()
start_time = time.localtime()

map = []


class Application(Frame):

    def popup_no_last(self):
        win = Toplevel()
        win.wm_title("Window")

        l = Label(win, text="No Record")
        l.grid(row=0, column=0)

        b = Button(win, text="Ok", command=win.destroy)
        b.grid(row=1, column=0)

    def reset_timer(self):
        global start_time
        start_time = time.localtime()
        self.label1.config(text="00:00:00", font='times 25')

    def start_record(self):
        global recorder, recordfile, recording, start_time
        if not recording:
            recordfile = recorder.open()
            recording = True
            self.reset_timer()
            recordfile.start_recording()
            return
        pass

    def stop_record(self):
        global recorder, recordfile, recording, map

        print recorder.fname

        recording = False
        recordfile.stop_recording()
        recordfile.export_reverse()

        map.append(recordfile.get_name_normal())
        recordfile.close()
        return
        pass

    def clock(self):
        global start_time, recording

        if recording:
            t1 = time.strftime('%H:%M:%S', time.localtime())
            t2 = time.strftime('%H:%M:%S', start_time)
            t = datetime.strptime(t1, '%H:%M:%S') - datetime.strptime(t2, '%H:%M:%S')
            if t != '':
                self.label1.config(text=t, font='times 25')

        self.after(1000, self.clock)



    def __play(self, index, reverse = False):
        global map
        try:
            if not recording:
                f = map[index]
                if reverse:
                    f = "reverse_" + f
                sound = AudioSegment.from_file(f, format="wav")
                play(sound)
        except IndexError:
            self.popup_no_last()

    def play_last_normal(self):
        self.__play(-2)

    def play_last_reverse(self):
        self.__play(-2, True)

    def play_normal(self):
        print map
        self.__play(-1)

    def play_reverse(self):
        self.__play(-1, True)

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "right"})

        self.start = Button(self)
        self.start["text"] = "Start",
        self.start["command"] = self.start_record

        self.stop = Button(self)
        self.stop["text"] = "Stop",
        self.stop["command"] = self.stop_record

        self.play = Button(self)
        self.play["text"] = "Play Normal"
        self.play["command"] = self.play_normal

        self.play_re = Button(self)
        self.play_re["text"] = "Play Reverse"
        self.play_re["command"] = self.play_reverse

        self.play_last = Button(self)
        self.play_last["text"] = "Play Last Normal"
        self.play_last["command"] = self.play_last_normal

        self.play_last_re = Button(self)
        self.play_last_re["text"] = "Play Last Reverse"
        self.play_last_re["command"] = self.play_last_reverse

        self.label1 = Label(self, justify='center')
        self.label1.pack({"side": "left"})
        self.reset_timer()
        self.clock()

        self.start.pack({"side": "left"})
        self.stop.pack({"side": "left"})
        self.play.pack({"side": "left"})
        self.play_re.pack({"side": "left"})
        self.play_last.pack({"side": "left"})
        self.play_last_re.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
