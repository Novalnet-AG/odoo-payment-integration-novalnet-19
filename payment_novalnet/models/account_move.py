import logging

from odoo import _, fields, models, api

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    novalnet_invoice_info_html = fields.Html(
        string="Payment Information:",
        compute="_compute_novalnet_invoice_info_html",
        sanitize=False,
    )

    @api.depends('payment_ids')
    def _compute_novalnet_invoice_info_html(self):
        for move in self:
            tx = move.transaction_ids.filtered(lambda t: t.provider_id.code == 'novalnet')[:1]
            if tx:
                move.novalnet_invoice_info_html = tx.render_novalnet_backend_info(order=move)
            else:
                move.novalnet_invoice_info_html = ''

    def _compute_invoice_payment_term_id(self):
        """ Override of `account` to preserve a payment term explicitly assigned via
        `payment.transaction.set_novalnet_payment_terms()`.

        In Odoo 19, `invoice_payment_term_id` is an editable compute field that depends on
        `partner_id` (`store=True, readonly=False`). If `partner_id` is touched anywhere else
        later in the same transaction, the base compute would silently reset the invoice back
        to the partner's default payment term, discarding the due date Novalnet provided.
        """
        novalnet_moves = self.filtered(
            lambda m: m.invoice_payment_term_id and m.invoice_payment_term_id.name
                      and m.invoice_payment_term_id.name.startswith('Novalnet payment due')
                      and m.transaction_ids.filtered(lambda t: t.provider_id.code == 'novalnet')[:1]
        )
        super(AccountMove, self - novalnet_moves)._compute_invoice_payment_term_id()
