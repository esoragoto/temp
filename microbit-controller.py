# ピン設定
joystick_x = AnalogPin.P0
joystick_y = AnalogPin.P1
joystick_select = DigitalPin.P2

# 無線設定（例：グループ1）
radio.set_group(1)

# サンプリング周期（ms）
sampling_period = 100

while True:
    # 左スティックの値を取得
    pins.digital_write_pin(joystick_select, 0)
    x_left = pins.analog_read_pin(joystick_x) & 0x3FF
    y_left = pins.analog_read_pin(joystick_y) & 0x3FF

    # 右スティックの値を取得
    pins.digital_write_pin(joystick_select, 1)
    x_right = pins.analog_read_pin(joystick_x) & 0x3FF
    y_right = pins.analog_read_pin(joystick_y) & 0x3FF

    # 取得した値をパッケージ化
    combined = (x_left << 30) | (y_left << 20) | (x_right << 10) | y_right
    data = str(x_left) + "," + str(y_left) + "," + str(x_right) + "," + str(y_right)

    # 無線送信
    radio.send_value("data", combined)

    print(data)
    for ii in range(5):
        for jj in range(5):
            led.unplot(ii,jj)
    led.plot(0, 4-Math.round(x_left/256.0))
    led.plot(1, 4-Math.round(y_left/256.0))
    led.plot(3, 4-Math.round(x_right/256.0))
    led.plot(4, 4-Math.round(y_right/256.0))

    # サンプリング周期待ち
    basic.pause(sampling_period)
