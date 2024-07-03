# context_processors.py in libroStoreNet
from .models import Cliente

def user_info(request):
    if request.session.get('cliente_id'):
        cliente = Cliente.objects.filter(id=request.session['cliente_id']).first()
        if cliente:
            return {
                'user_name': f"{cliente.nombresCliente} {cliente.apellidoPaternoCliente}"
            }
    return {}
