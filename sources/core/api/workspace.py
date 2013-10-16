from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from core.api.user import CreatedByUserSerializer
from core.models import Workspace


class WorkspaceSerializer(ModelSerializer):
    created_by = CreatedByUserSerializer(required=False)

    class Meta:
        model = Workspace
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'created_by')

class WorkspaceViewSet(ModelViewSet):
    """
    API endpoint that allows workspaces to be viewed or edited.
    """
    model = Workspace
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkspaceSerializer

    def pre_save(self, object):
        if object.pk is None:
            object.created_by = self.request.user;
        return super(WorkspaceViewSet, self).pre_save(object)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Workspace.objects.filter(created_by=self.request.user)
        return queryset