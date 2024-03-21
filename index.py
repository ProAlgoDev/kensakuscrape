import time
import threading
from openpyxl import load_workbook
from libs.check_time import check_current_time
from classes.kensaku import Kensaku
from libs.check_last_information import init_json
from CONSTANT import SHORT_WAIT_TIME, LONG_WAIT_TIME, MID_WAIT_TIME


def multi_thread_function():

    threads = []

    new_instance = Kensaku()

    thread = threading.Thread(target = new_instance.get_information)
    time.sleep(SHORT_WAIT_TIME)
    thread.start()
    threads.append(thread)
    

    for thread in threads:
        thread.join()



def main():
    
    init_json()


    while True:

        time_result = check_current_time()
        
        if 1:
            print("starting...")
            # multi_thread_function()
            new_instance = Kensaku()
            new_instance.get_information()
        else:
            pass
        
        time.sleep(10)
    
    
    
# check with postal code
main()