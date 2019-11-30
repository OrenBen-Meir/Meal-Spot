# Generated by Django 2.2.6 on 2019-11-30 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20191130_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplyorder',
            name='salesperson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Salesperson'),
        ),
        migrations.CreateModel(
            name='RestaurantAddress',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.Address')),
                ('default', models.BooleanField(default=False)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Restaurant')),
            ],
            bases=('database.address',),
        ),
    ]
