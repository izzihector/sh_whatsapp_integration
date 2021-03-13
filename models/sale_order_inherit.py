# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api,_
from odoo.exceptions import UserError
import uuid

class SaleOrder(models.Model):
    _inherit="sale.order"
    
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
            url = '/download/so/' + '%s?access_token=%s' % (
                self.id,
                self._get_token()
            )
        return url
    
    text_message = fields.Text("Message",compute="get_message_detail")
    
    @api.depends('partner_id','currency_id','company_id')
    def get_message_detail(self):
        if self:
            for rec in self:
                txt_message = ""
                if rec.company_id.order_information_in_message and rec.partner_id and rec.currency_id and rec.company_id:
                    txt_message +=  "Estimado " + str(rec.partner_id.name)+","+"%0A%0A"+"Aquí esta su orden "+'*'+rec.name+'*'+" Por un monto de "+'*'+str(rec.amount_total)+'*'+""+str(rec.currency_id.symbol)+" de "+rec.company_id.name+"%0A%0A"    
                if rec.company_id.order_product_detail_in_message:
                    txt_message += "A continuación se muestran los detalles de su pedido."+"%0A"
                    if rec.order_line:
                        for sale_line in rec.order_line:
                            if sale_line.display_type != 'line_note' and sale_line.display_type != 'line_section':
                                txt_message +=  "%0A"+"*"+sale_line.product_id.display_name+"*"+"%0A"+"*Cantidad:* "+str(sale_line.product_uom_qty)+"%0A"+"*Precio:* "+str(sale_line.price_unit)+""+str(sale_line.order_id.currency_id.symbol)+"%0A"
                                if sale_line.discount > 0.00:
                                    txt_message +=  "*Descuento:* "+str(sale_line.discount)+"%25"+"%0A"
                                txt_message += "________________________"+"%0A"
                    txt_message += "*"+"Monto Total:"+"*"+"%20"+str(rec.amount_total)+""+str(rec.currency_id.symbol)
                   
                    if rec.company_id.send_pdf_in_message:
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                        quot_url = "%0A%0A Haga clic aquí para descargar el informe : %0A"+base_url+rec.get_download_report_url()
                        txt_message+= quot_url
                    
                if rec.company_id.signature and rec.env.user.sign:
                    txt_message += "%0A%0A%0A"+str(rec.env.user.sign)
            rec.text_message = txt_message.replace('&','%26')
            
    @api.multi
    def send_by_whatsapp_direct(self):
        if self and self.company_id.display_in_message:
            message=''
            if self.text_message:
                message =  str(self.text_message).replace('*','').replace('_','').replace('%0A','<br/>').replace('%20',' ').replace('%26','&')
            self.env['mail.message'].create({
                                            'partner_ids':[(6,0,self.partner_id.ids)],
                                            'model':'sale.order',
                                            'res_id':self.id,
                                            'author_id':self.env.user.partner_id.id,
                                            'body':message or False,
                                            'message_type':'comment',
                                        })
        
        if self.partner_id.mobile:
            return {
                    'type': 'ir.actions.act_url',
                    'url': "https://web.whatsapp.com/send?l=&phone="+self.partner_id.mobile+"&text=" + self.text_message,
                    'target': 'new',
                    'res_id': self.id,
                }
        else:
            raise UserError("Partner Mobile Number Not Exist")
 