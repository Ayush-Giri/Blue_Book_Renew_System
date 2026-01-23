from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collector", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="collectormodel",
            name="is_pickup_available",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]