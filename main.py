from machine import Pin, UART, PWM
import time

if __name__=='__main__':
	FULL_FORWARD = int(0.165 * 65536)
	HALF_FORWARD = int(0.16 * 65536)
	BRAKE = int(0.15 * 65536)
	HALF_BACKWARD = int(0.1425 * 65536)
	FULL_BACKWARD = int(0.135 * 65536)
	LEFT = int(0.19 * 65536)
	STRAIGHT = int(0.15 * 65536)
	RIGHT = int(0.11 * 65536)

	servo = PWM(Pin(2), freq = 100)
	motor = PWM(Pin(3), freq = 100)
	uart0 = UART(0, baudrate = 9600, tx = Pin(0), rx = Pin(1), timeout = 10)
	uart1 = UART(1, baudrate = 9600, tx = Pin(8), rx = Pin(9), timeout_char = 10)
	uart0.init(bits = 8, parity = None, stop = 1)
	uart1.init(bits = 8, parity = None, stop = 1)
	enable = True
	motor.duty_u16(BRAKE)
	servo.duty_u16(STRAIGHT)
	time.sleep(1)
	motor.duty_u16(HALF_FORWARD)

	while True:
		motor.duty_u16(HALF_FORWARD)

		if uart1.any():
			try:
				msg = uart1.readline().decode('utf-8')

				if msg == "start":
					enable = True
				elif msg == "stop":
					motor.duty_16(BRAKE)
					servo.duty_16(STRAIGHT)
					enable = False
				elif msg == "exit":
					break
			except:
				pass

		if enable and uart0.any():
			try:
				msg = uart0.readline().decode('utf-8')
				error = float(msg)
				temp = error
				error = min(1, error) if error > 0 else max(-1, error)
				print(str(temp) + ", " + str(error))
				servo.duty_u16(int(65536 * (0.15 + 0.04 * error)))
			except Exception as error:
				print(error)

	servo.deinit()
	motor.deinit()
