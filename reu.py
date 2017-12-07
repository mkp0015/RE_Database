#Automating REU Research
import netcCDF4 as nc
import numpy as np
import datetime
import matplotlib.pyplot as plt

def read_track(filename):
    "This function reads in HC tracks from the given txt file"
    track = open(filename)
    raw_data = track.readlines()
    yymmdd = []
    lat = []
    lon = []
    for line in raw_data[3:]:
        yymmdd.append(datetime.datetime(int(line[6:10]), int(line[:2]), int(line[3:5]), int(line[11:13]), int(line[14:16]), int(line[17:19])))
        lat.append(float(line(24:30)))
        lon.append(float(line(37:42)))

    track.close()
    return np.array(yymmdd), np.array(lat), np.array(lon)

def extract_data(fname):
    "This function extracts data from the netCDF data files"
    ncf = nc.Dataset(fname)
    lon = ncf.variables["Longitude"][:]
    lat = ncf.variables["Latitude"][:]
    u_850 = ncf.variables["u"][6,:,:]
    v_850 = ncf.variables["v"][6,:,:]
    u_200 = ncf.variables["u"][22,:,:]
    v_200 = ncf.variables["v"][22,:,:]
    temp = ncf.variables["T"][19,:,:]
    spec_hum = ncf.variables["SH"][19,:,:]
    ncf.close()

    return lon, lat, u_850, v_850, u_200, v_200, temp, spec_hum

def hc_func(filepath):
    "This function will open data, create variables, then plot"

    import netCDF4 as nc
    %pylab
    from mpl_toolkits.basemap import Basemap

    plt.close()
    ncf = nc.Dataset(filepath)
    lon = ncf.variables["Longitude"][:]
    lat = ncf.variables["Latitude"][:]
    u_850 = ncf.variables["u"][6,:,:]
    v_850 = ncf.variables["v"][6,:,:]
    u_200 = ncf.variables["u"][22,:,:]
    v_200 = ncf.variables["v"][22,:,:]
    temp = ncf.variables["T"][19,:,:]
    spec_hum = ncf.variables["SH"][19,:,:]
    alt = ncf.variables["Altitude"][:]

    #plot 300mb temp & use mouse click to find center @ 300mb
    lon2d, lat2d = np.meshgrid(lon,lat)
    mapproj = Basemap(projection='cyl', llcrnrlat=10, urcrnrlat=40, llcrnrlon=260, urcrnrlon=300)
    x,y = mapproj(lon2d, lat2d)
    mapproj.drawparallels(np.array([10,15,20,25,30,35,40]), labels=[1,0,0,0])
    mapproj.drawmeridians(np.array([-95,-90,-85,-80,-75,-70,-65]),labels=[0,0,0,1])
    mapproj.contour(x,y,temp,20,cmap=matplotlib.cm.jet)
    plt.colorbar()
    plt.show()
    xyo = plt.ginput(n=3)
    print xyo

def coord_ind(lon_track,lat_track,lat0,lon0):
    "this func obtains index values for surface center"
    i = np.argwhere(lon>= lon0)[0][0]
    j = np.argwhere(lat>= lat0)[0][0]

    return i,j

def avg_w_shear(i,j,tvs):
    "this func calculates avg wind shear for coord"
    avgtvs = np.mean(tvs[i-1:i+1, j-1:j+1])
    return avgtvs

def avg_temp(k,1,temp):
    "this func calculates avg temp for coord"
    avgtemp = np.mean(temp[k-1:k+1,l-1:l+1])
    return avgtemp

def avg_spec_hum(k,1,spec_hum):
    "this func calculates avg specific humidity for coord"
    avgspechum = np.mean(spec_hum[k-1:k+1, l-1:l+1])
    return avgspechum

track=open("Katrina.track.txt")
yymmdd,lat_track,lon_track = read_track("Katrina.track.txt")

hrs = ['00', '06', '12', '18']
dts = ['200508', +str(dd)+'T' +hh+'0000Z.ncd' for dd in range(24,30) for hh in hrs]
print dts

pd = '/bigstor/reanalysis/ERAINTERIM/pressure/netcdf/6-hourly/2005/200508/'
lat0=[]
lon0=[]
time_ind=[]
wshear=[]
lat3=[]
lon3=[]
temp3=[]
spec_hum3=[]

for fil_ind in range(24):
    lon,lat,u_850,v_850,u_200,v200,temp,spec_hum = extract_data(pd +dts[fil_ind])
    tvs = np.sqrt((u_200-u_850)**2 + (v_200-v_850)**2)
    tmp = np.where(yymmdd >= datetime.datetime(2005,8,int(dts[fil_ind][6:8]),int(dts[fil_ind][9:11]),0,0))[0][0]
    time_ind.append(temp)
    lat0.append(lat_track[tmp])
    lon0.append(lon_track[temp])
    i,j = coord_index(lon_track, lat_track, lat0[-1], lon0[-1])
    print i,j
    wshear.append(avg_w_shear(i,j,tvs))
    tlon3,tlat3 = hc_func(pd + dts[fil_ind], dts[fil_ind][:-4])
    lon3.append(360-tlon3)
    lat3.append(360-tlat3)
    k,l = coord_index(lon,lat,tlat3,tlon3)
    temp3.append((avg_temp(k,l,temp)))
    spec_hum3.append(1000*avg_spec_hum(l,k,spec_hum))

shear_t_sh = np.array([wshear,temp3,spec_hum]).T
print shear_t_sh

coord = np.array([lat0,lon0,lat3,lon3]).T
print coord

hdr = 'Date,Hour,Lat_Surf,Lon_Surf,Lat_300,Lon_300,Wind_Shear,Temp,Spec_Hum'
days = np.array([int(dts[i][:8]) for i in range(24)])
zz = np.array([int(dts[i][9:11]) for i in range(24)])
fmt = '%d %02d %5.3f %5.3f %5.3f %5.3f %5.3f %5.3f %5.3f'

katrina_data = column_stack([days,zz,coord,shear_t_sh])
savetxt('katrina_data', katrina_data, fmt=fmt, delimiter=' ', header=hdr)
