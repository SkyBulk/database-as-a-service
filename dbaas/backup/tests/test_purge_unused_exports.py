from datetime import datetime
from unittest import TestCase

from mock import patch, MagicMock
from model_mommy import mommy

from physical.models import Volume
from backup.tasks import purge_unused_exports


class PurgeUnusedExports(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.instance = mommy.make(
            'Instance',
            port=1000
        )
        cls.environment = cls.instance.databaseinfra.environment

    def setUp(self):
        self.export = mommy.make(
            'Volume'
        )
        self.export.host = self.instance.hostname
        self.export.is_active = False
        self.export.save()

        self.assertEqual(1, len(self.exports))
        self.assertIn(self.export, self.exports)

    @property
    def exports(self):
        return Volume.objects.all()

    def tearDown(self):
        Volume.objects.all().delete()

    @patch('backup.tasks.VolumeProviderSnapshot.destroy_volume')
    @patch('backup.tasks.VolumeProviderSnapshot.detach_disk')
    @patch('backup.tasks.VolumeProviderSnapshot.clean_up')
    @patch('backup.tasks.VolumeProviderSnapshot.add_access')
    def test_delete_only_inactive(self, add_access, clean_up, detach_disk, destroy):
        self.assertTrue(purge_unused_exports())

        add_access.assert_called_once_with(self.export, self.export.host)
        clean_up.assert_called_once_with(self.export)
        detach_disk.assert_called_once_with(self.export)
        destroy.assert_called_once_with(self.export)

    @patch('backup.tasks.VolumeProviderSnapshot.destroy_volume')
    @patch('backup.tasks.VolumeProviderSnapshot.detach_disk')
    @patch('backup.tasks.VolumeProviderSnapshot.clean_up')
    @patch('backup.tasks.VolumeProviderSnapshot.add_access')
    def test_cannot_delete_inactive_with_active_snapshot(
        self, add_access, clean_up, detach_disk, destroy
    ):
        mommy.make(
            'Snapshot',
            volume=self.export
        )

        mommy.make(
            'Snapshot',
            instance=self.instance,
            volume=self.export,
            purge_at=datetime.now()
        )

        self.assertTrue(purge_unused_exports())

        add_access.assert_not_called()
        clean_up.assert_not_called()
        detach_disk.assert_not_called()
        destroy.assert_not_called()

    @patch('backup.tasks.VolumeProviderSnapshot.destroy_volume')
    @patch('backup.tasks.VolumeProviderSnapshot.detach_disk')
    @patch('backup.tasks.VolumeProviderSnapshot.clean_up')
    @patch('backup.tasks.VolumeProviderSnapshot.add_access')
    def test_can_delete_inactive_with_inactive_snapshot(
        self, add_access, clean_up, detach_disk, destroy
    ):
        mommy.make(
            'Snapshot',
            instance=self.instance,
            volume=self.export,
            purge_at=datetime.now()
        )

        self.assertTrue(purge_unused_exports())

        add_access.assert_called_once_with(self.export, self.export.host)
        clean_up.assert_called_once_with(self.export)
        detach_disk.assert_called_once_with(self.export)
        destroy.assert_called_once_with(self.export)

    @patch('backup.tasks.VolumeProviderSnapshot.destroy_volume', new=MagicMock())
    @patch('backup.tasks.VolumeProviderSnapshot.detach_disk', new=MagicMock())
    @patch('backup.tasks.VolumeProviderSnapshot.clean_up', new=MagicMock())
    @patch('backup.tasks.VolumeProviderSnapshot.add_access', new=MagicMock())
    def test_task_with_success(self):
        task = mommy.make('TaskHistory')
        self.assertIsNone(task.details)
        self.assertTrue(purge_unused_exports(task))
        self.assertIn('Removing: {}'.format(self.export), task.details)
        self.assertIn('Success', task.details)

    @patch('backup.tasks.VolumeProviderSnapshot.add_access')
    def test_task_with_error(self, add_access):
        add_access.side_effect = Exception('Fake error')

        task = mommy.make('TaskHistory')
        self.assertIsNone(task.details)
        self.assertFalse(purge_unused_exports(task))
        self.assertIn('Removing: {}'.format(self.export), task.details)
        self.assertIn('Error: Fake error'.format(self.export), task.details)
