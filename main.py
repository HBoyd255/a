import serial

# TODO add a way to read in the com port
COM_PORT = "COM3"
BAUDRATE = 230400
TIMEOUT = 0.1

try:
    ser = serial.Serial(port=COM_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
except Exception as e:
    raise Exception(f"{COM_PORT} not found.") from e

print("oi")
ser.write(b"zmb-wr-mtr 30 0")
ser.flush()  # Ensure the command is sent immediately
