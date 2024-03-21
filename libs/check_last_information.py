import json
import os
import CONSTANT 


def init_json():

    file_path = "check.json" 

    if os.path.exists(file_path):
        print("File (check.json) exists!")
    else:
        print("File does not exist. Made new file")

        data = {
            CONSTANT.KENSAKU: "",
        }

        with open("check.json", "w") as file:
            json.dump(data, file)
            file.close()



def check_last_lawyer_information():

    with open("check.json", "r") as file:
        try:
            data = json.load(file)
        except:
            return False
    return data

    # if data[site_name] == last_info :
    #     print("Last lawyer data has been not yet updated.")
    #     return data
    # else:

    #     print('Last lawyer data has been updated.')
    #     return True




def update_last_lawyer_information(site_name, last_info):
    
    # with open("check.json", "r") as file:
    #     try:
    #         data = json.load(file)
    #     except:
    #         data = False
    #         pass
    # info = []
    # if data != False:
    #     info=data
    # info.append(last_info)

    with open("check.json", "w") as file:
        json.dump(last_info, file)
        file.close()