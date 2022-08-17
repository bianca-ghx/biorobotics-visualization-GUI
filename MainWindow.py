from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtGui, QtWidgets
import Motor
import ADBoard
from UiMenu import Ui_Menu
from UiForceDistance import Ui_ForceDistance
from UiElectronic import Ui_Electronic
import time
import datetime as dt
import sys
import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from qt_material import apply_stylesheet

def catch_exceptions(t, val, tb):
   QtWidgets.QMessageBox.critical(None,
                                  "An exception was raised",
                                  "Exception type: {}".format(t))
   old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

class MplCanvas(FigureCanvasQTAgg):

   def __init__(self, parent=None, width=7, height=1, dpi=100):
       self.fig = Figure(figsize=(width, height), dpi=dpi)
       self.ax = self.fig.add_subplot(111)
       super(MplCanvas, self).__init__(self.fig)

class Menu(QtWidgets.QMainWindow, Ui_Menu):

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.setupUi(self)
       self.setWindowTitle("Measurements GUI")
       self.menuPage()

   def menuPage(self):
       self.distanceButton.clicked.connect(self.distancePage)
       self.electronicButton.clicked.connect(self.electronicPage)
       self.show()

   def distancePage(self):
       # self.close()
       self.distanceWindow = ForceDistance()
       self.distanceWindow.show()

   def electronicPage(self):
       # self.close()
       self.electronicWindow = Electronic()
       self.electronicWindow.show()

