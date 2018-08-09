# -*- coding: utf-8 -*-
# © 2013-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Magnus (Willem Hulshof <w.hulshof@magnus.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountCutoff(models.Model):
    _inherit = 'account.cutoff'

    def get_prepaid_lines(self):
        self.ensure_one()
        #        import pdb; pdb.set_trace()
        if not self.source_journal_ids:
            raise UserError(
                _("You should set at least one Source Journal!"))
        cutoff_date_str = str(self.cutoff_date)
        sj_ids = self.source_journal_ids.ids
        str_lst = ','.join([str(item) for item in sj_ids])
        cutoff_id = self.id

        # Delete existing lines
        query = ("""DELETE FROM account_cutoff_line
                        WHERE parent_id = %s;""")
        self.env.cr.execute(query, [cutoff_id])

        if self.forecast:
            start_date_str = str(self.start_date)
            end_date_str = str(self.end_date)
            vara = "WHEN l.start_date < '%s' AND l.end_date > '%s' " \
                   "THEN l.end_date - l.start_date + 1 - ('%s' - start_date) - (end_date - '%s') " \
                   "WHEN l.start_date > '%s' AND l.end_date > '%s' " \
                   "THEN l.end_date - l.start_date + 1 - (end_date - '%s') " \
                   "WHEN l.start_date > '%s' AND l.end_date < '%s' " \
                   "THEN l.end_date - l.start_date + 1 " % (
                   start_date_str, end_date_str, start_date_str, end_date_str, start_date_str, end_date_str,
                   end_date_str,
                   start_date_str, end_date_str)
            varb = "l.start_date <= '%s' AND l.journal_id IN (%s) AND l.end_date >= '%s' " % (
            end_date_str, str_lst, start_date_str)

        else:
            vara = "WHEN l.start_date > '%s' " \
                   "THEN l.end_date - l.start_date + 1 ELSE l.end_date - '%s'" % (cutoff_date_str, cutoff_date_str)
            varb = "l.start_date IS NOT NULL AND l.journal_id IN (%s) AND l.end_date > '%s' AND l.date <= '%s' " % (
            str_lst, cutoff_date_str, cutoff_date_str)

        sql_query = ("""
                        INSERT INTO account_cutoff_line (
                                                        parent_id, 
                                                        move_line_id, 
                                                        partner_id, 
                                                        name, 
                                                        start_date,
                                                        end_date, 
                                                        account_id, 
                                                        cutoff_account_id, 
                                                        analytic_account_id,
                                                        operating_unit_id,
                                                        total_days, 
                                                        prepaid_days, 
                                                        amount, 
                                                        currency_id, 
                                                        cutoff_amount,
                                                        create_uid,
                                                        create_date,
                                                        write_uid,
                                                        write_date
                                                        )
                        SELECT {0} AS parent_id,
                                l.id AS move_line_id, 
                                l.partner_id AS partner_id, 
                                l.name AS name, 
                                l.start_date AS start_date, 
                                l.end_date AS end_date, 
                                l.account_id AS account_id,
                                CASE
                                  WHEN a.cutoff_account_id IS NULL THEN l.account_id
                                  ELSE a.cutoff_account_id
                                END AS cutoff_account_id,
                                l.analytic_account_id AS analytic_account_id,
                                l.operating_unit_id AS operating_unit_id,
                                l.end_date - l.start_date + 1 AS total_days,
                                CASE
                                  {1}
                                END AS prepaid_days,
                                l.credit - l.debit AS amount, 
                                {2} AS currency_id, 
                                (l.debit - l.credit) * (CASE {1} END) / (l.end_date - l.start_date + 1) AS cutoff_amount,
                                {5} as create_uid,
                                {6} as create_date,
                                {5} as write_uid,
                                {6} as write_date


                        FROM    account_move_line l LEFT JOIN account_cutoff_mapping a 
                        ON (l.account_id = a.account_id {4})
                        WHERE {3};                
            """.format(cutoff_id,
                       vara,
                       self.company_currency_id.id,
                       varb,
                       "AND a.company_id = %s AND a.cutoff_type = '%s'" % (self.company_id.id, str(self.type)),
                       self._uid,
                       "'%s'" % str(fields.Datetime.to_string(fields.datetime.now()))
                       ))
        self.env.cr.execute(sql_query)
        return True


