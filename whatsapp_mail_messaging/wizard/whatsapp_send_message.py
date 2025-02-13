from odoo import api, fields, models


class WhatsappSendMessage(models.TransientModel):
    """ Wizard for sending WhatsApp messages. """
    _name = 'whatsapp.send.message'
    _description = 'WhatsApp Send Message'

    partner_ids = fields.Many2many('res.partner',
                                   string="Recipients",
                                   help="Select multiple partners to send messages to.")
    mobile = fields.Char(string="Contact Numbers",
                         required=True,
                         help="Comma-separated contact numbers of selected partners.")
    message = fields.Text(string="Message",
                          required=True,
                          help="Message to send via WhatsApp.")
    image_1920 = fields.Binary(string='Image', help="Image of the first selected partner.")

    @api.onchange('partner_ids')
    def _onchange_partner_ids(self):
        """ Updates mobile numbers and image based on selected partners. """
        if self.partner_ids:
            # Fetch and join mobile numbers of all selected partners
            self.mobile = ', '.join(filter(None, self.partner_ids.mapped('mobile')))

            # Set image to the first selected partner (if any)
            self.image_1920 = self.partner_ids[0].image_1920 if self.partner_ids else False

    def send_message(self):
        """ Sends WhatsApp messages to multiple recipients. """
        if self.message and self.partner_ids:
            message_string = self.message.replace(' ', '%20')  # Format message for WhatsApp URL

            for partner in self.partner_ids:
                if partner.mobile:
                    partner.message_post(body=self.message)  # Logs message in chatter

                    # Open WhatsApp for each recipient
                    return {
                        'type': 'ir.actions.act_url',
                        'url': f"https://api.whatsapp.com/send?phone={partner.mobile}&text={message_string}",
                        'target': 'new',
                        'res_id': self.id,
                    }
