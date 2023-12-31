# Generated by Django 4.2.1 on 2023-08-30 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField(max_length=15)),
                ('email', models.EmailField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('college', models.CharField(max_length=150)),
                ('books', models.ManyToManyField(blank=True, to='book.books')),
            ],
        ),
    ]
