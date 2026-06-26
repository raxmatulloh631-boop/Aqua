from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Rasm'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Mahsulot nomi'),
        ),
    ]
