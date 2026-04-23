# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hashlib
import logging
import requests
from werkzeug import urls

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_edfapay.controllers.main import EdfaPayController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Override of payment to return EdfaPay-specific rendering values.
        
        :param dict processing_values: The generic and specific processing values
        :return: The dict of provider-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'edfapay':
            return res

        # Prepare the payment initiation request to EdfaPay
        base_url = self.provider_id.get_base_url()
        
        # Calculate hash: SHA1(MD5(order_id.amount.currency.description.PASSWORD))
        hash_string = (
            f"{self.reference}"
            f"{self.amount:.2f}"
            f"{self.currency_id.name}"
            f"{self.reference}"  # Using reference as description
            f"{self.provider_id.edfapay_password}"
        )
        hash_md5 = hashlib.md5(hash_string.upper().encode('utf-8')).hexdigest()
        hash_value = hashlib.sha1(hash_md5.encode('utf-8')).hexdigest()

        # Prepare the API request data
        api_url = self.provider_id._edfapay_get_api_url()
        term_url = urls.url_join(base_url, EdfaPayController._return_url)
        
        payload = {
            'action': 'SALE',
            'edfa_merchant_id': self.provider_id.edfapay_merchant_key,
            'order_id': self.reference,
            'order_amount': f"{self.amount:.2f}",
            'order_currency': self.currency_id.name,
            'order_description': self.reference,
            'req_token': 'N',
            'payer_first_name': self.partner_name.split(' ')[0] if self.partner_name else 'Customer',
            'payer_last_name': ' '.join(self.partner_name.split(' ')[1:]) if self.partner_name and len(self.partner_name.split(' ')) > 1 else 'Name',
            'payer_address': self.partner_address or 'N/A',
            'payer_country': self.partner_country_id.code if self.partner_country_id else 'SA',
            'payer_city': self.partner_city or 'N/A',
            'payer_zip': self.partner_zip or '00000',
            'payer_email': self.partner_email or 'noreply@example.com',
            'payer_phone': self.partner_phone or '0000000000',
            'payer_ip': self._get_customer_ip(),
            'term_url_3ds': term_url,
            'auth': 'N',
            'recurring_init': 'N',
            'hash': hash_value,
        }

        # Make the API call to get redirect URL
        try:
            _logger.info("Initiating EdfaPay payment for transaction %s", self.reference)
            
            response = requests.post(api_url, data=payload, timeout=10)
            response.raise_for_status()
            
            response_data = response.json()
            
            if 'redirect_url' in response_data:
                redirect_url = response_data['redirect_url']
                _logger.info("EdfaPay redirect URL received for transaction %s", self.reference)
                
                return {
                    'api_url': redirect_url,
                }
            else:
                error_msg = response_data.get('error_message', 'Unknown error from EdfaPay')
                _logger.error("EdfaPay error for transaction %s: %s", self.reference, error_msg)
                raise ValidationError(_("EdfaPay Error: %s") % error_msg)
                
        except requests.exceptions.RequestException as e:
            _logger.exception("EdfaPay API request failed for transaction %s: %s", self.reference, e)
            raise ValidationError(_("Unable to connect to EdfaPay payment gateway. Please try again later."))

    def _get_customer_ip(self):
        """Get the customer's IP address.
        
        :return: The customer's IP address
        :rtype: str
        """
        # Try to get the real IP from request headers
        if hasattr(self.env, 'request') and self.env.request:
            request = self.env.request
            return (
                request.httprequest.headers.get('X-Forwarded-For', '').split(',')[0].strip()
                or request.httprequest.headers.get('X-Real-IP', '')
                or request.httprequest.remote_addr
                or '0.0.0.0'
            )
        return '0.0.0.0'

    @api.model
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Override of payment to find the transaction based on EdfaPay data.
        
        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'edfapay' or len(tx) == 1:
            return tx

        reference = notification_data.get('order_id')
        if not reference:
            raise ValidationError(
                _("EdfaPay: Received data with missing reference (%s)", reference)
            )

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'edfapay')])
        if not tx:
            raise ValidationError(
                _("EdfaPay: No transaction found matching reference %s.", reference)
            )
            
        return tx

    def _process_notification_data(self, notification_data):
        """Override of payment to process the transaction based on EdfaPay data.
        
        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        # Only call super if this is not an EdfaPay transaction
        if self.provider_code != 'edfapay':
            # Try calling super only if the method exists (for compatibility)
            if hasattr(super(), '_process_notification_data'):
                super()._process_notification_data(notification_data)
            return

        # Store the provider reference
        self.provider_reference = notification_data.get('trans_id', notification_data.get('payment_id', ''))

        # Get transaction status
        result = notification_data.get('result', '')
        status = notification_data.get('status', '')
        
        _logger.info(
            "Processing EdfaPay notification for transaction %s - Result: %s, Status: %s",
            self.reference, result, status
        )

        # Process based on result and status
        if result == 'SUCCESS' and status in ['SETTLED', 'PENDING']:
            self._set_done()
            _logger.info("Transaction %s marked as done", self.reference)
            
        elif result == 'REDIRECT' and status in ['3DS', 'REDIRECT']:
            self._set_pending()
            _logger.info("Transaction %s marked as pending (3DS)", self.reference)
            
        elif result == 'DECLINED' or status == 'DECLINED':
            error_msg = notification_data.get('decline_reason', 'Payment declined by gateway')
            self._set_canceled(state_message=error_msg)
            _logger.warning("Transaction %s declined: %s", self.reference, error_msg)
            
        elif result == 'ERROR':
            error_msg = notification_data.get('error_message', 'Unknown error')
            self._set_error(state_message=error_msg)
            _logger.error("Transaction %s error: %s", self.reference, error_msg)
            
        else:
            error_msg = f"Unexpected result: {result}, status: {status}"
            self._set_error(state_message=error_msg)
            _logger.warning("Transaction %s - %s", self.reference, error_msg)
