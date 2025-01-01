def set_motor_speed(motor: str, speed: number, direction: str):
    # モーターの速度と方向を設定する関数
    # Args:
    # motor: モーター (left または right)
    # speed: 速度 (0-1023)
    # direction: 方向 (forward または backward)
    if motor == "left":
        if direction == "forward":
            pins.digital_write_pin(left_motor_forward, 1)
            pins.digital_write_pin(left_motor_backward, 0)
        else:
            pins.digital_write_pin(left_motor_forward, 0)
            pins.digital_write_pin(left_motor_backward, 1)
        pins.analog_write_pin(left_motor_enable, speed)
    elif motor == "right":
        if direction == "forward":
            pins.digital_write_pin(right_motor_forward, 1)
            pins.digital_write_pin(right_motor_backward, 0)
        else:
            pins.digital_write_pin(right_motor_forward, 0)
            pins.digital_write_pin(right_motor_backward, 1)
        pins.analog_write_pin(right_motor_enable, speed)

# ジョイスティックの値からモーターの速度と方向を決定
def control_motors(y_left: number, y_right: number):

    # モーターの速度を制限する最大値
    max_speed = 1023

    # y_left, y_rightの値が大きいほど前進、小さいほど後退
    # 0付近では停止
    left_speed = Math.round(abs(y_left))
    right_speed = Math.round(abs(y_right))
    if y_left > 0:
        left_direction = "forward"
    elif y_left < 0:
        left_direction = "backward"
    else:
        left_speed = 0
    if y_right > 0:
        right_direction = "forward"
    elif y_right < 0:
        right_direction = "backward"
    else:
        right_speed = 0
    # モーターの速度と方向を設定
    set_motor_speed("left", min(left_speed, max_speed), left_direction)
    set_motor_speed("right", min(right_speed, max_speed), right_direction)

def on_received_number(receivedNumber):
    global x_left, y_left, x_right, y_right
    if receivedNumber:
        x_left  = receivedNumber >> 24 & 0xFF
        y_left  = receivedNumber >> 16 & 0xFF
        x_right = receivedNumber >> 8  & 0xFF
        y_right = receivedNumber       & 0xFF
        data = "" + str(x_left) + "," + ("" + str(y_left)) + "," + ("" + str(x_right)) + "," + ("" + str(y_right))

        print(data)

__name__ = '__main__'
if __name__ == '__main__':
    # 無線設定（送信側と同じグループに設定）
    radio.set_group(1)
    radio.on()

    # モータードライバのピン設定
    left_motor_enable = AnalogPin.P1
    right_motor_enable = AnalogPin.P2
    left_motor_forward = DigitalPin.P3
    left_motor_backward = DigitalPin.P4
    right_motor_forward = DigitalPin.P5
    right_motor_backward = DigitalPin.P6
    x_left  = 128
    y_left  = 128
    x_right = 128
    y_right = 128

    while True:
        # データ受信
        radio.on_received_number(on_received_number)
        if on_received_number:
            # 例: 受信した値を使ってモーターを制御
            control_motors(y_left, y_right)
            for ii in range(5):
                for jj in range(5):
                    led.unplot(ii, jj)
            led.plot(0, 4 - Math.round(x_left  / 64))
            led.plot(1, 4 - Math.round(y_left  / 64))
            led.plot(3, 4 - Math.round(x_right / 64))
            led.plot(4, 4 - Math.round(y_right / 64))
        
        basic.pause(100)
