import logging

logger = logging.getLogger(__name__)


def update_or_add_to_basket(user, basket_obj, product_obj, basket_model):
    if not basket_obj.exists():
        basket_model.objects.create(user=user, product=product_obj, quantity=1)
        logger.debug('Create basket obj')
    else:
        basket = basket_model.objects.first()
        basket.quantity += 1
        basket.save()
        logger.debug('Update basket obj')


def create_basket_item_json(product_name, quantity, price, _sum):
    basket_item = {
        'product_name': product_name,
        'quantity': quantity,
        'price': price,
        'sum': _sum,
    }
    return basket_item
