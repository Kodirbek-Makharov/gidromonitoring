from .models import *
import datetime 
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# class aApiDalolatnomaList(APIView):
#     def get(self, request):
#         dalolatnoma = Dalolatnoma.objects.select_related("tuman__viloyat", 'noqonuniy_holat_turi', 'stansiya', 'inspektor').order_by('-korsatma_sana').all()
#         serializer = DalolatnomaSerializer(dalolatnoma, many=True, context={'request': request})
#         return Response(serializer.data)

class ApiDalolatnomaList(generics.ListCreateAPIView):
    queryset = Dalolatnoma.objects.select_related("tuman__viloyat", 'noqonuniy_holat_turi', 'stansiya', 'inspektor').order_by('-korsatma_sana').all()
    serializer_class = DalolatnomaSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = PersonFilter

    def post(self, request):
        stansiya_prefix = Stansiya.objects.filter(pk=request.data['stansiya']).first().seriya
        serializer = DalolatnomaSerializer(data=request.data, context={'stansiya_prefix': stansiya_prefix})
        if serializer.is_valid():
            # inspektor_id = request.data.get('inspektor')
            # serializer.validated_data['inspektor'] = User.objects.get(pk=inspektor_id)
            factor=serializer.save()
            
            return Response({"status": "saved", "id": factor.pk }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiDalolatnomaShow(generics.RetrieveAPIView):
    queryset = Dalolatnoma.objects.select_related("tuman__viloyat", 'noqonuniy_holat_turi', 'stansiya', 'inspektor').order_by('-korsatma_sana').all()
    serializer_class = DalolatnomaSerializer 


@api_view(['POST'])
def api_get_user(request):
    login = request.data.get('login')
    password = request.data.get('password')

    if not login or not password:
        return Response({"error": "Login and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=login, password=password)

    if user is not None and user.is_active:
        return Response({"user_id": user.id}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found or inactive."}, status=status.HTTP_404_NOT_FOUND)
    
# class ApiBemorShowEditDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer



# class PersonFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(lookup_expr='icontains') 
#     jshshir = django_filters.CharFilter(lookup_expr='icontains') 
#     pasportData = django_filters.CharFilter(lookup_expr='icontains') 
#     homilaMuddati = django_filters.NumberFilter()
#     birthDate = django_filters.DateFilter()

#     class Meta:
#         model = Patient
#         fields = ['name', 'jshshir', 'pasportData', 'homilaMuddati', 'birthDate']