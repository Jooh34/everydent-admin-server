import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "everydent.settings")
django.setup()

from product_app.models import Manufacturer

manufacturer_list = [
  {
    'name': '메가젠',
    'code': '63882',
  },
  {
    'name': '원큐/에스큐 QR',
    'code': '61691',
  },
  {
    'name': '원큐/에스큐 1D',
    'code': 'LPFX',
  }
]

for manufacturer in manufacturer_list:
    manu = Manufacturer(name=manufacturer['name'], code=manufacturer['code'])
    manu.save()
