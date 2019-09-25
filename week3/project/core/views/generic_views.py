from rest_framework import generics
from rest_framework import mixins
from core.models import Block
from core.serializers import ProjectSerializer, BlockSerializer
from rest_framework.permissions import IsAuthenticated



class BlockListView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.request.data['project_id'])
        print(project)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)
