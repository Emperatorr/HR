from .models import *
from django.db.models import Count
import json

def number_of_travel_by_ministry(all_elem):
    return all_elem

def categorie_of_travelers():
    all_elem = Mission.objects.select_related() \
    .values('ministry', 'ministry__name', 'missionpersonne__persone__state') \
    .annotate(etats=Count('ministry'))\
    .order_by('ministry')

    return all_elem
# number of travel by ministry
def travel_by_ministry_old():
    data = []
    all_names = []

    all_elem = Mission.objects.select_related() \
    .values('ministry', 'ministry__name') \
    .annotate(voyages=Count('ministry'))\
    .order_by('ministry')

    for val in all_elem:
        data.append({
            'name' : val.get('ministry__name'),
            'data' : [val.get('voyages')]
        })
        all_names.append(
            val.get('ministry__name')
            )
    # after the loop we add it to the returned values
    data.append({
        'names' : all_names
    })

    return data
# price of travel by ministry
def travel_by_ministry():
    data = []
    all_data = []
    all_elem = Mission.objects.select_related() \
    .values('ministry', 'ministry__name') \
    .annotate(voyages=Count('ministry'))\
    .order_by('ministry')

    for val in all_elem:
        # 'name' : val.get('ministry__name'),
        temp = [
            val.get('ministry__name'),
            val.get('voyages')
        ]
        all_data.append(
            temp
        )

    data.append({
        'name': 'Les voyages',
        'data' : all_data
    })

    return data

# price of travel by ministry
def price_by_ministry():
    data = []
    all_elem = Mission.objects.all() \
    .values('ministry', 'id', 'ministry__name', 'ministry__id') \
    .annotate(voyages=Count('ministry'))\
    .order_by('ministry')

    temp = dict()

    for val in all_elem:
        mission_id = val.get('id')
        ministry_id = val.get('ministry__id')
        ministry_name = val.get('ministry__name')

        # the proposition
        proposition = FlightSuggestion.objects.filter(mission=mission_id, user_validated=True)

        if proposition:
            if  ministry_id in temp:
                temp[ministry_id]['gnf'] += proposition[0].price
                temp[ministry_id]['usd'] += proposition[0].price_usd
            else:
                temp[ministry_id] = dict()
                temp[ministry_id]['name'] = ministry_name
                temp[ministry_id]['gnf'] = proposition[0].price
                temp[ministry_id]['usd'] = proposition[0].price_usd

    # convert the list to array
    arr = []
    for val in temp:
        elem = temp.get(val)
        arr.append(elem)

    # then format it for chart
    all_gnf = [i['gnf'] for i in arr]
    all_usd = [i['usd'] for i in arr]
    all_names = [i['name'] for i in arr]

    data.append({
        'name' : 'USD',
        'data' : all_usd
    })

    data.append({
        'name' : 'GNF',
        'data' : all_gnf
    })
    data.append({
        'names': all_names
    })

    return data


# categorie of travel by ministry
def categorie_by_ministry():
    data = []
    all_elem = Mission.objects.all() \
    .values('ministry', 'id', 'ministry__name', 'ministry__id') \
    .annotate(voyages=Count('ministry'))\
    .order_by('ministry')

    temp = dict()

    for val in all_elem:
        mission_id = val.get('id')
        ministry_id = val.get('ministry__id')
        ministry_name = val.get('ministry__name')

        # the proposition
        mission_personne = Mission_Personne.objects.filter(mission=mission_id)

        if mission_personne:
            for val in mission_personne:

                # Choices
                minister = STATE_CHOICES[0][0]
                public_worker = STATE_CHOICES[1][0]
                contractual = STATE_CHOICES[2][0]
                consultant = STATE_CHOICES[3][0]
                trainee = STATE_CHOICES[4][0]

                state = val.persone.state

                if ministry_id in temp:
                    if (state == minister and minister != None):
                        temp[ministry_id]['ministre'] += 1
                    elif (state == public_worker and public_worker != None):
                        temp[ministry_id]['fonctionnaire'] += 1
                    elif (state == contractual and contractual != None):
                        temp[ministry_id]['contractuel'] += 1
                    elif (state == consultant and consultant != None):
                        temp[ministry_id]['consultant'] += 1
                    elif (state == trainee and trainee != None):
                        temp[ministry_id]['stagiaire'] += 1
                else:
                    temp[ministry_id] = dict()
                    temp[ministry_id]['name'] = ministry_name
                    temp[ministry_id]['ministre'] = 0
                    temp[ministry_id]['fonctionnaire'] = 0
                    temp[ministry_id]['contractuel'] = 0
                    temp[ministry_id]['consultant'] = 0
                    temp[ministry_id]['stagiaire'] = 0

                    if (state == minister and minister != None):
                        temp[ministry_id]['ministre'] = 1
                    elif (state == public_worker and public_worker != None):
                        temp[ministry_id]['fonctionnaire'] = 1
                    elif (state == contractual and contractual != None):
                        temp[ministry_id]['contractuel'] = 1
                    elif (state == consultant and consultant != None):
                        temp[ministry_id]['consultant'] = 1
                    elif (state == trainee and trainee != None):
                        temp[ministry_id]['stagiaire'] = 1

        # convert the list to array
    arr = []
    for val in temp:
        elem = temp.get(val)
        arr.append(elem)

    # then format it for chart
    all_minister = []
    all_public_worker = []
    all_contractual = []
    all_consultant = []
    all_trainee = []
    all_names = []

    for i in arr:
        all_minister.append(
            i['ministre']
        )
        all_public_worker.append(
            i['fonctionnaire']
        )
        all_contractual.append(
            i['contractuel']
        )
        all_consultant.append(
            i['consultant']
        )
        all_trainee.append(
            i['stagiaire']
        )

        all_names.append(
            i['name']
        )

    data.append({
        'name' : 'Ministre',
        'data' : all_minister
    })
    data.append({
        'name' : 'Fonctionnaire',
        'data' : all_public_worker
    })

    data.append({
        'name' : 'Contractuel',
        'data' : all_contractual
    })

    data.append({
        'name' : 'Consultant',
        'data' : all_consultant
    })

    data.append({
        'name' : 'Stagiaire',
        'data' : all_trainee
    })

    data.append({
        'names': all_names
    })

    return data

