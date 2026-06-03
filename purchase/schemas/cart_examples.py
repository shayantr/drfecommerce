from drf_spectacular.utils import OpenApiExample


class CartExample:
    create_request = OpenApiExample(
        "مثال ۱",
        value={
            "product": 2,
            "quantity": 3
        },
        request_only=True,
    )
    retrieve = OpenApiExample(
        "مثال ۱",
        value={
            'id': 2
        }
    )