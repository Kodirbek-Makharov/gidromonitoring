from monitoring.models import Dalolatnoma
from datetime import datetime

def header_context(request):
    # muddati_otmagan = Dalolatnoma.objects.filter(bartaraf_etilganligi=False).count()
    muddati_otgan = Dalolatnoma.objects.filter(bartaraf_etilganligi=False, amal_qilish_muddati__lt=datetime.now().date()).count()
    muddati_otmagan = Dalolatnoma.objects.filter(bartaraf_etilganligi=False, amal_qilish_muddati__gte=datetime.now().date()).count()
    return {'muddati_otgan': muddati_otgan, 'muddati_otmagan': muddati_otmagan}

# def footer_context(request):
#     footer_info = FooterInfo.objects.first()
#     return {'footer_info': footer_info}