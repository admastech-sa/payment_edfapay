# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models
from . import controllers

from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    """Setup the EdfaPay provider after installation."""
    setup_provider(env, 'edfapay')


def uninstall_hook(env):
    """Reset the EdfaPay provider upon uninstallation."""
    reset_payment_provider(env, 'edfapay')
