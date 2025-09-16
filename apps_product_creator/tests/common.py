# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase
from odoo.tools import config


class Common(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Trick this configuration value for avoiding an error
        config["source_code_local_path"] = "/tmp/"
        cls.organization1 = cls.env["github.organization"].create(
            {"name": "Organization 1", "github_name": "login"}
        )

        cls.organization_serie1 = cls.env["github.organization.serie"].create(
            {"name": "12.0", "sequence": 1, "organization_id": cls.organization1.id}
        )

        cls.repository1 = cls.env["github.repository"].create(
            {"name": "Repository1", "organization_id": cls.organization1.id}
        )

        cls.branch1 = cls.env["github.repository.branch"].create(
            {
                "name": "12.0",
                "repository_id": cls.repository1.id,
                "organization_id": cls.organization1.id,
            }
        )

        cls.odoo_module2 = cls.env["odoo.module"].create(
            {"technical_name": "odoo_module2"}
        )

        cls.odoo_module1_version2 = cls.env["odoo.module.version"].create(
            {
                "name": "Odoo Module 2",
                "technical_name": "odoo_module2",
                "module_id": cls.odoo_module2.id,
                "repository_branch_id": cls.branch1.id,
                "license": "AGPL-3",
                "summary": "Summary Test",
                "website": "Website Test",
                "description_rst": "Description Test",
                "version": "10.0",
                "author": "OCA",
                "depends": "base",
                "external_dependencies": "{}",
                "full_module_path": "/repo/10.0/odoo_module_2",
            }
        )

        cls.odoo_module1 = cls.env["odoo.module"].create(
            {
                "technical_name": "odoo_module1",
                "dependence_module_version_ids": [
                    (6, 0, [cls.odoo_module1_version2.id])
                ],
            }
        )

        cls.odoo_module1_version1 = cls.env["odoo.module.version"].create(
            {
                "name": "Odoo Module 1",
                "technical_name": "odoo_module1",
                "module_id": cls.odoo_module1.id,
                "repository_branch_id": cls.branch1.id,
                "license": "AGPL-3",
                "summary": "Summary Test",
                "website": "Website Test",
                "description_rst": "Description Test",
                "version": "10.0",
                "author": "OCA",
                "depends": "base",
                "external_dependencies": "{}",
                "full_module_path": "/repo/10.0/odoo_module_1",
            }
        )
        cls.odoo_module2.action_create_product()
