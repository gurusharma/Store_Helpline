import RPi.GPIO as GPIO
import serial
import time

ENABLE_PIN  = 14              # The BCM pin number corresponding to GPIO1

SERIAL_PORT = '/dev/ttyS0'   # RPi 3 has apparently used 'ttyAMA0' for
                              # Bluetooth and assigned 'ttyS0' to the GPIO
                              # serial port, so uncomment the appropriate
                              # SERIAL_PORT definition for your setup.
                              # Failing that, check the output of:
                              #   $ dmesg | grep serial
                              # to get an idea as to where serial has been
                              # assigned to.

                              
def validate_rfid(code):
    # A valid code will be 12 characters long with the first char being
    # a line feed and the last char being a carriage return.
    s = code.decode('ascii')
       
    if (len(s) == 12):
	return s[1:11]
    
def main():
    # Initialize the Raspberry Pi by quashing any warnings and telling it
    # we're going to use the BCM pin numbering scheme.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # This pin corresponds to GPIO1, which we'll use to turn the RFID
    # reader on and off with.
    GPIO.setup(ENABLE_PIN, GPIO.OUT)

    # Setting the pin to LOW will turn the reader on.  You should notice
    # the green LED light on the reader turn red if successfully enabled.

    print("Enabling RFID reader and reading from serial port: " + SERIAL_PORT)
    GPIO.output(ENABLE_PIN, GPIO.LOW)

    # Set up the serial port as per the Parallax reader's datasheet.
    ser = serial.Serial(baudrate = 2400,
                        bytesize = serial.EIGHTBITS,
                        parity   = serial.PARITY_NONE,
                        port     = SERIAL_PORT,
                        stopbits = serial.STOPBITS_ONE,
                        timeout  = 3)
    #ser = serial.Serial("/dev/ttyAMA0",baudrate=2400, timeout=5)
    # Wrap everything in a try block to catch any exceptions.
    try:
       var = 1
        # Loop forever, or until CTRL-C is pressed.
       while var:
	    GPIO.setup(6,GPIO.OUT)
	    GPIO.output(6,GPIO.HIGH)
	    #Read in 12 bytes from the serial port.
            print("Reading tag...")
            data = ser.read(12)
            #Attempt to validate the data we just read.
            code = validate_rfid(data)
         
	    #If validate_rfid() returned a code, display it.
            if code:
                print("Read RFID code: " + code);
		if ("415D7D42C" in code):
			print("Welcome User1")
			var = 0
	        	GPIO.output(ENABLE_PIN, GPIO.HIGH)
			GPIO.output(6,GPIO.LOW);
		elif ("415EA0D36" in code):
			print("Welcome User2")
			var = 0
	        	GPIO.output(ENABLE_PIN, GPIO.HIGH)
			GPIO.output(6, GPIO.LOW);
		else:
			print("Please contact admin to register first")
			var = 0
	        	GPIO.output(ENABLE_PIN, GPIO.HIGH)
			GPIO.output(6, GPIO.LOW);
		
    except Exception as e:
	print (e)
        # If we caught an exception, then disable the reader by setting
        # the pin to HIGH, then exit.
        print("Disabling RFID reader...")
        GPIO.output(ENABLE_PIN, GPIO.HIGH)
	GPIO.output(6, GPIO.LOW);

        
if __name__ == "__main__":
    main()

