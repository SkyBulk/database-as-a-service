# -*- coding: utf-8 -*-
from physical.models import Instance
from .base import BaseTopology, InstanceDeploy


class BaseSQLServer(BaseTopology):
    pass


class SQLServerSingle(BaseSQLServer):

    @property
    def driver_name(self):
        return 'sqlserver_single'

    def deploy_instances(self):
        return [[InstanceDeploy(Instance.SQLSERVER, 1433)]]

    def get_deploy_steps(self):
        return [
            {
            'Creating SQL Server infra': (
                'workflow.steps.util.host_provider.CreateSQlServerInfra',
            )}, {
            'Creating Database': (
                'workflow.steps.util.database.Create',
            )}, {
            'Creating Empty Step': (
                'workflow.steps.util.host_provider.EmptyStep',
            )}
        ]

class SQLServerAlwaysOn(BaseSQLServer):

    @property
    def driver_name(self):
        return 'sqlserver_always_On'
