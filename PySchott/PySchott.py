import serial
import threading

class Light(object):
    """
    Driver for the MCLS Schott light sources
    """
    def __init__(self, port):
        """
        Light source object creator

        Parameters
        ----------
        port : string
            port used to establish the serial communication
            for windows users it will be 'COMX' with X being an integer
        """
        self.lock = threading.Lock()
        self.ser = serial.Serial(port=port,
                                baudrate=9600,
                                bytesize=8,
                                stopbits = serial.STOPBITS_ONE,
                                #timeout=0.1,
                                parity=serial.PARITY_NONE,
                                )


    def read(self):
        """
        Serial read

        Returns
        -------
        answer : string
            string read from the controller

        """
        string = self.ser.readline()
        answer = string[0:-1].decode('ascii')
        return answer

    def write(self, command):
        """
        Serial write.

        Parameters
        ----------
        command : string
            command to be written in the controller.
        """
        AA = '&'
        CR = "\r"
        input_bytes = bytes(AA + command + CR, 'ascii')
        self.ser.write(input_bytes)

    def query(self, string):
        """
        Write a command and read the reply.

        Parameters
        ----------
        command : string
            command to be written to the controller

        Returns
        -------
        answer : string
            answer read from the controller
        """
        with self.lock:
          self.write(string)
          answer = self.read()
          return answer 
  
    def set_on(self):
        """
        Enable LED output
        """
        self.write('L1')
        self.on = True
    def set_off(self):
        """
        Disable LED output
        """
        self.write('L0')
        self.on = False
        
    def set_intensity(self, e):
        """
        Adjust LED intensity 

        Parameters
        ----------
        e : float
            emissivity in the 0.5-1 range
        """
        if 0<e<=1:
            self.intensity = e
            X = hex(int(e*255))
            self.write('I' + X)
