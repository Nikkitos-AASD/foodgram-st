from django.http import HttpResponse


def generate_shopping_list(ingredients):
    shopping_list = ['Shopping List\n']
    for ingredient in ingredients:
        shopping_list.append(
            f'{ingredient["product__name"]} - '
            f'{ingredient["amount"]} {ingredient["product__unit"]}\n'
        )

    response = HttpResponse(
        ''.join(shopping_list),
        content_type='text/plain'
    )
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )
    return response 