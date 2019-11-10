import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "everydent.settings")
django.setup()

from product_app.models import Product, ProductInfo, Manufacturer

exist_list = []
for pi in Manufacturer.objects.get(name="오스템").product_infos.all():
    if pi.name in exist_list:
        print(pi.name + ' 중복')
        for p in pi.product_set.all():
            print('  {}'.format(p.full_code))
        # if len(ProductInfo.objects.filter(name=pi.name)) > 2:
        #     if pi.code == ProductInfo.objects.filter(name=pi.name)[1].code:
        #         print('일치')
        #         for p in pi.product_set.all():
        #             p.product_info = ProductInfo.objects.filter(name=pi.name)[1]
        #             p.save()
        #         pi.delete()
    else:
        exist_list.append(pi.name)
        print(pi.name)
        for p in pi.product_set.all():
            print('  {}'.format(p.full_code))

# for pi in Manufacturer.objects.get(name="오스템").product_infos.all():
#     # print(pi.name)
#     # for p in pi.product_set.all():
#     #     print(p.full_code)
#     # print('\n')
#     full_code = pi.product_set.all()[0].full_code
#     product_code = full_code[3:8]
#     pi.code = product_code
#     pi.save()
