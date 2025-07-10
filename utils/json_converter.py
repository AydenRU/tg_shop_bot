import json

def json_in_list(data) -> list:
    return  json.loads(data)


async def json_basket(data: list[dict]) -> str:
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