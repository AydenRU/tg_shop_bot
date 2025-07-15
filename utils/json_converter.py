import json

def json_in_list(data) -> list:
    """
    распаковка json файлов
    :param data:
    :return:
    """
    return  json.loads(data)


async def json_basket(data: list[dict]) -> str:
    """
    Подготовка данных в json формате
    :param data:
    :return:
    """
    result = []
    for item in data:
        cost = float(item['cost'])

        result.append({
            'name_product': item['nameproduct'],
            'quantity': item['quantity'],
            'cost': cost,
        })

    return json.dumps(result, ensure_ascii=False)


# products.id, products.nameproduct, baskets.quantity, products.cost