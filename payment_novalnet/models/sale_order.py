import logging

from odoo import _, fields, models, api

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    novalnet_backend_order_info_html = fields.Html(
        string="Payment Information:",
        compute="_compute_novalnet_info_html",
        sanitize=False
    )

    @api.depends('transaction_ids')
    def _compute_novalnet_info_html(self):
        for order in self:
            tx = order.transaction_ids.filtered(lambda t: t.provider_id.code == 'novalnet')[:1]
            if tx:
                order.novalnet_backend_order_info_html = tx.render_novalnet_backend_info(order=order)
            else:
                order.novalnet_backend_order_info_html = ''

    def _compute_payment_term_id(self):
        """ Override of `sale` to preserve a payment term explicitly assigned via
        `payment.transaction.set_novalnet_payment_terms()`.

        In Odoo 19, `payment_term_id` is an editable compute field that depends on
        `partner_id` (`store=True, readonly=False`). If `partner_id` is touched anywhere
        else later in the same transaction (e.g. during order confirmation or post-processing
        that follows a Novalnet webhook), the base compute would silently reset the order back
        to the partner's default payment term, discarding the due date Novalnet provided.

        In addition to matching the term's name, we also confirm the order is actually linked
        to a Novalnet transaction, so a merchant-created term that merely happens to share the
        naming pattern doesn't get accidentally protected.
        """
        novalnet_orders = self.filtered(
            lambda o: o.payment_term_id and o.payment_term_id.name
                      and o.payment_term_id.name.startswith('Novalnet payment due') and
                      o.transaction_ids.filtered(lambda t: t.provider_id.code == 'novalnet')[:1]
        )
        super(SaleOrder, self - novalnet_orders)._compute_payment_term_id()
