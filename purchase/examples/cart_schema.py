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
    patch = extend_schema(
        summary='آپدیت کردن تعداد محصول',
        description="آپدیت کردن تعداد محصول با گرفتن آیدی آیتم در سبد خرید و تغییر تعداد محصول یا آیتم انتخابی",
        examples=[CartExample.put]
    )
    delete = extend_schema(
        summary='پاک کردن آیتم داخل سبد کارت',
        description="با استفاده از آیدی یکتای آیتم در سبد خرید میتوانید محصول مورد نظر را پاک کنید"
    )
    apply_discount = extend_schema(
        summary="اضافه کردن کد تخفیف به سبد",
        description="اضافه کردن کد تخفیف با استفاده از متد پچ در سبد خرید",
        examples=[CartExample.apply_discount]
    )