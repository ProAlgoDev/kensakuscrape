import requests
import time


def get_time_from_world_clock():
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/Asia/tokyo')
    except Exception as error:
        print('network error', error)
        return False

    current_time_json = response.json()

    return current_time_json


def normal_check(current_time_json):
    current_time =  current_time_json['datetime'].split('T')[1]
    current_time_hour = current_time.split(":")[0]
    current_time_minute = current_time.split(":")[1]
    current_time_second = current_time.split(":")[2].split('.')[0]

    print(f'current time: {current_time_hour}:{current_time_minute}:{current_time_second}')

    
    if (int(current_time_hour) == 7) & (int(current_time_minute) >= 58):
        return True
    else:
        return False
    

def check_current_time():

    current_time_json = get_time_from_world_clock()

    print('preparing...')      
    if normal_check(current_time_json):
        return True
    else:  
        return False
    
