from .models import*

def slick(request):
    info = AppInfo.objects.get(pk=1)
    cat = Category.objects.all()


    context = {
        'info':info,
        'cat':cat,
    }

    return context