# price of travel by ministry
def document_submission_by_ministry():
    data = []
    all_elem = Mission.objects.all() \
    .values('ministry', 'id', 'ministry__name', 'ministry__id', 'is_document_uploaded_lately') \
    .annotate(voyages=Count('ministry'))\
    .order_by('ministry')

    temp = dict()

    for val in all_elem:

        ministry_id = val.get('ministry__id')
        ministry_name = val.get('ministry__name')

        is_document_uploaded_lately = val.get('is_document_uploaded_lately', False)

        if  ministry_id in temp:
            if is_document_uploaded_lately:
                temp[ministry_id]['lately'] += 1
            else:
                temp[ministry_id]['early'] += 1
        else:
            temp[ministry_id] = dict()
            temp[ministry_id]['name'] = ministry_name

            temp[ministry_id]['early'] = 0
            temp[ministry_id]['lately'] = 0

            if is_document_uploaded_lately is True:
                temp[ministry_id]['lately'] += 1
            else:
                temp[ministry_id]['early'] += 1

    # convert the list to array
    arr = []
    for val in temp:
        elem = temp.get(val)
        arr.append(elem)

    # then format it for chart
    all_early = []
    all_lately = []
    all_names = []

    all_early = [i['early'] for i in arr]
    all_lately = [i['lately'] for i in arr]
    all_names = [i['name'] for i in arr]

    data.append({
        'name' : 'OM tardif',
        'data' : all_lately
    })

    data.append({
        'name' : 'OM en regle',
        'data' : all_early
    })
    data.append({
        'names': all_names
    })

    return data
##########################################################################################

# categorie of travel by ministry
def approuve_by_ministry() :
    data = []
    all_elem = Mission.objects.all() \
    .values('ministry', 'id', 'ministry__name', 'ministry__id', 'status') \
    .annotate(voyages=Count('ministry'))\
    .order_by('ministry')

    temp = dict()

    for val in all_elem:
        
        ministry_id = val.get('ministry__id')
        ministry_name = val.get('ministry__name')

        is_document_uploaded_lately = val.get('status', 0)

        if  ministry_id in temp :
            if is_document_uploaded_lately < 6:
                temp [ministry_id]['Approuvée'] +=  1
            else:
                temp [ministry_id]['Non Approuvée'] +=  1    
        else:
            temp [ministry_id] = dict()
            temp [ministry_id]['name'] = ministry_name
            
            temp [ministry_id]['Approuvée'] =  0
            temp [ministry_id]['Non Approuvée'] = 0

            if is_document_uploaded_lately < 6:
                temp [ministry_id]['Approuvée'] += 1
            else:
                temp [ministry_id]['Non Approuvée'] += 1

    # convert the list to array
    arr = []
    for val in temp:
        elem = temp.get(val)
        arr.append(elem)
    
    # then format it for chart
    all_early = [] 
    all_lately = []
    all_names = []

    all_early = [i['Approuvée'] for i in arr]
    all_lately = [i['Non Approuvée'] for i in arr]
    all_names = [i['name'] for i in arr]
    
    data.append ({
        'name' : 'Approuvée',
        'data' : all_lately
     })
    
    data.append ({
        'name' : 'Non Approuvée',
        'data' : all_early
        })
    data.append ({
        'names': all_names
    })

    return data

# document of mission
def documents_submission_by_ministry() :
    data = []
    all_elem = Mission.objects.all() \
    .values('ministry', 'id', 'ministry__name', 'ministry__id', 'document') \
    .annotate(voyages=Count('ministry'))\
    .order_by('ministry')

    temp = dict()

    for val in all_elem:
        
        ministry_id = val.get('ministry__id')
        ministry_name = val.get('ministry__name')

        is_document_uploaded_lately = val.get('document', '')

        if  ministry_id in temp :
            if is_document_uploaded_lately == '':
                temp [ministry_id]['lately'] +=  1
            else:
                temp[ministry_id]['early'] += 1
        else:
            temp[ministry_id] = dict()
            temp[ministry_id]['name'] = ministry_name

            temp[ministry_id]['early'] = 0
            temp[ministry_id]['lately'] = 0

            if is_document_uploaded_lately is True:
                temp[ministry_id]['lately'] += 1
            else:
                temp[ministry_id]['early'] += 1

    # convert the list to array
    arr = []
    for val in temp:
        elem = temp.get(val)
        arr.append(elem)

    # then format it for chart
    all_early = []
    all_lately = []
    all_names = []

    all_early = [i['early'] for i in arr]
    all_lately = [i['lately'] for i in arr]
    all_names = [i['name'] for i in arr]
    
    data.append ({
        'name' : "Pas d'ordre de mission",
        'data' : all_lately
     })
    
    data.append ({
        'name' : 'Ordre de mission',
        'data' : all_early
    })
    data.append({
        'names': all_names
    })

    return data

