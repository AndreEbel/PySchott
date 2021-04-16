import serial
import threading
import numpy as np

class Light(object):
    """
    General Light class with basic functions to communicate with the controller 
    """
    start = None
    terminator = None
    baudrate = 9600
    bytesize = 8
    stopbits = serial.STOPBITS_ONE
    timeout = 0.1
    parity = serial.PARITY_NONE
    
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
                                baudrate=self.baudrate,
                                bytesize=self.bytesize,
                                stopbits = self.stopbits,
                                timeout=self.timeout,
                                parity=self.parity,
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
        
        input_bytes = bytes(self.start + command + self.terminator, 'ascii')
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
      
class MCLS_Light(Light):
    """
    Driver for the MCLS Schott light sources
    Warning: This is for the MCLS series, it is not KL protocol version 2.0 used on KL 2500 LED 
    However, MCLS lightsources can be controlled with KL protocol version 2.0
    See class KL_Light for KL series lightsources 
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
        
        super().__init__(port)
        self.start = '&'
        self.terminator = '\r'
  
    def set_on(self):
        """
        Enable LED output
        """
        answer = self.query('L1')
        if answer[-1] =='1':
            self.on = True
       
        
    def set_off(self):
        """
        Disable LED output
        """
        answer = self.query('L0')
        if answer[-1] =='0':
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
            #self.intensity = e
            X = hex(int(e*255))
            self.write('I' + X)
    
    @property 
    def knob_input_value(self): 
        """
        Get the front knob position as a percentage of full scale.

        Returns
        -------
        kiv : float
            front knob position as a percentage of full scale.

        """
        answer = self.query('A0?')
        kiv = float(answer[3:])/10
        return kiv
    
    @property 
    def rear_input_value(self): 
        """
        Get the rear analog input as a percentage of full scale (0 – 5V).

        Returns
        -------
        riv : float
            rear analog input in % of full scale

        """
        answer = self.query('A1?')
        riv = float(answer[3:])/10
        return riv
    
    @property 
    def board_temperature(self): 
        """
        Get the current temperature of the internal PCB in Celsius.

        Returns
        -------
        T_C : float
            temperature in °C

        """
        answer = self.query('BT?')
        T_C = float(answer[3:])
        return T_C
    
    @property
    def front_switch_state(self): 
        """
        Get the state of the front switch.

        Returns
        -------
        fss : bool
            state of the front switch

        """
        answer = self.query('D0?')
        if answer[-1]=='1': 
            fss = True 
        elif answer[-1]=='0': 
            fss = False
        return fss
    
    @property
    def remote_digital_input_state(self): 
        """
        Get the state of the digital input of the IN/OUT port (pin 1).
        This input will read “high” when the pin is disconnected.

        Returns
        -------
        rdis : bool
            state of the digital input (False is low, True is high)

        """
        answer = self.query('D1?')
        if answer[-1]=='1': 
            rdis = True 
        elif answer[-1]=='0': 
            rdis = False
        return rdis
    
    @property
    def firmware_version(self): 
        """
        Get the firmware version of the unit

        Returns
        -------
        version : float 
            firmware version of the unit

        """
        answer = self.query('F?')
        version = float(answer[2:])
        return version
    
    @property
    def fan_speed(self): 
        """
        Get the fan speed in RPM.

        Returns
        -------
        RPM : float
            fan speed in RPM.

        """
        answer = self.query('G?')
        RPM = float(answer[2:])
        return RPM
    
    @property
    def front_control_lockout(self): 
        """
        check the front panel knob and button controls.

        Returns
        -------
        control : bool
            True if enabled, False otherwise

        """
        answer = self.query('HLF?')
        if int(answer[-1])==0: 
            control = False # 'front control is disabled'
        if int(answer[-1])==1: 
            control = True #'front control is enabled'
        return control 
    
    @property
    def analog_control_lockout(self): 
        """
        check if remote analog input is enabled

        Returns
        -------
        control : bool
            True if enabled, False otherwise

        """
        answer = self.query('HLM?')
        if int(answer[-1])==0: 
            control = False # 'front control is disabled'
        if int(answer[-1])==1: 
            control = True #'front control is enabled'
        return control 
    
    @property
    def intensity(self):
        """
        LED intensity 
        """
        answer = self.query('I?')
        hexa_value = answer[-2]   + answer[-1]   
        intensity = int(hexa_value, 16)/255                 
        return np.round(intensity, 2)     
    
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
    def control_lockout(self): 
        """
        Get the control lockout setting.

        Returns
        -------
        control : string
            Description of the control lockout setting.

        """
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
    
    @property
    def LED_output_enable(self):
        """
        Check if the LED output is enabled.

        Returns
        -------
        output : bool
            True: LED output is enabled
            False: LED output is disabled
            
        """
        answer = self.query('L?')
        if answer[-1]=='1': 
            output = True
        elif answer[-1]=='0': 
            output = False
        return output
        
    @property 
    def LED_heatsink_temperature(self): 
        """
        Get the heatsink temperature in degrees Celsius.

        Returns
        -------
        T_C : float 
            heatsink temperature in degrees Celsius in the range -5.0 to 99.9°C

        """
        answer = self.query('LT?')
        T_C = float(answer[3:])
        return T_C
    
    
    @property 
    def control_source(self): 
        """
        Get the interface that is controlling the unit. 
        An interface gains control of the unit if it adjusts the intensity or enables/disables the LED.
        The RS232 and USB ports claim control whenever the "L", "I", or "IP" commands are sent.
        The front panel or rear analog input claim control when the power button is pressed, the digital input is toggled, or the light intensity is adjusted.

        Returns
        -------
        control : string
            interface controlling the unit

        """
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
    def product_name(self): 
        """
        Get the product name.

        Returns
        -------
        name : string
            product name

        """
        answer = self.query('Q')
        name = answer[2:]
        return name
    
    @property 
    def input_voltage(self): 
        """
        Gets the input voltage.        

        Returns
        -------
        VI : TYPE
            DESCRIPTION.

        """
        answer = self.query('VI?')
        VI = float(answer[3:])
        return VI
    
    @property 
    def serial_number(self): 
        """
        Get the unit's serial number.

        Returns
        -------
        serial : int
            serial number.

        """
        answer = self.query('Z')
        serial = int(answer[3:])
        return serial
    
    @property 
    def model_number(self): 
        """
        Gets the unit's model number.

        Returns
        -------
        model : string
            model number 

        """
        answer = self.query('ZM')
        model = answer[3:]
        return model 
    
    
    
    
class KL_Light(object):
    """
    Driver for the KL series Schott light sources
    KL protocol version 2.0 used on KL 2500 LED
    Warning: This is not the MCLS series, see class MCLS_Light for MCLS series lightsources 
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
        super().__init__(port)
        self.start = '0'
        self.terminator = ';'

   
   
    