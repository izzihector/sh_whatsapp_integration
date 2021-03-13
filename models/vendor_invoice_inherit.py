# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit="account.invoice"
    
    text_message = fields.Text("Message")
    
