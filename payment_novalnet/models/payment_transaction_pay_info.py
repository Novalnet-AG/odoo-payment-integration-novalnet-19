"""
Store Novalnet Transaction Payment Informationy
"""
from odoo import fields, models


class NovalnetPaymentTransactionBank(models.Model):
    """
     Store Novalnet Bank Details
    """
    _name = 'novalnet.payment.transaction.bank'
    _description = 'Novalnet bank details for a transaction'

    account_holder = fields.Char(string="Account holder name")
    bank_name = fields.Char(string="Name of the bank that need to be transferred")
    bank_place = fields.Char(string="Place of the bank that need to be transferred")
    bic = fields.Char(string="BIC")
    iban = fields.Char(string="IBAN")


class NovalnetPaymentInstalmentDetails(models.Model):
    """
    Store Novalnet Instalment Details
    """
    _name = 'novalnet.payment.instalment.details'
    _description = 'Novalnet Instalment Details'

    current_executed_cycle = fields.Integer(string="Current Cycle")
    due_instalment = fields.Integer(string="Due Instalment")
    cycle_amount = fields.Char(string="Cycle Amount")
    next_instalment_date = fields.Char(string="Next Instalment Date")
    instalment_all_details = fields.Json(string="Instalment All Details")
    prepaid = fields.Integer(string="Prepaid")
