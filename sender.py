import serial
import datetime, calendar
from time import sleep

class Sender:
    def __init__(self, ser):
        self.ser = ser
        self.continueFlag = True # 「中止」が押されたらすぐに止めるため
        self.endFlag = True # コマンド実行中に他のコマンドを送らないようにするため
        self.switch_day = -1 # Switchの日付を記録 初期値は-1
        self.reset_timestamp = datetime.datetime.now() # 最後に日付をリセットした時間

    def send(self, msg, duration=0, slp=0, prt=True):
        """
        Switchにコマンドを送る。

        Parameters
        ----------
        msg : string
            送るコマンド
        duration : int
            ボタンを押し続ける秒数
        slp : int
            ボタンを離したあと待機する秒数
        prt : Bool
            送ったコマンドを標準出力するかどうか
        """
        if self.continueFlag:
            now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            if prt:
                print("[{}] {}".format(now, msg))
            self.ser.write(f'{msg}\r\n'.encode('utf-8'))
            sleep(duration)
            self.ser.write(b'RELEASE\r\n')
            sleep(slp)

    def send_hold(self, msg, duration=0, slp=0, prt=True):
        """
        Switchにコマンドを記憶させる。
        送ったコマンドがスティック操作の場合はRELEASEされるまで固定される。

        Parameters
        ----------
        msg : string
            送るコマンド
        duration : int
            ボタンを押し続ける秒数
        slp : int
            ボタンを離したあと待機する秒数
        prt : Bool
            送ったコマンドを標準出力するかどうか
        """
        if self.continueFlag:
            now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            if prt:
                print("[{}] {}".format(now, msg))
            self.ser.write(f'{msg}\r\n'.encode('utf-8'))
            sleep(duration)
            self.ser.write(b'HOLD_RE\r\n')
            sleep(slp)

    def onFlag(self):
        """
        continueFlagをTrueにする。
        """
        self.continueFlag = True

    def offFlag(self):
        """
        continueFlagをFalseにする。
        これによってコマンドを送らないようにできる。
        """
        self.continueFlag = False

    def getEndFlag(self):
        """
        endFlagを返す。
        コマンドが終了しているかどうかを判定できる。

        Returns
        -------
        endFlag : Bool
            コマンドが終了していればTrue
            実行中ならFalse
        """
        return self.endFlag

    def battletower(self): # バトルタワー
        """
        コマンド「バトルタワー」を実行する。
        バトルタワーでBPを無限回収する。
        """
        self.endFlag = False
        while self.continueFlag:
            self.send('Button A', 0.1, 0.8, False)
            self.send('Button A', 0.1,  15, False) # 0.8-14=32=29.5 # 0.8-15=30.8 16=29.6 17=29.3
            self.send('Button A', 0.1, 0.8, False)
            self.send('Button A', 0.1, 0.8, False)
            self.send('LY MIN',   0.1, 0.8, False)
            self.send('Button A', 0.1, 0.8, False)
            self.send('Button A', 0.1, 0.8, False)
            self.send('LY MIN',   0.1, 0.8, False)
            self.send('Button A', 0.1, 0.8, False)
            self.send('Button A', 0.1, 0.8, False)
            self.send('Button A', 0.1,  15, False)
            self.send('Button A', 0.1, 0.8, False)
            self.send('Button A', 0.1, 0.8, False)
            self.send('Button B', 0.1, 0.8, False)
            self.send('Button B', 0.1, 0.8, False)
            self.send('LY MIN',   0.1, 0.8, False)
        print("[End] バトルタワー")
        self.endFlag = True

    def tournament(self): # トーナメント
        """
        コマンド「トーナメント」を実行する。
        ポケモンリーグのトーナメントを周回する。
        手持ちはザシアン1体にしておく。
        実行中は左スティックが右斜め上に固定される。
        """
        self.endFlag = False
        self.send_hold('HOLD_LX 170', 0.1, 0)
        self.send_hold('HOLD_LY MIN', 0.1, 0)
        while self.continueFlag:
            self.send_hold('Button A', 0.1, 0.3, False)
            self.send_hold('Button A', 0.1, 0.3, False)
            self.send_hold('Button A', 0.1, 0.3, False)
            self.send_hold('Button A', 0.1, 0.3, False)
            self.send_hold('Button A', 0.1, 0.4, False)
            self.send_hold('Button B', 0.1, 0.4, False)
            self.send_hold('Button A', 0.1, 0.3, False)
            self.send_hold('Button A', 0.1, 0.3, False)
            self.hold_day()
            self.endFlag = False
        print("[End] トーナメント")
        self.endFlag = True

    def hold_day(self):
        dt_now = datetime.datetime.now()
        elapsed_time = dt_now - self.reset_timestamp
        if elapsed_time.seconds // 3600 >= 6: # 6時間以上経過したら
            print("日付をリセットします")
            self.send('RELEASE')
            self.switch_day = -1
            self.setfirst()
            self.reset_timestamp = dt_now
            self.send_hold('Button A', 0.1, 0.5)
            self.send_hold('Button A', 0.1, 0.5)
            self.send_hold('Button A', 0.1, 0.5)
            self.send_hold('HOLD_LX 170', 0.1, 0)
            self.send_hold('HOLD_LY MIN', 0.1, 0)

    def anahori(self): # 穴掘り
        """
        コマンド「穴掘り」を実行する。
        Aボタンを連打するだけ。
        """
        self.endFlag = False
        while self.continueFlag:
            self.send('Button A', 0.1, 0.35)
        print("[End] 穴掘り")
        self.endFlag = True

    def kaseki(self, num=1, kaseki="パッチラゴン"): # 化石掘り
        """
        コマンド「化石復元」を実行する。
        6番道路で指定の化石を指定の数だけ復元する。

        Parameters
        ----------
        num : int
            復元する化石の数
        kaseki : String
            復元する化石の種類(パッチラゴン、パッチルドン、ウオノラゴン、ウオチルドン)
        """
        self.endFlag = False
        print("{}を{}匹復元します".format(kaseki, num))
        cnt = 0
        while cnt < num and self.continueFlag:
            self.send('Button A', 0.1, 0.6, False)
            self.send('Button A', 0.1, 0.7, False)
            if kaseki == "ウオノラゴン" or kaseki == "ウオチルドン":
                self.send('LY MAX',   0.1, 0.1, False)
            self.send('Button A', 0.1, 0.7, False)
            if kaseki == "ウオチルドン" or kaseki == "パッチルドン":
                self.send('LY MAX',   0.1, 0.1, False)
            self.send('Button A', 0.1, 0.7, False)
            self.send('Button A', 0.1, 0.5, False)
            self.send('Button A', 0.1, 3.7, False)
            self.send('Button A', 0.1, 0.6, False)
            self.send('Button A', 0.1, 0.3, False)
            self.send('Button A', 0.1, 0.3, False)
            self.send('Button A', 0.1, 4.1, False)
            self.send('Button A', 0.1, 1.5, False)
            self.send('Button A', 0.1, 1.4, False)
            cnt += 1
            print(cnt)
        print("[End] 化石復元")
        self.endFlag = True

    def year(self):
        """
        ホームに戻り、1年戻して1年進める。
        ランクマバグを使用した状態でこの関数を実行するとIDくじが何度も引けるようになる。
        """
        if self.continueFlag:
            self.send('Button HOME', 0.1, 0.5) # ホームに戻る
            self.send('LY MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('Button A', 0.1, 0.15) # 設定を開く
            self.send('LY MAX',   1.8, 0.1)
            self.send('Button A', 0.1, 0.1) # 「本体」
            self.send('LY MAX',   0.04, 0.04)
            self.send('LY MAX',   0.04, 0.04)
            self.send('LY MAX',   0.04, 0.04)
            self.send('LY MAX',   0.04, 0.04)
            self.send('Button A', 0.1, 0.15) # 「日付と時刻」
            self.send('LY MAX',   0.04, 0.04)
            self.send('LY MAX',   0.04, 0.04)
            self.send('Button A', 0.1, 0.1) # 「現在の日付と時刻」
            self.send('LY MAX',   0.04, 0.04) # 1年戻す
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('Button A', 0.1, 0.1) # OK
            self.send('Button A', 0.1, 0.1) # 「現在の日付と時刻」
            self.send('LX MIN',   0.04, 0.04)
            self.send('LX MIN',   0.04, 0.04)
            self.send('LX MIN',   0.04, 0.04)
            self.send('LX MIN',   0.04, 0.04)
            self.send('LX MIN',   0.04, 0.04)
            self.send('LY MIN',   0.04, 0.04) # 1年進める
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('LX MAX',   0.04, 0.04)
            self.send('Button A', 0.1, 0.1) # OK
            self.send('Button HOME', 0.1, 0.5)
            self.send('Button HOME', 0.1, 0.8) # ゲームに戻る

    def rotomi(self):
        """
        IDくじを1回引く。
        ロトミの前で使用する。
        """
        if self.continueFlag:
            self.send('Button A', 0.1, 0.2) # ロトミ起動
            self.send('Button A', 0.1, 0.4)
            self.send('LY MAX',   0.1, 0.1)
            self.send('Button A', 0.1, 0.8) # IDくじ選択
            self.send('Button A', 0.1, 0.5)
            self.send('Button A', 0.1, 0.5)
            self.send('Button A', 0.1, 0.6)
            self.send('Button A', 0.1, 1.6) # レポートを書く
            self.send('Button A', 0.1, 0.5)
            self.send('Button A', 0.1, 0.7) # ..... ..... .....
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 2.3) # 抽選
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 2.5) # アイテム受け取り
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.5)
            self.send('Button A', 0.1, 0.4)

    def idkuji(self): # IDくじ
        """
        コマンド「IDくじ」を実行する。
        IDくじを無限に引く。
        ランクマバグを使用した状態でロトミの前で実行する。
        中止されるとくじを引いた回数を出力する。
        """
        self.endFlag = False
        cnt = 0
        while self.continueFlag:
            self.year()
            self.rotomi()
            cnt += 1
        print("Count :", cnt)
        print("[End] IDくじ")
        self.endFlag = True

    def watt(self): # ワット
        """
        コマンド「ワット」を実行する。
        ワットを無限に回収する。
        ランクマバグを使用した状態で願いのかたまりを使用した巣穴の前で使用する。
        中止されるとワットを受け取った回数を出力する。
        """
        self.endFlag = False
        cnt = 0
        while self.continueFlag:
            self.year()
            self.send('Button A', 0.1, 0.3) # ワット回収 「巣穴からエネルギーが少しだけでている！▼」
            self.send('Button B', 0.1, 0.3) # 「シベリアは1000W手に入れた！▼」
            self.send('Button B', 0.1, 0.6) # レイドが開く
            self.send('Button B', 0.1, 1.0) # レイド閉じる
            cnt += 1
        print("Count :", cnt)
        print("[End] ワット")
        self.endFlag = True

    def pokejob(self, poke=1, day=1): # ポケジョブ
        """
        コマンド「ポケジョブ」を実行する。
        指定した数のポケモンを指定の日数分ポケジョブでレベルを上げる。
        ランクマバグを使用した状態で、ロトミの前で実行する。
        育成したいポケモンをボックス1の一番上の行に左から置く。
        ポケジョブはリストの一番上のものを選ぶ。

        Parameters
        ----------
        poke : int
            育成したいポケモンの数(1～6)
        day : int
            育成する日数
        """
        self.endFlag = False
        if self.switch_day + day > 28 or self.switch_day == -1:
            print("実行前に日付をリセットします")
            self.setfirst()
        cnt = 0
        while cnt < day and self.continueFlag:
            self.send('Button A', 0.1, 0.2) # ロトミにアクセス
            self.send('Button A', 0.1, 0.3)
            self.send('LY MAX',   0.1, 0.1)
            self.send('LY MAX',   0.1, 0.1)
            self.send('Button A', 0.1, 2.8) # ポケジョブを開く
            self.send('Button A', 0.1, 0.2)
            self.send('Button A', 0.1, 0.3)
            self.send('Button A', 0.1, 0.3)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 1.2)
            self.send('Button Y', 0.1, 0.3)
            self.send('Button A', 0.1, 0.3) # ポケモンを選ぶ
            for _ in range(1, poke):
                self.send('LX MAX',   0.1, 0.1)
                self.send('Button A', 0.1, 0.1) # ポケモンを選ぶ 上限6匹
            self.send('Button B', 0.1, 0.4)
            self.send('Button A', 0.1, 2.1)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            print("いってらっしゃいムービー")
            self.send('Button A', 0.1, 9.5) # 1日で送り出す
            self.send('Button A', 0.1, 0.3)
            self.send('Button A', 0.1, 0.3)
            self.send('Button B', 0.1, 0.6)
            self.send('Button A', 0.1, 0.3)

            print("時渡り")
            self.send('Button HOME', 0.1, 0.5) # ホームに戻る
            self.send('LY MAX',   0.05, 0.05)
            self.send('LX MAX',   0.05, 0.05)
            self.send('LX MAX',   0.05, 0.05)
            self.send('LX MAX',   0.05, 0.05)
            self.send('LX MAX',   0.05, 0.05)
            self.send('Button A', 0.1, 0.2) # 設定を開く
            self.send('LY MAX',   1.8, 0.1)
            self.send('Button A', 0.1, 0.2) # 「本体」
            self.send('LY MAX',   0.05, 0.05)
            self.send('LY MAX',   0.05, 0.05)
            self.send('LY MAX',   0.05, 0.05)
            self.send('LY MAX',   0.05, 0.05)
            self.send('Button A', 0.1, 0.2) # 「日付と時刻」
            self.send('LY MAX',   0.05, 0.05)
            self.send('LY MAX',   0.05, 0.05)
            self.send('Button A', 0.1, 0.2) # 「現在の日付と時刻」
            self.send('LX MAX',   0.05, 0.05)
            self.send('LX MAX',   0.05, 0.05)
            self.send('LY MIN',   0.05, 0.05) # 1日進める
            self.send('LX MAX',   0.05, 0.05)
            self.send('LX MAX',   0.05, 0.05)
            self.send('LY MIN',   0.05, 0.05) # 1分進める
            self.send('LX MAX',   0.05, 0.05)
            self.send('Button A', 0.1, 0.2) # OK
            if self.continueFlag:
                self.switch_day += 1
            self.send('Button HOME', 0.1, 0.5)
            self.send('Button HOME', 0.1, 0.5) # ゲームに戻る

            # self.idkuji()

            self.send('Button A', 0.1, 0.2) # ロトミにアクセス
            self.send('Button A', 0.1, 0.3)
            self.send('LY MAX',   0.1, 0.1)
            self.send('LY MAX',   0.1, 0.1)
            self.send('Button A', 0.1, 3.0) # ポケジョブを開く
            self.send('Button A', 0.1, 0.4) # 新しいジョブがあります
            print("おかえりムービー")
            self.send('Button A', 0.1, 13.0)
            self.send('Button A', 0.1, 0.5)
            self.send('Button A', 0.1, 0.5)
            self.send('Button A', 0.1, 2.6)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button B', 0.1, 0.6) # 閉じる
            self.send('Button A', 0.1, 0.4)
            cnt += 1
        print("[End] ポケジョブ")
        self.endFlag = True

    def horidasi(self): # 掘り出し物市
        """
        コマンド「掘り出し物市」を実行する。
        ラテラルタウンの掘り出し物市で掘り出し物を買い続ける。
        ランクマバグを使用した状態で掘り出し物市の人の前で実行する。
        中止されると買った回数を出力する。
        """
        self.endFlag = False
        cnt = 0
        while self.continueFlag:
            self.year()
            self.send('Button A', 0.1, 0.5)
            self.send('Button A', 0.1, 0.7)
            self.send('Button A', 0.1, 0.6)
            self.send('Button A', 0.1, 2.2)
            self.send('Button A', 0.1, 2.4)
            self.send('Button A', 0.1, 0.4)
            self.send('Button A', 0.1, 1.1)
            self.send('Button B', 0.1, 0.4)
            self.send('Button B', 0.1, 0.5)
            self.send('Button A', 0.1, 0.5)
            cnt += 1
        print("Count :", cnt)
        print("[End] 掘り出し物市")
        self.endFlag = True

    def day(self, prt=False):
        """
        レイドを開いて1日進める。
        願いのかたまりを使用した巣穴の前で実行する。
        Switch dayを1進める。

        Parameters
        ----------
        prt : Bool
            送ったコマンドを標準出力するかどうか
        """
        if self.continueFlag:
            self.send('Button A', 0.1, 0.5, prt) # 巣穴を見る
            self.send('Button A', 0.1, 3.3, prt) # みんなで挑戦を選択
            self.send('Button HOME', 0.1, 0.5, prt) # ホームに戻る
            self.send('LY MAX',   0.04, 0.04, prt)
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('Button A', 0.1, 0.15, prt) # 設定を開く
            self.send('LY MAX',   1.8, 0.1, prt)
            self.send('Button A', 0.1, 0.1, prt) # 「本体」
            self.send('LY MAX',   0.04, 0.04, prt)
            self.send('LY MAX',   0.04, 0.04, prt)
            self.send('LY MAX',   0.04, 0.04, prt)
            self.send('LY MAX',   0.04, 0.04, prt)
            self.send('Button A', 0.1, 0.15, prt) # 「日付と時刻」
            self.send('LY MAX',   0.04, 0.04, prt)
            self.send('LY MAX',   0.04, 0.04, prt)
            self.send('Button A', 0.1, 0.1, prt) # 「現在の日付と時刻」
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('LY MIN',   0.04, 0.04, prt) # 1日進める
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('LX MAX',   0.04, 0.04, prt)
            self.send('Button A', 0.1, 0.1, prt) # OK
        if self.continueFlag:
            self.switch_day += 1
        if self.continueFlag:
            self.send('Button HOME', 0.1, 0.5, prt)
            self.send('Button HOME', 0.1, 0.5, prt) # ゲームに戻る
            self.send('Button B', 0.1, 0.6, prt)
            self.send('Button A', 0.1, 4.2, prt) # 募集をやめる
            self.send('Button A', 0.1, 0.3, prt) # ワット回収 「巣穴からエネルギーが少しだけでている！▼」
            self.send('Button B', 0.1, 0.3, prt) # 「シベリアは1000W手に入れた！▼」

    def one_day(self): # 1日進める
        """
        コマンド「1日進める」を実行する。
        レイドで1日進めてワットを回収する。
        柱のある巣穴の前で使用する。
        """
        self.endFlag = False
        if self.switch_day > 27 or self.switch_day == -1:
            print("実行前に日付をリセットします")
            self.setfirst()
        if self.continueFlag:
            self.day()
            self.send('Button B', 0.1, 1.0, prt=False) # ダイアログを閉じる
            self.send('Button B', 0.1, 1.0, prt=False) # レイドを閉じる
            # print("Switch day:", self.switch_day)
        print("[End] 1日進める")
        self.endFlag = True

    def internet(self):
        """
        インターネットに繋げる。
        """
        if self.continueFlag:
            print("YY通信")
            self.send('Button Y', 0.1, 0.6, prt=False) # YY通信
            print("インターネット")
            self.send('Button START', 0.1, 7.3, prt=False) # インターネット
            print("接続完了")
            self.send('Button A', 0.1, 0.3, prt=False)
            self.send('Button B', 0.1, 1.0, prt=False)

    def online_raid(self):
        """
        レイドをパスワード付きで募集する。
        """
        if self.continueFlag:
            self.send('Button A', 0.1, 2.7) # 巣穴を見る
            print("パスワード:", end="")
            self.send('Button START', 0.1, 0.8, prt=False) # パスワード
            print("1", end="")
            self.send('Button A', 0.05, 0.05, prt=False) # 1
            print("1", end="")
            self.send('Button A', 0.05, 0.05, prt=False) # 1
            print("1", end="")
            self.send('Button A', 0.05, 0.05, prt=False) # 1
            self.send('LY MAX', 0.05, 0.05)
            print("4")
            self.send('Button A', 0.05, 0.05, prt=False) # 4
            self.send('Button START', 0.1, 1.0) # OK
            self.send('Button A', 0.1, 0.5) # Pass OK

    def n_days(self, num=1): # n日進めて「ひとりで挑戦」
        """
        コマンド「n日進める」を実行する。
        レイドで指定の日数進める。
        願いのかたまりを使用した巣穴の前で使用する。

        Parameters
        ----------
        num : int
            進める日数
        """
        self.endFlag = False
        last_day = int(calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1]) # 今月の最終日
        if self.switch_day + num > last_day or self.switch_day == -1:
            print("実行前に日付をリセットします")
            self.setfirst()
        cnt = 0
        while cnt < num and self.continueFlag:
            self.day(prt=False)
            if self.continueFlag:
                cnt += 1
                print(cnt, "day")
        if self.continueFlag:
            self.send('Button A', 0.1, 1.0, False) # 巣穴を見る
            # self.send('LY MAX',   0.1, 0.3, False) # 「ひとりで挑戦」にカーソルをあわせる
            # レイド周回
            # self.internet()
            # self.online_raid()

            # print("Switch day:", self.switch_day)
        print("[End] n日進める")
        self.endFlag = True

    def shohi(self, num=0): # 乱数消費
        """
        コマンド「フレーム消費」を実行する。
        指定のフレーム数消費する。
        ランクマバグを使用した状態で、HOME>設定>本体>日付と時刻>現在の日付と時刻>OKを一度押した状態で実行する。
        開始時、日付は31日ある月にし、1日に合わせておく。
        また、30消費ごとに現在の消費数を出力する。

        Parameters
        ----------
        num : int
            消費したいフレーム数
        """
        self.endFlag = False
        cnt = 0
        day = 1
        while cnt < num and self.continueFlag:
            self.send('Button A', 0.1, 0.11, False)
            self.send('LX MIN',   0.05, 0.04, False)
            self.send('LX MIN',   0.05, 0.04, False)
            self.send('LX MIN',   0.05, 0.04, False)
            self.send('LY MIN',   0.05, 0.04, False) # 1日進める
            self.send('LX MAX',   0.05, 0.04, False)
            self.send('LX MAX',   0.05, 0.04, False)
            self.send('LX MAX',   0.05, 0.04, False)
            self.send('Button A', 0.1, 0.11, False) # OK
            day += 1
            if day == 32:
                day = 1
                print("Count :", cnt)
            else:
                cnt += 1
        print("[End] フレーム消費")
        self.endFlag = True

    def kotei_gensen(self, num=3): # 固定厳選
        """
        コマンド「固定厳選」を実行する。
        一度ソフトを再起動し、指定の日数進める。
        願いのかたまりを使用した巣穴の前で使用する。
        ３日後以降はレイドの出現ポケモンが固定されていないため、狙って出すことができる。

        Parameters
        ----------
        num : int
            進める日数
        """
        self.endFlag = False
        if self.continueFlag:
            self.restart()
            self.n_days(num)
        print("[End] 固定厳選")
        self.endFlag = True

    def seed(self): # Seed厳選
        """
        コマンド「Seed厳選」を実行する。
        一度ソフトを再起動し、1日進めてレポートを書き、3日進める。
        願いのかたまりを使用した巣穴の前で使用する。
        Seedが特定できない場合に、次のSeedに進める。
        """
        self.endFlag = False
        if self.continueFlag:
            self.restart()
            self.one_day()
            self.report()
            self.n_days(3)
        print("[End] Seed厳選")
        self.endFlag = True

    def restart(self): # 再起動
        """
        ソフトを再起動する。
        """
        self.endFlag = False
        if self.continueFlag:
            self.send('Button HOME', 0.1, 0.4, prt=False)
            self.send('Button X', 0.1, 0.2, prt=False)
            print("ソフト終了")
            self.send('Button A', 0.1, 2.6, prt=False) # ソフト終了
            print("ソフト起動")
            self.send('Button A', 0.1, 0.8, prt=False) # ソフト起動
            self.send('Button A', 0.1, 17.0, prt=False) # ユーザー選択
            self.send('Button A', 0.1, 8.0, prt=True)
        print("[End] 再起動")
        self.endFlag = True

    def report(self): # レポート
        """
        レポートを書く。
        """
        self.endFlag = False
        if self.continueFlag:
            print("メニュー")
            self.send('Button X', 0.1, 0.5, prt=False)
            print("レポート")
            self.send('Button R', 0.1, 1.2, prt=False)
            print("冒険を記録")
            self.send('Button A', 0.1, 3.0, prt=False)
        print("[End] レポート")
        self.endFlag = True

    def setfirst(self, reset_type="日付のみ"): # 日付リセット
        """
        コマンド「日付リセット」を実行する。
        Switchの日付を現在の月の1日に戻す。
        初めて実行するときはインターネットで時刻を合わせて1日の0時にリセットする。
        switch_dayに現在の日付が記録されるようになる。
        ２回目以降はswitch_dayに記録された現在の日付に従って1日にリセットする。

        Parameters
        ----------
        reset_type : String
            日付のみリセットか日付と時間をリセットするか指定する
        """
        self.endFlag = False
        print("Switch day:", self.switch_day)
        if self.switch_day == -1 or reset_type == "日付&時間":
            today = int(datetime.date.today().day)
        else:
            today = self.switch_day
        if self.continueFlag:
            self.send('Button HOME', 0.1, 0.5, prt=False) # ホームに戻る
            self.send('LY MAX',   0.04, 0.04, prt=False)
            self.send('LX MAX',   0.04, 0.04, prt=False)
            self.send('LX MAX',   0.04, 0.04, prt=False)
            self.send('LX MAX',   0.04, 0.04, prt=False)
            self.send('LX MAX',   0.04, 0.04, prt=False)
            self.send('Button A', 0.1, 0.15, prt=False) # 設定を開く
            self.send('LY MAX',   1.8, 0.1, prt=False)
            self.send('Button A', 0.1, 0.1, prt=False) # 「本体」
            self.send('LY MAX',   0.04, 0.04, prt=False)
            self.send('LY MAX',   0.04, 0.04, prt=False)
            self.send('LY MAX',   0.04, 0.04, prt=False)
            self.send('LY MAX',   0.04, 0.04, prt=False)
            self.send('Button A', 0.1, 0.15, prt=False) # 「日付と時刻」
        if (self.switch_day == -1 or reset_type == "日付&時間") and self.continueFlag: # Switchの日付が初期値なら、インターネットで時間を合わせる
            self.send('Button A', 0.1, 0.1, prt=False) # 「インターネットで時間をあわせる」ON
            self.send('Button A', 0.1, 0.2, prt=False) # 「インターネットで時間をあわせる」OFF
        if self.continueFlag:
            self.send('LY MAX',   0.04, 0.04, prt=False)
            self.send('LY MAX',   0.04, 0.04, prt=False)
            self.send('Button A', 0.1, 0.1, prt=False) # 「現在の日付と時刻」
            self.send('LX MAX',   0.04, 0.04, prt=False)
            self.send('LX MAX',   0.04, 0.04, prt=False)
            for _ in range(today - 1):
                self.send('LY MAX',   0.04, 0.04, prt=False) # 1日戻す
            print("1日に設定")
            self.send('LX MAX',   0.04, 0.04, prt=False)
            if self.switch_day == -1 or reset_type == "日付&時間":
                for _ in range(24 - int(datetime.datetime.now().hour)):
                    self.send('LY MIN',   0.04, 0.04, prt=False) # 0時に戻す
                print("0時に設定")
            self.send('LX MAX',   0.04, 0.04, prt=False)
            self.send('LX MAX',   0.04, 0.04, prt=False)
            self.send('Button A', 0.1, 0.1, prt=False) # OK
            self.send('Button HOME', 0.1, 0.5, prt=False)
            self.send('Button HOME', 0.1, 1.0, prt=False) # ゲームに戻る
            if self.continueFlag:
                self.switch_day = 1
            # print("Switch day:", self.switch_day)
        print("[End] 日付リセット")
        self.endFlag = True

    def backup(self): # バックアップ
        """
        ソフトをバックアップデータで再起動する。
        """
        self.endFlag = False
        if self.continueFlag:
            self.send('Button HOME', 0.1, 0.4, prt=False)
            self.send('Button X', 0.1, 0.2, prt=False)
            print("ソフト終了")
            self.send('Button A', 0.1, 2.6, prt=False) # ソフト終了
            print("ソフト起動")
            self.send('Button A', 0.1, 0.8, prt=False) # ソフト起動
            self.send('Button A', 0.1, 17.0, prt=False) # ユーザー選択
            self.send_hold('HOLD_LY MIN', prt=False)
            self.send_hold('Button BX', 0.1, 2.5, prt=True)
            print("バックアップデータで始める")
            self.send('Button A', 0.1, 1.1, prt=False) # バックアップデータで始める
            self.send('Button A', 0.1, 5.5, prt=False)
            # レイド周回
            # self.internet()
            # self.online_raid()
        print("[End] バックアップ")
        self.endFlag = True

    def controller(self, str): # コントローラー
        if str == "a" or str == "":
            self.send('Button A', 0.1, 0.1)
        elif str == "b":
            self.send('Button B', 0.1, 0.1)
        elif str == "x":
            self.send('Button X', 0.1, 0.1)
        elif str == "y":
            self.send('Button Y', 0.1, 0.1)
        elif str == "l1":
            self.send('Button L', 0.1, 0.1)
        elif str == "r1" or str == "z":
            self.send('Button R', 0.1, 0.1)
        elif str == "h":
            self.send('Button HOME', 0.1, 0.1)
        elif str == 'p':
            self.send('Button START', 0.1, 0.1)
        elif str == 'm':
            self.send('Button SELECT', 0.1, 0.1)
        elif str == "r":
            self.send('LX MAX',   0.2, 0.1)
        elif str == "l":
            self.send('LX MIN',   0.2, 0.1)
        elif str == "u":
            self.send('LY MIN',   0.2, 0.1)
        elif str == "d":
            self.send('LY MAX',   0.2, 0.1)
        else:
            print("unkown command.")

def main():
    ser = serial.Serial("/dev/ttyS7", 9600)
    self.sender = self.Sender(ser)

if __name__ == "__main__":
    main()
