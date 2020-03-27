
def get_object(model_class, id):
    try:
        obj = model_class.objects.get(id=id)
    except:
        obj = None
    return obj