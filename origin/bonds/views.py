from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Bond
from .serializers import BondSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondView(APIView):
    serializer_class = BondSerializer

    def get(self, request):
        legal_name_filter = request.query_params.get('legal_name')
        if legal_name_filter:
            bonds = Bond.objects.filter(legal_name__icontains=legal_name_filter).all()
        else:
            bonds = Bond.objects.all()
        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BondSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
