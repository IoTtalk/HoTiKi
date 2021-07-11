# -*- coding: UTF-8 -*-
from flask import Flask, request, abort, send_from_directory, make_response, redirect, render_template
from os import listdir
from os.path import exists, join, isdir
from os import system
import DAI, DF, config

IMG_DIR_PATH = config.IMG_DIR_PATH
HISTORY_IMG_DIR_PATH = config.HISTORY_IMG_DIR_PATH
LOG_PATH = config.LOG_PATH


app = Flask(__name__)


def saveLog(data):
        idFile = open(LOG_PATH, 'a')
        idFile.write(data)
        idFile.close()

@app.route("/img", methods=['GET'])
def fileService():
    file_list = []
    name_list = []
    try:
        name_list =  listdir(IMG_DIR_PATH)
    except OSError:
        pass #ignore errors
    else:
        for name in name_list:
            if '.jpg' not in name: continue
            file_path = join(IMG_DIR_PATH, name)
            if not isdir(file_path):
               file_list.append(name) 

    return render_template('index.html', file_list=file_list, device_id='HoTiKi')

@app.route("/img/<path:path>", methods=['GET'])
def ImgService(path):
    fullpath = join(IMG_DIR_PATH, path)
    no_cache_headers = {
        'Cache-Control': ('no-store, no-cache, must-revalidate, '
                          'post-check=0, pre-check=0, max-age=0'),
        'Pragma': 'no-cache',
        'Expires': '-1',
    }
    return send_from_directory(IMG_DIR_PATH, path)

@app.route("/history", methods=['GET'])
def history():
    file_list = []
    name_list = []
    try:
        name_list =  listdir(HISTORY_IMG_DIR_PATH)
    except OSError:
        pass #ignore errors
    else:
        for name in name_list:
            if '.jpg' not in name: continue
            file_path = join(IMG_DIR_PATH, name)
            if not isdir(file_path):
               file_list.append(name)
    file_list.sort()
    return render_template('history.html', file_list=file_list, device_id='000')

@app.route("/history/<path:path>", methods=['GET'])
def historyService(path):
    fullpath = join(HISTORY_IMG_DIR_PATH, path)
    no_cache_headers = {
        'Cache-Control': ('no-store, no-cache, must-revalidate, '
                          'post-check=0, pre-check=0, max-age=0'),
        'Pragma': 'no-cache',
        'Expires': '-1',
    }
    return send_from_directory(HISTORY_IMG_DIR_PATH, path)

