# Copyright 2021 Camptocamp SA
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo.tests import common
from odoo.tools.misc import mute_logger


class TestPackagingLevelRequired(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.template"].create(
            {"name": "Product Test", "type": "consu"}
        )
        cls.default_level = cls.env.ref(
            "product_packaging_level.product_packaging_level_default"
        )
        cls.default_level.write({"auto_create_packaging": True})
        cls.test_level = cls.env["product.packaging.level"].create(
            {
                "name": "Packaging Level Test",
                "code": "TEST2",
                "sequence": 2,
                "auto_create_packaging": True,
            }
        )
        # Create packaging only for one of them
        cls.pkg_box = cls.env["product.packaging"].create(
            {
                "name": "Box",
                "product_id": cls.product.product_variant_ids.id,
                "qty": 50,
                "packaging_level_id": cls.default_level.id,
                "barcode": "BOX",
            }
        )

    @mute_logger(
        "odoo.addons.product_packing_level_required.models.product_packaging_level"
    )
    def test_cron_create(self):
        products_count = self.env["product.product"].search_count(
            [("type", "=", "consu")]
        )
        count_packaging = self.env["product.packaging"].search_count
        domain1 = [("packaging_level_id", "=", self.test_level.id)]
        self.assertEqual(count_packaging(domain1), 0)

        domain2 = [("packaging_level_id", "=", self.default_level.id)]
        self.assertEqual(count_packaging(domain2), 1)

        res = self.env["product.packaging.level"].cron_check_create_required_packaging()
        # We get one required packaging per level per product
        self.assertEqual(count_packaging(domain1), products_count)
        self.assertEqual(count_packaging(domain2), products_count)
        # 1 was already created at the setup
        created_count = (products_count * 2) - 1
        self.assertEqual(res, f"CREATED {created_count} required packaging")

        # Let's add another one
        self.env["product.packaging.level"].create(
            {
                "name": "Packaging Level Test 3",
                "code": "TEST3",
                "sequence": 3,
                "auto_create_packaging": True,
            }
        )
        res = self.env["product.packaging.level"].cron_check_create_required_packaging()
        self.assertEqual(res, f"CREATED {products_count} required packaging")
