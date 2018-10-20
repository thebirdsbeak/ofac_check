import requests
import arrow
import  os
import csv
from fuzzywuzzy import fuzz

SENSITIVITY = 60

def download_data():
        '''Downloads and decodes the dataset 
        and passes to org_list function'''
        dataset = [] 
        timenow = arrow.now('GMT').format('MMYY')
        filename = "{}paydata.csv".format(timenow)
        if filename in os.listdir('.'):
                print("\nOpening {}\n".format(filename))
                with open(filename, 'r') as olddata:
                        readdata = olddata.read()
                        csv_read = csv.reader(readdata.splitlines(), delimiter=",")
        else:
                print("\nDeleting old files...")
                for i in os.listdir('.'):
                    if 'sdn' in i:
                        print("\nDeleting: {}\n".format(i))
                        os.remove(i)
                print("\nRetrieving {}\n".format(filename))
                with open(filename, 'w+') as data_file:
                        data = 'https://www.treasury.gov/ofac/downloads/sdn.csv'
                        with requests.Session() as sesh:
                                download = sesh.get(data)
                                decoded_content = download.content.decode('utf-8')
                                data_file.write(decoded_content)
                                csv_read = csv.reader(decoded_content.splitlines(), delimiter=",")

        my_list = list(csv_read)
        for i in (my_list[1::]):
                dataset.append(i)
        return dataset
        
        
datas = download_data()

user_input = input("Enter name: ")

for i in datas:
        try:
                if fuzz.ratio(user_input.upper(), i[1].upper()) > SENSITIVITY:
                        print(i[1])
        except IndexError:
                pass
