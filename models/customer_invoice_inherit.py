# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api,_
import uuid
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit="account.invoice"
    
    text_message = fields.Text("Message",compute="get_message_detail_so")
    
    report_token = fields.Char("Access Token")
    
    def _get_token(self):
        """ Get the current record access token """
        if self.report_token:
            return self.report_token
        else:
            report_token= str(uuid.uuid4())
            self.write({'report_token':report_token})
            return report_token
    
    def get_download_report_url(self):
        url =''
        if self.id:
            self.ensure_one()
            url = '/download/inv/' + '%s?access_token=%s' % (
                self.id,
                self._get_token()
            )
        return url
    
    @api.depends('partner_id','currency_id','company_id')
    def get_message_detail_so(self):
        if self and self.type in ['out_invoice','out_refund']:
            for inv in self:
                txt_message = ""
                if inv.company_id.invoice_order_information_in_message and inv.partner_id and inv.currency_id and inv.company_id:
                    txt_message +=  "Estimado " + str(inv.partner_id.name)+","+"%0A%0A"
                    if inv.sequence_number_next_prefix and inv.sequence_number_next:
                        txt_message +=  "Aquí está su factura "+'*'+str(inv.sequence_number_next_prefix)+str(inv.sequence_number_next)+'*'+""
                    elif inv.number:
                        txt_message +=  "Aquí está su factura "+'*'+str(inv.number)+'*'+""
                    txt_message += " Por un monto de  "+'*'+str(inv.amount_total)+'*'+""+str(inv.currency_id.symbol)+" de "+inv.company_id.name+"."
                    if inv.state =="paid":
                        txt_message += "Esta factura ya está pagada."+"%0A%0A"
                    else:
                        txt_message += "Por favor remita el pago a su más pronta conveniencia."+"%0A%0A"    
                if inv.company_id.invoice_product_detail_in_message:
                    txt_message += "A continuación se muestran los detalles de su pedido."+"%0A"
                    if inv.invoice_line_ids:
                        for invoices_line in inv.invoice_line_ids:
                            if invoices_line.product_id:
                                txt_message +=  "%0A"+"*"+invoices_line.product_id.display_name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Precio:* "+str(invoices_line.price_unit)+""+str(invoices_line.invoice_id.currency_id.symbol)+"%0A"
                            else:
                                txt_message +=  "%0A"+"*"+invoices_line.name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Precio:* "+str(invoices_line.price_unit)+""+str(invoices_line.invoice_id.currency_id.symbol)+"%0A"
                            if invoices_line.discount > 0.00:
                                txt_message +=  "*Descuento:* "+str(invoices_line.discount)+"%25"+"%0A"
                            txt_message += "________________________"+"%0A"
                        txt_message += "*"+"Monto Total:"+"*"+"%20"+str(inv.amount_total)+""+str(inv.currency_id.symbol)    
                if inv.company_id.inv_send_pdf_in_message:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                    inv_url = "%0A%0A Haga clic aquí para descargar el informe : %0A"+base_url+inv.get_download_report_url()
                    txt_message+= inv_url
                
                if inv.company_id.invoice_signature and inv.env.user.sign:
                    txt_message += "%0A%0A%0A"+str(inv.env.user.sign)
            inv.text_message = txt_message.replace('&','%26')
            
            
        if self and self.type in ['in_invoice','in_refund']:
            for inv in self:
                txt_message = ""
                if inv.company_id.invoice_order_information_in_message and inv.partner_id and inv.currency_id and inv.company_id:
                    txt_message +=  "Estimado " + str(inv.partner_id.name)+","+"%0A%0A"
                    if inv.sequence_number_next_prefix and inv.sequence_number_next:
                        txt_message +=  "Aquí está su factura "+'*'+str(inv.sequence_number_next_prefix)+str(inv.sequence_number_next)+'*'+""
                    elif inv.number:
                        txt_message +=  "Aquí está su factura "+'*'+str(inv.number)+'*'+""
                    txt_message += " Por un monto de "+'*'+str(inv.amount_total)+'*'+""+str(inv.currency_id.symbol)+" de "+inv.company_id.name+"."
                    if inv.state =="paid":
                        txt_message += "Esta factura ya está pagada."+"%0A%0A"
                    else:
                        txt_message += "Por favor remita el pago a su más pronta conveniencia."+"%0A%0A"
                if inv.company_id.invoice_product_detail_in_message:
                    txt_message += "A continuación se muestran los detalles de su pedido."+"%0A"
                    if inv.invoice_line_ids:
                        for invoices_line in inv.invoice_line_ids:
                            if invoices_line.product_id:
                                txt_message +=  "%0A"+"*"+invoices_line.product_id.display_name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Precio:* "+str(invoices_line.price_unit)+""+str(invoices_line.invoice_id.currency_id.symbol)+"%0A"
                            else:
                                txt_message +=  "%0A"+"*"+invoices_line.name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Precio:* "+str(invoices_line.price_unit)+""+str(invoices_line.invoice_id.currency_id.symbol)+"%0A"
                            if invoices_line.discount > 0.00:
                                txt_message +=  "*Descuento:* "+str(invoices_line.discount)+"%25"+"%0A"
                            txt_message += "________________________"+"%0A"
                        txt_message += "*"+"Monto Total:"+"*"+"%20"+str(inv.amount_total)+""+str(inv.currency_id.symbol)
                if inv.company_id.inv_send_pdf_in_message:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                    inv_url = "%0A%0A Haga clic aquí para descargar el informe : %0A"+base_url+inv.get_download_report_url()
                    txt_message+= inv_url
                    
                if inv.company_id.invoice_signature and inv.env.user.sign:
                    txt_message += "%0A%0A%0A"+str(inv.env.user.sign)  
            inv.text_message = txt_message.replace('&','%26')
    
    
    @api.multi
    def send_by_whatsapp_direct_to_ci(self):
        
        if self and self.company_id.invoice_display_in_message and self.type == 'out_invoice':
            message=''
            if self.text_message:
                message =  str(self.text_message).replace('*','').replace('_','').replace('%0A','<br/>').replace('%20',' ').replace('%26','&')
            self.env['mail.message'].create({
                                            'partner_ids':[(6,0,self.partner_id.ids)],
                                            'model':'account.invoice',
                                            'res_id':self.id,
                                            'author_id':self.env.user.partner_id.id,
                                            'body':message or False,
                                            'message_type':'comment',
                                        })
        
        
        if self.partner_id.mobile and self.type == 'out_invoice':
            return {
                    'type': 'ir.actions.act_url',
                    'url': "https://web.whatsapp.com/send?l=&phone="+self.partner_id.mobile+"&text=" + self.text_message,
                    'target': 'new',
                    'res_id': self.id,
                }
        else:
            raise UserError("Partner Mobile Number Not Exist")
        
        
    @api.multi
    def send_by_whatsapp_direct_to_vendor_inv(self):
        if self and self.company_id.invoice_display_in_message and self.type == 'in_invoice':
            message=''
            if self.text_message:
                message =  str(self.text_message).replace('*','').replace('_','').replace('%0A','<br/>').replace('%20',' ').replace('%26','&')
            self.env['mail.message'].create({
                                            'partner_ids':[(6,0,self.partner_id.ids)],
                                            'model':'account.invoice',
                                            'res_id':self.id,
                                            'author_id':self.env.user.partner_id.id,
                                            'body':message or False,
                                            'message_type':'comment',
                                        })
        
        if self.partner_id.mobile and self.type == 'in_invoice':
            return {
                    'type': 'ir.actions.act_url',
                    'url': "https://web.whatsapp.com/send?l=&phone="+self.partner_id.mobile+"&text=" + self.text_message,
                    'target': 'new',
                    'res_id': self.id,
                }
        else:
            raise UserError("Partner Mobile Number Not Exist")
        
        