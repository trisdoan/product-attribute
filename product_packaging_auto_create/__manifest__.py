# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Packaging Auto Create",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "summary": "Product Packaging Auto Create",
    "author": "Camptocamp, " "Odoo Community Association (OCA)",
    "maintainers": ["simahawk", "dcrier"],
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": ["product_packaging_level"],
    "data": ["data/cron.xml", "views/product_packaging_level_views.xml"],
    "installable": True,
    "auto_install": False,
}
