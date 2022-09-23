from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,AllowAny)
from mynews.apis.pagination import StandardResultsSetPagination
from rest_framework import generics
from mynews.apis.serializers import ItemsSerializer
from mynews.models import Items

class ItemsListAPIView(APIView):
    page_size = 100
    queryset = Items.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    serializer_class = ItemsSerializer

    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"detail":serializer.errors}, status.HTTP_400_BAD_REQUEST)
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                 self._paginator = None
            else:
                 self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)




class ItemUpdateDeleteAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemsSerializer

    def put(self, request, pk ,*args, **kwargs):
        to_update = Items.objects.filter(hacker_id = pk, hackernews=False, deleted=False, dead=False).last()
        if to_update is not None:
            serializer = self.serializer_class(to_update,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail":"News item updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail":"News Item not found"}, status.HTTP_404_NOT_FOUND)
        return Response({"detail":serializer.errors}, status.HTTP_400_BAD_REQUEST)     

    def delete(self, request, pk):
        to_update = Items.objects.filter(hacker_id = pk, hackernews=False, deleted=False, dead=False).last()
        if to_update is not None:
            to_update.deleted = True
            to_update.dead = True
            to_update.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"News Item not found"}, status.HTTP_404_NOT_FOUND)



    
        




class UpdateNewsItemView(generics.UpdateAPIView):
    serializer_class = ItemsSerializer
    model = Items
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            to_update = Items.objects.filter(id = serializer.validated_data['id'], hackernews=False).exists()

            if to_update:
                serializer.save()
                return Response({"detail":"News item saved successfully"}, status=status.HTTP_200_OK)

            else:
                return Response({"detail":"News Item not found"}, status.HTTP_404_NOT_FOUND)

        return Response({"detail":serializer.errors}, status.HTTP_400_BAD_REQUEST)     

