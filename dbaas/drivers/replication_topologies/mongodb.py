# -*- coding: utf-8 -*-
from physical.models import Instance
from .base import BaseTopology, InstanceDeploy


class BaseMongoDB(BaseTopology):

    def get_configure_ssl_steps(self):
        return [{
            'Disable monitoring and alarms': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
            ),
        }] + [{
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateOpenSSlLib',
                'workflow.steps.util.ssl.MongoDBUpdateCertificates',
                'workflow.steps.util.ssl.CreateSSLFolder',
                'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfra',
                'workflow.steps.util.ssl.RequestSSLForInfra',
                'workflow.steps.util.ssl.CreateJsonRequestFileInfra',
                'workflow.steps.util.ssl.CreateCertificateInfraMongoDB',
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDB',
                'workflow.steps.util.ssl.SetInfraConfiguredSSL',
                'workflow.steps.util.ssl.SetInfraSSLModeAllowTLS',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
            ),
        }] + [{
            'Restart Database': (
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.database.CheckIfSwitchMasterRollback',
                'workflow.steps.util.vm.ChangeMasterRollback',
            ),
        }] + [{
            'Enabling monitoring and alarms': (
                'workflow.steps.util.db_monitor.UpdateInfraSSLMonitor',
                'workflow.steps.util.zabbix.UpdateMongoDBSSL',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            ),
        }]

    def get_update_ssl_steps(self):
        return [{
            'Disable monitoring and alarms': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
                'workflow.steps.util.ssl.UpdateExpireAtDateRollback',
                'workflow.steps.util.ssl.BackupSSLFolder',
            ),
        }] + [{
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateSSLForInfra',
                'workflow.steps.util.ssl.CreateJsonRequestFileInfra',
                'workflow.steps.util.ssl.CreateCertificateInfraMongoDB',
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDB',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            ),
        }] + [{
            'Restart Database': (
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.ssl.RestoreSSLFolder4Rollback',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            ),
        }] + [{
            'Enabling monitoring and alarms': (
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            ),
        }]

    def get_set_require_ssl_steps(self):
        return [{
            'Disable monitoring and alarms': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
            ),
        }] + [{
            'Setting SSL Mode to Prefer': (
                'workflow.steps.util.ssl.SetInfraSSLModePreferTLS',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.ssl.SetMongoDBPreferTLSParameter',
                'workflow.steps.util.database.StopNonDatabaseInstance',
                'workflow.steps.util.database.StartNonDatabaseInstance',
            ),
        }] + [{
            'Setting SSL Mode to Require': (
                'workflow.steps.util.ssl.SetInfraSSLModeRequireTLS',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.ssl.SetMongoDBRequireTLSParameter',
                'workflow.steps.util.database.StopNonDatabaseInstance',
                'workflow.steps.util.database.StartNonDatabaseInstance',
                'workflow.steps.mongodb.database.RecreateMongoLogRotateScript',
            ),
        }] + [{
            'Enabling monitoring and alarms': (
                'workflow.steps.util.db_monitor.UpdateInfraSSLMonitor',
                'workflow.steps.util.zabbix.UpdateMongoDBSSL',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            ),
        }]

    def get_set_not_require_ssl_steps(self):
        return [{
            'Disable monitoring and alarms': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
            ),
        }] + [{
            'Setting SSL Mode to Prefer': (
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.ssl.SetInfraSSLModePreferTLS',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
            ),
        }] + [{
            'Setting SSL Mode to Allow': (
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.ssl.SetInfraSSLModeAllowTLS',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.mongodb.database.RecreateMongoLogRotateScript',
            ),
        }] + [{
            'Enabling monitoring and alarms': (
                'workflow.steps.util.db_monitor.UpdateInfraSSLMonitor',
                'workflow.steps.util.zabbix.UpdateMongoDBSSL',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            ),
        }]

    def get_configure_ssl_libs_and_folder_steps(self):
        return (
            'workflow.steps.util.ssl.UpdateOpenSSlLibIfConfigured',
            'workflow.steps.util.ssl.MongoDBUpdateCertificatesIfConfigured',
            'workflow.steps.util.ssl.CreateSSLFolderIfConfigured',
        )

    def get_configure_ssl_ip_steps(self):
        return (
            'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfraIPIfConfigured',
            'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
            'workflow.steps.util.ssl.CreateJsonRequestFileInfraIfConfigured',
            'workflow.steps.util.ssl.CreateCertificateInfraMongoDBIfConfigured',
            'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
            'workflow.steps.util.ssl.UpdateExpireAtDate',
        )

    def get_configure_ssl_dns_steps(self):
        return (
            'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfraIfConfigured',
            'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
            'workflow.steps.util.ssl.CreateJsonRequestFileInfraIfConfigured',
            'workflow.steps.util.ssl.CreateCertificateInfraMongoDBIfConfigured',
            'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
            'workflow.steps.util.ssl.UpdateExpireAtDate',
        )


