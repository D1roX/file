import serial
import time


def calculate_checksum(data):
    ck_a = 0
    ck_b = 0
    for byte in data:
        ck_a += byte
        ck_a &= 0xff
        ck_b += ck_a
        ck_b &= 0xff
    return bytes([ck_b, ck_a])


def create_package(msg_id, x, y, distance):
    data = bytearray([0xAA])  # Признак включения
    data.extend(round(x).to_bytes(4))  # X
    data.extend(round(y).to_bytes(4))  # Y
    data.extend(round(distance * 2**10).to_bytes(4))  # Расстояние 2^(-10)

    checksum = calculate_checksum(msg_id + data)
    package = msg_id + data + checksum
    return package


def read_package(package):
    print(
        f'msg_id: {int.from_bytes(package[:5])}\n'
        f'признак включения: {int.from_bytes(package[5:6])}\n'
        f'x: {int.from_bytes(package[6:10])}\n'
        f'y: {int.from_bytes(package[10:14])}\n'
        f'дистанция: {int.from_bytes(package[14:18]) / 2 ** 10}\n'
        f'контрольная сумма: {int.from_bytes(package[18:])}\n\n'
    )


def run():
    msg_id = b'\x55\xDD\x15\x16\x17'

    port = 'COM1'
    rate = 115200
    bytesize = serial.EIGHTBITS
    parity = serial.PARITY_NONE
    stop_bits = serial.STOPBITS_ONE

    ser = serial.Serial(port, rate, bytesize, parity, stop_bits)
    for _ in range(10):
        x = 10.5
        y = 5.2
        distance = 2.7

        package = create_package(msg_id, x, y, distance)

        ser.write(package)

        print(f'Отправлен пакет: {package.hex()}')
        print(f'Количество байт: {len(package)}')

        # Задержка 20 мс (50 Гц)
        time.sleep(0.02)

    ser.close()


if __name__ == '__main__':
    run()