@app.route("/", methods=['POST'])
def receive():
    if not request.json:
        return 'argument is not in JSON format', 400

    data = request.json
    saveLog(str(data)+';\n\n')
    #print(data)

    station_id = data.get('station_id')
    if station_id == None: return 400
    print ('station_id:', data.get('station_id'))

    obs_time = data.get('obs_time')
    print ('obs_time:', obs_time)

    rain_10m = data.get('rain_10m')
    if rain_10m != None: print ('rain_10m:', rain_10m)

    rain_h = data.get('rain_h')
    if rain_h != None: 
        DAI.push(station_id, DF.name.get('rain_h'), rain_h)
        print ('rain_h:', rain_h)

    rain_d = data.get('rain_d')
    if rain_d != None: print ('rain_d:', rain_d)

    bug_h = data.get('bug_h')
    if bug_h != None: print ('bug_h:', bug_h)

    bug_d = data.get('bug_d')
    if bug_d != None: print ('bug_d:', bug_d)

    Leaf_wet = data.get('sensor', {}).get('Leaf', {}).get('wet')
    if Leaf_wet != None: print ('Leaf_wet:', Leaf_wet)

    Leaf_temp = data.get('sensor', {}).get('Leaf', {}).get('temp')
    if Leaf_temp != None: print ('Leaf_temp:', Leaf_temp)

    InnerBall_pres = data.get('sensor', {}).get('InnerBall', {}).get('pres')
    if InnerBall_pres != None: print ('InnerBall_pres:', InnerBall_pres)

    InnerBall_lux = data.get('sensor', {}).get('InnerBall', {}).get('lux')
    if InnerBall_lux != None: print ('InnerBall_lux:', InnerBall_lux)

    InnerBall_rh = data.get('sensor', {}).get('InnerBall', {}).get('rh')
    if InnerBall_rh != None: print ('InnerBall_rh:', InnerBall_rh)    

    InnerBall_tx = data.get('sensor', {}).get('InnerBall', {}).get('tx')
    if InnerBall_tx != None: print ('InnerBall_tx:', InnerBall_tx)
   
    Soil_elec = data.get('sensor', {}).get('Soil', {}).get('elec')
    if Soil_elec != None:
        DAI.push(station_id, DF.name.get('Soil_elec'), Soil_elec)
        print ('Soil_elec:', Soil_elec)

    Soil_water = data.get('sensor', {}).get('Soil', {}).get('water')
    if Soil_water != None:
        DAI.push(station_id, DF.name.get('Soil_water'), Soil_water)
        print ('Soil_water:', Soil_water)

    Soil_temp = data.get('sensor', {}).get('Soil', {}).get('temp')
    if Soil_temp != None:
        DAI.push(station_id, DF.name.get('Soil_temp'), Soil_temp)
        print ('Soil_temp:', Soil_temp)

    Soil_2_elec = data.get('sensor', {}).get('Soil_2', {}).get('elec')
    if Soil_2_elec != None: print ('Soil_2_elec:', Soil_2_elec)

    Soil_2_water = data.get('sensor', {}).get('Soil_2', {}).get('water')
    if Soil_2_water != None: print ('Soil_2_water:', Soil_2_water)

    Soil_2_temp = data.get('sensor', {}).get('Soil_2', {}).get('temp')
    if Soil_2_temp != None: print ('Soil_2_temp:', Soil_2_temp)

    Soil_3_elec = data.get('sensor', {}).get('Soil_3', {}).get('elec')
    if Soil_3_elec != None: print ('Soil_3_elec:', Soil_3_elec)

    Soil_3_water = data.get('sensor', {}).get('Soil_3', {}).get('water')
    if Soil_3_water != None: print ('Soil_3_water:', Soil_3_water)

    Soil_3_temp = data.get('sensor', {}).get('Soil_3', {}).get('temp')
    if Soil_3_temp != None: print ('Soil_3_temp:', Soil_3_temp)

    Soil_4_elec = data.get('sensor', {}).get('Soil_4', {}).get('elec')
    if Soil_4_elec != None: print ('Soil_4_elec:', Soil_4_elec)

    Soil_4_water = data.get('sensor', {}).get('Soil_4', {}).get('water')
    if Soil_4_water != None: print ('Soil_4_water:', Soil_4_water)

    Soil_4_temp = data.get('sensor', {}).get('Soil_4', {}).get('temp')
    if Soil_4_temp != None: print ('Soil_4_temp:', Soil_4_temp)

    Wind_wd = data.get('sensor', {}).get('Wind', {}).get('wd')
    if Wind_wd != None: print ('Wind_wd:', Wind_wd)

    Wind_ws = data.get('sensor', {}).get('Wind', {}).get('ws')
    if Wind_ws != None: print ('Wind_ws:', Wind_ws)

    Radia_radia = data.get('sensor', {}).get('Radia', {}).get('radia')
    if Radia_radia != None: print ('Radia_radia:', Radia_radia)

    Shelter_2_pres = data.get('sensor', {}).get('Shelter_2', {}).get('pres')
    if Shelter_2_pres != None:
        DAI.push(station_id, DF.name.get('Shelter_2_pres'), Shelter_2_pres)
        print ('Shelter_2_pres:', Shelter_2_pres)

    Shelter_2_lux = data.get('sensor', {}).get('Shelter_2', {}).get('lux')
    if Shelter_2_lux != None:
        DAI.push(station_id, DF.name.get('Shelter_2_lux'), Shelter_2_lux)
        print ('Shelter_2_lux:', Shelter_2_lux)

    Shelter_2_rh = data.get('sensor', {}).get('Shelter_2', {}).get('rh')
    if Shelter_2_rh != None:
        DAI.push(station_id, DF.name.get('Shelter_2_rh'), Shelter_2_rh)
        print ('Shelter_2_rh:', Shelter_2_rh)

    Shelter_2_tx = data.get('sensor', {}).get('Shelter_2', {}).get('tx')
    if Shelter_2_tx != None:
        DAI.push(station_id, DF.name.get('Shelter_2_tx'), Shelter_2_tx)
        print ('Shelter_2_tx:', Shelter_2_tx)

    StickTxRh_rh = data.get('sensor', {}).get('StickTxRh', {}).get('rh')
    if StickTxRh_rh != None:
        DAI.push(station_id, DF.name.get('StickTxRh_rh'), StickTxRh_rh)
        print ('StickTxRh_rh:', StickTxRh_rh)

    StickTxRh_tx = data.get('sensor', {}).get('StickTxRh', {}).get('tx')
    if StickTxRh_tx != None:
        DAI.push(station_id, DF.name.get('StickTxRh_tx'), StickTxRh_tx)
        print ('StickTxRh_tx:', StickTxRh_tx)

    pic_time = data.get('pic_time')
    if pic_time:
        img_url_list =  data.get('img_last')
        if img_url_list and len(img_url_list)>0:
            img_url_list.sort()
            for url in img_url_list:
                cmd = 'wget -P {} -N {}'.format(IMG_DIR_PATH, url)
                system(cmd)
                f_name = url.split('/')[-1]
                cmd = 'cp {}/{} {}/"{}-{}.jpg"'.format(IMG_DIR_PATH, f_name, HISTORY_IMG_DIR_PATH, f_name[:-4], pic_time) 
                system(cmd)

    return 'OK', 200


    


if __name__ == "__main__":
    
    app.run('127.0.0.1', port=32767, threaded=True, use_reloader=False)

    


