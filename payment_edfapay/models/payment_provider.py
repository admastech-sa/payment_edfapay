# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('edfapay', 'EdfaPay')],
        ondelete={'edfapay': 'set default'}
    )
    
    edfapay_merchant_key = fields.Char(
        string='Merchant Key',
        help='Your EdfaPay Merchant Key (UUID format)',
        required_if_provider='edfapay',
        groups='base.group_system'
    )
    
    edfapay_password = fields.Char(
        string='Password',
        help='Your EdfaPay Password for hash calculation',
        required_if_provider='edfapay',
        groups='base.group_system'
    )

    def _edfapay_get_api_url(self):
        """Return the API URL according to the provider state.
        
        :return: The API URL
        :rtype: str
        """
        self.ensure_one()
        
        if self.state == 'enabled':
            return 'https://api.edfapay.com/payment/initiate'
        else:  # test mode
            return 'https://sandbox.edfapay.com/api/payment/initiate'

    def _get_supported_currencies(self):
        """Override of payment to return the supported currencies."""
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'edfapay':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in [
                    'SAR', 'AED', 'BHD', 'KWD', 'OMR', 'QAR',
                    'USD', 'EUR', 'GBP', 'EGP', 'JOD'
                ]
            )
        return supported_currencies

    def _get_default_payment_method_id(self):
        """Override to return the default payment method for EdfaPay."""
        self.ensure_one()
        if self.code != 'edfapay':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_edfapay.payment_method_edfapay_card', raise_if_not_found=False)

    def _edfapay_make_request(self, endpoint, data=None):
        """Make a request to EdfaPay API.
        
        :param str endpoint: The endpoint to be reached by the request
        :param dict data: The payload of the request
        :return: The JSON-formatted content of the response
        :rtype: dict
        """
        url = f"{self._edfapay_get_api_url()}"
        
        try:
            response = self.env['payment.provider']._make_request(
                url, data=data, method='POST'
            )
            return response
        except Exception as e:
            _logger.exception("Unable to communicate with EdfaPay: %s", e)
            raise ValidationError(_("Could not establish the connection to EdfaPay."))
