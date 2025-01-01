# ピン設定
joystick_x = AnalogPin.P0
joystick_y = AnalogPin.P1
joystick_select = DigitalPin.P2

# 無線設定（例：グループ1）
radio.set_group(1)
radio.on()

# サンプリング周期（ms）
sampling_period = 100

while True:
    # 左スティックの値を取得
    pins.digital_write_pin(joystick_select, 0)
    x_left = (int(pins.analog_read_pin(joystick_x)) & 0x3FC) >> 2
    y_left = (int(pins.analog_read_pin(joystick_y)) & 0x3FC) >> 2

    # 右スティックの値を取得
    pins.digital_write_pin(joystick_select, 1)
    x_right = (int(pins.analog_read_pin(joystick_x)) & 0x3FC) >> 2
    y_right = (int(pins.analog_read_pin(joystick_y)) & 0x3FC) >> 2


    # 取得した値をパッケージ化
    combined  = 0x7FFFFFFF
    val1 = (x_left  & 0xFF) << 24
    val2 = (y_left  & 0xFF) << 16
    val3 = (x_right & 0xFF) << 8
    val4 = (y_right & 0xFF)
    combined  = val1 | val2 | val3 | val4
    data = str(x_left) + "," + str(y_left) + "," + str(x_right) + "," + str(y_right)

    # 無線送信
    radio.send_number(combined)

    print(data)
    for ii in range(5):
        for jj in range(5):
            led.unplot(ii,jj)
    led.plot(0, 4-Math.round(x_left/64.0))
    led.plot(1, 4-Math.round(y_left/64.0))
    led.plot(3, 4-Math.round(x_right/64.0))
    led.plot(4, 4-Math.round(y_right/64.0))

    # サンプリング周期待ち
    basic.pause(sampling_period)
