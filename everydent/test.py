import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "everydent.settings")
django.setup()

from product_app.models import Product, ProductInfo, Manufacturer

# request post
import requests

url = "221.139.14.189/API/alimtalk_api"
data = {
    'api_key': 'NJZ58CKQW8X1113',
    'template_code': 'SJT_036954',
    'variable': '테스트',
    'dstaddr': '01038953444',
    'next_type': '0',
    'send_reserve': '0',
    'callback': '01038953444',
}

r = requests.post(url = API_ENDPOINT, data = data) 
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)

# 오스템 코드 수정
#
# exist_list = []
# for pi in Manufacturer.objects.get(name="오스템").product_infos.all():
#     if pi.name in exist_list:
#         print(pi.name + ' 중복')
#         for p in pi.product_set.all():
#             print('  {}'.format(p.full_code))
#         # if len(ProductInfo.objects.filter(name=pi.name)) > 2:
#         #     if pi.code == ProductInfo.objects.filter(name=pi.name)[1].code:
#         #         print('일치')
#         #         for p in pi.product_set.all():
#         #             p.product_info = ProductInfo.objects.filter(name=pi.name)[1]
#         #             p.save()
#         #         pi.delete()
#     else:
#         exist_list.append(pi.name)
#         print(pi.name)
#         for p in pi.product_set.all():
#             print('  {}'.format(p.full_code))

# for pi in Manufacturer.objects.get(name="오스템").product_infos.all():
#     # print(pi.name)
#     # for p in pi.product_set.all():
#     #     print(p.full_code)
#     # print('\n')
#     full_code = pi.product_set.all()[0].full_code
#     product_code = full_code[3:8]
#     pi.code = product_code
#     pi.save()

# 겹치는 이름 ?
# exist_list = []
# for pi in ProductInfo.objects.all():
#     if pi.name in exist_list:
#         same_list = ProductInfo.objects.filter(name=pi.name)
#         for i, same in enumerate(same_list):
#             print('{} <{}>'.format(same.name, i+1))
#             for p in same.product_set.all():
#                 print('  {}'.format(p.full_code))
#             print('\n')
#     else:
#         exist_list.append(pi.name)

#product_list = ProductInfo.objects.filter(name__icontains='Ts')
#for p in product_list:
#    p.delete()


### ---- date before ****** -----------
# import re
# import datetime
#
# f = open("2019_12_04_before.txt", "w", encoding = "utf-8")
#
# def is_name_exist(name, list):
#     for el in list:
#         if name == el['name']:
#             return True
#     return False
#
# result = []
# product_info_list = ProductInfo.objects.all().order_by("name")
# convert = lambda text: int(text) if text.isdigit() else text
# alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key.name) ]
# product_info_list = sorted( product_info_list, key=alphanum_key )
#
# for productinfo in product_info_list:
#     # count all same name of p_i
#     date = datetime.date(2019, 12, 5)
#     pi_list = ProductInfo.objects.filter(name=productinfo.name)
#     product_sum = 0
#     returned_sum = 0
#     used_sum = 0
#     for pi in pi_list:
#         product_sum = product_sum + Product.objects.filter(created_time__lte=date, status=1, product_info=pi).count()
#         used_sum = used_sum + Product.objects.filter(created_time__lte=date, status=2, product_info=pi).count()
#         returned_sum = returned_sum + Product.objects.filter(created_time__lte=date, status=3, product_info=pi).count()
#
#     # check duplication
#     if is_name_exist(productinfo.name, result):
#         pass
#     else:
#         result.append({
#             'name' : productinfo.name,
#         })
#         f.write('{} {}개\n'.format(productinfo.name, product_sum + used_sum + returned_sum))
#
# f.close()
##################################
