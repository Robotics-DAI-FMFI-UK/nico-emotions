import serial
import serial.tools.list_ports
import time
import os

if __name__ == '__main__':
    from config import PREFFERED_PORT, LAST_CONNECTED_PORT
else:
    from Controllers.config import PREFFERED_PORT, LAST_CONNECTED_PORT

def print_on_main(message):
    if __name__ == '__main__':
        print(message)

def find_microcontroller():

    for port in [PREFFERED_PORT, LAST_CONNECTED_PORT]:
        if port is None:
            continue

        returned_port = try_port(port)

        if returned_port is not None:
            save_found_port(returned_port)
            return returned_port

    ports = serial.tools.list_ports.comports()

    for port in ports:

        if 'CH' not in port.description and "Serial Device" not in port.description:
            continue

        returned_port = try_port(port.device)

        if returned_port is not None:
            save_found_port(returned_port)
            return returned_port
    
    print('Microcontroller not found')

    return None

def try_port(port):
    try:
        print_on_main(f'Trying port: {port}')
        ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(0.1)

        ser.write(('HELLO NICO\n').encode())
        start_time = time.time()
        response = ''

        while time.time() - start_time < 1:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                response = line
                break

        print_on_main(f'Microcontroller response: {response}')

        if 'HELLO' in response:
            print_on_main(f'Microcontroller found on {port}')
            ser.close()
            return port
        else:
            ser.close()
    except (OSError, serial.SerialException):
        pass

    return None


def save_found_port(port):
    if LAST_CONNECTED_PORT == port:
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, 'config.py')

    try:
        with open(path, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            f.seek(0)

            for line in lines:
                if line.strip().startswith('LAST_CONNECTED_PORT'):
                    f.write(f'LAST_CONNECTED_PORT = "{port}"\n')
                else:
                    f.write(line)
                    
            f.truncate()
    except FileNotFoundError:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f'LAST_CONNECTED_PORT = "{port}"\n')

if __name__ == '__main__':
    find_microcontroller()
