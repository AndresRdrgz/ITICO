"""
Management command to create initial currencies and exchange rates for the Balance Sheet feature
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from contrapartes.models import Moneda, TipoCambio
from decimal import Decimal
from datetime import date


class Command(BaseCommand):
    help = 'Creates initial currencies and exchange rates for Balance Sheet functionality'

    def handle(self, *args, **options):
        # Get or create a system user for creating initial data
        system_user, created = User.objects.get_or_create(
            username='system',
            defaults={
                'email': 'system@itico.com',
                'first_name': 'System',
                'last_name': 'User',
                'is_staff': False,
                'is_superuser': False
            }
        )

        # Create common currencies
        currencies = [
            {
                'codigo': 'USD',
                'nombre': 'Dólar estadounidense',
                'simbolo': '$'
            },
            {
                'codigo': 'COP',
                'nombre': 'Peso colombiano',
                'simbolo': '$'
            },
            {
                'codigo': 'EUR',
                'nombre': 'Euro',
                'simbolo': '€'
            },
            {
                'codigo': 'GBP',
                'nombre': 'Libra esterlina',
                'simbolo': '£'
            },
            {
                'codigo': 'JPY',
                'nombre': 'Yen japonés',
                'simbolo': '¥'
            },
            {
                'codigo': 'BRL',
                'nombre': 'Real brasileño',
                'simbolo': 'R$'
            },
            {
                'codigo': 'MXN',
                'nombre': 'Peso mexicano',
                'simbolo': '$'
            },
            {
                'codigo': 'PEN',
                'nombre': 'Sol peruano',
                'simbolo': 'S/'
            },
            {
                'codigo': 'CLP',
                'nombre': 'Peso chileno',
                'simbolo': '$'
            }
        ]

        created_currencies = []
        for currency_data in currencies:
            currency, created = Moneda.objects.get_or_create(
                codigo=currency_data['codigo'],
                defaults={
                    'nombre': currency_data['nombre'],
                    'simbolo': currency_data['simbolo'],
                    'activo': True,
                    'creado_por': system_user
                }
            )
            if created:
                created_currencies.append(currency)
                self.stdout.write(
                    self.style.SUCCESS(f'Created currency: {currency.codigo} - {currency.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Currency already exists: {currency.codigo}')
                )

        # Create sample exchange rates (approximate rates as of 2024)
        exchange_rates = [
            # COP to USD (Colombian Peso)
            {'codigo': 'COP', 'tasa_usd': Decimal('0.00025'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'COP', 'tasa_usd': Decimal('0.00024'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'COP', 'tasa_usd': Decimal('0.00023'), 'fecha': date(2024, 12, 1)},
            
            # EUR to USD (Euro)
            {'codigo': 'EUR', 'tasa_usd': Decimal('1.10'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'EUR', 'tasa_usd': Decimal('1.08'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'EUR', 'tasa_usd': Decimal('1.09'), 'fecha': date(2024, 12, 1)},
            
            # GBP to USD (British Pound)
            {'codigo': 'GBP', 'tasa_usd': Decimal('1.27'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'GBP', 'tasa_usd': Decimal('1.25'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'GBP', 'tasa_usd': Decimal('1.26'), 'fecha': date(2024, 12, 1)},
            
            # JPY to USD (Japanese Yen)
            {'codigo': 'JPY', 'tasa_usd': Decimal('0.0067'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'JPY', 'tasa_usd': Decimal('0.0065'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'JPY', 'tasa_usd': Decimal('0.0066'), 'fecha': date(2024, 12, 1)},
            
            # BRL to USD (Brazilian Real)
            {'codigo': 'BRL', 'tasa_usd': Decimal('0.20'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'BRL', 'tasa_usd': Decimal('0.18'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'BRL', 'tasa_usd': Decimal('0.17'), 'fecha': date(2024, 12, 1)},
            
            # MXN to USD (Mexican Peso)
            {'codigo': 'MXN', 'tasa_usd': Decimal('0.059'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'MXN', 'tasa_usd': Decimal('0.056'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'MXN', 'tasa_usd': Decimal('0.055'), 'fecha': date(2024, 12, 1)},
            
            # PEN to USD (Peruvian Sol)
            {'codigo': 'PEN', 'tasa_usd': Decimal('0.27'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'PEN', 'tasa_usd': Decimal('0.26'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'PEN', 'tasa_usd': Decimal('0.25'), 'fecha': date(2024, 12, 1)},
            
            # CLP to USD (Chilean Peso)
            {'codigo': 'CLP', 'tasa_usd': Decimal('0.0011'), 'fecha': date(2024, 1, 1)},
            {'codigo': 'CLP', 'tasa_usd': Decimal('0.0010'), 'fecha': date(2024, 6, 1)},
            {'codigo': 'CLP', 'tasa_usd': Decimal('0.0009'), 'fecha': date(2024, 12, 1)},
        ]

        created_rates = 0
        for rate_data in exchange_rates:
            try:
                moneda = Moneda.objects.get(codigo=rate_data['codigo'])
                rate, created = TipoCambio.objects.get_or_create(
                    moneda=moneda,
                    fecha=rate_data['fecha'],
                    defaults={
                        'tasa_usd': rate_data['tasa_usd'],
                        'creado_por': system_user
                    }
                )
                if created:
                    created_rates += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created exchange rate: {moneda.codigo} = {rate.tasa_usd} USD on {rate.fecha}'
                        )
                    )
            except Moneda.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Currency not found: {rate_data["codigo"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary:\n'
                f'- Created {len(created_currencies)} new currencies\n'
                f'- Created {created_rates} new exchange rates\n'
                f'- Total currencies in system: {Moneda.objects.count()}\n'
                f'- Total exchange rates in system: {TipoCambio.objects.count()}'
            )
        )
