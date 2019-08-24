import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "everydent.settings")
django.setup()

from product_app.models import Manufacturer, ProductInfo

manufacturer_list = [
  {
    'name': '메가젠 QR',
    'code': '08806388',
  },
  {
    'name': '덴티스 QR',
    'code': '08806169',
  },
  {
    'name': '덴티스 1D',
    'code': 'LPFX',
  },
  {
    'name': '오스템 1D',
    'code': '18L0',
  },
  {
    'name': '티타늄 QR',
    'code': '07630031',
  }
]

product_info_list = [
  {
    'manufacturer_name': '메가젠 QR',
    'name': 'AnyOne Internal Fixture 4.5/L10.0',
    'code': '220908',
  },
  {
    'manufacturer_name': '덴티스 QR',
    'name': 's-Clean OneQ-SL 4.7 x 8mm',
    'code': '127587',
  },
]

for manufacturer in manufacturer_list:
    manu = Manufacturer(name=manufacturer['name'], code=manufacturer['code'])
    manu.save()

for product_info in product_info_list:
    manu = Manufacturer.objects.get(name=product_info['manufacturer_name'])
    pi = ProductInfo(
        name=product_info['name'],
        code=product_info['code'],
        manufacturer=manu,
    )
    pi.save()
