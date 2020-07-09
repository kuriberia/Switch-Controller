import sys, serial
import datetime
import tkinter
import tkinter.scrolledtext
from tkinter import ttk
from ttkthemes import themed_tk
import threading

import sender

class Application(ttk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.GUI()
        sys.stdout = self.StdoutRedirector(self.out)
        sys.stderr = self.StderrRedirector(self.out)
        self.ser = serial.Serial("/dev/ttyS7", 9600)
        self.sender = sender.Sender(self.ser)
        self.start_time = datetime.datetime.now()

        master.title("Pokémon SWSH Macro Contoller")
        master.resizable(False, False)
        master['bg'] = "white smoke"

    class IORedirector(object):
        def __init__(self, out):
            self.out = out

    class StdoutRedirector(IORedirector):
        def write(self, st):
            self.out.insert(tkinter.INSERT, st)
            self.out.see("end")

    class StderrRedirector(IORedirector):
        def write(self, st):
            self.out.insert(tkinter.INSERT, st)
            self.out.see("end")

    def GUI(self):
        style = ttk.Style()
        style.configure("BW.TFrame", foreground="black", background="white")
        self.radio_var = tkinter.IntVar()
        self.radio_var.set(0)

        f1 = ttk.LabelFrame(self.master, text="周回")
        f1.grid(column=0, row=0, padx=5, pady=5, sticky=tkinter.NSEW, rowspan=2)
        f2 = ttk.LabelFrame(self.master, text="便利")
        f2.grid(column=1, row=1, padx=5, pady=5, sticky=tkinter.NS + tkinter.EW)
        f3 = ttk.LabelFrame(self.master, text="乱数調整")
        f3.grid(column=1, row=0, padx=5, pady=5, sticky=tkinter.EW, columnspan=2)
        f4 = ttk.LabelFrame(self.master, text="コントローラー")
        f4.grid(column=1, row=2, padx=5, pady=5, sticky=tkinter.EW, columnspan=2)
        f5 = ttk.LabelFrame(self.master, text="実行")
        f5.grid(column=2, row=1, padx=5, pady=5, sticky=tkinter.N + tkinter.EW)
        f6 = ttk.LabelFrame(self.master, text="出力")
        f6.grid(column=0, row=2, padx=5, pady=5, sticky=tkinter.EW)
        # 周回
        ttk.Radiobutton(f1, text="バトルタワー", width=10, value=1, variable=self.radio_var).grid(column=0, row=0, padx=5, pady=5)
        ttk.Radiobutton(f1, text="トーナメント", width=10, value=2, variable=self.radio_var).grid(column=0, row=1, padx=5, pady=5)
        ttk.Radiobutton(f1, text="穴掘り", width=10, value=3, variable=self.radio_var).grid(column=0, row=2, padx=5, pady=5)
        ttk.Radiobutton(f1, text="化石復元", width=10, value=4, variable=self.radio_var).grid(column=0, row=3, padx=5, pady=5)
        self.kaseki_num = tkinter.IntVar()
        tkinter.Spinbox(f1, textvariable=self.kaseki_num, from_=1, to=50, increment=1, width=3).grid(column=1, row=3, padx=5, pady=5)
        ttk.Label(f1, text="個", width=3).grid(column=2, row=3, padx=5, pady=5, sticky=tkinter.W)
        self.kaseki_type = tkinter.StringVar()
        kaseki_list = ["パッチラゴン", "ウオノラゴン", "パッチルドン", "ウオチルドン"]
        combobox_kaseki = ttk.Combobox(f1, textvariable=self.kaseki_type, values=kaseki_list, width=8, state="readonly")
        combobox_kaseki.current(0)
        combobox_kaseki.grid(column=3, row=3, padx=5, pady=5, columnspan=2)
        ttk.Radiobutton(f1, text="IDくじ", width=10, value=5, variable=self.radio_var).grid(column=0, row=4, padx=5, pady=5)
        ttk.Radiobutton(f1, text="ワット", width=10, value=6, variable=self.radio_var).grid(column=0, row=5, padx=5, pady=5)
        ttk.Radiobutton(f1, text="ポケジョブ", width=10, value=7, variable=self.radio_var).grid(column=0, row=6, padx=5, pady=5)
        self.pokejob_num = tkinter.IntVar()
        self.pokejob_days = tkinter.IntVar()
        tkinter.Spinbox(f1, textvariable=self.pokejob_num, from_=1, to=6, increment=1, wrap=True, width=3).grid(column=1, row=6, padx=5, pady=5)
        tkinter.Spinbox(f1, textvariable=self.pokejob_days, from_=1, to=27, increment=1, width=3).grid(column=3, row=6, padx=5, pady=5)
        ttk.Label(f1, text="匹", width=3).grid(column=2, row=6, padx=5, pady=5, sticky=tkinter.W)
        ttk.Label(f1, text="日間", width=4).grid(column=4, row=6, padx=5, pady=5, sticky=tkinter.W)
        ttk.Radiobutton(f1, text="掘り出し物市", width=10, value=15, variable=self.radio_var).grid(column=0, row=7, padx=5, pady=5)
        # 便利
        ttk.Radiobutton(f2, text="再起動", width=10, value=8, variable=self.radio_var).grid(column=0, row=0, padx=5, pady=5)
        ttk.Radiobutton(f2, text="レポート", width=10, value=9, variable=self.radio_var).grid(column=0, row=1, padx=5, pady=5)
        ttk.Radiobutton(f2, text="バックアップ", width=10, value=17, variable=self.radio_var).grid(column=0, row=2, padx=5, pady=5)
        # 乱数調整
        ttk.Radiobutton(f3, text="1日進める", width=10, value=10, variable=self.radio_var).grid(column=0, row=0, padx=5, pady=5)
        ttk.Radiobutton(f3, text="n日進める", width=10, value=11, variable=self.radio_var).grid(column=0, row=1, padx=5, pady=5)
        self.spin_days = tkinter.IntVar()
        self.spin_days.set(3) # initial value
        tkinter.Spinbox(f3, textvariable=self.spin_days, from_=1, to=30, increment=1, width=3).grid(column=1, row=1, padx=5, pady=5, sticky=tkinter.W)
        ttk.Label(f3, text="日", width=2).grid(column=2, row=1, padx=5, pady=5, sticky=tkinter.W)
        ttk.Radiobutton(f3, text="フレーム消費", width=10, value=12, variable=self.radio_var).grid(column=0, row=2, padx=5, pady=5)
        self.spin_frame = tkinter.IntVar()
        tkinter.Spinbox(f3, textvariable=self.spin_frame, from_=1, to=10000, increment=1, width=6).grid(column=1, row=2, padx=5, pady=5, sticky=tkinter.W, columnspan=2)
        ttk.Label(f3, text="F", width=2).grid(column=3, row=2, padx=5, pady=5, sticky=tkinter.W)
        ttk.Radiobutton(f3, text="固定厳選", width=10, value=13, variable=self.radio_var).grid(column=0, row=3, padx=5, pady=5)
        self.spin_kotei = tkinter.IntVar()
        self.spin_kotei.set(3) # initial value
        tkinter.Spinbox(f3, textvariable=self.spin_kotei, from_=1, to=30, increment=1, width=3).grid(column=1, row=3, padx=5, pady=5, sticky=tkinter.W)
        ttk.Label(f3, text="日", width=2).grid(column=2, row=3, padx=5, pady=5, sticky=tkinter.W)
        ttk.Radiobutton(f3, text="Seed厳選", width=10, value=14, variable=self.radio_var).grid(column=0, row=4, padx=5, pady=5)
        ttk.Radiobutton(f3, text="日付リセット", width=10, value=16, variable=self.radio_var).grid(column=0, row=5, padx=5, pady=5)
        self.reset_type = tkinter.StringVar()
        reset_list = ["日付のみ", "日付&時間"]
        combobox_reset = ttk.Combobox(f3, textvariable=self.reset_type, values=reset_list, width=8, state="readonly")
        combobox_reset.current(1)
        combobox_reset.grid(column=1, row=5, padx=5, pady=5, columnspan=3, sticky=tkinter.W)
        # コントローラー
        up = ttk.Button(f4, text="↑", width=2)
        up.bind("<ButtonPress>", lambda e:self.stick_on("u"))
        up.bind("<ButtonRelease>", lambda e:self.stick_off())
        up.grid(column=1, row=0, padx=5, pady=5)
        down = ttk.Button(f4, text="↓", width=2)
        down.bind("<ButtonPress>", lambda e:self.stick_on("d"))
        down.bind("<ButtonRelease>", lambda e:self.stick_off())
        down.grid(column=1, row=2, padx=5, pady=5)
        right = ttk.Button(f4, text="→", width=2)
        right.bind("<ButtonPress>", lambda e:self.stick_on("r"))
        right.bind("<ButtonRelease>", lambda e:self.stick_off())
        right.grid(column=2, row=1, padx=5, pady=5)
        left = ttk.Button(f4, text="←", width=2)
        left.bind("<ButtonPress>", lambda e:self.stick_on("l"))
        left.bind("<ButtonRelease>", lambda e:self.stick_off())
        left.grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(f4, text="A", width=2, command=lambda:self.button_ctrl("a")).grid(column=5, row=1, padx=5, pady=5)
        ttk.Button(f4, text="B", width=2, command=lambda:self.button_ctrl("b")).grid(column=4, row=2, padx=5, pady=5)
        ttk.Button(f4, text="X", width=2, command=lambda:self.button_ctrl("x")).grid(column=4, row=0, padx=5, pady=5)
        ttk.Button(f4, text="Y", width=2, command=lambda:self.button_ctrl("y")).grid(column=3, row=1, padx=5, pady=5)
        ttk.Button(f4, text="L", width=2, command=lambda:self.button_ctrl("l1")).grid(column=0, row=0, padx=5, pady=5)
        ttk.Button(f4, text="R", width=2, command=lambda:self.button_ctrl("r1")).grid(column=5, row=0, padx=5, pady=5)
        ttk.Button(f4, text="HOME", width=5, command=lambda:self.button_ctrl("h")).grid(column=2, row=2, padx=5, pady=5, columnspan=2)
        ttk.Button(f4, text="＋", width=2, command=lambda:self.button_ctrl("p")).grid(column=3, row=0, padx=5, pady=5)
        ttk.Button(f4, text="－", width=2, command=lambda:self.button_ctrl("m")).grid(column=2, row=0, padx=5, pady=5)
        # 実行
        ttk.Button(f5, text="実行", width=10, command=self.button_exec).grid(column=0, row=0, padx=5, pady=5)
        ttk.Button(f5, text="中止", width=10, command=self.button_stop).grid(column=0, row=1, padx=5, pady=5)

        self.out = tkinter.scrolledtext.ScrolledText(f6, height=6, width=40)
        self.out.grid(column=0, row=0, padx=5, pady=5)

    def button_ctrl(self, cmd):
        self.sender.onFlag()
        self.sender.controller(cmd)

    def stick_on(self, cmd):
        self.sender.onFlag()
        now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        if cmd == "u":
            self.ser.write(b'LY MIN\r\n')
            print(f'[{now}] LY MIN')
        elif cmd == "d":
            self.ser.write(b'LY MAX\r\n')
            print(f'[{now}] LY MAX')
        elif cmd == "r":
            self.ser.write(b'LX MAX\r\n')
            print(f'[{now}] LX MAX')
        elif cmd == "l":
            self.ser.write(b'LX MIN\r\n')
            print(f'[{now}] LX MIN')

    def stick_off(self):
        self.ser.write(b'RELEASE\r\n')

    def button_exec(self):
        if not self.sender.getEndFlag():
            print("コマンド終了待ちのため、実行できません")
            return
        print("[Start] " , end="")
        self.sender.onFlag()
        self.start_time = datetime.datetime.now()
        num = self.radio_var.get()
        if num == 1:
            print("バトルタワー")
            th = threading.Thread(target=self.sender.battletower)
            th.setDaemon(True)
            th.start()
        elif num == 2:
            print("トーナメント")
            th = threading.Thread(target=self.sender.tournament)
            th.setDaemon(True)
            th.start()
        elif num == 3:
            print("穴掘り")
            th = threading.Thread(target=self.sender.anahori)
            th.setDaemon(True)
            th.start()
        elif num == 4:
            print("化石復元")
            th = threading.Thread(target=self.sender.kaseki, args=(self.kaseki_num.get(), self.kaseki_type.get(),))
            th.setDaemon(True)
            th.start()
        elif num == 5:
            print("IDくじ")
            th = threading.Thread(target=self.sender.idkuji)
            th.setDaemon(True)
            th.start()
        elif num == 6:
            print("ワット")
            th = threading.Thread(target=self.sender.watt)
            th.setDaemon(True)
            th.start()
        elif num == 7:
            print("ポケジョブ")
            th = threading.Thread(target=self.sender.pokejob, args=(self.pokejob_num.get(), self.pokejob_days.get(),))
            th.setDaemon(True)
            th.start()
        elif num == 8:
            print("再起動")
            th = threading.Thread(target=self.sender.restart)
            th.setDaemon(True)
            th.start()
        elif num == 9:
            print("レポート")
            th = threading.Thread(target=self.sender.report)
            th.setDaemon(True)
            th.start()
        elif num == 10:
            print("1日進める")
            th = threading.Thread(target=self.sender.one_day)
            th.setDaemon(True)
            th.start()
        elif num == 11:
            print("n日進める")
            th = threading.Thread(target=self.sender.n_days, args=(self.spin_days.get(),))
            th.setDaemon(True)
            th.start()
        elif num == 12:
            print("フレーム消費")
            th = threading.Thread(target=self.sender.shohi, args=(self.spin_frame.get(),))
            th.setDaemon(True)
            th.start()
        elif num == 13:
            print("固定厳選")
            th = threading.Thread(target=self.sender.kotei_gensen, args=(self.spin_kotei.get(),))
            th.setDaemon(True)
            th.start()
        elif num == 14:
            print("seed厳選")
            th = threading.Thread(target=self.sender.seed)
            th.setDaemon(True)
            th.start()
        elif num == 15:
            print("掘り出し物市")
            th = threading.Thread(target=self.sender.horidasi)
            th.setDaemon(True)
            th.start()
        elif num == 16:
            print("日付リセット")
            th = threading.Thread(target=self.sender.setfirst, args=(self.reset_type.get(),))
            th.setDaemon(True)
            th.start()
        elif num == 17:
            print("バックアップ")
            th = threading.Thread(target=self.sender.backup)
            th.setDaemon(True)
            th.start()

    def button_stop(self):
        self.sender.offFlag() # コマンドを中止
        self.stick_off() # スティック・ボタンをRELEASE
        if self.sender.getEndFlag():
            print("実行中のコマンドはありません")
        else:
            exec_time = datetime.datetime.now() - self.start_time
            print("[中止] 実行時間:", exec_time)

def main():
    root = themed_tk.ThemedTk()
    # root = tkinter.Tk()
    root.get_themes()
    root.set_theme("arc")
    # icon = 'icon/482azelf.png'
    icon = 'icon/preciousball.png'
    # icon = 'icon/premiereball.png'
    root.iconphoto(True, tkinter.PhotoImage(file=icon))
    app = Application(root)
    app.mainloop()

if __name__ == "__main__":
    main()
