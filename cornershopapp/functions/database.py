from ..models import Store,Department
from django.db import transaction

"""
Parte para inserir novas stores no banco de dados, segue esses passos.
1 - validar se o banco já foi salvo no db, se sim ele retorna True.
2 - Caso nao tenha salvo a store ainda, ele sera salvo e retornara o obj da models salvo.
3 - Em caso de erro retornara False.
"""
def save_store(**stores):
    try:
        if store_exists(store_code=stores['code']):
            return True
        with transaction.atomic():
            store_db = Store(**stores)
            store_db.save()
            if store_db.pk:
                return store_db
    except Exception as e:
        print(e)
        return False


def store_exists(store_code):
    store = Store.objects.filter(code=store_code)
    return store.exists()

def save_departament(**departament):
    try:
        departament_db = Department.objects.filter(cod=departament['cod'])
        if departament_db.exists():
            return True
        else:
            with transaction.atomic():
                new_departament = Department(**departament)
                new_departament.save()
                if new_departament.pk:
                    return new_departament
    except Exception as e:
        print(e)
        return False




    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    cod = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    image_link = models.URLField()
    class Meta:
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['cod']),
        ]
