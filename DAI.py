import time, requests
import DAN, DF, config

# Change to your IoTtalk IP or None for autoSearching
# Use (http/https)://(domain/IP)[:port]
# ex: http://192.168.1.1:9999
#     https://test.domain
ServerURL = config.ServerURL

df_list=[]
for key in DF.name: df_list.append(DF.name[key])
profile = {
    'dm_name': 'HoTiKi',
    'df_list': df_list,
}

d_list = {}

def HoTiKi_device_register(device_id):
    global d_list
    Reg_addr = DAN.getMacAddr() + '-' + device_id
    profile['d_name'] = device_id
    d_list[device_id] = DAN.DAN(profile, ServerURL, Reg_addr)
    d_list[device_id].device_registration_with_retry()
    

def push(device_id, df, data):
    if not df: 
        print('Device feature name not found.')
        return
    if device_id not in d_list:
        HoTiKi_device_register(device_id)

    try:
        d_list[device_id].push(df, data)
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            d_list[device_id].device_registration_with_retry()
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)

