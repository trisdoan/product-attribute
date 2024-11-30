# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductPackagingLevel(models.Model):
    _inherit = "product.packaging.level"

    auto_create_packaging = fields.Boolean(
        help="A cron will create a packaging "
        "for each product missing a packaging with this level"
    )

    @api.model
    def cron_check_create_required_packaging(self):
        """Create required packagings for each consumable product if missing."""
        existing_products = self.env["product.product"].search([("type", "=", "consu")])
        required_packaging_levels = self.search([("auto_create_packaging", "=", True)])
        packaging_model = self.env["product.packaging"]
        create_values = []
        for product in existing_products:
            packagings = product.packaging_ids
            existing_packaging_levels = packagings.mapped("packaging_level_id")
            missing_packaging_levels = (
                required_packaging_levels - existing_packaging_levels
            )
            if not missing_packaging_levels:
                continue
            create_values.extend(
                [
                    plevel._prepare_required_packaging_vals(product)
                    for plevel in missing_packaging_levels
                ]
            )
        if create_values:
            # TODO: consider using queue.job to split this in smaller chunks
            # and have less impact on perf.
            packaging_model.create(create_values)
            msg = f"CREATED {len(create_values)} required packaging"
            _logger.info(msg)
            return msg
        return True

    def _prepare_required_packaging_vals(self, product):
        res = {
            "packaging_level_id": self.id,
            "name": self.name,
            "product_id": product.id,
        }
        return res
