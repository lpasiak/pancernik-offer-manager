import requests
import pandas as pd
import config
from lxml import etree

url = "https://mobiwear.pl/data/export/feed10024_136da4b82a149cf3d9c16964.xml"
file_path = f'{config.SHEETS_DIR}/mobiwear.xml'

# def download_xml_file(path, url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(path, "wb") as f:
#             f.write(response.content)
#         print("File downloaded and saved as downloaded_file.xml")
#     else:
#         print(f"Failed to download file. Status code: {response.status_code}")
        
# download_xml_file(file_path, url)

tree = etree.parse(file_path)
root = tree.getroot()
products = root.xpath('.//product')
data = []

for prod in products:
    prod_dict = {
        "id": prod.attrib.get("id"),
        "code_on_card": prod.attrib.get("code_on_card"),
        "series": prod.findtext("series"),
        "name": prod.find("description/name").text,
        "short_desc": prod.find("description/short_desc").text,
        "long_desc": prod.find("description/long_desc").text,
        "price_net": prod.find("price").attrib.get("net"),
        "price_gross": prod.find("price").attrib.get("gross"),
    }

    # Add first size (you can extend to loop all sizes)
    size = prod.find("sizes/size")
    if size is not None:
        prod_dict.update({
            "size_code": size.attrib.get("code"),
            "code_producer": size.attrib.get("code_producer"),
            "code_external": size.attrib.get("code_external"),
            "size_price_net": size.find("price").attrib.get("net"),
            "size_price_gross": size.find("price").attrib.get("gross"),
        })

    # Parameters (flatten values as comma-separated strings)
    params = {}
    for param in prod.findall("parameters/param"):
        name = param.attrib.get("name")
        values = [val.text for val in param.findall("value") if val.text]
        params[name] = ", ".join(values) if values else None

    prod_dict.update(params)

    # Images
    images = prod.findall("images/images/large/image")
    image_urls = [img.attrib["url"] for img in images]
    images_string = '; '.join(image_urls)
    prod_dict["image_urls"] = images_string

    data.append(prod_dict)

df = pd.DataFrame(data)
df.to_csv(config.SHEETS_DIR/'mobiwear.csv', sep=';', index=False)