class MongoDBSingle(BaseMongoDB):

    def get_upgrade_steps_extra(self):
        return ('workflow.steps.mongodb.upgrade.vm.ChangeBinaryTo36',) + \
            super(MongoDBSingle, self).get_upgrade_steps_extra() + (
            'workflow.steps.util.plan.ConfigureForUpgrade',
            'workflow.steps.util.plan.ConfigureLog',
            'workflow.steps.util.database.Start',
            'workflow.steps.util.database.CheckIsUp',
            ('workflow.steps.mongodb.upgrade.database'
             '.SetFeatureCompatibilityVersion36'),
            'workflow.steps.util.database.Stop',
            'workflow.steps.util.database.CheckIsDown',
            'workflow.steps.mongodb.upgrade.vm.ChangeBinaryTo40',
            'workflow.steps.util.plan.ConfigureForUpgradeOnlyDBConfigFile',
            'workflow.steps.util.metric_collector.ConfigureTelegraf',
        )

    def get_upgrade_steps_final(self):
        return [{
            'Setting feature compatibility version 4.0': (
                ('workflow.steps.mongodb.upgrade.database'
                 '.SetFeatureCompatibilityVersion40'),
            ),
        }] + super(MongoDBSingle, self).get_upgrade_steps_final()

    @property
    def driver_name(self):
        return 'mongodb_single'

    def deploy_instances(self):
        return [[InstanceDeploy(Instance.MONGODB, 27017)]]

    def get_deploy_steps(self):
        return [{

            'Creating Service Account': (
                'workflow.steps.util.host_provider.CreateServiceAccount',
                'workflow.steps.util.host_provider.SetServiceAccountRoles'
            )}, {
            'Creating virtual machine': (
                'workflow.steps.util.host_provider.AllocateIP',
                'workflow.steps.util.host_provider.CreateVirtualMachine',
            )}, {
            'Creating dns': (
                'workflow.steps.util.dns.CreateDNS',
            )}, {
            'Creating disk': (
                'workflow.steps.util.volume_provider.NewVolume',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.vm.UpdateOSDescription'
            )}, {
            'Check DNS': (
                'workflow.steps.util.dns.CheckIsReady',
            )}, {
            'Configuring database': (
                'workflow.steps.util.volume_provider.AttachDataVolumeWithUndo',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.plan.InitializationForNewInfra',
            )}, {
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateOpenSSlLib',
                'workflow.steps.util.ssl.MongoDBUpdateCertificates',
                'workflow.steps.util.ssl.CreateSSLFolderRollbackIfRunning',
                'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfra',
                'workflow.steps.util.ssl.RequestSSLForInfra',
                'workflow.steps.util.ssl.CreateJsonRequestFileInfra',
                'workflow.steps.util.ssl.CreateCertificateInfraMongoDB',
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDB',
                'workflow.steps.util.ssl.SetInfraConfiguredSSL',
                'workflow.steps.util.ssl.SetInfraSSLModeAllowTLS',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.plan.ConfigureForNewInfra',
                'workflow.steps.util.plan.ConfigureLogForNewInfra',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.infra.UpdateEndpoint',
            )}, {
            'Creating Database': (
                'workflow.steps.util.database.Create',
            )}, {
            'Check ACL': (
                'workflow.steps.util.acl.BindNewInstance',
            )}, {
            'Creating monitoring and alarms': (
                'workflow.steps.util.zabbix.CreateAlarms',
                'workflow.steps.util.db_monitor.CreateInfraMonitoring',
            )}, {
            'Create Extra DNS': (
                'workflow.steps.util.database.CreateExtraDNS',
            )}, {
            'Update Host Disk Size': (
                'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            )
        }]

    def get_host_migrate_steps(self):
        return [{
            'Creating virtual machine': (
                ('workflow.steps.util.host_provider.CreateVirtualMachineMigrate'),
            )}, {
            'Creating disk': (
                'workflow.steps.util.volume_provider.NewVolume',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.vm.UpdateOSDescription',
                'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            )}, {
            'Configuring database': (
                'workflow.steps.util.volume_provider.AttachDataVolume',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.plan.Initialization',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.plan.ConfigureLog',
            )}, {
            'Check patch': (
                ) + self.get_change_binaries_upgrade_patch_steps() + (
            )}, {
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateOpenSSlLibIfConfigured',
                ('workflow.steps.util.ssl.MongoDBUpdateCertificatesIfConfigured'),
                'workflow.steps.util.ssl.CreateSSLFolderIfConfigured',
                ('workflow.steps.util.ssl.MongoDBCreateSSLConfForInfraIPIfConfigured'),
                'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
                ('workflow.steps.util.ssl.CreateJsonRequestFileInfraIfConfigured'),
                ('workflow.steps.util.ssl.CreateCertificateInfraMongoDBIfConfigured'),
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Backup and restore': (
                'workflow.steps.util.volume_provider.TakeSnapshotFromMaster',
                ('workflow.steps.util.volume_provider.WaitSnapshotAvailableMigrate'),
                'workflow.steps.util.volume_provider.AddAccessRecreateSlave',
                ('workflow.steps.util.volume_provider.MountDataVolumeRecreateSlave'),
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.disk.CleanDataMigrate',
                'workflow.steps.util.volume_provider.CopyDataFromSnapShot',
                'workflow.steps.util.disk.RemoveDeprecatedFiles',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.volume_provider.DetachDataVolumeRecreateSlave',
                ('workflow.steps.util.volume_provider.UmountDataVolumeRecreateSlave'),
                ('workflow.steps.util.volume_provider.RemoveAccessRecreateSlave'),
                'workflow.steps.util.volume_provider.RemoveSnapshotMigrate',
            )}, {
            'Check access between instances': (
                'workflow.steps.util.vm.CheckAccessToMaster',
                'workflow.steps.util.vm.CheckAccessFromMaster',
            )}, {
            'Replicate ACL': (
                'workflow.steps.util.acl.ReplicateAclsMigrate',
            )}, {
            'Stopping database': (
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
            )}, {
            'Destroy Alarms': (
                'workflow.steps.util.zabbix.DestroyAlarms',
            )}, {
            'Update and Check DNS': (
                'workflow.steps.util.dns.ChangeEndpoint',
                'workflow.steps.util.dns.CheckIsReady',
            )}, {
            'Configure SSL': (
                ('workflow.steps.util.ssl.MongoDBCreateSSLConfForInfraIfConfigured'),
                'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
                ('workflow.steps.util.ssl.CreateJsonRequestFileInfraIfConfigured'),
                ('workflow.steps.util.ssl.CreateCertificateInfraMongoDBIfConfigured'),
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Recreate Alarms': (
                'workflow.steps.util.zabbix.CreateAlarms',
                ('workflow.steps.util.db_monitor.UpdateInfraCloudDatabaseMigrate'),
            )}, {
            'Cleaning up': (
                'workflow.steps.util.disk.ChangeSnapshotOwner',
                'workflow.steps.util.volume_provider.DestroyOldEnvironment',
                ('workflow.steps.util.host_provider.DestroyVirtualMachineMigrate'),
            )}]

    def get_clone_steps(self):
        return [{
            'Creating Service Account': (
                'workflow.steps.util.host_provider.CreateServiceAccount',
                'workflow.steps.util.host_provider.SetServiceAccountRoles'
            )}, {
            'Creating virtual machine': (
                'workflow.steps.util.host_provider.AllocateIP',
                'workflow.steps.util.host_provider.CreateVirtualMachine',
            )}, {
            'Creating dns': (
                'workflow.steps.util.dns.CreateDNS',
            )}, {
            'Creating disk': (
                'workflow.steps.util.volume_provider.NewVolume',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.vm.UpdateOSDescription'
            )}, {
            'Check DNS': (
                'workflow.steps.util.dns.CheckIsReady',
            )}, {
            'Configuring database': (
                'workflow.steps.util.volume_provider.AttachDataVolume',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.plan.InitializationForNewInfra',
            )}, {
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateOpenSSlLib',
                'workflow.steps.util.ssl.MongoDBUpdateCertificates',
                'workflow.steps.util.ssl.CreateSSLFolderRollbackIfRunning',
                'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfra',
                'workflow.steps.util.ssl.RequestSSLForInfra',
                'workflow.steps.util.ssl.CreateJsonRequestFileInfra',
                'workflow.steps.util.ssl.CreateCertificateInfraMongoDB',
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDB',
                'workflow.steps.util.ssl.SetInfraConfiguredSSL',
                'workflow.steps.util.ssl.SetInfraSSLModeAllowTLS',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.plan.ConfigureForNewInfra',
                'workflow.steps.util.plan.ConfigureLogForNewInfra',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.infra.UpdateEndpoint',
            )}, {
            'Creating Database': (
                'workflow.steps.util.database.Clone',
                'workflow.steps.util.clone.clone_database.CloneDatabaseData'
            )}, {
            'Check ACL': (
                'workflow.steps.util.acl.BindNewInstance',
            )}, {
            'Creating monitoring and alarms': (
                'workflow.steps.util.zabbix.CreateAlarms',
                'workflow.steps.util.db_monitor.CreateInfraMonitoring',
            )}, {
            'Create Extra DNS': (
                'workflow.steps.util.database.CreateExtraDNS',
            )}, {
            'Update Host Disk Size': (
                'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            )
        }]

    def get_restore_snapshot_steps(self):
        return [{
            'Disable monitoring': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
            )}, {
            'Restoring': (
                'workflow.steps.util.volume_provider.RestoreSnapshot',
            )}, {
            'Stopping database': (
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
            )}, {
            'Configuring': (
                'workflow.steps.util.volume_provider.AddAccessRestoredVolume',
                'workflow.steps.util.volume_provider.UnmountActiveVolume',
                'workflow.steps.util.volume_provider.AttachDataVolumeRestored',
                'workflow.steps.util.volume_provider.MountDataVolumeRestored',
                'workflow.steps.util.disk.RemoveDeprecatedFiles',
                'workflow.steps.util.plan.ConfigureRestore',
                'workflow.steps.util.plan.ConfigureLog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
            )}, {
            'Configure SSL': (
                'workflow.steps.util.disk.CleanSSLDir',
                ('workflow.steps.util.ssl'
                 '.MongoDBCreateSSLConfForInfraIfConfigured'),
                'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
                ('workflow.steps.util.ssl'
                 '.CreateJsonRequestFileInfraIfConfigured'),
                ('workflow.steps.util.ssl'
                 '.CreateCertificateInfraMongoDBIfConfigured'),
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Old data': (
                'workflow.steps.util.volume_provider.TakeSnapshot',
                'workflow.steps.util.volume_provider.UpdateActiveDisk',
            )}, {
            'Enabling monitoring': (
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )
        }]

    def get_filer_migrate_steps(self):
        return [{
            'Migrating': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
                'workflow.steps.util.volume_provider.NewInactiveVolume',
                'workflow.steps.util.metric_collector.StopTelegraf',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.volume_provider.AddAccessNewVolume',
                'workflow.steps.util.volume_provider.MountDataLatestVolume',
                'workflow.steps.util.volume_provider.CopyPermissions',
                'workflow.steps.util.volume_provider.CopyFiles',
                'workflow.steps.util.volume_provider.UnmountDataLatestVolume',
                'workflow.steps.util.volume_provider.DetachDataVolume',
                'workflow.steps.util.volume_provider.UnmountDataVolume',
                'workflow.steps.util.volume_provider.MountDataNewVolume',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.volume_provider.TakeSnapshotOldDisk',
                'workflow.steps.util.volume_provider.UpdateActiveDisk',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )}
        ]

    def get_change_binaries_upgrade_patch_steps(self):
        return (
            'workflow.steps.util.database_upgrade_patch.MongoDBCHGBinStep',
        )


