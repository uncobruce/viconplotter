import serial, sys, os
import csv
import math

#192.168.0.117

# For windows set to "COM" eg. "COM19". For Linux set to eg "/dev/ttyUSB0". Baud rate is 115200
PORTNAME="/dev/ttyUSB0"
time = []
x = []
y = []
theta = []
leftvel = []
rightvel = []


ser = serial.Serial(PORTNAME,baudrate=115200, timeout=2)


def write2csv(time,x,y,theta,leftvel,rightvel):
    with open('./qbii_data/square_2m_cw_vicon.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time (s)", "x (cm)", "y (cm)", "theta (deg)", "left velocity ()", "right velocity ()"])

        for i in range(len(time)):
            writer.writerow([time[i], x[i], y[i], theta[i]*360/(math.pi*2), leftvel[i], rightvel[i]])


try:
    while True:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode("utf-8")
        
        # decode_bytes: str
        print(decoded_bytes)
        
        new = decoded_bytes.split(',')
        
        try:
            leftvel.append(float(new[0]))
            rightvel.append(float(new[1]))
            time.append(float(new[2]))
            x.append(float(new[3]))
            y.append(float(new[4]))
            theta.append(float(new[5]))
        except:
            pass

except KeyboardInterrupt:
    print('\nClosing...')
    try:
        write2csv(time,x,y,theta,leftvel,rightvel)
        print('Output File Sucessfully Saved\n')
        sys.exit(0)
    except SystemExit:
        os._exit(0)


# print('time = ', time[:10])
# print('x = ', x[:10])
# print('y = ', y[:10])
# print('theta = ', theta[:10])
# print('leftvel = ', leftvel[:10])
# print('rightvel = ', rightvel[:10])


