"""
South Side Hackerspace: Chicago

Based on code from RFD900 Balloon Telemetry Senior Capstone Final Project Report(Madison Martinsen, Annie Bachman, Michael Valentino-Manno)
"""

import tkinter as tk
import serial
import time
import csv

packet_count = 0
succ = 0
Decoded_Raw_Data = []
Final_Data = []
# Degree Symbol for GUI
degree_sign = u"\N{DEGREE SIGN}"

fix_sources = [
    (0, "No Fix"),
    (1, "Dead Reckoning"),
    (2, "2D"),
    (3, "3D"),
    (4, "GNSS + Dead Reckoning"),
]

# CSV HEADERS
header = ["Packet Number", "SIV", "FixType", "Latitude", \
    "Longitude", "Altitude", "Year", "Month", "Day", \
    "Hour", "Min", "Sec", "NNV", "NEV", "NDV", "Battery" ,\
    "3v3 Supply", "5v Supply", "Radio Supply", "Analog Internal", \
    "Analog External", "Altimeter Temp", "Digital Internal", \
    "Digital Eternal", "Pressure", "Accel A", "Accel Y", "Accel z", \
    "Pitch", "Roll", "Yaw"]


def Label_Update(serial_port):
    packet=lat=lon=0
    siv=fix=alt=year=month=day=hour=minute=sec=nedN=nedE=nedD=bat=bat33=bat51=bat52=aint=aext=ptemp=dint=dent=pres=ax=ay=az=pitch=roll=yaw=a1=string_csv_data=""
    serial_port.reset_input_buffer()
    source_data = serial_port.readline()

    # CSV
    Decoded_Raw_Data = source_data.decode("utf-8")
    Final_Data = Decoded_Raw_Data.split(",")
    string_csv_data = str(Decoded_Raw_Data).split(",")
    
    # write a new line in the csv if there is data
    if len(Final_Data) > 10:
        with open(fileName, "a", newline = '\n') as f:
            csv.writer(f, delimiter=',').writerow(Final_Data)
            packet_count += 1

    # Save radio data
    if len(string_csv_data) >= 31:
        packet = int(string_csv_data[0].strip())
        siv = string_csv_data[1].strip()
        fix = string_csv_data[2].strip()
        lat = float(string_csv_data[3].strip())
        lat = lat * .0000001
        lon = float(string_csv_data[4].strip())
        lon = lon * .0000001
        alt = float(string_csv_data[5].strip())
        alt = alt / 1000
        year = string_csv_data[6].strip()
        month = string_csv_data[7].strip()
        day = string_csv_data[8].strip()
        hour = string_csv_data[9].strip()
        minute = string_csv_data[10].strip()
        sec = string_csv_data[11].strip()
        nedN = string_csv_data[12].strip()
        nedE = string_csv_data[13].strip()
        nedD = string_csv_data[14].strip()
        bat = string_csv_data[15].strip()
        bat33 = string_csv_data[16].strip()
        bat51 = string_csv_data[17].strip()
        bat52 = string_csv_data[18].strip()
        aint = string_csv_data[19].strip()
        aext = string_csv_data[20].strip()
        ptemp = string_csv_data[21].strip()
        dint = string_csv_data[22].strip()
        dent = string_csv_data[23].strip()
        pres = string_csv_data[24].strip()
        ax = string_csv_data[25].strip()
        ay = string_csv_data[26].strip()
        az = string_csv_data[27].strip()
        pitch = string_csv_data[28].strip()
        roll = string_csv_data[29].strip()
        yaw = string_csv_data[30].strip()
        if succ == 0:
            succ=packet

    if fix != "":
        a1 = fix_sources[int(fix)]
    else:
        a1 = "No Data"
        packet = 1 #
        lat = 0#
        lon = 0#
        siv=fix=alt=year=month=day=hour=minute=sec=nedN=nedE=nedD=bat=bat33=bat51=bat52=aint=aext=ptemp=dint=dent=pres=ax=ay=az=pitch=roll=yaw=""
        
            
    Title = tk.Label(root, font = ("Helvetica", "30"))
    Title.grid(row=0,column=0,padx=(0, 0), pady=(0,0))
    Title.config(text=('MSGC RDF900x'))
            
    # Col 0
    Data1 = tk.Label(root, font = ("Helvetica", "22"))
    Data1.grid(row=1,column=0,padx=(5, 15), pady=(0,0))
    Data1.config(text=(
        'Current Packet #' + str(packet) + "\n" +
        'Packets Received: ' + str(packet_count)+ "/" + str(packet-succ+1) + ", " + \
        str(round(((packet_count/(packet-succ+1))*100),2))+ "%\n" +
        'Date: ' + year + "-" + month +"-" + day + "\n" +
        'Time: ' + hour + ":" + minute +":" + sec + "\n\n\n" +
        'Battery Voltage: ' + str(bat) + " V\n" +
        '3.3 Voltage: ' + str(bat33) + " V\n" +
        '5.0 Voltage: ' + str(bat51) + " V\n" +
        'Radio Voltage: ' + str(bat52) + " V\n\n\n" +
        'Analog Internal Temperature: ' + str(aint)+ degree_sign + "C\n" +
        'Analog External Temperature: ' + str(aext) + degree_sign + "C\n" +
        'Digital Internal Temperature: ' + str(dint) + degree_sign + "C\n" +
        'Digital External Temperature: ' + str(dent) + degree_sign + "C\n" +
        'Pressure Sensor Temperature: ' + str(ptemp) + degree_sign + "C\n")
    )
                        
    # Col 1
    Data2 = tk.Label(root, font = ("Helvetica", "22"))
    Data2.grid(row=1,column=1,padx=(5, 5), pady=(0,0))
    Data2.config(text=(
        'Satellites In View: ' + str(siv)+ "\n" +
        'Fix Type: ' + a1 + " (" + str(fix)+ ")" + "\n" +
        'Latitude: ' + str(round(float(lat), 6)) + "\n" +
        'Longitude: ' + str(round(float(lon), 6)) + "\n" +
        'Altitude: ' + str(alt)+ " m\n" +
        'Pressure: ' + str(pres) + " mbar\n\n" +
        'NedNorthVel: ' + str(nedN) + " mm/s\n" +
        'NedEastVel: ' + str(nedE) + " mm/s\n" +
        'NedDownVel: ' + str(nedD) + " mm/s\n\n" +
        'Acceleration X: ' + str(ax)+ " m/s\u00b2 \n" +
        'Acceleration Y: ' + str(ay)+ " m/s\u00b2 \n" +
        'Acceleration Z: ' + str(az)+ " m/s\u00b2 \n" +
        'Pitch: ' + str(pitch)+ degree_sign +"\n" +
        'Roll: ' + str(roll)+ degree_sign +"\n" +
        'Yaw: ' + str(yaw)+ degree_sign +""
        ))

##################################################################

# User enter serial port
while True:
    # Open Serial Port, if it doesn't work, reprompt user
    try:
        serial_port = serial.Serial( port = "/dev/cu.usbserial-AB0JNQSY", baudrate = 57600, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 1 )
        break
    except IOError:
        print("Device not found in specified COM port. Please try again.\n")

root = tk.Tk()
root.title("MSGC RFD900x")
blank = []
fileName = "RFD900x_Data.csv"
file = open(fileName, "a")
file.close()

with open(fileName, "a", newline = '\n') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)

print(fileName + " created to hold data. If file exists, data will be appended\n")
# MSGC LOGO
while True:
    Label_Update(serial_port)
    time.sleep(0.5)
    root.update_idletasks()
    root.update()
