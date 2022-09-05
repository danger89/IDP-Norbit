import requests
from fake_useragent import UserAgent
from pathlib import Path
import json

def getJSON(url):
    header = {
        'User-Agent': UserAgent().safari
    }
    res = requests.get(url, headers=header)
    return res.json()

def getFilter(filters, name):
    att = next(x for x in filters if x["title"] == name)['remainingItems']
    name_id_dic = {}
    for i in att:
        name_id_dic[i['text']] = i['id']
    return name_id_dic

def storeProductIds():
    """Stores the feature ids that are needed for creating search filters. Should be used run in a while, to account for any changes on the server side."""

    url = 'https://www.idealo.de/mvc/CategoryData/results/category/4012?pageIndex=0&sortKey=DEFAULT&onlyNew=false&onlyBargain=false&onlyAvailable=false'
    res = getJSON(url)
    filters = res['productJsonFilterRows']['popularFilterAttributes']

    brands = getFilter(filters, "Hersteller")
    sizes = getFilter(filters, "Bildschirmgröße")

    output_file = Path(__file__).parent / 'data'
    output_file.mkdir(exist_ok=True, parents=True)
    with open(output_file / 'brands.json', 'w') as f:
        json.dump(brands, f, indent=4)
    with open(output_file / 'sizes.json', 'w') as f:
        json.dump(sizes, f, indent=4)


if __name__ == "__main__":
    storeProductIds()