from xml.etree.ElementTree import tostring
from pymysql import NULL
import requests
import geojson
from time import sleep
# Базовый URL получения данных
# URL ="https://www.edenred.fr/api/outlets?result_level=full&radius=5&page_size=30&location=48.856483%2C2.352414&supported_products=CTR_4C"
URL ="https://www.spar.hu/uzletek/_jcr_content.stores.v2.html?"
# Функция извлечения данных
def get_data (url=None):
    
    # Обработчик ошибки если отсутствует аргумент url
    if url is None:
        return False
    
    # Запрос методом GET
    response = requests.get(URL)

    # Если статус ответа 200 возвращаем данные
    if response.status_code is 200:
        print("Data successfully extracted")
        return response.json()
    else:
        print("Error while extracting data")
        return False


def save_data (data=None):
    if data is None:
        return False

    with open('spar.json', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True


def addZero(i):
    zerTo = i["openingHours"]["to1"]["minute"]
    if (zerTo==0):
        zerTo = "00"
    else:
        zerTo = str(zerTo)
    zerFrom = i["openingHours"]["from1"]["minute"]
    if (zerFrom==0):
        zerFrom = "00"
    else:
        zerFrom = str(zerFrom)  
    return (zerFrom,zerTo)  
def parse_date(data):
    workingDays = []
    # features = []
    num = 0
    for row in data:
        num+=1  
        print(num)     
        for i in row["shopHours"]:
            try:
                zerFrom, zerTo = addZero(i)  
                if (i["openingHours"]["dayType"]=="hétfő"):
                    workingDays.append("Monday: "+ str(i["openingHours"]["from1"]["hourOfDay"])+":"+zerFrom
                    +" - " + str(i["openingHours"]["to1"]["hourOfDay"])+":"+ zerTo)
                if (i["openingHours"]["dayType"]=="kedd"):                
                    workingDays.append("Tuesday: "+ str(i["openingHours"]["from1"]["hourOfDay"])+":"+zerFrom
                    +" - " + str(i["openingHours"]["to1"]["hourOfDay"])+":"+ zerTo)
                if (i["openingHours"]["dayType"]=="szerda"):            
                    workingDays.append("Wednesday: "+ str(i["openingHours"]["from1"]["hourOfDay"])+":"+zerFrom
                    +" - " + str(i["openingHours"]["to1"]["hourOfDay"])+":"+ zerTo)
                if (i["openingHours"]["dayType"]=="csütörtök"):                
                    workingDays.append("Thursday: "+ str(i["openingHours"]["from1"]["hourOfDay"])+":"+zerFrom
                    +" - " + str(i["openingHours"]["to1"]["hourOfDay"])+":"+ zerTo)
                if (i["openingHours"]["dayType"]=="péntek"):                
                    workingDays.append("Friday: "+ str(i["openingHours"]["from1"]["hourOfDay"])+":"+zerFrom
                    +" - " + str(i["openingHours"]["to1"]["hourOfDay"])+":"+ zerTo)
                if (i["openingHours"]["dayType"]=="szombat"):                
                    workingDays.append("Saturday: "+ str(i["openingHours"]["from1"]["hourOfDay"])+":"+zerFrom
                    +" - " + str(i["openingHours"]["to1"]["hourOfDay"])+":"+ zerTo)      
                if (i["openingHours"]["dayType"]=="vasárnap"):               
                        workingDays.append("Sunday: "+ str(i["openingHours"]["from1"]["hourOfDay"])+":"+zerFrom
                        +" - " + str(i["openingHours"]["to1"]["hourOfDay"])+":"+ zerTo) 
            except:
                workingDays.append("No information about opening hours")

               
            # workingDays[
            #     i["openingHours"]["dayType"] + i["from1"]["hourOfDay"]+":"["from1"]["minute"]
            # ] 
                
                    # dateFrom = r["openingHours"]["from1"]["hourOfDay"]
                    # workingDays["Monday"] = dateFrom
                
    print(workingDays)




        # num+=1
        # s = ''
        # if 'phone_number' in row:
        #     s  = row['phone_number']
        # else:
        #     s = ' '



    #     workingHours = [
    #         'mo' = row["name"]
    #     ]
    #     feature = {
    #                 "type": "Feature",
    #                 "properties": {
    #                     'workingHours' : workingHours
    #                     # 'num' : num,
    #                     # 'name': row['name'],
    #                     # 'addr_full': row["address"],
    #                     # 'city': row["city"],
    #                     # 'postcode': row['zipCode'],

    #                     # # 'phone': s,
                        
    #                 },
    #                 "geometry": {
    #                     "type": "Point",
    #                     "coordinates": [row["longitude"], row["latitude"]]
    #                 }
    #             }

    #     features.append(feature)
    # featureCollection = {
    #    "type": "FeatureCollection",
    #     "features": features
    # }
    # print(f"Data successfully parsed, {num} points found")
    # return (featureCollection)


if __name__ == "__main__":
    data = get_data(url=URL)
    # print(data)

    featureCollection = parse_date(data)
    # print(featureCollection)
    # isSaved = save_data(featureCollection)
    # if isSaved:
    #     print("Data successfully saved")
    # else:
    #     print("Error while saving data")