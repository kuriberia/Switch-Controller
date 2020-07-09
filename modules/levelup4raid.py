#!/usr/bin/env python3
import argparse
import serial
import time
from time import sleep
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default="/dev/ttyS7")
args = parser.parse_args()

def send(ser, msg, duration=0, slp=0):
    now = datetime.datetime.now()
    print(f'[{now}] {msg}')
    ser.write(f'{msg}\r\n'.encode('utf-8'))
    sleep(duration)
    ser.write(b'RELEASE\r\n')
    sleep(slp)

ser = serial.Serial(args.port, 9600)

try:
    print("Start")
    send(ser, 'Button B', 0.1, 0.5)
    cnt = 0

    while(cnt < 1):
        send(ser, 'Button A', 0.1, 0.2) # ロトミにアクセス
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'Button A', 0.1, 2.8) # ポケジョブを開く
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 1.1)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3) # ポケモンを選ぶ
        send(ser, 'Button B', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 2.1)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 9.0) # 1日で送り出す
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button B', 0.1, 0.6)
        send(ser, 'Button A', 0.1, 0.3)

        send(ser, 'LX MAX',   0.4, 0.0)
        send(ser, 'LY MAX',   1.2, 3.0) # ポケセンから出る

        send(ser, 'Button X', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 2.2) # マップを開く
        send(ser, 'LY MIN',   0.1, 0.0)
        send(ser, 'LX MAX',   0.1, 0.1) # ハノシマ原っぱにカーソル移動
        send(ser, 'Button A', 0.1, 0.6)
        send(ser, 'Button A', 0.1, 7.5) # そらとぶタクシー

        send(ser, 'RX MAX',   0.495, 0.1) # 巣穴に移動
        send(ser, 'LY MIN',   6.8, 0.1)

        send(ser, 'Button A', 0.1, 0.3) # 巣穴を見る
        send(ser, 'Button A', 0.1, 2.7) # みんなで挑戦
        send(ser, 'Button HOME', 0.1, 0.5) # ホームに戻る
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # 設定を開く
        send(ser, 'LY MAX',   1.8, 0.1)
        send(ser, 'Button A', 0.1, 0.2) # 「本体」
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # 「日付と時刻」
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'LY MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # 「現在の日付と時刻」
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LY MIN',   0.05, 0.05) # 1日進める
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'LX MAX',   0.05, 0.05)
        send(ser, 'Button A', 0.1, 0.2) # OK

        send(ser, 'Button HOME', 0.1, 0.5)
        send(ser, 'Button HOME', 0.1, 0.5) # ゲームに戻る
        send(ser, 'Button B', 0.1, 0.6)
        send(ser, 'Button A', 0.1, 4.2) # 募集をやめる
        send(ser, 'Button A', 0.1, 0.3) # ワット回収
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'Button A', 0.1, 1.0)
        send(ser, 'Button B', 0.1, 1.7)

        send(ser, 'Button X', 0.1, 0.4) # エンジンシティに戻る
        send(ser, 'Button A', 0.1, 2.2) # マップを開く
        send(ser, 'LX MIN',   0.1, 0.0)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'Button A', 0.1, 0.6)
        send(ser, 'Button A', 0.1, 9.9) # そらとぶタクシー

        send(ser, 'LY MIN',   0.5, 2.5) # ポケセンに入る
        send(ser, 'LY MIN',   1.1, 0.1)
        send(ser, 'LX MIN',   0.5, 0.2) # ロトミの前に移動

        send(ser, 'Button A', 0.1, 0.2) # ロトミにアクセス
        send(ser, 'Button A', 0.1, 0.3)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'LY MAX',   0.1, 0.1)
        send(ser, 'Button A', 0.1, 3.0) # ポケジョブを開く
        send(ser, 'Button A', 0.1, 0.4) # 新しいジョブがあります
        send(ser, 'Button A', 0.1, 13.0)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 2.5)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button A', 0.1, 0.4)
        send(ser, 'Button B', 0.1, 0.6) # 閉じる
        send(ser, 'Button A', 0.1, 0.4)

        cnt += 1

except KeyboardInterrupt:
    send(ser, 'RELEASE')
    print("End.")
    ser.close()
