# Copyright 2022 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api


def pre_init_hook(cr):
    if openupgrade.table_exists(cr, "product_packaging_type"):
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Re-mapping the name for the xml record to be the same as the new version
        openupgrade.logged_query(
            cr,
            query="""
            UPDATE ir_model_data
            SET name = 'product_packaging_level_default'
            WHERE name = 'product_packaging_type_default'
            AND module = 'product_packaging_type';
            """,
        )

        # Former version of the module is present
        models = [("product.packaging.type", "product.packaging.level")]
        openupgrade.rename_models(env.cr, models)
        tables = [("product_packaging_type", "product_packaging_level")]
        openupgrade.rename_tables(env.cr, tables)
        fields = [
            (
                "product.packaging",
                "product_packaging",
                "packaging_type_id",
                "packaging_level_id",
            )
        ]
        openupgrade.rename_fields(env, fields, no_deep=True)

        modules = [("product_packaging_type", "product_packaging_level")]
        openupgrade.update_module_names(env.cr, modules, merge_modules=True)
