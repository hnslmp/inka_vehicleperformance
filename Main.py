
# Main program
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

import sys
import csv
from datetime import datetime
import os.path

import atexit

# Plotter
import numpy as np
from scipy import constants

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import ( NavigationToolbar2QT  as  NavigationToolbar )
from matplotlib.figure import Figure

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

class runres_calc (QMainWindow) :
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("runres_calc.ui",self)
        self.setWindowTitle("Vehicle Performance Calculator")
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

        self.output_massa_total.setText(str(round(massa_total,3)))
        self.output_kec_max_rpm.setText(str(round(kec_max_rpm,3)))
        self.output_kec_ops_rpm.setText(str(round(kec_ops_rpm,3)))
        self.output_accel.setText(str(round(accel,3)))
        self.output_theta_percentage.setText(str(round(theta_percentage,3)))

        #Menghitung Running Resistance
        v_runres = np.arange(0,121,1)

        jumlah_variasi = 5
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
        
        print(runres_vehicle)
        self.RunresVehicle.canvas.ax.clear()
        # for i in range (0,len(variasi_array)):
        self.RunresVehicle.canvas.ax.plot(v_runres,runres_vehicle)
        self.RunresVehicle.canvas.ax.set_xlabel("Speed (km/h)")
        self.RunresVehicle.canvas.ax.set_ylabel("Force (N)")
        self.RunresVehicle.canvas.ax.set_title("Vehicle Running Resistance")
        self.RunresVehicle.canvas.ax.grid()
        self.RunresVehicle.canvas.figure.tight_layout()
        self.RunresVehicle.canvas.draw()


app = QApplication([])
mainwindow = runres_calc()
app.setQuitOnLastWindowClosed(True)
mainwindow.show()
sys.exit(app.exec_())