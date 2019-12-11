import requests
from .models import Manufacturer, ProductInfo, Product

def cron_job():
    def is_name_exist(name, list):
        for el in list:
            if name == el['name']:
                return True
        return False

    result = []
    product_info_list = ProductInfo.objects.all()
    #product_info_list = ProductInfo.objects.all().annotate(num_product=Count('product_set', filter=Q(product_set__status=1))).order_by('num_product')
    for productinfo in product_info_list:
        if productinfo.product_set.count() < productinfo.min_stock:
            # count all same name of p_i
            pi_list = ProductInfo.objects.filter(name=productinfo.name)
            sum = 0
            for pi in pi_list:
                sum = sum + Product.objects.filter(status=1, product_info=pi).count()

            # check sum
            if sum < productinfo.min_stock:
                # check duplication
                if is_name_exist(productinfo.name, result):
                    pass
                else:
                    result.append({
                        'name' : productinfo.name,
                        'product_total_count' : sum,
                        'product_min_stock': productinfo.min_stock,
                    })

    result = sorted(result, key=lambda pi: pi['product_total_count'])

    str = ''
    for el in result:
        str += '{} ({}/{})\n'.format(result['name'], result['product_total_count'], result['product_min_stock'])

    phones = ['01038953444']

    for phone in phones:
        url = "http://221.139.14.189/API/alimtalk_api"
        data = {
            'api_key': 'NJZ58CKQW8X1113',
            'template_code': 'SJT_036954',
            'variable': str,
            'dstaddr': phone,
            'next_type': '0',
            'send_reserve': '0',
            'callback': phone,
        }
        requests.post(url = url, data = data)
