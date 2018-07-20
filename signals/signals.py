from django.db.models.signals import post_save
from django.dispatch import receiver
from hr_leaves.models import Employe, Conge, Type_conge

def init_employe_leave(instance):
    all_types = Type_conge.objects.all()
    for typ in all_types:
        conge = Conge()
        conge.employe = instance,
        conge.type_conge = typ
        conge.save()

def new_leave_type(instance):
    all_employe = Employe.objects.all()
    for employe in all_employe:
        conge = Conge()
        
        conge.employe = employe,
        conge.type_conge = instance
        conge.save()
        
# est declancher a chaque fois que le model
# employe est modifier
# donc pour chaque nouvelle creation nous initialisation les conges
@receiver(post_save, sender=Employe)
def employe_post_save(sender, instance, created, **kwargs):
    if created:
        init_employe_leave(instance)

# a chaque fois qu'une nouvelle type de conge est creer
# on initialiser pour tous les utilisateur ce type
# de conge la
@receiver(post_save, sender=Type_conge)
def type_conge_post_save(sender, instance, created, **kwargs):
    if created:
        new_leave_type(instance)

