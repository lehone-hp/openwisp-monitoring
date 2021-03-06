from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid

from openwisp_monitoring.device.models import DeviceMonitoring


def create_device_monitoring(apps, schema_editor):
    """
    Data migration
    """
    Device = apps.get_model('config', 'Device')
    DeviceMonitoring = apps.get_model('device_monitoring', 'DeviceMonitoring')
    for device in Device.objects.all():
        DeviceMonitoring.objects.create(device=device)


class Migration(migrations.Migration):
    dependencies = [
        ('config', '0018_config_context'),
        ('device_monitoring', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='DeviceMonitoring',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('ok', 'ok'), ('problem', 'problem'), ('critical', 'critical')], default='ok', db_index=True,
                                                          help_text=DeviceMonitoring._meta.get_field('status').help_text,
                                                          max_length=100, no_check_for_status=True, verbose_name='health status')),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='monitoring', to='config.Device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(
            create_device_monitoring,
            reverse_code=migrations.RunPython.noop
        ),
    ]
