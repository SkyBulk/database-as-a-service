from django.test import TestCase
from mock import patch, MagicMock
from datetime import datetime

from model_mommy import mommy

from backup.tasks import make_instance_snapshot_backup
from backup.models import Snapshot, BackupGroup
from dbaas.tests.helpers import DatabaseHelper
from physical.models import Environment


FAKE_MAKE_DATABASE_BACKUP_HOUR = [12, 23]
FAKE_RUN_SCRIPT_OUTPUT = {
       'stdout': ['978'],
       'stdin': '',
       'stderr': ''
}


class BaseTestCase(TestCase):

    def setUp(self):
        self.backup_hour = 5
        self.year = 2020
        self.month = 1
        self.day = 1

        mommy.make(
            'Configuration', name='backup_hour', value=str(self.backup_hour)
        )
        mommy.make(
            'Configuration', name='make_database_backup_hour',
            value=','.join(map(str, FAKE_MAKE_DATABASE_BACKUP_HOUR))
        )
        self.dev_env = mommy.make(
            'Environment', name='dev', stage=Environment.DEV
        )
        mommy.make('Environment', name='prod', stage=Environment.PROD)
        self.engine_type = mommy.make(
            'EngineType', name='mysql'
        )
        self.engine = mommy.make(
            'Engine', engine_type=self.engine_type
        )
        self.replication_topology = mommy.make(
            'ReplicationTopology',
            name='MySQL Single 5.7.25',
            class_path='drivers.replication_topologies.mysql.MySQLSingle'
        )
        self.plan = mommy.make(
            'Plan', engine=self.engine,
            replication_topology=self.replication_topology
        )
        self.infra = mommy.make(
            'DatabaseInfra', backup_hour=self.backup_hour,
            plan__has_persistence=True,
            environment=self.dev_env,
            plan=self.plan,
            endpoint='127.0.0.1:1111'
        )
        self.host = mommy.make_recipe(
              'physical.host',
       )
        self.instance = mommy.make(
            'Instance', databaseinfra=self.infra,
            hostname=self.host
        )
        self.volume = mommy.make(
            'Volume', host=self.host
        )
        self.database = DatabaseHelper.create(
            environment=self.dev_env,
            databaseinfra=self.infra
        )
        self.group = BackupGroup()


class CreateSnapshotTestCase(BaseTestCase):
    @patch('backup.tasks.Snapshot.create')
    @patch('backup.tasks.lock_instance',
           new=MagicMock())
    @patch('backup.tasks.unlock_instance',
           new=MagicMock())
    @patch('backup.tasks.mysql_binlog_save',
           new=MagicMock())
    @patch('backup.tasks.VolumeProviderSnapshot',
           new=MagicMock())
    @patch('physical.ssh.HostSSH.run_script',
           new=MagicMock(return_value=FAKE_RUN_SCRIPT_OUTPUT))
    @patch('physical.ssh.HostSSH.connect',
           new=MagicMock())
    @patch('backup.tasks.register_backup_dbmonitor',
           new=MagicMock())
    @patch('physical.models.DatabaseInfra.get_driver',
           new=MagicMock())
    def test_params(self, create_mock):
        make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        create_mock.assert_called_with(
            self.instance,
            self.group,
            self.volume,
            environment=self.dev_env
        )


@patch('backup.tasks.Snapshot.done')
@patch('backup.tasks.lock_instance',
       new=MagicMock(return_value=False))
@patch('backup.tasks.unlock_instance',
       new=MagicMock())
@patch('backup.tasks.mysql_binlog_save',
       new=MagicMock())
@patch('backup.tasks.VolumeProviderSnapshot.take_snapshot')
@patch('physical.ssh.HostSSH.run_script',
       new=MagicMock(return_value=FAKE_RUN_SCRIPT_OUTPUT))
@patch('physical.ssh.HostSSH.connect',
       new=MagicMock())
@patch('backup.tasks.register_backup_dbmonitor',
       new=MagicMock())
@patch('physical.models.DatabaseInfra.get_driver',
       new=MagicMock())
class SnapshotStatusTestCase(BaseTestCase):

    def test_snapshot_warning_when_fail_to_lock(self,
                                                take_snapshot_mock, done_mock):
        snapshot = make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertEqual(snapshot.status, Snapshot.WARNING)
        self.assertTrue(take_snapshot_mock.called)
        self.assertTrue(done_mock.called)

    def test_snapshot_with_error_when_current_hour_in_backup_hour_list(
            self, take_snapshot_mock, done_mock):
        mommy.make(
            'Snapshot',
            status=Snapshot.WARNING,
            instance=self.instance,
            end_at=datetime.now()
        )
        snapshot = make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
            current_hour=FAKE_MAKE_DATABASE_BACKUP_HOUR[1]
        )
        self.assertEqual(snapshot.status, Snapshot.ERROR)
        self.assertFalse(take_snapshot_mock.called)
        self.assertFalse(done_mock.called)

    def test_snapshot_with_warning_when_not_in_backup_hour_list(
            self, take_snapshot_mock, done_mock):
        mommy.make(
            'Snapshot',
            status=Snapshot.WARNING,
            instance=self.instance,
            end_at=datetime.now()
        )
        snapshot = make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
            current_hour=15
        )
        self.assertEqual(snapshot.status, Snapshot.WARNING)
        self.assertFalse(take_snapshot_mock.called)
        self.assertFalse(done_mock.called)

@patch('backup.tasks.Snapshot',
       new=MagicMock())
