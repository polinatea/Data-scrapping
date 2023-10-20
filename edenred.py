import requests
import geojson

# Базовый URL получения данных
# URL ="https://www.edenred.fr/api/outlets?result_level=full&radius=5&page_size=30&location=48.856483%2C2.352414&supported_products=CTR_4C"
URL ="https://www.edenred.fr/api/outlets?result_level=full&radius=1000000&page_size=200"
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

    with open('edenred.json', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True

def parse_data(data):

    features = []
    num = 0
    for row in data:
        num+=1
        s = ''
        if 'phone_number' in row:
            s  = row['phone_number']
        else:
            s = ' '
        feature = {
                    "type": "Feature",
                    "properties": {
                        'num' : num,
                        'name': row['title'],
                        'addr_full': row["address"]["street_name"],
                        'city': row['address']["city_name"],
                        'postcode': row['address']['zip_code'],
                        'phone': s,
                        
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [row["address"]["longitude"], row["address"]["latitude"]]
                    }
                }

        features.append(feature)
    featureCollection = {
       "type": "FeatureCollection",
        "features": features
    }
    print(f"Data successfully parsed, {num} points found")
    return (featureCollection)

if __name__ == "__main__":
    data = get_data(url=URL)
    print(data)
    featureCollection = parse_data(data)
    isSaved = save_data(featureCollection)
    if isSaved:
        print("Data successfully saved")
    else:
        print("Error while saving data")

    
    