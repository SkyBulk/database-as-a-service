# -*- coding: utf-8 -*-
from . import BaseDriver
from util import get_credentials_for
from dbaas_credentials.models import CredentialType


class SQLServer(BaseDriver):

    @classmethod
    def topology_name(cls):
        return ['sqlserver_single']

    @property
    def credential_type(self):
        return CredentialType.SQLSERVER

    def build_new_infra_auth(self):
        credential = get_credentials_for(
            environment=self.databaseinfra.environment,
            credential_type=self.credential_type
        )
        return credential.user, credential.password, None

    def create_database(self, database):
        pass

    def remove_database(self, database):
        pass

    def create_user(self, credential):
        pass

    def update_user(self, credential):
        pass

    def remove_user(self, credential):
        pass

class SQLServerAlwaysOn(SQLServer):

    @classmethod
    def topology_name(cls):
        return ['sqlserver_always_On']
