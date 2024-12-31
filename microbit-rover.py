import microbit
import time

# 無線設定（送信側と同じグループに設定）
radio.config(group=1)

# モータードライバのピン設定
left_motor_enable = pin1
right_motor_enable = pin2
left_motor_forward = pin3
left_motor_backward = pin4
right_motor_forward = pin5
right_motor_backward = pin6

# モーターの速度を制限する最大値
max_speed = 1023

def set_motor_speed(motor, speed, direction):
    """
    モーターの速度と方向を設定する関数

    Args:
        motor: モーター (left または right)
        speed: 速度 (0-1023)
        direction: 方向 (forward または backward)
    """
    if motor == 'left':
        pin1.write_analog(speed)
        if direction == 'forward':
            pin3.write_digital(1)
            pin4.write_digital(0)
        else:
            pin3.write_digital(0)
            pin4.write_digital(1)
    elif motor == 'right':
        pin2.write_analog(speed)
        if direction == 'forward':
            pin5.write_digital(1)
            pin6.write_digital(0)
        else:
            pin5.write_digital(0)
            pin6.write_digital(1)

# ジョイスティックの値からモーターの速度と方向を決定
def control_motors(y_left, y_right):
    # y_left, y_rightの値が大きいほど前進、小さいほど後退
    # 0付近では停止

    left_speed = int(abs(y_left))
    right_speed = int(abs(y_right))

    if y_left > 0:
        left_direction = 'forward'
    elif y_left < 0:
        left_direction = 'backward'
    else:
        left_speed = 0

    if y_right > 0:
        right_direction = 'forward'
    elif y_right < 0:
        right_direction = 'backward'
    else:
        right_speed = 0

    # モーターの速度と方向を設定
    set_motor_speed('left', min(left_speed, max_speed), left_direction)
    set_motor_speed('right', min(right_speed, max_speed), right_direction)



while True:
    # データ受信
    received_data = radio.receive()

    if received_data:
        # 受信データをカンマで分割
        values = received_data.split(',')

        # 文字列をfloat型に変換して変数に格納
        x_left = float(values[0])
        y_left = float(values[1])
        x_right = float(values[2])
        y_right = float(values[3])

        # 取得した値を表示
        print("左スティックX:", x_left)
        print("左スティックY:", y_left)
        print("右スティックX:", x_right)
        print("右スティックY:", y_right)

        # 例: 受信した値を使ってモーターを制御
        control_motors(y_left, y_right)


