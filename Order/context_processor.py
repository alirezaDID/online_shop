from .session import OrderSession



def basket(request):
    return {
        'basket': OrderSession(request)
    }


def is_check_out(request):
    return {
        'is_check_out': request.session.get("check_out")
    }


def check_out_order(request):
    return {
        'check_out_order': request.session.get("check_out_order")
    }