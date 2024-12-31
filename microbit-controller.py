import microbit
import time

# ピン設定
joystick_x = pin0
joystick_y = pin1
joystick_select = pin2

# 無線設定（例：グループ1）
radio.config(group=1)

# サンプリング周期（秒）
sampling_period = 0.1

while True:
    # 左スティックの値を取得
    joystick_select.write_digital(0)
    x_left = joystick_x.read_analog()
    y_left = joystick_y.read_analog()

    # 右スティックの値を取得
    joystick_select.write_digital(1)
    x_right = joystick_x.read_analog()
    y_right = joystick_y.read_analog()

    # 取得した値をパッケージ化（例：文字列）
    data = str(x_left) + "," + str(y_left) + "," + str(x_right) + "," + str(y_right)

    # 無線送信
    radio.send(data)

    # サンプリング周期待ち
    time.sleep(sampling_period)
