# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class res_partner(models.Model):
    _inherit="res.partner"
    
#     due_payment = fields.Char("Due Payment",compute="get_payment")
#     
#     @api.multi
#     def get_payment(self):
#         for rec in self:
#             rec.due_payment = rec.get_due_values()
#         
#     def _get_account_move_lines(self, partner_ids):
#         res = {x: [] for x in partner_ids}
#         self.env.cr.execute("SELECT m.name AS move_id, l.date, l.name, l.ref, l.date_maturity, l.partner_id, l.blocked, l.amount_currency, l.currency_id, "
#             "CASE WHEN at.type = 'receivable' "
#                 "THEN SUM(l.debit) "
#                 "ELSE SUM(l.credit * -1) "
#             "END AS debit, "
#             "CASE WHEN at.type = 'receivable' "
#                 "THEN SUM(l.credit) "
#                 "ELSE SUM(l.debit * -1) "
#             "END AS credit, "
#             "CASE WHEN l.date_maturity < %s "
#                 "THEN SUM(l.debit - l.credit) "
#                 "ELSE 0 "
#             "END AS mat "
#             "FROM account_move_line l "
#             "JOIN account_account_type at ON (l.user_type_id = at.id) "
#             "JOIN account_move m ON (l.move_id = m.id) "
#             "WHERE l.partner_id IN %s AND at.type IN ('receivable', 'payable') AND l.full_reconcile_id IS NULL GROUP BY l.date, l.name, l.ref, l.date_maturity, l.partner_id, at.type, l.blocked, l.amount_currency, l.currency_id, l.move_id, m.name", (((fields.date.today(), ) + (tuple(partner_ids),))))
#         for row in self.env.cr.dictfetchall():
#             res[row.pop('partner_id')].append(row)
#         return res
#     
#     
#     @api.multi
#     def get_due_values(self):
#         totals = {}
#         lines = self._get_account_move_lines(self.ids)
#         #print("\n\n\n lines",lines)
#         lines_to_display = {}
#         company_currency = self.env.user.company_id.currency_id
#         for partner_id in self.ids:
#             #print("\n\n\n partner_id",partner_id)
#             lines_to_display[partner_id] = {}
#             totals[partner_id] = {}
#             for line_tmp in lines[partner_id]:
#                 line = line_tmp.copy()
#                 currency = line['currency_id'] and self.env['res.currency'].browse(line['currency_id']) or company_currency
#                 if currency not in lines_to_display[partner_id]:
#                     lines_to_display[partner_id][currency] = []
#                     totals[partner_id][currency] = dict((fn, 0.0) for fn in ['due', 'paid', 'mat', 'total'])
#                 if line['debit'] and line['currency_id']:
#                     line['debit'] = line['amount_currency']
#                 if line['credit'] and line['currency_id']:
#                     line['credit'] = line['amount_currency']
#                 if line['mat'] and line['currency_id']:
#                     line['mat'] = line['amount_currency']
#                 lines_to_display[partner_id][currency].append(line)
#                 if not line['blocked']:
#                     totals[partner_id][currency]['due'] += line['debit']
#                     totals[partner_id][currency]['paid'] += line['credit']
#                     totals[partner_id][currency]['mat'] += line['mat']
#                     totals[partner_id][currency]['total'] += line['debit'] - line['credit']
# 
#         print ("\n\n\n lines_to_display",lines_to_display)
#         print("\n\n\n lines",lines)
    
class res_users(models.Model):
    _inherit="res.users"
    
    sign = fields.Text('Signature')
    
    