# Generated by Django 3.2.4 on 2021-06-19 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('profile_pic', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Destino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(choices=[('Cerro Navia', 'Cerro Navia'), ('El Bosque', 'El Bosque'), ('Maipú', 'Maipú'), ('Pudahuel', 'Pudahuel'), ('Puente Alto', 'Puente Alto'), ('La Granja', 'La Granja'), ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'), ('Renca', 'Renca'), ('San Bernardo', 'San Bernardo'), ('La Pintana', 'La Pintana'), ('Lo Espejo', 'Lo Espejo'), ('Quilicura', 'Quilicura')], max_length=150)),
                ('destino', models.CharField(choices=[('Centro de Santiago', 'Centro de Santiago')], default='Centro de Santiago', max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recorrido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('origen', models.CharField(max_length=300)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('destino', models.CharField(max_length=300)),
                ('tiempo_con', models.CharField(max_length=100)),
                ('tiempo_sin', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('mini_description', models.TextField(max_length=200)),
                ('color_tag', models.CharField(choices=[('bg-primary', 'bg-primary'), ('bg-secondary', 'bg-secondary'), ('bg-success', 'bg-success'), ('bg-danger', 'bg-danger'), ('bg-warning', 'bg-warning'), ('bg-info', 'bg-info'), ('bg-light', 'bg-light'), ('bg-dark', 'bg-dark'), ('bg-orange', 'bg-orange'), ('bg-brown', 'bg-brown'), ('bg-purple', 'bg-purple'), ('bg-magenta', 'bg-magenta')], default='bg-primary', max_length=100)),
                ('img', models.ImageField(upload_to='')),
                ('fuente', models.URLField(blank=True, null=True)),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.author')),
            ],
        ),
    ]
