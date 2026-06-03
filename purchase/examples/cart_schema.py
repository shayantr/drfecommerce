from drf_spectacular.utils import extend_schema

from purchase.schemas.cart_examples import CartExample


class CartSchemas:
    create = extend_schema(
        summary="سبد خرید",
        description="اضافه کردن به سبد خرید با پاس دادن آیدی محصول و تعداد انتخابی",
        examples=[CartExample.create_request]
    )
    retrieve = extend_schema(
        summary="جزئیات محصول داخل سبد",
        description="دریافت جزئیات محصول به همراه تعداد و جمع مبلغ محصول سبد خرید با گرفتن آیدی آیتم",
        examples=[CartExample.retrieve]
    )
    list = extend_schema(
        summary='لیست سبد خرید',
        description='گرفتن لیست سبد خرید به همراه جمع مبالغ هر محصول و کل محصولات بدون نیاز به گرفتن آیدی سبد خرید',
    )