class ForceDistance(QtWidgets.QMainWindow, Ui_ForceDistance):

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.setupUi(self)
       self.setWindowTitle("Force and Distance Measurements")

       self.comboBox1.addItems(Motor.ComportAvailable())  # added
       self.comboBox2.addItems(['300', '1200', '2400', '4800', '9600', '19200', '38400', '57600', '74880', '115200', '230400', '250000', '500000', '1000000', '2000000'])
       self.pushButton1.clicked.connect(self.pushButton1clicked)
       self.pushButton2.clicked.connect(self.pushButton2clicked)
       self.pushButton3.clicked.connect(self.pushButton3clicked)
       self.pushButton4.clicked.connect(self.pushButton4clicked)
       self.pushButton5.clicked.connect(self.pushButton5clicked)
       # self.pushButton6.clicked.connect(self.menuPage)
       self.pushButton6.clicked.connect(self.pushButton6clicked)

       self.plot1 = MplCanvas(self, width=8, height=5, dpi=100)
       toolbar = NavigationToolbar(self.plot1, self)
       self.verticalLayout2.addWidget(toolbar)
       self.verticalLayout2.addWidget(self.plot1)

       self.show()

   def pushButton1clicked(self):

       self.listWidget.clear()
       self.arduino = Motor.MotorConnect(self.comboBox1.currentText(), self.comboBox2.currentText())
       self.listWidget.addItem('Successfully connected to Arduino! \n')
       self.listWidget.addItem('Calculating average distance...')
       self.listWidget.scrollToBottom()
       QCoreApplication.processEvents()

       # total_range (sensor+motor-free_range)
       range_ = int(self.lineEdit2.text())

       distances=[]

       i = 0
       while i<5:
           measurement, _ = Motor.MotorRead(self.arduino)
           measurement_sample = measurement.split()
           if measurement_sample[0] == 'Distance:':
               distances.append(int(measurement_sample[1]))
               self.listWidget.addItem('.')
               self.listWidget.scrollToBottom()
               QCoreApplication.processEvents()
               i+=1

       avg_distance=sum(distances)/len(distances)
       self.initial_distance = avg_distance - range_
       self.initial_distance = round(self.initial_distance, 2)
       self.listWidget.addItem(f'The free range distance is: {self.initial_distance}  \n')

   def pushButton2clicked(self):

       # total_range (sensor+motor-free_range)
       range_ = int(self.lineEdit2.text())

       free_range_distance=self.lineEdit1.text()

       total_range=str(int(free_range_distance)+range_)
       target_distance_b=total_range.encode()
       target_reached=0

       self.time_distance=[]
       self.distance=[]
       self.time_force=[]
       self.force=[]

       self.measurements_df = pd.DataFrame(columns=['Time', 'Distance', 'Weight'])
       start_time = time.time()

       i=0
       while True:
           if i==0:
               self.arduino.write(target_distance_b)  # Send the value to arduino
               i+=1
           measurement, meas_time = Motor.MotorRead(self.arduino)
           measurement_sample = measurement.split()
           timeDelta = meas_time-start_time
           if measurement_sample[0]=='Distance:':
               measurement_sample[1] = str(int(measurement_sample[1])-range_)
               self.time_distance.append(timeDelta)
               self.distance.append(float(measurement_sample[1]))
           elif measurement_sample[0]=='Weight:':
               if float(measurement_sample[1])<0:
                   measurement_sample[1]="0"
               self.time_force.append(timeDelta)
               self.force.append(float(measurement_sample[1]))
           else:
               continue

           if measurement_sample[0]=='Distance:' and int(measurement_sample[1])==int(free_range_distance):
               target_reached+=1
           else:
               pass

           if target_reached==15:
               break

           if measurement_sample[0] == 'Distance:':
               self.listWidget.addItem(f"Distance:{measurement_sample[1]}")
               self.listWidget.scrollToBottom()
               QCoreApplication.processEvents()
           elif measurement_sample[0] == 'Weight:':
               self.listWidget.addItem(f"Weight:{measurement_sample[1]}")
               self.listWidget.scrollToBottom()
               QCoreApplication.processEvents()


       self.listWidget.addItem('\n')
       self.listWidget.addItem('Done Measuring!')
       self.listWidget.scrollToBottom()
       QCoreApplication.processEvents()

       lengths=[len(self.time_force), len(self.distance), len(self.force)]
       min_len=min(lengths)

       self.time_force=self.time_force[0:min_len]
       self.distance = self.distance[0:min_len]
       self.force = self.force[0:min_len]

       self.measurements_df['Time'] = self.time_force
       self.measurements_df['Distance'] = self.distance
       self.measurements_df['Weight'] = self.force

   def pushButton3clicked(self):
       if self.measurements_df.empty:
           pass
       else:
           self.measurements_df.to_excel(f"ForceDistance_Measurement_{dt.datetime.now().strftime('%H.%M.%S_%m.%d.%y')}.xlsx")
           self.listWidget.addItem('\n')
           self.listWidget.addItem('Measurements Saved! :)')
           self.listWidget.scrollToBottom()
           QCoreApplication.processEvents()

   def pushButton4clicked(self):
       time = list(self.measurements_df['Time'])
       distance = list(self.measurements_df['Distance'])
       force = list(self.measurements_df['Weight'])
       self.plot1.ax.clear()
       self.plot1.ax.plot(time, distance, color='#AB47BC', label="Distance")
       self.plot1.ax.plot(time, force, color='#000000', label="Force")
       self.plot1.ax.set_xlabel('Time [s]')
       self.plot1.ax.set_ylabel('Distance & Force')
       self.plot1.ax.set_title("Distance & Force Measurement")
       self.plot1.ax.legend()
       self.plot1.draw()

   def pushButton5clicked(self):
       pass
       self.plot1.fig.savefig(f'ForceDistance_Plot_{dt.datetime.now().strftime("%H.%M.%S_%m.%d.%Y")}.png')
       self.listWidget.addItem('\n')
       self.listWidget.addItem('Plot Saved! :)')
       self.listWidget.scrollToBottom()
       QCoreApplication.processEvents()

   def pushButton6clicked(self):
       self.arduino.close()
       self.lineEdit1.clear()
       self.lineEdit2.clear()
       self.listWidget.clear()
       self.plot1.ax.clear()
       self.plot1.draw()
       self.listWidget.addItem('Done resetting. You can start over. \n')
       QCoreApplication.processEvents()


