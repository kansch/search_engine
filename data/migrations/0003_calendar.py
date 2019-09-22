from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_camper_discount_default_0'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camper_is_available', models.BooleanField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('camper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendars', to='data.Camper')),
            ],
        ),
    ]
