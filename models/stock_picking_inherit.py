# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api,_
from odoo.exceptions import UserError
import uuid

class StockPicking(models.Model):
    _inherit="stock.picking"
    
    text_message = fields.Text("Message",compute="get_outgoing_detail")
    
    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        if self.picking_type_id.code == "outgoing":
            return 'Delivery Slip %s' % (self.name)
        elif self.picking_type_id.code == "incoming":
            return 'Picking Slip %s' % (self.name)
        else:
            return '%s' % (self.name)
        
    
    report_token = fields.Char("Access Token")
    
    def _get_token(self):
        """ Get the current record access token """
        if self.report_token:
            return self.report_token
        else:
            report_token= str(uuid.uuid4())
            self.write({'report_token':report_token})
            return report_token
    
    def get_ship_download_report_url(self):
        url =''
        if self.id:
            self.ensure_one()
            url = '/download/ship/' + '%s?access_token=%s' % (
                self.id,
                self._get_token()
            )
        return url
    
    def get_do_download_report_url(self):
        url =''
        if self.id:
            self.ensure_one()
            url = '/download/do/' + '%s?access_token=%s' % (
                self.id,
                self._get_token()
            )
        return url
    
    @api.depends('partner_id')
    def get_outgoing_detail(self):
        if self and self.picking_type_id.code == "outgoing":
            for rec in self:
                txt_message = ""
                if rec.partner_id and rec.company_id.inventory_information_in_message:
                    txt_message += "Estimado " + str(rec.partner_id.name)+","+"%0A%0A"+"Aqui esta el orden "+'*'+rec.name+'*'+"%0A%0A"+"A continuación se muestran los detalles de su pedido."+"%0A%0A"
                    if rec.move_ids_without_package:
                        for picking in rec.move_ids_without_package:
                            if picking.quantity_done >0.00:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"*Cantidad de entrega:* "+str(picking.quantity_done)+"%0A"+"________________________"+"%0A"
                            else:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"________________________"+"%0A"
                    if rec.company_id.stock_send_pdf_in_message:
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                        stock_url = "%0A%0A Haga clic aquí para descargar el informe : %0A"+base_url+rec.get_do_download_report_url()
                        txt_message+= stock_url
                    
                    if rec.env.user.sign:
                        txt_message += "%0A%0A%0A"+str(rec.env.user.sign)
                elif rec.company_id.inventory_information_in_message:
                    txt_message += "Aqui esta el orden "+'*'+rec.name+'*'+"%0A%0A"+"Following is your order details."+"%0A%0A"
                    if rec.move_ids_without_package:
                        for picking in rec.move_ids_without_package:
                            if picking.quantity_done >0.00:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"*Cantidad de entrega:* "+str(picking.quantity_done)+"%0A"+"________________________"+"%0A"
                            else:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"________________________"+"%0A"
                    if rec.company_id.stock_send_pdf_in_message:
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                        stock_url = "%0A%0A Haga clic aquí para descargar el informe : %0A"+base_url+rec.get_do_download_report_url()
                        txt_message+= stock_url
                    
                    if rec.env.user.sign:
                        txt_message += "%0A%0A%0A"+str(rec.env.user.sign)
            rec.text_message = txt_message.replace('&','%26')
        
        if self and self.picking_type_id.code == "incoming":
            for rec in self:
                txt_message = ""
                if rec.partner_id and rec.company_id.inventory_information_in_message:
                    txt_message += "Estimado " + str(rec.partner_id.name)+","+"%0A%0A"+"Aqui esta el orden "+'*'+rec.name+'*'+"%0A%0A"+"A continuación se muestran los detalles de su pedido."+"%0A%0A"
                    if rec.move_ids_without_package:
                        for picking in rec.move_ids_without_package:
                            if picking.quantity_done >0.00:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"*Cantidad de entrega:* "+str(picking.quantity_done)+"%0A"+"________________________"+"%0A"
                            else:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"________________________"+"%0A"
                    if rec.company_id.stock_send_pdf_in_message:
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                        stock_url = "%0A%0A Haga clic aquí para descargar el informe : %0A"+base_url+rec.get_ship_download_report_url()
                        txt_message+= stock_url
                        
                    if rec.env.user.sign:
                        txt_message += "%0A%0A%0A"+str(rec.env.user.sign)
                elif rec.company_id.inventory_information_in_message:
                    txt_message += "Aqui esta el orden "+'*'+rec.name+'*'+"%0A%0A"+"A continuación se muestran los detalles de su pedido."+"%0A%0A"
                    if rec.move_ids_without_package:
                        for picking in rec.move_ids_without_package:
                            if picking.quantity_done >0.00:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"*Cantidad de entrega:* "+str(picking.quantity_done)+"%0A"+"________________________"+"%0A"
                            else:
                                txt_message += "%0A"+'*'+picking.product_id.display_name+'*'+"%0A"+"*Cantidad requerida:* "+str(picking.product_uom_qty)+"%0A"+"________________________"+"%0A"
                    if rec.company_id.stock_send_pdf_in_message:
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                        stock_url = "%0A%0A Haga clic aquí para descargar el informe : %0A"+base_url+rec.get_ship_download_report_url()
                        txt_message+= stock_url
                        
                    if rec.env.user.sign:
                        txt_message += "%0A%0A%0A"+str(rec.env.user.sign)
            rec.text_message = txt_message.replace('&','%26')
    
    @api.multi
    def send_by_whatsapp_direct_to_cust_del(self):
        if self and self.company_id.inventory_display_in_message:
            message=''
            if self.text_message:
                message =  str(self.text_message).replace('*','').replace('_','').replace('%0A','<br/>').replace('%20',' ').replace('%26','&')
            self.env['mail.message'].create({
                                            'partner_ids':[(6,0,self.partner_id.ids)],
                                            'model':'stock.picking',
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
        
        