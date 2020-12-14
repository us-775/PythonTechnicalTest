from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Bond
from .serializers import BondSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondView(APIView):
    serializer_class = BondSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Bond.objects.filter(user=request.user)
        legal_name_filter = request.query_params.get('legal_name')
        if legal_name_filter:
            qs = qs.filter(legal_name__icontains=legal_name_filter)
        bonds = qs.all()
        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BondSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
