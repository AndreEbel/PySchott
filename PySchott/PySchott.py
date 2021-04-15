import serial
import threading

class Light(object):
    """
    Driver for the MCLS Schott light sources
    Warning: This is for the MCLS series, it is not KL protocol version 2.0 used on KL 2500 LED 
    However, MCLS lightsources can be controlled with KL protocol version 2.0
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
        start = '&'
        terminator = "\r"
        input_bytes = bytes(start + command + terminator, 'ascii')
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
            answer = self.query('I' + X)
            return answer      
    
    @property
    def intensity(self):
        """
        LED intensity 
        """
        answer = self.query('I?')
        hexa_value = answer[-2]   + answer[-1]   
        intensity = int(hexa_value, 16)/255                 
        return intensity     
    
    @property
    def precise_intensity(self):
        """
        LED precise intensity 
        """
        answer = self.query('IP?')
        hexa_value = answer[-3] + answer[-2] + answer[-1]   
        intensity = int(hexa_value, 16)
        if intensity > 2047: 
            intensity = 2047                 
        return intensity/2047     
    
    @property 
    def product_name(self): 
        answer = self.query('Q')
        return answer[1:]
    
    @property 
    def serial_number(self): 
        answer = self.query('Z$')
        return answer
    
    @property 
    def model_number(self): 
        answer = self.query('ZM$')
        return answer
    
    @property 
    def control_source(self): 
        answer = self.query('M?')
        if int(answer[-1])==0: 
            control = 'Front panel'
        if int(answer[-1])==1: 
            control = 'Rear analog control'
        if int(answer[-1])==2: 
            control = 'RS232 port'
        if int(answer[-1])==4: 
            control = 'USB port'
        if int(answer[-1])==7: 
            control = None
        return control
    
    @property 
    def control_lockout(self): 
        answer = self.query('K?')
        if int(answer[-1])==0: 
            control = 'all controls enabled'
        if int(answer[-1])==1: 
            control = 'front knob and switch disabled'
        if int(answer[-1])==2: 
            control = 'analog input disabled'
        if int(answer[-1])==3: 
            control = 'front knob, switch and analog input disabled'
        return control

    