# Generated by Django 2.2.10 on 2021-01-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0020_claimapplication_total_receipt_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimapplication',
            name='accommodation_type',
            field=models.CharField(choices=[('hotel', 'Hotel'), ('lojing', 'Lojing')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='claimapplication',
            name='claim_category',
            field=models.CharField(choices=[('mileage', 'Mileage'), ('fi', 'FI'), ('public_transport', 'Public Transport'), ('accommodation', 'Accommodation'), ('others', 'Others')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='claimapplication',
            name='other_type',
            field=models.CharField(choices=[('mileage', 'Mileage'), ('fi', 'FI'), ('public_transport', 'Public Transport'), ('accommodation', 'Accommodation'), ('others', 'Others')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='claimapplication',
            name='state_from',
            field=models.CharField(choices=[('MELAKA', 'MELAKA'), ('JOHOR', 'JOHOR'), ('NEGERI SEMBILAN', 'NEGERI SEMBILAN'), ('PAHANG', 'PAHANG'), ('TERENGGANU', 'TERENGGANU'), ('KELANTAN', 'KELANTAN'), ('PERAK', 'PERAK'), ('PERLIS', 'PERLIS'), ('KEDAH', 'KEDAH'), ('SELANGOR', 'SELANGOR'), ('WILAYAH PERSEKUTUAN KUALA LUMPUR', 'KUALA LUMPUR'), ('SABAH', 'SABAH'), ('SARAWAK', 'SARAWAK'), ('PULAU PINANG', 'PULAU PINANG')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='claimapplication',
            name='state_to',
            field=models.CharField(choices=[('MELAKA', 'MELAKA'), ('JOHOR', 'JOHOR'), ('NEGERI SEMBILAN', 'NEGERI SEMBILAN'), ('PAHANG', 'PAHANG'), ('TERENGGANU', 'TERENGGANU'), ('KELANTAN', 'KELANTAN'), ('PERAK', 'PERAK'), ('PERLIS', 'PERLIS'), ('KEDAH', 'KEDAH'), ('SELANGOR', 'SELANGOR'), ('WILAYAH PERSEKUTUAN KUALA LUMPUR', 'KUALA LUMPUR'), ('SABAH', 'SABAH'), ('SARAWAK', 'SARAWAK'), ('PULAU PINANG', 'PULAU PINANG')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='claimapplication',
            name='transport_type',
            field=models.CharField(choices=[('airplane', 'Airplane'), ('train', 'Train'), ('car', 'Car'), ('bus', 'Bus')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='creditdebitcard',
            name='card_no',
            field=models.CharField(max_length=50, null=True, verbose_name='Credit/ Debit card number'),
        ),
        migrations.AlterField(
            model_name='onlinebanking',
            name='account_bank',
            field=models.CharField(choices=[('cimbclicks', 'CIMB Clicks'), ('maybank2u', 'Maybank2u'), ('affinbank', 'Affin Bank'), ('bsn', 'Bank Simpanan Nasional')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='onlinebanking',
            name='account_type',
            field=models.CharField(choices=[('saving_account', 'Saving Account')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('online_banking', 'Online Banking'), ('credit_debit_card', 'Credit/ Debit card')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receipt_type',
            field=models.CharField(choices=[('receipt', 'Receipt'), ('invoice', 'Invoice')], max_length=50, null=True),
        ),
    ]
