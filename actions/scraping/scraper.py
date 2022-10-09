import json
from pathlib import Path
from .util import fetchJSON

def readJson(path):
    path += '.json'
    path = Path(__file__).parent / path
    with path.open() as json_file:
        data = json_file.read()
        data = json.loads(data)
        return data

# Expects data to be populated by idfetcher.py
brands = readJson('data/brands')
sizes = readJson('data/sizes')
types = readJson('data/types')

def getBrands():
    return brands

def getTypes():
    return types

def getBrandId(brand):
    try:
        return brands[brand]
    except KeyError:
        raise ValueError('Invalid brand supplied')

def getSizeId(size):
    for s, id in sizes.items():
        if float(s.split()[0].replace(",", ".")) == float(size):
            return id
    raise ValueError('Size not found')

def getTypeId(type):
    id = types.get(type)
    if id == None:
        raise ValueError('Type not found')
    return id

def getValidSize(size):
    # get closest number
    valid_size = min(sizes, key=lambda x:
        abs(float(x.replace(',', '.').replace(' Zoll', '')) - size)
    )
    valid_size = float(valid_size.replace(',', '.').replace(' Zoll', ''))
    return valid_size

def createSearchUrl(price_range, brand, size, type):
    url = "https://www.idealo.de/mvc/CategoryData/results/category/4012?pageIndex=0&sortKey=DEFAULT&onlyNew=false&onlyBargain=false&onlyAvailable=false"

    url += f"&p={price_range[0]}-{price_range[1]}" if price_range != None else ""
    url += f"&filters={getBrandId(brand)}" if brand != None else ""
    url += f"&filters={getSizeId(size)}" if size != None else ""
    url += f"&filters={getTypeId(type)}" if type != None else ""
    return url


def findProducts(price_range, brand, size, type):
    url = createSearchUrl(price_range, brand, size, type)

    products = []
    while url != None and len(products) < 50:
        res = fetchJSON(url)
        products += res['categoryJsonResults']['entries']

        pagination = res['categoryPagination']
        url = pagination['nextPageAjaxLink'] if pagination != None else None
    return products

# For testing
# ps = findProducts((0, 550), "Samsung", 65, "4K")
# for p in ps:
#     print(p['link']['productLink']['href'])
# correct_results = ['/preisvergleich/OffersOfProduct/201240173_-gu65au7179u-samsung.html',
#       'https://www.idealo.de/preisvergleich/OffersOfProduct/201452975_-ue65tu7095uxxc-samsung.html']
# if ps != correct_results:
#     raise ValueError("invalid result")