class Electronic(QtWidgets.QMainWindow, Ui_Electronic):

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.setupUi(self)
       self.setWindowTitle("Electronic Measurements")

       self.measuements = []
       self.start_measure = 0
       self.measurements_df = pd.DataFrame(columns=['No.', 'Frequency', 'Abs(Z)', 'Phase', 'Capacitance', 'Re(Z)', 'Im(Z)'])

       self.plot2 = MplCanvas(self, width=8, height=5, dpi=100)
       toolbar = NavigationToolbar(self.plot2, self)
       self.verticalLayout2.addWidget(toolbar)
       self.verticalLayout2.addWidget(self.plot2)

       self.comboBox2.addItems(Motor.ComportAvailable())
       self.comboBox3.addItems(['Frequency', 'Time', 'Re(Z)'])
       self.comboBox4.addItems(['Abs(Z)', 'Im(Z)', 'Re(Z)', 'Phase', 'Capacitance'])

       self.pushButton2.clicked.connect(self.pushButton2clicked)
       self.pushButton3.clicked.connect(self.pushButton3clicked)
       self.pushButton4.clicked.connect(self.pushButton4clicked)
       self.pushButton5.clicked.connect(self.pushButton5clicked)
       self.pushButton6.clicked.connect(self.pushButton6clicked)
       self.pushButton7.clicked.connect(self.pushButton7clicked)

   def pushButton2clicked(self):
       print(self.comboBox2.currentText())
       self.listWidget.clear()
       self.ADBoardm = ADBoard.ADBoardConnect(self.comboBox2.currentText(), 230400)
       self.listWidget.addItem('Successfully connected to ADuCM3029.\n')
       QCoreApplication.processEvents()

   def pushButton3clicked(self):
       self.listWidget.addItem('Preparing measurement, please wait: \n')
       QCoreApplication.processEvents()
       self.measurements = []
       while True:
           meas = ADBoard.ADBoardRead(self.ADBoardm)
           if meas == 'end' and len(self.measurements) == 0:
               self.start_measure = 1
           elif meas == 'end' and len(self.measurements) != 0:
               self.start_measure = 0
               break
           elif meas != 'end' and self.start_measure == 1:
               self.measurements.append(list(map(float, meas.split(','))))
               df_length = len(self.measurements_df)
               self.measurements_df.loc[df_length] = self.measurements[-1]
               self.listWidget.addItem(meas)
               self.listWidget.scrollToBottom()
               QCoreApplication.processEvents()
           else:
               self.listWidget.addItem('.')
               QCoreApplication.processEvents()
               self.listWidget.scrollToBottom()
       self.measurements_df.set_index('No.', inplace=True)

   def pushButton4clicked(self):
       if self.measurements_df.empty:
           pass
       else:
           self.measurements_df.to_excel(f"impedance_meas_{dt.datetime.now().strftime('%H.%M.%S_%m.%d.%y')}.xlsx")
           self.listWidget.addItem('\n')
           self.listWidget.addItem('Measurements Saved! :)')

   def pushButton5clicked(self):
       x_axis = self.comboBox3.currentText()
       y_axis = self.comboBox4.currentText()
       self.update_plot(self.measurements_df[x_axis], self.measurements_df[y_axis])

   def update_plot(self, x_vals, y_vals):
       self.plot2.ax.clear()

       if self.checkBox1.isChecked():
           self.plot2.ax.set_xscale('log')

       if self.checkBox2.isChecked():
           self.plot2.ax.set_yscale('log')

       self.plot2.ax.plot(x_vals, y_vals, color='#AB47BC')
       self.plot2.ax.set_xlabel(self.comboBox3.currentText())
       self.plot2.ax.set_ylabel(self.comboBox4.currentText())
       self.plot2.ax.set_title(f"{self.comboBox3.currentText()} vs {self.comboBox4.currentText()} measurement")
       self.plot2.draw()

   def pushButton6clicked(self):
       self.plot2.fig.savefig(f'Plot_{dt.datetime.now().strftime("%H.%M.%S_%m.%d.%Y")}.png')
       self.listWidget.addItem('\n')
       self.listWidget.addItem('Plot Saved! :)')
       self.listWidget.scrollToBottom()
       QCoreApplication.processEvents()

   def pushButton7clicked(self):
       self.ADBoardm.close()
       self.listWidget.clear()
       self.listWidget.addItem('Done resetting. You can start over. \n')
       QCoreApplication.processEvents()

if __name__ == '__main__':
   app = QtWidgets.QApplication(sys.argv)
   window = Menu()
   app.setWindowIcon(QtGui.QIcon('pictures\\UpcLogo.png'))
   # setup stylesheet
   apply_stylesheet(app, theme='dark_purple.xml')
   window.show()
   app.exec_()
