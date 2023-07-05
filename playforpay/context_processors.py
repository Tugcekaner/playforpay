

from market.models import Shoping

def cart_counter(request):
    if request.user.is_authenticated:
        cart_count = Shoping.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}
