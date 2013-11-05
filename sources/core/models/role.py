from django.db import models
from django.db.models.deletion import PROTECT, CASCADE
from django.db.models.manager import Manager
from django.db.models.query_utils import Q
from core.models.role_fields import RoleLevelField, RoleTypeField


class RoleManager(Manager):

    def all_for_user(self, user):
        from core.models.workspace import Workspace
        from core.models.vault import Vault
        from core.models.card import Card

        # all workspaces user has permission write
        workspaces = Workspace.objects.filter(
            role__member__user=user,
            role__level=RoleLevelField.LEVEL_WRITE
        ).distinct()
        # roles to workspaces
        all_roles_to_workspaces = Q(to_workspace__in=workspaces, type=RoleTypeField.TYPE_WORKSPACE)

        #all vaults, where workspace is writable by user
        vaults = Vault.objects.filter(
            workspace__in=workspaces
        )
        # all roles to vaults
        all_roles_to_vaults = Q(to_vault__in=vaults, type=RoleTypeField.TYPE_VAULT)

        #all cards of vaults
        cards = Card.objects.filter(
            vault__in=vaults
        )
        # all roles to vaults
        all_roles_to_cards = Q(to_card__in=cards, type=RoleTypeField.TYPE_CARD)

        roles = Role.objects.filter(
            Q(all_roles_to_workspaces | all_roles_to_vaults | all_roles_to_cards)
        )

        return roles


    def create_or_update_role(self, role):
        existing = None
        try:
            existing = Role.objects.filter(
                member=role.member,
                to_workspace=role.to_workspace,
                to_vault=role.to_vault,
                to_card=role.to_card
            )[0]

        except:
            pass

        if not existing:
            role.save()
            return role
        else:
            existing.level = role.level
            existing.member = role.member
            existing.save()
            return existing


class Role(models.Model):
    class Meta:
        db_table = u'vaultier_role'
        app_label = 'core'

    objects = RoleManager()

    member = models.ForeignKey('core.Member', on_delete=CASCADE)
    type = RoleTypeField()
    to_workspace = models.ForeignKey('core.Workspace', on_delete=CASCADE, null=True, blank=True)
    to_vault = models.ForeignKey('core.Vault', on_delete=CASCADE, null=True, blank=True)
    to_card = models.ForeignKey('core.Card', on_delete=CASCADE, null=True, blank=True)
    level = RoleLevelField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('core.User', on_delete=PROTECT, related_name='roles_created')

    def compute_type(self, force=None):
        if not self.type or force:
            type_set = False

            if self.to_workspace:
                if type_set:
                    raise RuntimeError('Role can reference only one object')
                self.type = RoleTypeField.TYPE_WORKSPACE
                type_set = True

            if self.to_vault:
                if type_set:
                    raise RuntimeError('Role can reference only one object')
                self.type = RoleTypeField.TYPE_VAULT
                type_set = True

            if self.to_card:
                if type_set:
                    raise RuntimeError('Role can reference only one object')
                self.type = RoleTypeField.TYPE_CARD
                type_set = True


    def get_object(self):
        self.compute_type()
        if self.type == RoleTypeField.TYPE_WORKSPACE:
            return self.to_workspace
        if self == RoleTypeField.TYPE_VAULT:
            return self.to_vault
        if self == RoleTypeField.TYPE_CARD:
            return self.to_card

        raise RuntimeError('Role has no associated object')

    def save(self, *args, **kwargs):
        self.compute_type()
        return super(Role, self).save(*args, **kwargs)
