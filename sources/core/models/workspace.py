from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.manager import Manager
from django.db.models import F, Q

from core.models.member import Member
from core.models.member_fields import MemberStatusField
from core.models.role import Role
from core.models.role_fields import RoleLevelField
from core.tools.tree import TreeItemMixin


class WorkspaceManager(Manager):

    def all_for_user(self, user):
        workspaces = self.filter(
            Q(
                Q(role__member__user=user) |
                Q(vault__role__member__user=user) |
                Q(vault__card__role__member__user=user)
            )
        ).distinct()

        return workspaces

    def create_member_with_workspace(self, workspace):
        attrs_needed = ['_user', ]
        if not all(hasattr(workspace, attr) for attr in attrs_needed):
            raise AttributeError('_user attribute is required to create related membership')

        m = Member(
            workspace=workspace,
            user=workspace._user,
            status=MemberStatusField.STATUS_MEMBER,
            created_by=workspace._user
        )
        m.save()

        r = Role(
            member=m,
            to_workspace=workspace,
            created_by=workspace._user,
            level=RoleLevelField.LEVEL_WRITE
        )
        r.save()


class Workspace(models.Model, TreeItemMixin):
    class Meta:
        db_table = u'vaultier_workspace'
        app_label = 'core'

    objects = WorkspaceManager()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.ForeignKey('core.User', on_delete=PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_parent_object(self):
        return None

    def save(self, *args, **kwargs):
        created = self.id == None
        super(Workspace, self).save(*args, **kwargs)
        if created:
            Workspace.objects.create_member_with_workspace(self)
