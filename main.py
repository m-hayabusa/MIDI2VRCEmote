import sys
import re
import mido
import keyboard
import time

shift = 0
wait = 0.05

try:
    with mido.open_input() as inport:
        for msg in inport:
            if msg.type == "sysex":
                # Aerophone Miniでピッチシフト操作した時のやつ
                if re.match(r'F0 41 10 00 00 00 5A 12 00 27 34 22 [0-9A-F]{2} [0-9A-F]{2} F7' , msg.hex()):
                    shift = msg.data[11]-5
                    print('SHIFT ' + str(shift))

            elif msg.type == "note_off":
                print('OFF   ' + str(msg.note))

            elif msg.type == "note_on":
                print('ON    ' + str(msg.note))
                note = (msg.note + shift)%12

                if   note == 0 or note == 1:
                    key = 1
                elif note == 2 or note == 3:
                    key = 0 # 2:Open Hand はOculusコンの場合入力されっぱなしになるためスキップ
                elif note == 4:
                    key = 3
                elif note == 5 or note == 6:
                    key = 4
                elif note == 7 or note == 8:
                    key = 5
                elif note == 9 or note == 10:
                    key = 6
                elif note == 11:
                    key = 7

                keyboard.press(42) #左Shift
                keyboard.press('F'+str(key+1))
                time.sleep(wait)
                keyboard.release('F'+str(key+1))
                keyboard.release(42)

except KeyboardInterrupt:
    sys.exit()