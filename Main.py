#############################################
###### ALL RIGHTS RESERVED TO PT INKA #######
########## HANSEL MATTHEW FTUI'18 ###########
####### KEMAS M RIZKI FADHILA FTUI'18 #######
#############################################

# Main program
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtGui

import sys
import csv
from datetime import datetime
import os.path

#Taskbar icon
import ctypes

#Calculator
import numpy as np
from scipy import constants

#Exporter
from fpdf import FPDF

#Plotter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import ( NavigationToolbar2QT  as  NavigationToolbar )
from matplotlib.figure import Figure

import logo_rc

# Program Input Window
from datetime import datetime

#Global variabel
p_motor = 0.0
final_gr = 0.0
e_battery = 0.0
p_battery = 0.0
highacc_const_t = 0.0
const_t = 0.0
kec_max_rpm = 0.0
theta_percentage = 0.0
lebar = 0.0
tinggi = 0.0
ca = 0.0
af = 0.0
kode = ""
jari_jari = 0.0
massa_kosong = 0.0
massa_isi = 0.0
massa_total = 0.0
gearbox = 0.0
axle = 0.0
mech_eff = 0.0
crr = 0.0
cd = 0.0
rho = 0.0
vw = 0.0
g = 0.0
ca = 0.0
v_cruise = 0.0
s_cruise = 0.0
cruise_percentage = 0.0
p_auxiliary = 0.0
t_cruise = 0.0
pt_cruise = 0.0
p_cruise = 0.0
wp = 0.0
avg_accel_real = 0.0
highacc_wp = 0.0

