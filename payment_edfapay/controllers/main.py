# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class EdfaPayController(http.Controller):
    """Controller to handle EdfaPay payment callbacks."""
    
    _return_url = '/payment/edfapay/return'

    @http.route(
        _return_url,
        type='http',
        auth='public',
        methods=['GET', 'POST'],
        csrf=False,
        save_session=False
    )
    def edfapay_return(self, **data):
        """Process the notification data sent by EdfaPay after payment.
        
        :param dict data: The notification data
        """
        _logger.info("Handling EdfaPay return with data:\n%s", pprint.pformat(data))
        
        # Process the notification data
        try:
            # Find transaction by reference (order_id in EdfaPay's case)
            if data.get('order_id'):
                tx_sudo = request.env['payment.transaction'].sudo().search([
                    ('reference', '=', data.get('order_id')),
                    ('provider_code', '=', 'edfapay')
                ], limit=1)
                
                if tx_sudo:
                    tx_sudo._process_notification_data(data)
                else:
                    _logger.warning("No transaction found for reference: %s", data.get('order_id'))
            else:
                _logger.warning("No order_id in notification data")
        except Exception as e:
            _logger.exception("Error processing EdfaPay notification: %s", e)
        
        # Redirect to payment status page
        return request.redirect('/payment/status')

    @http.route(
        '/payment/edfapay/webhook',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False,
        save_session=False
    )
    def edfapay_webhook(self, **data):
        """Process webhook/callback notifications from EdfaPay.
        
        EdfaPay sends callbacks to the notification URL with payment results.
        
        :param dict data: The webhook data
        :return: 'OK' if successful, 'ERROR' otherwise
        :rtype: str
        """
        _logger.info("Received EdfaPay webhook with data:\n%s", pprint.pformat(data))
        
        try:
            # Find transaction by reference (order_id in EdfaPay's case)
            if data.get('order_id'):
                tx_sudo = request.env['payment.transaction'].sudo().search([
                    ('reference', '=', data.get('order_id')),
                    ('provider_code', '=', 'edfapay')
                ], limit=1)
                
                if tx_sudo:
                    tx_sudo._process_notification_data(data)
                    return 'OK'
                else:
                    _logger.warning("No transaction found for reference: %s", data.get('order_id'))
                    return 'ERROR'
            else:
                _logger.warning("No order_id in webhook data")
                return 'ERROR'
        except Exception as e:
            _logger.exception("Error processing EdfaPay webhook: %s", e)
            return 'ERROR'
