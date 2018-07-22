from django.db.models.signals import post_save
from django.dispatch import receiver
from hr_leaves.models import Employe, Conge, Type_conge
import datetime

def init_employe_leave(instance):
    all_types = Type_conge.objects.all()
    for typ in all_types:
        conge = Conge.objects.filter(employe=instance, type_conge=typ)
        # si j'enleve cette condition, il y'aura des doublons dans la bd
        # normalement c'est le else de cette condition qui devrai empecher cela
        # mais bizzarement ca ne marche pas et je ne sais pourquoi,
        # par pur hazard j'ai mis dans dans le if et ca marché :-)
        # donc je le garde pour le moment
        if conge:
            conge = Conge.objects.create(
                employe = instance,
                type_conge = typ,
                last_calculation_date = datetime.datetime.now()
            )

def new_leave_type(instance):
    all_employe = Employe.objects.all()
    for employe in all_employe:
        Conge.objects.create(
            employe = employe,
            type_conge = instance,
            last_calculation_date = datetime.datetime.now()
        )
        
# est declancher a chaque fois que le model
# employe est modifier
# donc pour chaque nouvelle creation nous initialisation les conges
@receiver(post_save, sender=Employe)
def employe_post_save(sender, instance, created, **kwargs):
    if created and isinstance(instance, Employe):
        init_employe_leave(instance)

# a chaque fois qu'une nouvelle type de conge est creer
# on initialiser pour tous les utilisateur ce type
# de conge la
@receiver(post_save, sender=Type_conge)
def type_conge_post_save(sender, instance, created, **kwargs):
    if created:
        new_leave_type(instance)

