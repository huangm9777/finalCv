from aip import AipOcr
import datetime
from collections import defaultdict
from prettytable import PrettyTable

APP_ID = '24171868'
API_KEY = 'vptTfoS5r6PBbnLLDpHZ2EaH'
SECRET_KEY = 'phFj3QsG00ppFKCCHvLPfkwGLyLMBwGx'
'''
APP_ID = '24223793'
API_KEY = 'yu8CmoiIctRZd1CsVBIKdiHe'
SECRET_KEY = 'YENTlOKIKN7vj3PhQG2nSWbd0u09OqIh'
'''
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
client.setConnectionTimeoutInMillis(5000)
client.setSocketTimeoutInMillis(5000)


def get_plate(filename):
    image=open(filename, 'rb').read()
    options = {}
    options['multi_detect'] = 'true'
    res = client.licensePlate(image, options)
    if len(res['words_result'])<1:
        raise ZeroDivisionError("No license plate or unsupported license plate")
    elif len(res['words_result'])>1:
        raise ValueError("Multiple vehicles identified, please take another picture")
    else:
        return res['words_result'][0]
class cheku:    
    def __init__(self):
        self.log=list()
        self.time_in=dict()
        self.time_out=dict()
        self.sp=['blue','green']
        self.vip=list()
        self.plates=list()

    def init_vip(self,vips):
        self.vip=vips
    def add_vip(self,vipp):
        self.log.append([datetime.datetime.now(),car['number'],car['color'],'Vip add'])
        self.vip.append(vipp)
    
    def ruku(self,car):        
        self.time_in[car['number']]=datetime.datetime.now()
        self.plates.append(car)
        self.log.append([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),car['number'],car['color'],'Car In'])
    
    def chuku(self,car):
        if car not in self.plates:
            print("The car is not in the garage")
        self.time_out[car['number']]=datetime.datetime.now()
        self.plates.remove(car)
        time=(self.time_out[car['number']]-self.time_in[car['number']]).seconds
        self.log.append([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),car['number'],car['color'],'Car Out'+f": stoped {time} seconds"])
        print(f"The car stopped for {time} seconds")

    def print_vip(self):        
        row1:PrettyTable=PrettyTable()
        row1.field_names=['vip','color']
        for i in self.vip:
           row1.add_row([i['number'],i['color']])        
        print(row1)

    def print_plates(self):        
        row1:PrettyTable=PrettyTable()
        row1.field_names=['plates','color', 'Is vip']
        for i in self.plates:
            vip_1=False
            if i in self.vip:
                vip_1=True
            row1.add_row([i['number'],i['color'],vip_1])
        print(row1)
    
    def print_log(self):
        row1:PrettyTable=PrettyTable()
        row1.field_names=['time','plates', 'color','events']
        for i in self.log:
            row1.add_row(i)
        print(row1)
    

if __name__ == '__main__':
    #for i in range(3):
        #car=get_plate("test"+str(i+1)+ ".jpg")
        #print(str(i+1)+',\t number:' + car['number']+'\tcolor:' + car['color'])
    ku=cheku()
    choose=input('Please enter your options :\n1, Add VIP \n2, car Entry \n3, car Exit \n4, List VIP car  \n5, List cars in the parking lot \n6, Print log\nq, Exit \nOther: Continue \n')
    while(True):
        
        if str(choose)=='1':
            #filename =filedialog.askopenfilename()
            #car=get_plate(filename)
            i=input('Enter the photo taken to add vip:')
            car=get_plate(i)
            ku.add_vip(car)
        elif str(choose)=='2':
            i=input('Enter the photo taken of Entrance:')
            car=get_plate(i)
            ku.ruku(car)
        elif str(choose)=='3':
            i=input('Enter the photo taken of Exit:')
            car=get_plate(i)
            ku.chuku(car)
        elif str(choose)=='4':
            ku.print_vip()
        elif str(choose)=='5':
            ku.print_plates()
        elif str(choose)=='6':
            ku.print_log()
        elif str(choose)=='q':
            break
        choose=input("Press 'q' to exit or any other key to continue\n")
        if str(choose)=='q':
            break
