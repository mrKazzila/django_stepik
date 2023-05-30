from .models import Basket


def baskets(request):
    """Context processor func for view user baskets"""
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
