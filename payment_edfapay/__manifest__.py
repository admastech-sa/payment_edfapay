# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'EdfaPay Payment Gateway',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': 'Integrate EdfaPay as a payment provider for Odoo website checkout.',
    'version': '19.0.1.0.1',
    'author': 'Arabian Admas Ltd Co',
    'website': 'https://www.admas.sa',
    'support': 'info@admas.sa',
    'description': """
EdfaPay Payment Gateway Integration for Odoo 19.

This module allows businesses to connect EdfaPay with Odoo and accept online
payments through the standard Odoo payment flow and website checkout.
""",
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/payment_edfapay_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'license': 'LGPL-3',
    'price': 350.0,
    'currency': 'EUR',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}