from PyQt5 import QtGui
from PyQt5.QtWidgets import  QWidget,QLineEdit,QVBoxLayout, QPushButton
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt

        
class LightWidget(QWidget):
    def __init__(self, light, verbose = True):
        super().__init__()
        self.verbose = verbose
        self.light = light
        self.setWindowTitle('MC-LS Control')
        
        # main vertical layout
        self.vbox = QVBoxLayout()
        # on off button 
        self.onoff_button = QPushButton('Set On',self)
        self.onoff_button.clicked.connect(self.ClickOn)       
        
        # intensity input 
        self.intensity_input = QLineEdit()
        self.intensity_input.setValidator(QDoubleValidator(decimals = 2, 
                                                            notation=QtGui.QDoubleValidator.StandardNotation))
        self.instensity_input.setMaxLength(2)
        self.intensity_input.setAlignment(Qt.AlignRight)
        
        # intensity buton 
        self.intensity_button = QPushButton('Set intensity (0-1)',self)
        self.intensity_button.clicked.connect(self.ClickSetIntensity)
        
        # add widgets to vbox layout 
        self.vbox.addWidget(self.onoff_button)
        self.vbox.addWidget(self.intensity_input)
        self.vbox.addWidget(self.intensity_button)
        # set the vbox layout as the widgets layout
        self.setLayout(self.vbox)
    
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickOn(self):
        self.onoff_button.clicked.disconnect(self.ClickOn)
        self.light.set_on()
        r = self.intensity_input.text()
        if r : 
            e = float(r.replace(',', '.'))
            self.light.set_intensity(e)
        else: 
            self.light.set_intensity(0.1)
        self.onoff_button.setText('Set Off')
        self.onoff_button.clicked.connect(self.ClickOff)
    
    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickOff(self):
        self.onoff_button.clicked.disconnect(self.ClickDisconnect)      
        self.light.set_off()
        self.onoff_button.setText('Set On')
        self.onoff_button.clicked.connect(self.ClickOn)
    
    def ClickSetIntensity(self):
        r = self.intensity_input.text()
        e = float(r.replace(',', '.'))
        self.light.set_intensity(e)
        if self.verbose: 
            print(self.light.intensity)   
  
    def closeEvent(self, event):
        if self.light.on: 
            self.light.set_off()
        event.accept()
        

        
    
        