class MongoDBReplicaset(BaseMongoDB):

    def get_filer_migrate_steps(self):
        return [{
            'Migrating': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.volume_provider.NewInactiveVolume',
                'workflow.steps.util.metric_collector.StopTelegraf',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.volume_provider.AddAccessNewVolume',
                'workflow.steps.util.volume_provider.MountDataLatestVolume',
                'workflow.steps.util.volume_provider.CopyPermissions',
                'workflow.steps.util.volume_provider.CopyFiles',
                'workflow.steps.util.volume_provider.UnmountDataLatestVolume',
                'workflow.steps.util.volume_provider.DetachDataVolume',
                'workflow.steps.util.volume_provider.UnmountDataVolume',
                'workflow.steps.util.volume_provider.MountDataNewVolume',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.WaitForReplication',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.volume_provider.TakeSnapshotOldDisk',
                'workflow.steps.util.volume_provider.UpdateActiveDisk',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )}
        ]

    def get_upgrade_steps_extra(self):
        return (
            'workflow.steps.mongodb.upgrade.vm.ChangeBinaryTo36',
            'workflow.steps.util.volume_provider.AttachDataVolume',
            'workflow.steps.util.volume_provider.MountDataVolume',
            'workflow.steps.util.plan.ConfigureForUpgrade',
            'workflow.steps.util.plan.ConfigureLog',
            'workflow.steps.util.plan.InitializationForUpgrade',
            'workflow.steps.util.metric_collector.ConfigureTelegraf',
        )

    def get_upgrade_steps_final(self):
        return [{
            'Upgrading to MongoDB 4.0': (
                ('workflow.steps.mongodb.upgrade.database'
                 '.SetFeatureCompatibilityVersion36'),
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.mongodb.upgrade.vm.ChangeBinaryTo40',
                'workflow.steps.util.plan.ConfigureForUpgradeOnlyDBConfigFile',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            ),
        }] + [{
            'Setting feature compatibility version 4.0': (
                ('workflow.steps.mongodb.upgrade.database'
                 '.SetFeatureCompatibilityVersion40'),
            ),
        }] + super(MongoDBReplicaset, self).get_upgrade_steps_final()

    def get_add_database_instances_middle_steps(self):
        return (
            'workflow.steps.util.volume_provider.AttachDataVolume',
            'workflow.steps.util.volume_provider.MountDataVolume',
            'workflow.steps.util.plan.Initialization',
            'workflow.steps.util.ssl.UpdateOpenSSlLibIfConfigured',
            'workflow.steps.util.ssl.MongoDBUpdateCertificatesIfConfigured',
            'workflow.steps.util.ssl.CreateSSLFolderRollbackIfRunningIfConfigured',
            'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfraIfConfigured',
            'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
            'workflow.steps.util.ssl.CreateJsonRequestFileInfraIfConfigured',
            'workflow.steps.util.ssl.CreateCertificateInfraMongoDBIfConfigured',
            'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
            'workflow.steps.util.ssl.UpdateExpireAtDate',
            'workflow.steps.util.plan.Configure',
            'workflow.steps.util.plan.ConfigureLog',
            'workflow.steps.util.metric_collector.ConfigureTelegraf'
            ) + self.get_change_binaries_upgrade_patch_steps() + (
            'workflow.steps.util.database.StartCheckOnlyOsProcess',
            'workflow.steps.mongodb.database.AddInstanceToReplicaSet',
            'workflow.steps.util.metric_collector.RestartTelegraf',
        )

    def get_resize_oplog_steps(self):
        return [{
            'Resize oplog': (
                'workflow.steps.util.database.ValidateOplogSizeValue',
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.plan.ConfigureForResizeLog',
                'workflow.steps.util.plan.ConfigureLog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.database.StartForResizeLog',
                'workflow.steps.util.database.CheckIsUpForResizeLog',
                'workflow.steps.util.database.ResizeOpLogSize',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.plan.ConfigureOnlyDBConfigFile',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )
        }] + self.get_change_parameter_steps_final()

    def get_resize_oplog_steps_and_retry_steps_back(self):
        return self.get_resize_oplog_steps(), 0

    @property
    def driver_name(self):
        return 'mongodb_replica_set'

    def deploy_instances(self):
        return [
            [InstanceDeploy(Instance.MONGODB, 27017)],
            [InstanceDeploy(Instance.MONGODB, 27017)],
            [InstanceDeploy(Instance.MONGODB_ARBITER, 27017)]
        ]

    def get_deploy_steps(self):
        return [{
            'Creating Service Account': (
                'workflow.steps.util.host_provider.CreateServiceAccount',
                'workflow.steps.util.host_provider.SetServiceAccountRoles'
            )}, {
            'Creating virtual machine': (
                'workflow.steps.util.host_provider.AllocateIP',
                'workflow.steps.util.host_provider.CreateVirtualMachine',
            )}, {
            'Creating dns': (
                'workflow.steps.util.dns.CreateDNS',
            )}, {
            'Creating disk': (
                'workflow.steps.util.volume_provider.NewVolume',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.vm.UpdateOSDescription'
            )}, {
            'Check DNS': (
                'workflow.steps.util.dns.CheckIsReady',
            )}, {
            'Configuring database': (
                'workflow.steps.util.volume_provider.AttachDataVolumeWithUndo',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.plan.InitializationForNewInfra',
            )}, {
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateOpenSSlLib',
                'workflow.steps.util.ssl.MongoDBUpdateCertificates',
                'workflow.steps.util.ssl.CreateSSLFolderRollbackIfRunning',
                'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfra',
                'workflow.steps.util.ssl.RequestSSLForInfra',
                'workflow.steps.util.ssl.CreateJsonRequestFileInfra',
                'workflow.steps.util.ssl.CreateCertificateInfraMongoDB',
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDB',
                'workflow.steps.util.ssl.SetInfraConfiguredSSL',
                'workflow.steps.util.ssl.SetInfraSSLModeAllowTLS',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.plan.ConfigureForNewInfra',
                'workflow.steps.util.plan.ConfigureLogForNewInfra',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Check Database': (
                'workflow.steps.util.plan.StartReplicationFirstNodeNewInfra',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.infra.UpdateEndpoint',
            )}, {
            'Creating Database': (
                'workflow.steps.util.database.Create',
            )}, {
            'Check ACL': (
                'workflow.steps.util.acl.BindNewInstance',
            )}, {
            'Creating monitoring and alarms': (
                'workflow.steps.util.zabbix.CreateAlarms',
                'workflow.steps.util.db_monitor.CreateInfraMonitoring',
            )}, {
            'Create Extra DNS': (
                'workflow.steps.util.database.CreateExtraDNS',
            )}, {
            'Update Host Disk Size': (
                'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            )
        }]

    def get_clone_steps(self):
        return [{
            'Creating Service Account': (
                'workflow.steps.util.host_provider.CreateServiceAccount',
                'workflow.steps.util.host_provider.SetServiceAccountRoles'
            )}, {
            'Creating virtual machine': (
                'workflow.steps.util.host_provider.AllocateIP',
                'workflow.steps.util.host_provider.CreateVirtualMachine',
            )}, {
            'Creating dns': (
                'workflow.steps.util.dns.CreateDNS',
            )}, {
            'Creating disk': (
                'workflow.steps.util.volume_provider.NewVolume',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.vm.UpdateOSDescription'
            )}, {
            'Check DNS': (
                'workflow.steps.util.dns.CheckIsReady',
            )}, {
            'Configuring database': (
                'workflow.steps.util.volume_provider.AttachDataVolume',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.plan.InitializationForNewInfra',
            )}, {
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateOpenSSlLib',
                'workflow.steps.util.ssl.MongoDBUpdateCertificates',
                'workflow.steps.util.ssl.CreateSSLFolderRollbackIfRunning',
                'workflow.steps.util.ssl.MongoDBCreateSSLConfForInfra',
                'workflow.steps.util.ssl.RequestSSLForInfra',
                'workflow.steps.util.ssl.CreateJsonRequestFileInfra',
                'workflow.steps.util.ssl.CreateCertificateInfraMongoDB',
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDB',
                'workflow.steps.util.ssl.SetInfraConfiguredSSL',
                'workflow.steps.util.ssl.SetInfraSSLModeAllowTLS',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.plan.ConfigureForNewInfra',
                'workflow.steps.util.plan.ConfigureLogForNewInfra',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Check Database': (
                'workflow.steps.util.plan.StartReplicationFirstNodeNewInfra',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.infra.UpdateEndpoint',
            )}, {
            'Creating Database': (
                'workflow.steps.util.database.Clone',
                'workflow.steps.util.clone.clone_database.CloneDatabaseData'
            )}, {
            'Check ACL': (
                'workflow.steps.util.acl.BindNewInstance',
            )}, {
            'Creating monitoring and alarms': (
                'workflow.steps.util.zabbix.CreateAlarms',
                'workflow.steps.util.db_monitor.CreateInfraMonitoring',
            )}, {
            'Create Extra DNS': (
                'workflow.steps.util.database.CreateExtraDNS',
            )}, {
            'Update Host Disk Size': (
                'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            )
        }]

    def get_restore_snapshot_steps(self):
        return [{
            'Disable monitoring': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
            )}, {
            'Restoring': (
                'workflow.steps.util.volume_provider.RestoreSnapshotToMaster',
            )}, {
            'Stopping database': (
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
            )}, {
            'Configuring': (
                'workflow.steps.util.volume_provider.AddAccessRestoredVolume',
                'workflow.steps.util.volume_provider.UnmountActiveVolume',
                'workflow.steps.util.volume_provider.DetachActiveVolume',
                'workflow.steps.util.volume_provider.AttachDataVolumeRestored',
                'workflow.steps.util.volume_provider.MountDataVolumeRestored',
                'workflow.steps.util.disk.RemoveDeprecatedFiles',
                'workflow.steps.util.disk.CleanData',
                'workflow.steps.util.disk.CleanDataArbiter',
                'workflow.steps.util.plan.ConfigureRestore',
                'workflow.steps.util.plan.ConfigureLog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
            )}, {
            'Configure SSL': (
                'workflow.steps.util.disk.CleanSSLDir',
                ('workflow.steps.util.ssl'
                 '.MongoDBCreateSSLConfForInfraIfConfigured'),
                'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
                ('workflow.steps.util.ssl'
                 '.CreateJsonRequestFileInfraIfConfigured'),
                ('workflow.steps.util.ssl'
                 '.CreateCertificateInfraMongoDBIfConfigured'),
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Check database': (
                'workflow.steps.util.database.CheckIsUp',
            )}, {
            'Check if there is a master': (
                'workflow.steps.util.database.CheckIfInstanceIsMasterRestore',
            )}, {
            'Old data': (
                'workflow.steps.util.volume_provider.TakeSnapshot',
                'workflow.steps.util.volume_provider.UpdateActiveDisk',
            )}, {
            'Enabling monitoring': (
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )
        }]

    def get_recreate_slave_steps(self):
        return [{
            'Recreate Slave': (
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
                'workflow.steps.util.volume_provider.TakeSnapshotFromMaster',
                ('workflow.steps.util.volume_provider'
                 '.WaitSnapshotAvailableMigrate'),
                'workflow.steps.util.database.StopIfRunning',
                'workflow.steps.util.disk.CleanDataRecreateSlave',
                'workflow.steps.util.volume_provider.AddAccessRecreateSlave',
                ('workflow.steps.util.volume_provider'
                 '.MountDataVolumeRecreateSlave'),
                'workflow.steps.util.volume_provider.CopyDataFromSnapShot',
                'workflow.steps.util.volume_provider.DetachDataVolumeRecreateSlave',
                ('workflow.steps.util.volume_provider'
                 '.UmountDataVolumeRecreateSlave'),
                ('workflow.steps.util.volume_provider'
                 '.RemoveAccessRecreateSlave'),
                'workflow.steps.util.volume_provider.RemoveSnapshotMigrate',
                'workflow.steps.util.disk.RemoveDeprecatedFiles',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.plan.ConfigureLog',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.WaitForReplication',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )
        }]

    def get_host_migrate_steps(self):
        return [{
            'Switch Master': (
                'workflow.steps.util.vm.ChangeMaster',
                'workflow.steps.util.database.CheckIfSwitchMaster',
            )}, {
            'Creating virtual machine': (
                ('workflow.steps.util.host_provider.CreateVirtualMachineMigrate'),
            )}, {
            'Creating disk': (
                'workflow.steps.util.volume_provider.NewVolume',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.vm.UpdateOSDescription',
                'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            )}, {
            'Configuring database': (
                'workflow.steps.util.volume_provider.AttachDataVolume',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.plan.Initialization',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.plan.ConfigureLog',
            )}, {
            'Check patch': (
                ) + self.get_change_binaries_upgrade_patch_steps() + (
            )}, {
            'Configure SSL': (
                'workflow.steps.util.ssl.UpdateOpenSSlLibIfConfigured',
                ('workflow.steps.util.ssl.MongoDBUpdateCertificatesIfConfigured'),
                'workflow.steps.util.ssl.CreateSSLFolderIfConfigured',
                ('workflow.steps.util.ssl.MongoDBCreateSSLConfForInfraIPIfConfigured'),
                'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
                ('workflow.steps.util.ssl.CreateJsonRequestFileInfraIfConfigured'),
                ('workflow.steps.util.ssl.CreateCertificateInfraMongoDBIfConfigured'),
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Check access between instances': (
                'workflow.steps.util.database.StopWithoutUndo',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.vm.CheckAccessToMaster',
                'workflow.steps.util.vm.CheckAccessFromMaster',
            )}, {
            'Replicate ACL': (
                'workflow.steps.util.acl.ReplicateAclsMigrate',
            )}, {
            'Backup and restore': (
                'workflow.steps.mongodb.database.AddInstanceToReplicaSet',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.volume_provider.TakeSnapshotFromMaster',
                ('workflow.steps.util.volume_provider.WaitSnapshotAvailableMigrate'),
                'workflow.steps.util.volume_provider.AddAccessRecreateSlave',
                ('workflow.steps.util.volume_provider.MountDataVolumeRecreateSlave'),
                'workflow.steps.util.disk.CleanDataRecreateSlave',
                'workflow.steps.util.volume_provider.CopyDataFromSnapShot',
                'workflow.steps.util.disk.RemoveDeprecatedFiles',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.volume_provider.DetachDataVolumeRecreateSlave',
                ('workflow.steps.util.volume_provider.UmountDataVolumeRecreateSlave'),
                ('workflow.steps.util.volume_provider.RemoveAccessRecreateSlave'),
                'workflow.steps.util.volume_provider.RemoveSnapshotMigrate',
                'workflow.steps.util.database.WaitForReplication',
                'workflow.steps.mongodb.database.SetNotEligible',
            )}, {
            'Stopping database': (
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
            )}, {
            'Destroy Alarms': (
                'workflow.steps.util.zabbix.DestroyAlarms',
            )}, {
            'Update and Check DNS': (
                'workflow.steps.util.dns.ChangeEndpoint',
                'workflow.steps.util.dns.CheckIsReady',
            )}, {
            'Configure SSL': (
                ('workflow.steps.util.ssl.MongoDBCreateSSLConfForInfraIfConfigured'),
                'workflow.steps.util.ssl.RequestSSLForInfraIfConfigured',
                ('workflow.steps.util.ssl.CreateJsonRequestFileInfraIfConfigured'),
                ('workflow.steps.util.ssl.CreateCertificateInfraMongoDBIfConfigured'),
                'workflow.steps.util.ssl.SetSSLFilesAccessMongoDBIfConfigured',
                'workflow.steps.util.ssl.UpdateExpireAtDate',
            )}, {
            'Starting database': (
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Recreate Alarms': (
                'workflow.steps.util.zabbix.CreateAlarms',
                ('workflow.steps.util.db_monitor.UpdateInfraCloudDatabaseMigrate'),
            )}, {
            'Cleaning up': (
                'workflow.steps.util.database.StartNonDatabaseInstanceRollback',
                'workflow.steps.mongodb.database.RemoveInstanceFromReplicaSet',
                'workflow.steps.util.disk.CleanDataNonDatabaseInstanceRollback',
                'workflow.steps.util.database.StopNonDatabaseInstanceRollback',
                'workflow.steps.util.disk.ChangeSnapshotOwner',
                'workflow.steps.util.volume_provider.DestroyOldEnvironment',
                ('workflow.steps.util.host_provider.DestroyVirtualMachineMigrate'),
            )}]

    def get_database_migrate_steps(self):
        return self.get_host_migrate_steps()

    def get_change_binaries_upgrade_patch_steps(self):
        return (
            'workflow.steps.util.database_upgrade_patch.MongoDBCHGBinStep',
        )

    def get_database_migrate_steps_stage_1(self):
        return [{
            'Creating Service Account': (
                'workflow.steps.util.host_provider.CreateServiceAccount',
                'workflow.steps.util.host_provider.SetServiceAccountRoles'
            )}, {
            'Creating virtual machine': (
                'workflow.steps.util.host_provider.AllocateIP',
                'workflow.steps.util.host_provider.CreateVirtualMachineMigrate',
                'workflow.steps.util.infra.MigrationCreateInstance',
            )}, {
            'Creating disk': (
                'workflow.steps.util.volume_provider.NewVolume',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.vm.UpdateOSDescription',
                'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            )}, {
            'Check patch': (
                ) + self.get_change_binaries_upgrade_patch_steps() + (
            )}, {
            'Configuring database': (
                'workflow.steps.util.volume_provider.AttachDataVolume',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.plan.Initialization',
                'workflow.steps.util.plan.ConfigureLog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.plan.Configure',
            )}, {
            'Configure SSL lib and folder': (
                ) + self.get_configure_ssl_libs_and_folder_steps() + (
            )}, {
            'Configure SSL (IP)': (
                ) + self.get_configure_ssl_ip_steps() + (
            )}, {
            'Replicate ACL': (
                'workflow.steps.util.acl.ReplicateAclsMigrate',
                'workflow.steps.util.acl.BindNewInstanceDatabaseMigrate',
            )}, {
            'Check Access': (
                'workflow.steps.util.database.Start',
                'workflow.steps.util.vm.CheckAccessToMaster',
                'workflow.steps.util.vm.CheckAccessFromMaster',
            )}, {
            'Configure replication': (
                'workflow.steps.mongodb.database.AddInstanceToReplicaSet',
                'workflow.steps.mongodb.database.SetFutureInstanceNotEligibleWithouUndo',
                'workflow.steps.util.database.StopWithoutUndo',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.volume_provider.TakeSnapshotMigrateAllInstances',
                'workflow.steps.util.volume_provider.WaitSnapshotAvailableMigrate',
                'workflow.steps.util.volume_provider.AddHostsAllowMigrateBackupHost',
                'workflow.steps.util.volume_provider.CreatePubKeyMigrateBackupHost',
                'workflow.steps.util.disk.CleanDataMigrate',
                'workflow.steps.util.volume_provider.RsyncDataFromSnapshotMigrateBackupHost',
                'workflow.steps.util.volume_provider.WaitRsyncFromSnapshotDatabaseMigrate',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.infra.EnableFutureInstances',
                'workflow.steps.util.volume_provider.RemovePubKeyMigrateHostMigrate',
                'workflow.steps.util.volume_provider.RemoveHostsAllowMigrateBackupHost',
            )}, {
            'Start telegraf and rsyslog': (
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Wait replication': (
                'workflow.steps.util.database.WaitForReplication',
        )}]


    def get_database_migrate_steps_stage_2(self):
        return [{
            'Destroy Alarms': (
                'workflow.steps.util.zabbix.DestroyAlarmsDatabaseMigrate',
            )}, {
            'Configure Telegraf': (
                'workflow.steps.util.metric_collector.RestartTelegrafRollback',
                'workflow.steps.util.metric_collector.ConfigureTelegrafRollback',
                'workflow.steps.util.metric_collector.RestartTelegrafSourceDBMigrateRollback',
                'workflow.steps.util.metric_collector.ConfigureTelegrafSourceDBMigrateRollback',
            )}, {
            'Update and Check DNS': (
                'workflow.steps.util.dns.CheckIsReadyDBMigrateRollback',
                'workflow.steps.util.dns.ChangeEndpointDBMigrate',
                'workflow.steps.util.dns.CheckIsReadyDBMigrate',
            )}, {
            'Configure SSL (DNS)': (
                ) + self.get_configure_ssl_dns_steps() + (
            )}, {
            'Restart Database': (
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
            )}, {
            'Configure Telegraf': (
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.metric_collector.ConfigureTelegrafSourceDBMigrate',
                'workflow.steps.util.metric_collector.RestartTelegrafSourceDBMigrate',
            )}, {
            'Configure Eligible Master': (
                'workflow.steps.mongodb.database.SetFutureInstanceEligible',
            )}, {
            'Change Master Rollback': (
                ## RICK TODO REVIEW
                #'workflow.steps.util.database.CheckIfSwitchMasterRollback',
                'workflow.steps.util.vm.ChangeMasterMigrateRollback',
            )}, {
            'Configure Eligible Master': (
                'workflow.steps.mongodb.database.SetFutureInstanceEligible',
                'workflow.steps.mongodb.database.SetSourceInstanceNotEligible',
            )}, {
            'Change Master': (
                'workflow.steps.util.vm.ChangeMaster',
                ## RICK TODO REVIEW
                #'workflow.steps.util.database.CheckIfSwitchMasterMigrate',
            )}, {
            'Configure Eligible Master': (
                'workflow.steps.mongodb.database.SetSourceInstanceNotEligible',
            )}, {
            'Recreate Alarms': (
                'workflow.steps.util.zabbix.CreateAlarmsDatabaseMigrate',
                'workflow.steps.util.db_monitor.UpdateInfraCloudDatabaseMigrate',
        )}]

    def get_database_migrate_steps_stage_3(self):
        return [{
            'Remove instance from replica set': (
                'workflow.steps.mongodb.database.RemoveInstanceFromReplicaSetWithouUndo',
                'workflow.steps.util.infra.DisableSourceInstances',
                'workflow.steps.util.database.StopSourceDatabaseMigrate',
            )}, {
            'Cleaning up': (
                'workflow.steps.util.volume_provider.DestroyOldEnvironment',
                'workflow.steps.util.host_provider.DestroyVirtualMachineMigrate',
        )}]


class MongoDBReplicaset40(MongoDBReplicaset):

    def get_resize_oplog_steps(self):
        return [{
            'Resize oplog': (
                'workflow.steps.util.database.ValidateOplogSizeValue',
                'workflow.steps.util.database.ResizeOpLogSize40',
                'workflow.steps.util.plan.ConfigureOnlyDBConfigFile',
            )
        }] + self.get_change_parameter_steps_final()

    def get_resize_oplog_steps_and_retry_steps_back(self):
        return self.get_resize_oplog_steps(), 0


class MongoDBReplicaset42(MongoDBReplicaset40):

    def get_upgrade_steps_final(self):
        return [{
            'Setting feature compatibility version': (
                'workflow.steps.mongodb.upgrade.database'
                '.SetFeatureCompatibilityToNewVersion',
            ),
        }] + [{
            self.get_upgrade_steps_final_description(): (
                'workflow.steps.util.db_monitor.UpdateInfraVersion',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.DestroyAlarms',
                'workflow.steps.util.zabbix.CreateAlarmsForUpgrade',
            ),
        }]

    def get_upgrade_steps_extra(self):
        return (
            'workflow.steps.util.volume_provider.AttachDataVolume',
            'workflow.steps.util.volume_provider.MountDataVolume',
            'workflow.steps.util.plan.InitializationForUpgrade',
            'workflow.steps.util.plan.ConfigureForUpgrade',
            'workflow.steps.util.plan.ConfigureLog',
            'workflow.steps.util.metric_collector.ConfigureTelegraf',
        )


class MongoDBSingle42(MongoDBSingle):

    def get_upgrade_steps_final(self):
        return [{
            'Setting feature compatibility version': (
                'workflow.steps.mongodb.upgrade.database'
                '.SetFeatureCompatibilityToNewVersion',
            ),
        }] + [{
            self.get_upgrade_steps_final_description(): (
                'workflow.steps.util.db_monitor.UpdateInfraVersion',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.DestroyAlarms',
                'workflow.steps.util.zabbix.CreateAlarmsForUpgrade',
            ),
        }]

    def get_upgrade_steps_extra(self):
        return (
            'workflow.steps.util.volume_provider.AttachDataVolume',
            'workflow.steps.util.volume_provider.MountDataVolume',
            'workflow.steps.util.plan.InitializationForUpgrade',
            'workflow.steps.util.plan.ConfigureForUpgrade',
            'workflow.steps.util.plan.ConfigureLog',
            'workflow.steps.util.metric_collector.ConfigureTelegraf',
        )


class MongoDBSingleK8s(MongoDBSingle):

    @property
    def driver_name(self):
        return 'mongodb_single_k8s'

    def get_resize_steps(self):
        return [{'Resizing database': (
            # 'workflow.steps.util.zabbix.DisableAlarms',
            'workflow.steps.util.vm.ChangeMaster',
            'workflow.steps.util.database.CheckIfSwitchMaster',
            # 'workflow.steps.util.agents.Stop',
            # 'workflow.steps.util.plan.ResizeConfigure',
            # 'workflow.steps.util.plan.ConfigureLog',
            # 'workflow.steps.util.dns.CheckIsReady',
            # 'workflow.steps.util.dns.UpdateDNS',
            'workflow.steps.util.database.CheckIsUp',
            # 'workflow.steps.util.k8s.UpdateHostMetadata',
            'workflow.steps.util.host_provider.WaitingNewDeployUndo',
            'workflow.steps.util.host_provider.ChangeOffering',
            'workflow.steps.util.host_provider.WaitingNewDeployDo',
            # 'workflow.steps.util.k8s.UpdateHostMetadata',
            # 'workflow.steps.util.agents.Start',
            'workflow.steps.util.database.CheckIsUp',
            # 'workflow.steps.util.dns.UpdateDNS',
            # 'workflow.steps.util.dns.CheckIsReady',
            'workflow.steps.util.database.WaitForReplication',
            'workflow.steps.util.infra.Offering',
            'workflow.steps.util.vm.InstanceIsSlave',
            # 'workflow.steps.util.zabbix.EnableAlarms',
        )}]

    def get_deploy_steps(self):
        return [{
            'Creating Service Account': (
                'workflow.steps.util.host_provider.CreateServiceAccount',
                'workflow.steps.util.host_provider.SetServiceAccountRoles'
            )}, {
            'Creating k8s Service': (
                'workflow.steps.util.k8s.NewServiceK8S',
            )}, {
            'Creating disk': (
                'workflow.steps.util.k8s.CreateHostMetadata',
                'workflow.steps.util.k8s.NewVolumeK8S',
            )}, {
            'Creating Config Map': (
                'workflow.steps.util.k8s.CreateConfigMap',
            )}, {
            'Creating Pod': (
                'workflow.steps.util.k8s.NewPodK8S',
            )}, {
            'Waiting VMs': (
                'workflow.steps.util.host_provider.WaitingNewDeployDo',
                # 'workflow.steps.util.vm.UpdateOSDescription'
            )}, {
            'Creating dns': (
                'workflow.steps.util.k8s.UpdateHostMetadata',
                #'workflow.steps.util.dns.CreateDNS',
            )}, {
            'Configuring database': (
                # 'workflow.steps.util.volume_provider.AttachDataVolume',
                # 'workflow.steps.util.volume_provider.MountDataVolume',
                # 'workflow.steps.util.plan.InitializationForNewInfra',
                # 'workflow.steps.util.plan.ConfigureForNewInfra',
                # 'workflow.steps.util.metric_collector.ConfigureTelegraf',
                # 'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                # 'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.infra.UpdateEndpoint',
            )}, {
            #'Check DNS': (
                #'workflow.steps.util.dns.CheckIsReady',
             #)}, {
             'Creating Database': (
                'workflow.steps.util.database.SetMongoDBUsersPasswordFromCredentials',
                'workflow.steps.util.database.Create',
             )}, {
             'Check ACL': (
                 'workflow.steps.util.acl.BindNewInstance',
            # )}, {
            # 'Creating monitoring and alarms': (
            #     'workflow.steps.util.zabbix.CreateAlarms',
            #     'workflow.steps.util.db_monitor.CreateInfraMonitoring',
            # )}, {
            # 'Create Extra DNS': (
            #     'workflow.steps.util.database.CreateExtraDNS',
            # )}, {
            # 'Update Host Disk Size': (
            #     'workflow.steps.util.host_provider.UpdateHostRootVolumeSize',
            # )
            )
        }]


class MongoGenericGCE(object):
    def get_recreate_slave_steps(self):
        return [{
            'Recreate Slave': (
                'workflow.steps.util.database.CheckIfSwitchMaster',
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
                'workflow.steps.util.volume_provider.TakeSnapshotFromMaster',
                ('workflow.steps.util.volume_provider'
                 '.WaitSnapshotAvailableMigrate'),
                'workflow.steps.util.database.StopIfRunning',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
                'workflow.steps.util.volume_provider.DetachDataVolume',
                'workflow.steps.util.volume_provider.DestroyVolume',
                'workflow.steps.util.volume_provider.NewVolumeFromMaster',
                'workflow.steps.util.volume_provider.AttachDataVolume',
                'workflow.steps.util.volume_provider.MountDataVolume',
                'workflow.steps.util.volume_provider.RemoveSnapshotMigrate',
                'workflow.steps.util.disk.RemoveDeprecatedFiles',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.plan.ConfigureLog',
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.database.WaitForReplication',
                'workflow.steps.util.metric_collector.RestartTelegraf',
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )
        }]

    def get_replica_migration_steps(self):
        return [{
            'Disable monitoring and alarms': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
            )}, {
            'Stop pevious database': (
                'workflow.steps.util.metric_collector.RestartTelegrafRollback',
                'workflow.steps.util.metric_collector.ConfigureTelegrafRollback',
                'workflow.steps.util.database.CheckIsUpRollback',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
            )}, {
            'Check patch if rollback': (
                ) + self.get_change_binaries_upgrade_patch_steps_rollback() + (
            )}, {
            'Configure if rollback': (
                'workflow.steps.util.plan.ConfigureLogRollback',
                'workflow.steps.util.plan.ConfigureRollback',
                'workflow.steps.util.plan.InitializationMigrateRollback',
            )}, {
            'Remove previous VM': (
                'workflow.steps.util.volume_provider.DetachDataVolume',
                'workflow.steps.util.vm.WaitingBeReadyRollback',
                'workflow.steps.util.host_provider.DestroyVirtualMachineMigrateKeepObject'
            )}, {
            'Create new VM': (
                'workflow.steps.util.host_provider.RecreateVirtualMachineMigrate',
            )}, {
            'Replicate ACL': (
                'workflow.steps.util.acl.ReplicateAclsMigrate',
            )}, {
            'Configure instance': (
                'workflow.steps.util.volume_provider.MoveDisk',
                'workflow.steps.util.volume_provider.AttachDataVolumeWithUndo',
                'workflow.steps.util.volume_provider.MountDataVolumeWithUndo',
                'workflow.steps.util.vm.WaitingBeReady',
                'workflow.steps.util.plan.InitializationMigrate',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.plan.ConfigureLog',
            )}, {
            'Check patch': (
                ) + self.get_change_binaries_upgrade_patch_steps() + (
            )}, {
            'Starting database': (
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Enabling monitoring and alarms': (
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )}
        ]

    def get_single_migration_steps(self):
        return [{
            'Disable monitoring and alarms': (
                'workflow.steps.util.zabbix.DisableAlarms',
                'workflow.steps.util.db_monitor.DisableMonitoring',
            )}, {
            'Stop previous database': (
                'workflow.steps.util.metric_collector.RestartTelegrafRollback',
                'workflow.steps.util.metric_collector.ConfigureTelegrafRollback',
                'workflow.steps.util.database.CheckIsUpRollback',
                'workflow.steps.util.database.Stop',
                'workflow.steps.util.database.StopRsyslog',
                'workflow.steps.util.database.CheckIsDown',
            )}, {
            'Check patch if rollback': (
                ) + self.get_change_binaries_upgrade_patch_steps_rollback() + (
            )}, {
            'Configure if rollback': (
                'workflow.steps.util.plan.ConfigureLogRollback',
                'workflow.steps.util.plan.ConfigureRollback',
            )}, {
            'Remove previous VM': (
                'workflow.steps.util.volume_provider.DetachDataVolume',
                'workflow.steps.util.vm.WaitingBeReadyRollback',
                'workflow.steps.util.host_provider.DestroyVirtualMachineMigrateKeepObject'
            )}, {
            'Create new VM': (
                'workflow.steps.util.host_provider.RecreateVirtualMachineMigrate',
            )}, {
            'Configure instance': (
                'workflow.steps.util.volume_provider.MoveDisk',
                'workflow.steps.util.volume_provider.AttachDataVolumeWithUndo',
                'workflow.steps.util.volume_provider.MountDataVolumeWithUndo',
                'workflow.steps.util.plan.Configure',
                'workflow.steps.util.plan.ConfigureLog',
            )}, {
            'Replicate ACL': (
                'workflow.steps.util.acl.ReplicateAclsMigrate',
            )}, {
            'Check patch': (
                ) + self.get_change_binaries_upgrade_patch_steps() + (
            )}, {
            'Starting database': (
                'workflow.steps.util.database.Start',
                'workflow.steps.util.database.CheckIsUp',
                'workflow.steps.util.database.StartRsyslog',
                'workflow.steps.util.metric_collector.ConfigureTelegraf',
                'workflow.steps.util.metric_collector.RestartTelegraf',
            )}, {
            'Enabling monitoring and alarms': (
                'workflow.steps.util.db_monitor.EnableMonitoring',
                'workflow.steps.util.zabbix.EnableAlarms',
            )}
        ]

    def get_change_binaries_upgrade_patch_steps(self):
        return (
            'workflow.steps.util.database_upgrade_patch.MongoDBCHGBinStep',
        )

    def get_change_binaries_upgrade_patch_steps_rollback(self):
        return (
            'workflow.steps.util.database_upgrade_patch.MongoDBCHGBinStepRollback',
        )


class MongoDBSingle42GCE(MongoGenericGCE, MongoDBSingle42):
    def get_host_migrate_steps(self):
        return self.get_single_migration_steps()


class MongoDBSingleGCE(MongoGenericGCE, MongoDBSingle):
    def get_host_migrate_steps(self):
        return self.get_single_migration_steps()


class MongoDBReplicaset42GCE(MongoGenericGCE, MongoDBReplicaset42):
    def get_host_migrate_steps(self):
        return self.get_replica_migration_steps()


class MongoDBReplicaset40GCE(MongoGenericGCE, MongoDBReplicaset40):
    def get_host_migrate_steps(self):
        return self.get_replica_migration_steps()


class MongoDBReplicasetGCE(MongoGenericGCE, MongoDBReplicaset):
    def get_host_migrate_steps(self):
        return self.get_replica_migration_steps()
