import urlparse
from django.conf import settings
from vaultier.business.mailer import VaultierMailer


class LostKeyMailer(VaultierMailer):
    """
    Custom VaultierMailer implementation for LostKey case
    """
    subject = '[Vaultier] lost key request'
    _template = 'mailer/lostkey'

    def _build_context(self, **kwargs):
        """
        Adds extra variable to template Context

        :return: Context
        """
        kwargs.update({'url': self._build_url()})
        return super(LostKeyMailer, self)._build_context(**kwargs)

    def send(self, **kwargs):
        """
        Adds lost key recipient

        :param kwargs:
        :return:
        """
        if self.object:
            self.add_to(self.object.created_by.email)
        return super(LostKeyMailer, self).send(**kwargs)

    def _build_url(self):
        """
        Generate frontend url to lost key page

        :return:
        """
        return urlparse.urljoin(
            settings.SITE_URL,
            '#/lostkey/{}/{}/'.format(self.object.id, self.object.hash)
        )


class InvitationMailer(VaultierMailer):
    """
    Sends email whenever user is send to new space

    """
    _template = 'mailer/invitation'
    subject = '[Vaultier] You have been invited'

    def send(self, **kwargs):
        """
        Adds recipient from object

        :param kwargs:
        :return:
        """
        if self.object:
            self.add_to(self.object.invitation_email)
        return super(InvitationMailer, self).send(**kwargs)

    def _build_context(self, **kwargs):
        """
        Adds extra variables to template Context

        :param kwargs: dict
        :return: Context
        """
        kwargs.update({
            'SITE_URL': settings.SITE_URL,
            'url': self._build_url()
        })
        return super(InvitationMailer, self)._build_context(**kwargs)

    def _build_url(self):
        """
        Generate frontend url to granted object

        :return: str
        """
        return urlparse.urljoin(
            settings.SITE_URL, '#/invitations/use/{}/{}/'.format(
                self.object.id, self.object.invitation_hash
            )
        )


class WorkspaceKeyTransferMailer(VaultierMailer):

    _template = 'mailer/transfer_workspace_key'

    def format_subject(self):
        """
        Return mail formatted subject

        :return:
        """
        return '[Vaultier] You can access the workspace: {}'.format(
            self.object.workspace.name
        )

    def send(self, **kwargs):
        """
        Adds recipient from object

        :param kwargs:
        :return:
        """
        if self.object:
            self.add_to(self.object.user.email)
        return super(WorkspaceKeyTransferMailer, self).send(**kwargs)

    def _build_context(self, **kwargs):
        """
        Adds extra variables to template Context

        :param kwargs: dict
        :return: Context
        """
        kwargs.update({
            'granted_workspace': self.object.workspace.name,
            'url': self._build_url()
        })
        return super(WorkspaceKeyTransferMailer, self)._build_context(**kwargs)

    def _build_url(self):
        """
        Generate frontend url to granted object

        :return: str
        """
        return urlparse.urljoin(settings.SITE_URL, '#/workspaces/w/{}/'.format(
            self.object.workspace.slug))