#Class PDF
class PDF(FPDF):
    def pdfer(self):

        #Halaman 1
        self.add_page()

        self.set_xy(10.0,0.0)
        self.image('logo.png',  link='', type='', w=700/15, h=450/15)

        #Set Warna
        self.set_text_color(0, 0, 0)\
        
        #Judul
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.cell(w=210.0, h=40.0, align='C', txt="PERFORMANCE REPORT", border=0)

        #Design Summary
        self.set_xy(10.0,35.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Design Summary", border=0)

        self.set_xy(10.0,45.0)
        self.set_font('Arial', '', 11)
        self.cell(w=0.0, h=0.0, align='L', txt="Motor Power = " + str(round(p_motor,3)) , border=0)

        self.set_xy(10.0,50.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Motor Nom Torque =" + str(round(const_t,3)), border=0)

        self.set_xy(10.0,55.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Motor Peak Torque =" + str(round(highacc_const_t,3)), border=0)

        self.set_xy(10.0,60.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Motor RPM =" + str(round(kec_max_rpm,3)), border=0)

        self.set_xy(100.0,45.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Gradeability =" + str(round(theta_percentage,3)), border=0)
        
        self.set_xy(100.0,50.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Battery Power = " + str(round(p_battery,3)), border=0)

        self.set_xy(100.0,55.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Battery Energy = " + str(round(e_battery,3)), border=0)

        self.set_xy(100.0,60.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Final Gear Ratio = " + str(round(final_gr,3)), border=0)

        #Grafik Motor Running Resistance
        self.set_xy(10.0,70.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik  Motor Running Resistance", border=0)

        self.set_xy(40.0,75.0)
        self.image('plot_motorrunres.png',  link='', type='', w=700/5, h=450/5)

        #Parameter Kendaraan
        self.set_xy(10.0,170.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Parameter Kendaraan", border=0)

        self.set_xy(10.0,180.0)
        self.set_font('Arial', '', 11)
        self.cell(w=0.0, h=0.0, align='L', txt="Lebar Kendaraan = " + str(round(lebar,3)), border=0)

        self.set_xy(10.0,185.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Tinggi Kendaraan = " + str(round(tinggi,3)), border=0)

        self.set_xy(10.0,190.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Ca = " + str(round(ca,3)), border=0)

        self.set_xy(10.0,195.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Af = " + str(round(af,3)), border=0)

        self.set_xy(10.0,205.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Kode Ban = " + kode, border=0)

        self.set_xy(10.0,210.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Jari - jari Ban = " + str(round(jari_jari,3)), border=0)

        self.set_xy(100.0,180.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Massa Kosong = " + str(round(massa_kosong,3)), border=0)

        self.set_xy(100.0,185.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Massa Isi = " + str(round(massa_isi,3)), border=0)

        self.set_xy(100.0,190.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Massa Total = " + str(round(massa_total,3)), border=0)

        self.set_xy(100.0,200.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Gear Box = " + str(round(gearbox,3)), border=0)
        
        self.set_xy(100.0,205.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Axle = " + str(round(axle,3)), border=0)

        self.set_xy(100.0,210.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Final GR = " + str(round(final_gr,3)), border=0)

        self.set_xy(150.0,200.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Mech Eff = " + str(round(mech_eff,3)), border=0)

        #Dinamika Bergerak
        self.set_xy(10.0,220.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Dinamika Bergerak", border=0)

        self.set_xy(10.0,230.0)
        self.set_font('Arial', '', 11)
        self.cell(w=0.0, h=0.0, align='L', txt="Rolling Resistance = " + str(round(crr,3)), border=0)

        self.set_xy(10.0,235.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Drag Resistance = " + str(round(cd,3)), border=0)

        self.set_xy(10.0,240.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Massa Jenis Udara = " + str(round(rho,3)), border=0)

        self.set_xy(100.0,230.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Kecepatan Angin = " + str(round(ca,3)), border=0)

        self.set_xy(100.0,235.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Percepatan Gravitasi = " + str(round(g,3)), border=0)

        self.set_xy(100.0,240.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Acceleration Margin = " + str(round(ca,3)), border=0)

        #Halaman 2
        self.add_page()

        #Vehicle Running Resistance
        self.set_xy(10.0,10.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik Vehicle Running Resistance", border=0)

        self.set_xy(30.0,15.0)
        self.image('rumus_vehiclerunres.png',  link='', type='', w=150, h=25)

        self.set_xy(40.0,40.0)
        self.image('plot_vehiclerunres.png',  link='', type='', w=700/5, h=450/5)

        #Wheel Running Resistance
        self.set_xy(10.0,145.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik Wheel Running Resistance", border=0)

        self.set_xy(30.0,150.0)
        self.image('rumus_wheelrunres.png',  link='', type='',w=150, h=25)

        self.set_xy(40.0,175.0)
        self.image('plot_wheelrunres.png',  link='', type='', w=700/5, h=450/5)

        #Halaman 3
        self.add_page()

        #Motor Running Resistance
        self.set_xy(10.0,10.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik Motor Side Running Resistance", border=0)

        self.set_xy(30.0,15.0)
        self.image('rumus_motorrunres.png',  link='', type='', w=150, h=25)

        self.set_xy(40.0,40.0)
        self.image('plot_motorrunres.png',  link='', type='', w=700/5, h=450/5)

        #Kebutuhan Power
        self.set_xy(10.0,150.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Kebutuhan Power", border=0)

        self.set_xy(30.0,155.0)
        self.image('rumus_kebutuhangaya.png',  link='', type='', w=150, h=30)

        self.set_xy(10.0,190.0)
        self.set_font('Arial', '', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Const T = " + str(round(const_t,3)), border=0)

        self.set_xy(10.0,195.0)
        self.cell(w=0.0, h=0.0, align='L', txt="High Acc Const T = " + str(round(highacc_const_t,3)), border=0)

        self.set_xy(10.0,200.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Weakening Point = " + str(round(wp,3)), border=0)

        self.set_xy(100.0,190.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Avg Acc = " + str(round(avg_accel_real,3)), border=0)

        self.set_xy(100.0,195.0)
        self.cell(w=0.0, h=0.0, align='L', txt="P Motor = " + str(round(p_motor,3)), border=0)

        self.set_xy(100.0,200.0)
        self.cell(w=0.0, h=0.0, align='L', txt="High Acc Weakening Point = " + str(round(highacc_wp,3)), border=0)

        #Halaman 4
        self.add_page()

        #Vehicle Force Running Resistance
        self.set_xy(10.0,10.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik Vehicle Force Running Resistance", border=0)

        self.set_xy(40.0,20.0)
        self.image('plot_vehicleforce.png',  link='', type='', w=700/5, h=450/5)

        #Wheel Torque Running Resistance
        self.set_xy(10.0,120.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik Wheel Torque Running Resistance", border=0)

        self.set_xy(40.0,130.0)
        self.image('plot_wheeltorque.png',  link='', type='', w=700/5, h=450/5)

        #Halaman 5
        self.add_page()

        #Motor Force Running Resistance
        self.set_xy(10.0,10.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik Motor Torque Running Resistance", border=0)

        self.set_xy(40.0,20.0)
        self.image('plot_motortorque.png',  link='', type='', w=700/5, h=450/5)
        
        #Kebutuhan Energi
        self.set_xy(10.0,120.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Kebutuhan Energi", border=0)

        self.set_xy(10.0,130.0)
        self.set_font('Arial', '', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="V Cruise = " + str(round(v_cruise,3)), border=0)

        self.set_xy(10.0,135.0)
        self.cell(w=0.0, h=0.0, align='L', txt="S Cruise = " + str(round(s_cruise,3)), border=0)

        self.set_xy(10.0,140.0)
        self.cell(w=0.0, h=0.0, align='L', txt="t Cruise = " + str(round(t_cruise,3)) , border=0)

        self.set_xy(10.0,145.0)
        self.cell(w=0.0, h=0.0, align='L', txt="% Cruise = " + str(round(cruise_percentage,3)) , border=0)

        self.set_xy(80.0,130.0)
        self.cell(w=0.0, h=0.0, align='L', txt="Pt Cruise = " + str(round(pt_cruise,3)) , border=0)

        self.set_xy(80.0,135.0)
        self.cell(w=0.0, h=0.0, align='L', txt="P Aux = " + str(round(p_auxiliary,3)), border=0)

        self.set_xy(80.0,140.0)
        self.cell(w=0.0, h=0.0, align='L', txt="P Cruise = " + str(round(p_cruise,3)), border=0)

        self.set_xy(150.0,130.0)
        self.cell(w=0.0, h=0.0, align='L', txt="E Battery = " + str(round(e_battery,3)), border=0)

        self.set_xy(150.0,135.0)
        self.cell(w=0.0, h=0.0, align='L', txt="P Battery = " + str(round(p_battery,3)), border=0)

        #Grafik Motor Cruise Running Resistance
        self.set_xy(10.0,155.0)
        self.set_font('Arial', 'B', 12)
        self.cell(w=0.0, h=0.0, align='L', txt="Grafik Motor Cruise Running Resistance", border=0)

        self.set_xy(40.0,165.0)
        self.image('plot_cruisetorque.png',  link='', type='', w=700/5, h=450/5)


class runres_calc (QMainWindow) :
    def __init__(self):
        #Load qt & gui
        QMainWindow.__init__(self)
        loadUi("runres_calc.ui",self)

        #Gui title & logo
        self.setWindowTitle("Vehicle Performance Calculator")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        
        #Display gui maximized
        self.showMaximized()
        
        #Button method
        self.TombolCalculate.clicked.connect(self.calculate_pressed)
        self.TombolExport.clicked.connect(self.export_pressed)

    def calculate_pressed(self):
        #Parameter Kendaraan
        global lebar, tinggi, ca, af,kode, jari_jari
        global massa_kosong, massa_isi, massa_total
        global gearbox, axle, mech_eff,final_gr
        global kec_max_kmh, kec_operasi_kmh, kec_max_rpm
        global p_motor, theta_percentage
        global e_battery, p_battery, wp
        global highacc_const_t,const_t
        global v_cruise, s_cruise, cruise_percentage, p_auxiliary, t_cruise, pt_cruise, p_cruise
        global avg_accel_real, highacc_wp

        #Parameter Lingkungan
        global t_ramp, theta
        global crr, cd, rho, vw, g, ca

        #Konstanta pi
        pi = np.pi

        #Input parameter keendaraan    
        lebar     = float(self.input_lebar.text())
        tinggi    = float(self.input_tinggi.text())
        ca        = float(self.input_ca.text())
        af        = float(self.input_af.text())

        kode      = self.input_kode.text()
        jari_jari = float(self.input_jari_jari.text())

        massa_kosong = float(self.input_massa_kosong.text())
        massa_isi    = float(self.input_massa_isi.text())
        massa_total  = massa_kosong + massa_isi

        gearbox  = float(self.input_gearbox.text())
        axle     = float(self.input_axle.text())
        mech_eff = float(self.input_mech_eff.text())
        final_gr = gearbox * axle

        #Input dinamika bergerak
        kec_max_kmh     = float(self.input_kec_max_kmh.text())
        kec_operasi_kmh = float(self.input_kec_ops_kmh.text())
        kec_max_rpm     = final_gr*30*(kec_max_kmh/3.6)/pi/jari_jari
        kec_ops_rpm     = final_gr*30*(kec_operasi_kmh/3.6)/pi/jari_jari

        t_ramp  = float(self.input_t_ramp.text())
        accel   = kec_max_kmh/3.6/t_ramp
        theta   = float(self.input_theta.text())
        theta_percentage = np.tan(np.radians(theta))*100

        #Input koefisien
        crr = float(self.input_crr.text())
        cd  = float(self.input_cd.text())
        rho = float(self.input_rho.text())
        vw  = float(self.input_vw.text())
        g   = float(self.input_g.text())
        ca  = float(self.input_ca.text())

        #Input kebutuhan power (const t ditentukan dari pasangan kecepatan dan gradien)
        wp                  = float(self.input_wp.text())
        v_cruise            = float(self.input_v_cruise.text())
        s_cruise            = float(self.input_s_cruise.text())
        cruise_percentage   = float(self.input_cruise_percentage.text())
        p_auxiliary         = float(self.input_p_auxiliary.text())

        #Display info dasar
        self.output_massa_total.setText(str(round(massa_total,3)))
        self.output_final_gr.setText(str(round(final_gr,3)))
        self.output_kec_max_rpm.setText(str(round(kec_max_rpm,3)))
        self.output_kec_ops_rpm.setText(str(round(kec_ops_rpm,3)))
        self.output_accel.setText(str(round(accel,3)))
        self.output_theta_percentage.setText(str(round(theta_percentage,3)))

        #Menghitung Running Resistance
        v_runres = np.arange(0,121,1)
        jumlah_variasi = int(self.jumlah_variasi.text())
        variasi_array = np.arange(0,jumlah_variasi+1,1)
        pengali = variasi_array/jumlah_variasi
        gradien = np.full(shape=len(variasi_array),fill_value=theta,dtype=int)*pengali
        
        rd = rho/2*af*cd*np.square((v_runres/3.6+vw/3.6))
        rg = massa_total*g*np.sin(np.radians(gradien))
        rrr = massa_total*crr*g*np.cos(np.radians(gradien))

        runres_vehicle = np.array([])
        for i in range (0,len(variasi_array)):
            temp = rd+rg[i]+rrr[i]
            runres_vehicle = np.concatenate((runres_vehicle,temp))
        runres_vehicle = np.reshape(runres_vehicle,(len(v_runres),len(variasi_array)),order='F')
        runres_wheel = runres_vehicle * jari_jari
        runres_motor = runres_wheel/final_gr
        
        # Menghitung Const t
        tractive_effort_n_gradien = massa_total*accel + runres_vehicle
        tractive_effort_nm_gradien  = tractive_effort_n_gradien*jari_jari
        tractive_effort_motor_torque_gradien = tractive_effort_nm_gradien/final_gr/mech_eff

        gradien_const_t           = int(self.gradien_const_t.text())
        kecepatan_const_t         = int(self.kecepatan_const_t.text())
        gradien_highacc_const_t   = int(self.gradien_highacc_const_t.text())
        kecepatan_highacc_const_t = int(self.kecepatan_highacc_const_t.text())

        const_t         = tractive_effort_motor_torque_gradien[kecepatan_const_t,gradien_const_t]
        highacc_const_t = tractive_effort_motor_torque_gradien[kecepatan_highacc_const_t,gradien_highacc_const_t]

        #Display const T
        self.output_const_t .setText(str(round(const_t ,3)))
        self.output_highacc_const_t .setText(str(round(highacc_const_t ,3)))

        #Menghitung Vehicle Force       
        const_f = const_t*final_gr/jari_jari*gearbox
        v_wp    = wp/3.6
        const_p = const_f*v_wp

        const_p_real = const_p/(v_runres[1:]/3.6)
        const_p_real = np.insert(const_p_real,0,const_p_real[0])
        const_f_real = np.full(shape=len(const_p_real),fill_value=const_f,dtype=np.int)

        const_fp_real = np.concatenate((const_f_real,const_p_real))
        const_fp_real = np.reshape(const_fp_real,(len(const_p_real),2),order='F')

        #Menghitung Tractive Effort
        vehicle_force       = const_fp_real.min(axis=1)
        wheel_torque        = vehicle_force*jari_jari
        motor_torque        = wheel_torque/final_gr/mech_eff
        motor_cruise_torque = motor_torque*cruise_percentage/100

        vehicle_force_arr = vehicle_force.reshape(vehicle_force.shape[0],-1)
        temp = vehicle_force_arr
        for i in range (0,jumlah_variasi):
            vehicle_force_arr = np.concatenate((vehicle_force_arr,temp),axis=1)

        accel_real     = np.subtract(vehicle_force_arr,runres_vehicle)/massa_total
        for i in range (len(accel_real)):
            if accel_real[i,0] < 0:
                break
            idx = i
        avg_accel_real  = accel_real[:idx,0].mean()
        p_motor         = (const_t*mech_eff*final_gr/jari_jari)*(wp/3.6)/1000
        highacc_wp = 3.6*p_motor*1000*jari_jari/highacc_const_t/final_gr

        #Display variabel gui
        self.output_avg_accel.setText(str(round(avg_accel_real ,3)))
        self.output_p_motor.setText(str(round(p_motor ,3)))
        self.output_highacc_wp.setText(str(round(highacc_wp ,3)))
        self.output_grad_const_t.setText(str(round(gradien[gradien_const_t ] ,3)))
        self.output_grad_highacc_const_t.setText(str(round(gradien[gradien_highacc_const_t ] ,3)))

        #Tractive Effort Calculation
        const_f_peak = highacc_const_t*final_gr/jari_jari*mech_eff
        v_wp_peak    = highacc_wp/3.6
        const_p_peak = const_f_peak*v_wp_peak
        const_p_peak_real = const_p_peak/(v_runres[1:]/3.6)
        const_p_peak_real = np.insert(const_p_peak_real,0,const_p_peak_real[0])
        const_f_peak_real = np.full(shape=len(const_p_peak_real),fill_value=const_f_peak,dtype=np.int)
        const_fp_peak_real = np.concatenate((const_f_peak_real,const_p_peak_real))
        const_fp_peak_real = np.reshape(const_fp_peak_real,(len(const_p_peak_real),2),order='F')
        vehicle_force_peak       = const_fp_peak_real.min(axis=1)
        wheel_torque_peak        = vehicle_force_peak*jari_jari
        motor_torque_peak        = wheel_torque_peak/final_gr/mech_eff
        motor_cruise_torque_peak = motor_torque_peak*cruise_percentage/100

        #Cruise Info
        t_cruise                 = s_cruise/v_cruise
        pt_cruise                = cruise_percentage/100*p_motor
        p_cruise                 = pt_cruise + p_auxiliary
        e_battery                = t_cruise*p_cruise
        p_battery                = p_auxiliary + p_motor

        #Display variabel gui
        self.output_t_cruise.setText(str(round(t_cruise,3)))
        self.output_pt_cruise.setText(str(round(pt_cruise,3)))
        self.output_p_cruise.setText(str(round(p_cruise,3)))
        self.output_e_battery.setText(str(round(e_battery,3)))
        self.output_p_battery.setText(str(round(p_battery,3)))

        #Plot grafik di GUI
        self.RunresVehicle.canvas.ax.clear()
        for i in range (0,len(variasi_array)):
            self.RunresVehicle.canvas.ax.plot(v_runres,runres_vehicle[:,i],label = "Runres " + str(gradien[i])+ "'")
        self.RunresVehicle.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresVehicle.canvas.ax.set_ylabel("Force (N)")
        self.RunresVehicle.canvas.ax.set_title("Vehicle Running Resistance",loc='left')
        self.RunresVehicle.canvas.ax.legend(bbox_to_anchor=[1.05, 1.1], loc='upper right',fontsize='xx-small')
        self.RunresVehicle.canvas.ax.grid()
        self.RunresVehicle.canvas.figure.tight_layout()
        self.RunresVehicle.canvas.draw()

        self.RunresWheel.canvas.ax.clear()
        for i in range (0,len(variasi_array)):
            self.RunresWheel.canvas.ax.plot(v_runres,runres_wheel[:,i],label = "Runres " + str(gradien[i])+ "'")
        self.RunresWheel.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresWheel.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresWheel.canvas.ax.set_title("Wheel Running Resistance",loc='left')
        self.RunresWheel.canvas.ax.legend(bbox_to_anchor=[1.05, 1.1], loc='upper right',fontsize='xx-small')
        self.RunresWheel.canvas.ax.grid()
        self.RunresWheel.canvas.figure.tight_layout()
        self.RunresWheel.canvas.draw()

        self.RunresMotor.canvas.ax.clear()
        for i in range (0,len(variasi_array)):
            self.RunresMotor.canvas.ax.plot(v_runres,runres_motor[:,i],label = "Runres " + str(gradien[i])+ "'")
        self.RunresMotor.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresMotor.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresMotor.canvas.ax.set_title("Motor Running Resistance",loc='left')
        self.RunresMotor.canvas.ax.legend(bbox_to_anchor=[1.05, 1.1], loc='upper right',fontsize='xx-small')
        self.RunresMotor.canvas.ax.grid()
        self.RunresMotor.canvas.figure.tight_layout()
        self.RunresMotor.canvas.draw()

        self.RunresVehicleForce.canvas.ax.clear()
        for i in range (0,len(variasi_array)):
            self.RunresVehicleForce.canvas.ax.plot(v_runres,runres_vehicle[:,i],label = "Runres " + str(gradien[i])+ "'")
        self.RunresVehicleForce.canvas.ax.plot(v_runres,vehicle_force,label="Force")
        self.RunresVehicleForce.canvas.ax.plot(v_runres,vehicle_force_peak,linestyle='--',label="Force Peak")
        self.RunresVehicleForce.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresVehicleForce.canvas.ax.set_ylabel("Force (N)")
        self.RunresVehicleForce.canvas.ax.set_title("Vehicle Running Resistance",loc='left')
        self.RunresVehicleForce.canvas.ax.legend(bbox_to_anchor=[1.05, 1.1], loc='upper right',fontsize='xx-small')
        self.RunresVehicleForce.canvas.ax.grid()
        self.RunresVehicleForce.canvas.figure.tight_layout()
        self.RunresVehicleForce.canvas.draw()

        self.RunresWheelForce.canvas.ax.clear()
        for i in range (0,len(variasi_array)):
            self.RunresWheelForce.canvas.ax.plot(v_runres,runres_wheel[:,i],label = "Runres " + str(gradien[i])+ "'")
        self.RunresWheelForce.canvas.ax.plot(v_runres,wheel_torque,label="Torque")
        self.RunresWheelForce.canvas.ax.plot(v_runres,wheel_torque_peak,linestyle='--',label="Torque Peak")
        self.RunresWheelForce.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresWheelForce.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresWheelForce.canvas.ax.set_title("Wheel Running Resistance",loc='left')
        self.RunresWheelForce.canvas.ax.legend(bbox_to_anchor=[1.05, 1.1], loc='upper right',fontsize='xx-small')
        self.RunresWheelForce.canvas.ax.grid()
        self.RunresWheelForce.canvas.figure.tight_layout()
        self.RunresWheelForce.canvas.draw()

        self.RunresMotorForce.canvas.ax.clear()
        for i in range (0,len(variasi_array)):
            self.RunresMotorForce.canvas.ax.plot(v_runres,runres_motor[:,i],label = "Runres " + str(gradien[i])+ "'")
        self.RunresMotorForce.canvas.ax.plot(v_runres,motor_torque,label="Torque")
        self.RunresMotorForce.canvas.ax.plot(v_runres,motor_torque_peak,linestyle='--',label="Torque Peak")
        self.RunresMotorForce.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresMotorForce.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresMotorForce.canvas.ax.set_title("Motor Running Resistance",loc='left')
        self.RunresMotorForce.canvas.ax.legend(bbox_to_anchor=[1.05, 1.1], loc='upper right',fontsize='xx-small')
        self.RunresMotorForce.canvas.ax.grid()
        self.RunresMotorForce.canvas.figure.tight_layout()
        self.RunresMotorForce.canvas.draw()

        self.RunresMotorCruise.canvas.ax.clear()
        for i in range (0,len(variasi_array)):
            self.RunresMotorCruise.canvas.ax.plot(v_runres, runres_motor[:,i],label = "Runres " + str(gradien[i])+ "'");
        self.RunresMotorCruise.canvas.ax.plot(v_runres,motor_torque,label="Torque")
        self.RunresMotorCruise.canvas.ax.plot(v_runres,motor_cruise_torque,label="Cruise Torque")
        self.RunresMotorCruise.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresMotorCruise.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresMotorCruise.canvas.ax.set_title("Motor Running Resistance",loc='left')
        self.RunresMotorCruise.canvas.ax.grid()
        self.RunresMotorCruise.canvas.ax.legend(bbox_to_anchor=[1.05, 1.1], loc='upper left',fontsize='xx-small')
        self.RunresMotorCruise.canvas.figure.tight_layout()
        self.RunresMotorCruise.canvas.draw()

        #Plot grafik dan disave .png untuk pdf
        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_vehicle[:,i],label = "Runres " + str(gradien[i])+ "'");
        ax.set(xlabel='Speed (km/h)', ylabel='Force (N)', title='Vehicle Running Resistance');
        ax.legend(bbox_to_anchor=[1.1, 1.1], loc='upper right',fontsize='xx-small')
        fig.savefig("plot_vehiclerunres.png")
        
        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_wheel[:,i],label = "Runres " + str(gradien[i])+ "'");
        ax.set(xlabel='Speed (km/h)', ylabel='Torque (Nm)', title='Wheel Running Resistance');
        ax.legend(bbox_to_anchor=[1.1, 1.1], loc='upper right',fontsize='xx-small')
        fig.savefig("plot_wheelrunres.png")

        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_motor[:,i],label = "Runres " + str(gradien[i])+ "'");
        ax.set(xlabel='Speed (km/h)', ylabel='Torque (Nm)', title='Motor Running Resistance');
        ax.legend(bbox_to_anchor=[1.1, 1.1], loc='upper right',fontsize='xx-small')
        fig.savefig("plot_motorrunres.png")

        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_vehicle[:,i],label = "Runres " + str(gradien[i])+ "'");
        ax.plot(v_runres,vehicle_force,label = "Force")
        ax.plot(v_runres,vehicle_force_peak,linestyle='--', label = "Force Peak")
        ax.set(xlabel='Speed (km/h)', ylabel='Force (N)', title='Vehicle Running Resistance');
        ax.legend(bbox_to_anchor=[1.1, 1.1], loc='upper right',fontsize='xx-small')
        fig.savefig("plot_vehicleforce.png")

        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_wheel[:,i],label = "Runres " + str(gradien[i])+ "'");
        ax.plot(v_runres,wheel_torque,label = "Torque")
        ax.plot(v_runres,wheel_torque_peak,linestyle='--', label = "Torque Peak")
        ax.set(xlabel='Speed (km/h)', ylabel='Torque (Nm)', title='Wheel Running Resistance');
        ax.legend(bbox_to_anchor=[1.1, 1.1], loc='upper right',fontsize='xx-small')
        fig.savefig("plot_wheeltorque.png")

        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_motor[:,i],label = "Runres " + str(gradien[i])+ "'");
        ax.plot(v_runres,motor_torque,label = "Torque")
        ax.plot(v_runres,motor_torque_peak,linestyle='--', label = "Torque Peak")
        ax.set(xlabel='Speed (km/h)', ylabel='Torque (Nm)', title='Motor Running Resistance');
        ax.legend(bbox_to_anchor=[1.1, 1.1], loc='upper right',fontsize='xx-small')
        fig.savefig("plot_motortorque.png")

        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_motor[:,i],label = "Runres " + str(gradien[i])+ "'");
        ax.plot(v_runres,motor_torque,label = "Torque")
        ax.plot(v_runres,motor_cruise_torque,linestyle='--', label = "Cruise Torque")
        ax.set(xlabel='Speed (km/h)', ylabel='Torque (Nm)', title='Motor Running Resistance');
        ax.legend(bbox_to_anchor=[1.1, 1.1], loc='upper right',fontsize='xx-small')
        fig.savefig("plot_cruisetorque.png")

        fig = plt.figure("Line Plot")
        legendFig = plt.figure("Legend plot")
        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
           ax.plot(v_runres, runres_vehicle[:,i],label = "Runres " + str(gradien[i]) + "'");
        ax.plot(v_runres, vehicle_force,label = "Vehicle Force (N)")
        ax.plot(v_runres, vehicle_force_peak,linestyle='--',label = "Vehicle Force Peak (N)")
        handles, labels = ax.get_legend_handles_labels()
        legendFig.legend(handles, labels)
        legendFig.savefig('legend.png')

    def export_pressed(self):
        #Get desktop address
        userhome_address = os.path.expanduser('~')
        desktop_address = userhome_address + '/Desktop/report.pdf'

        #Make pdf
        pdf = PDF(orientation='P', unit='mm', format='A4')
        pdf.pdfer()
        pdf.output(desktop_address,'F')

#Make Qt Object
app = QApplication([])
mainwindow = runres_calc()
app.setQuitOnLastWindowClosed(True)

#Untuk icon taskbar
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

sys.exit(app.exec_())