from openupgradelib import openupgrade

def _migrate_dropship_operating_unit(env, version):
    # migrate dropship svl
    env.cr.execute(
        """
    update stock_valuation_layer
    set operating_unit_id = dropship.operating_unit_id
    from (select sm.id, sp.operating_unit_id
        from stock_move sm,
            (select  sl.id, sl.usage
            from stock_location sl
            where sl.usage = 'supplier') supplier_location,
             (select  sl.id, sl.usage
            from stock_location sl
            where sl.usage = 'customer') customer_location,
             stock_picking sp
        where sm.location_dest_id= customer_location.id
            and sm.location_id = supplier_location.id
            and sm.picking_id = sp.id) dropship
    where stock_move_id = dropship.id""")
    env.cr.commit()

    # dropship return
    env.cr.execute("""
    update stock_valuation_layer svl
    set operating_unit_id = dropship_return.operating_unit_id
    from (select sm.id, sp.operating_unit_id
        from stock_move sm,
            (select  sl.id, sl.usage
            from stock_location sl
            where sl.usage = 'supplier') supplier_location,
             (select  sl.id, sl.usage
            from stock_location sl
            where sl.usage = 'customer') customer_location,
             stock_picking sp
        where sm.location_id = customer_location.id
            and sm.location_dest_id = supplier_location.id
            and sm.picking_id = sp.id) dropship_return
    where dropship_return.id = svl.stock_move_id
    """
    )
    env.cr.commit()

def _migrate_in_operating_unit(env, version):
    env.cr.execute("""
    update stock_valuation_layer svl
    set operating_unit_id = in_move_ou.operating_unit_id
    from (
         select sm.id, sl.operating_unit_id
         from stock_move_line sml
                  inner join stock_move sm on sm.id = sml.move_id
                  inner join(select id, usage, company_id
                             from stock_location sl
                             where not (usage = 'internal'
                                 or (usage = 'transit' and company_id is not null))) source_location
                            on sml.location_id = source_location.id
                  inner join(select id, usage, company_id
                             from stock_location sl
                             where usage = 'internal'
                                or (usage = 'transit' and company_id is not null)) internal_location
                            on sml.location_dest_id = internal_location.id
                  inner join stock_location sl on sm.location_dest_id = sl.id
                  left join res_company rc on sml.owner_id = rc.partner_id
             ) in_move_ou
    where svl.stock_move_id = in_move_ou.id
    """)
    env.cr.commit()

def _migrate_out_operating_unit(env, version):
    env.cr.execute("""
    update stock_valuation_layer svl
    set operating_unit_id = out_move_ou.operating_unit_id
    from (
         select sm.id, sl.operating_unit_id
         from stock_move_line sml
              inner join stock_move sm on sm.id = sml.move_id
              inner join(select id, usage, company_id
                         from stock_location sl
                         where not (usage = 'internal'
                             or (usage = 'transit' and company_id is not null))) dest_location
                        on sml.location_dest_id = dest_location.id
              inner join(select id, usage, company_id
                         from stock_location sl
                         where usage = 'internal'
                            or (usage = 'transit' and company_id is not null)) internal_location
                        on sml.location_id = internal_location.id
              inner join stock_location sl on sm.location_id = sl.id
              left join res_company rc on sml.owner_id = rc.partner_id
         ) out_move_ou
    where svl.stock_move_id = out_move_ou.id
    """)
    env.cr.commit()

@openupgrade.migrate()
def migrate(env, version):
    _migrate_dropship_operating_unit(env, version)
    _migrate_in_operating_unit(env, version)
    _migrate_out_operating_unit(env, version)
