# Generated manually for CSV attachment support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semesters', '0006_programmingquestionaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmingquestion',
            name='csv_file',
            field=models.FileField(blank=True, help_text="Optional CSV/data file for pandas/numpy questions (e.g. data for ML). Available as 'data.csv' when user runs code.", null=True, upload_to='programming_data/'),
        ),
    ]