@patch('backup.tasks.lock_instance',
       new=MagicMock())
@patch('backup.tasks.unlock_instance',
       new=MagicMock())
@patch('backup.tasks.mysql_binlog_save')
@patch('backup.tasks.VolumeProviderSnapshot.take_snapshot',
       new=MagicMock())
@patch('physical.ssh.HostSSH.run_script',
       new=MagicMock(return_value=FAKE_RUN_SCRIPT_OUTPUT))
@patch('physical.ssh.HostSSH.connect',
       new=MagicMock())
@patch('backup.tasks.register_backup_dbmonitor',
       new=MagicMock())
@patch('drivers.mysqldb.MySQL.get_client',
       new=MagicMock())
class BinlogSaveTestCase(BaseTestCase):

    def test_binlog_save_when_is_mysql_single(self, mysql_binlog_save_mock):
        make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertTrue(mysql_binlog_save_mock.called)

    def test_binlog_save_when_is_mysql_foxha(self, mysql_binlog_save_mock):
        self.replication_topology.name = 'MySQL FoxHA 5.7.25',
        self.replication_topology.class_path = (
            'drivers.replication_topologies.mysql.MySQLFoxHA'
        )
        self.replication_topology.save()
        make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertTrue(mysql_binlog_save_mock.called)

    def test_binlog_save_when_is_mysql_percona(self, mysql_binlog_save_mock):
        self.replication_topology.name = 'MySQL Percona FoxHA 5.7.25',
        self.replication_topology.class_path = (
            'drivers.replication_topologies.mysql_percona.MySQLPerconaFoxHA'
        )
        self.replication_topology.save()
        make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertTrue(mysql_binlog_save_mock.called)

    def test_not_call_binlog_save_when_not_mysql(self, mysql_binlog_save_mock):
        self.replication_topology.name = 'Redis Sentinel 4.0',
        self.replication_topology.class_path = (
            'drivers.replication_topologies.redis.RedisSentinel'
        )
        self.replication_topology.save()
        make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertFalse(mysql_binlog_save_mock.called)

@patch('backup.tasks.Snapshot.done',
       new=MagicMock())
@patch('backup.tasks.lock_instance',
       new=MagicMock())
@patch('backup.tasks.unlock_instance',
       new=MagicMock())
@patch('backup.tasks.mysql_binlog_save',
       new=MagicMock())
@patch('backup.tasks.VolumeProviderSnapshot.take_snapshot',
       new=MagicMock())
@patch('backup.tasks.register_backup_dbmonitor',
       new=MagicMock())
@patch('physical.models.DatabaseInfra.get_driver',
       new=MagicMock())
class SnapshotSizeTestCase(BaseTestCase):
    @patch('physical.ssh.HostSSH.run_script',
           return_value=FAKE_RUN_SCRIPT_OUTPUT)
    @patch('physical.ssh.HostSSH.connect',
           new=MagicMock())
    def test_get_snapshot_size(self, run_script_mock):
        snapshot = make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertTrue(run_script_mock.called)
        self.assertEqual(snapshot.size, 978)

    @patch('physical.models.HostSSH.run_script',
           side_effect=IndexError)
    @patch('physical.models.HostSSH.connect',
           new=MagicMock())
    def test_snapshot_size_0_when_got_a_error_on_command(
            self, run_script_mock):
        snapshot = make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertTrue(run_script_mock.called)
        self.assertEqual(snapshot.size, 0)


@patch('backup.tasks.Snapshot.done',
       new=MagicMock())
@patch('backup.tasks.lock_instance',
       new=MagicMock())
@patch('backup.tasks.unlock_instance',
       new=MagicMock())
@patch('backup.tasks.mysql_binlog_save',
       new=MagicMock())
@patch('backup.tasks.VolumeProviderSnapshot.take_snapshot',
       new=MagicMock())
@patch('physical.ssh.HostSSH.run_script',
       side_effect=IndexError)
@patch('physical.ssh.HostSSH.connect',
       new=MagicMock())
@patch('backup.tasks.register_backup_dbmonitor',
       new=MagicMock())
@patch('physical.models.DatabaseInfra.get_driver',
       new=MagicMock())
class BackupPathTestCase(BaseTestCase):

    def test_call_second_remote_command_if_backup_path_exist(
            self, run_script_mock):
        database = self.infra.databases.first()
        database.backup_path = 'fake/path'
        database.save()
        make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertEqual(run_script_mock.call_count, 2)


@patch('backup.tasks.Snapshot.done',
       new=MagicMock())
@patch('backup.tasks.lock_instance',
       new=MagicMock())
@patch('backup.tasks.unlock_instance',
       new=MagicMock())
@patch('backup.tasks.mysql_binlog_save',
       new=MagicMock())
@patch('backup.tasks.VolumeProviderSnapshot.take_snapshot',
       new=MagicMock())
@patch('physical.ssh.HostSSH.run_script',
       new=MagicMock(return_value=FAKE_RUN_SCRIPT_OUTPUT))
@patch('physical.ssh.HostSSH.connect',
       new=MagicMock())
@patch('backup.tasks.register_backup_dbmonitor')
@patch('physical.models.DatabaseInfra.get_driver',
       new=MagicMock())
class RegisterDBMonitorTestCase(BaseTestCase):

    def test_register_on_dbmonitor_when_finish(self, register_dbmonitor_mock):
        make_instance_snapshot_backup(
            instance=self.instance,
            error={},
            group=self.group,
        )
        self.assertTrue(register_dbmonitor_mock.called)
