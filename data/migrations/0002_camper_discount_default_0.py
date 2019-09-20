from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camper',
            name='weekly_discount',
            field=models.FloatField(default=0),
        ),
    ]
