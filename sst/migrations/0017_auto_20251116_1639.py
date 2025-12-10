from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('sst', '0016_alter_campaña_estado'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE sst_usuario DROP CONSTRAINT IF EXISTS sst_usuario_email_key;",
            reverse_sql="ALTER TABLE sst_usuario ADD CONSTRAINT sst_usuario_email_key UNIQUE (email);"
        ),
    ]