
# Main program
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtGui

import sys
import csv
from datetime import datetime
import os.path

import atexit

import ctypes

# Plotter
import numpy as np
from scipy import constants

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import ( NavigationToolbar2QT  as  NavigationToolbar )
from matplotlib.figure import Figure

import logo_rc

# Program Input Window
from datetime import datetime

# lebar   = 0.0
# tinggi  = 0.0
# ca      = 0.0
# af      = 0.0
# kode    = 'string'
# jari_jari   = 0.0
# massa_kosong    = 0.0
# massa_kosong    = 0.0
# axle            = 0.0
# mech_eff        = 0.0
# kec_max_kmh = 0.0
# kec_operasi_kmh = 0.0
# t_ramp = 0.0
# theta = 0.0
# crr = 0.0
# cd = 0.0
# rho = 0.0
# g = 0.0
# ca = 0.0
# const_t         = 908.19
# highacc_const_t = 1251.89
# wp              = 35

# v_cruise            = 60
# s_cruise            = 200
# cruise_percentage   = 33

class runres_calc (QMainWindow) :
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("runres_calc.ui",self)
        self.setWindowTitle("Vehicle Performance Calculator")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.showMaximized()
        #App Selection
        self.TombolCalculate.clicked.connect(self.calculate_pressed)

    def calculate_pressed(self):
        #Parameter Kendaraan
        global lebar, tinggi, ca, af,kode, jari_jari
        global massa_kosong, massa_isi
        global gearbox, axle, mech_eff
        global kec_max_kmh, kec_operasi_kmh

        #Parameter Lingkungan
        global t_ramp, theta
        global crr, cd, rho, vw, g, ca

        pi = np.pi
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

        kec_max_kmh     = float(self.input_kec_max_kmh.text())
        kec_operasi_kmh = float(self.input_kec_ops_kmh.text())
        kec_max_rpm     = final_gr*30*(kec_max_kmh/3.6)/pi/jari_jari
        kec_ops_rpm     = final_gr*30*(kec_operasi_kmh/3.6)/pi/jari_jari


        t_ramp  = float(self.input_t_ramp.text())
        accel   = kec_max_kmh/3.6/t_ramp
        theta   = float(self.input_theta.text())
        theta_percentage = np.tan(np.radians(theta))*100

        crr = float(self.input_crr.text())
        cd  = float(self.input_cd.text())
        rho = float(self.input_rho.text())
        vw  = float(self.input_vw.text())
        g   = float(self.input_g.text())
        ca  = float(self.input_ca.text())


 
        # const_t         = float(self.input_const_t.text())
        # highacc_const_t = float(self.input_highacc_const_t.text())
        wp              = float(self.input_wp.text())

        v_cruise            = float(self.input_v_cruise.text())
        s_cruise            = float(self.input_s_cruise.text())
        cruise_percentage   = float(self.input_cruise_percentage.text())
        p_auxiliary         = float(self.input_p_auxiliary.text())

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

        print(gradien)

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

        self.output_const_t .setText(str(round(const_t ,3)))
        self.output_highacc_const_t .setText(str(round(highacc_const_t ,3)))

        # Mencari Vehicle Force       
        const_f = const_t*final_gr/jari_jari*gearbox
        v_wp    = wp/3.6
        const_p = const_f*v_wp

        const_p_real = const_p/(v_runres[1:]/3.6)
        const_p_real = np.insert(const_p_real,0,const_p_real[0])
        const_f_real = np.full(shape=len(const_p_real),fill_value=const_f,dtype=np.int)

        const_fp_real = np.concatenate((const_f_real,const_p_real))
        const_fp_real = np.reshape(const_fp_real,(len(const_p_real),2),order='F')

        #Tractive Effort
        vehicle_force       = const_fp_real.min(axis=1)
        wheel_torque        = vehicle_force*jari_jari
        motor_torque        = wheel_torque/final_gr/mech_eff
        motor_cruise_torque = motor_torque*cruise_percentage/100



        vehicle_force_arr = vehicle_force.reshape(vehicle_force.shape[0],-1)
        temp = vehicle_force_arr
        for i in range (0,jumlah_variasi):
            vehicle_force_arr = np.concatenate((vehicle_force_arr,temp),axis=1)
        # print ( np.concatenate((,vehicle_force),axis=1))
        # print(vehicle_force_arr)

        accel_real     = np.subtract(vehicle_force_arr,runres_vehicle)/massa_total

        for i in range (len(accel_real)):
            if accel_real[i,0] < 0:
                break
            idx = i

        avg_accel_real  = accel_real[:idx,0].mean()
        p_motor         = (const_t*mech_eff*final_gr/jari_jari)*(wp/3.6)/1000
        highacc_wp = 3.6*p_motor*1000*jari_jari/highacc_const_t/final_gr

        self.output_avg_accel.setText(str(round(avg_accel_real ,3)))
        self.output_p_motor.setText(str(round(p_motor ,3)))
        self.output_highacc_wp.setText(str(round(highacc_wp ,3)))
        self.output_grad_const_t.setText(str(round(gradien[gradien_const_t ] ,3)))
        self.output_grad_highacc_const_t.setText(str(round(gradien[gradien_highacc_const_t ] ,3)))
        print(gradien[0])

        #Traffic Effort Peak
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

        self.output_t_cruise.setText(str(round(t_cruise,3)))
        self.output_pt_cruise.setText(str(round(pt_cruise,3)))
        self.output_p_cruise.setText(str(round(p_cruise,3)))
        self.output_e_battery.setText(str(round(e_battery,3)))
        self.output_p_battery.setText(str(round(p_battery,3)))

        self.RunresVehicle.canvas.ax.clear()
        self.RunresVehicle.canvas.ax.plot(v_runres,runres_vehicle)
        self.RunresVehicle.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresVehicle.canvas.ax.set_ylabel("Force (N)")
        self.RunresVehicle.canvas.ax.set_title("Vehicle Running Resistance")
        self.RunresVehicle.canvas.ax.grid()
        self.RunresVehicle.canvas.ax.legend()
        self.RunresVehicle.canvas.figure.tight_layout()
        self.RunresVehicle.canvas.draw()

        self.RunresWheel.canvas.ax.clear()
        self.RunresWheel.canvas.ax.plot(v_runres,runres_wheel)
        self.RunresWheel.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresWheel.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresWheel.canvas.ax.set_title("Wheel Running Resistance")
        self.RunresWheel.canvas.ax.grid()
        self.RunresWheel.canvas.figure.tight_layout()
        self.RunresWheel.canvas.draw()

        self.RunresMotor.canvas.ax.clear()
        self.RunresMotor.canvas.ax.plot(v_runres,runres_motor)
        self.RunresMotor.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresMotor.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresMotor.canvas.ax.set_title("Motor Running Resistance")
        self.RunresMotor.canvas.ax.grid()
        self.RunresMotor.canvas.figure.tight_layout()
        self.RunresMotor.canvas.draw()

        self.RunresVehicleForce.canvas.ax.clear()
        self.RunresVehicleForce.canvas.ax.plot(v_runres,runres_vehicle)
        self.RunresVehicleForce.canvas.ax.plot(v_runres,vehicle_force)
        self.RunresVehicleForce.canvas.ax.plot(v_runres,vehicle_force_peak,linestyle='--')
        self.RunresVehicleForce.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresVehicleForce.canvas.ax.set_ylabel("Force (N)")
        self.RunresVehicleForce.canvas.ax.set_title("Vehicle Running Resistance")
        self.RunresVehicleForce.canvas.ax.grid()
        self.RunresVehicleForce.canvas.figure.tight_layout()
        self.RunresVehicleForce.canvas.draw()

        self.RunresWheelForce.canvas.ax.clear()
        self.RunresWheelForce.canvas.ax.plot(v_runres,runres_wheel)
        self.RunresWheelForce.canvas.ax.plot(v_runres,wheel_torque)
        self.RunresWheelForce.canvas.ax.plot(v_runres,wheel_torque_peak,linestyle='--')
        self.RunresWheelForce.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresWheelForce.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresWheelForce.canvas.ax.set_title("Wheel Running Resistance")
        self.RunresWheelForce.canvas.ax.grid()
        self.RunresWheelForce.canvas.figure.tight_layout()
        self.RunresWheelForce.canvas.draw()

        self.RunresMotorForce.canvas.ax.clear()
        self.RunresMotorForce.canvas.ax.plot(v_runres,runres_motor)
        self.RunresMotorForce.canvas.ax.plot(v_runres,motor_torque)
        self.RunresMotorForce.canvas.ax.plot(v_runres,motor_torque_peak,linestyle='--')
        self.RunresMotorForce.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresMotorForce.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresMotorForce.canvas.ax.set_title("Motor Running Resistance")
        self.RunresMotorForce.canvas.ax.grid()
        self.RunresMotorForce.canvas.figure.tight_layout()
        self.RunresMotorForce.canvas.draw()

        self.RunresMotorCruise.canvas.ax.clear()
        self.RunresMotorCruise.canvas.ax.plot(v_runres,runres_motor)
        self.RunresMotorCruise.canvas.ax.plot(v_runres,motor_torque)
        self.RunresMotorCruise.canvas.ax.plot(v_runres,motor_cruise_torque)
        self.RunresMotorCruise.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresMotorCruise.canvas.ax.set_ylabel("Torque (Nm)")
        self.RunresMotorCruise.canvas.ax.set_title("Motor Running Resistance")
        self.RunresMotorCruise.canvas.ax.grid()
        self.RunresMotorCruise.canvas.figure.tight_layout()
        self.RunresMotorCruise.canvas.draw()

        fig, ax = plt.subplots()
        for i in range (0,len(variasi_array)):
            ax.plot(v_runres, runres_vehicle[:,i]);
        ax.set(xlabel='Speed (km/h)', ylabel='Force (N)', title='Vehicle Running Resistance');
        fig.savefig("motorrunres.png")

app = QApplication([])
mainwindow = runres_calc()
app.setQuitOnLastWindowClosed(True)
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
sys.exit(app.exec_())