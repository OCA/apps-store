# pylint: disable=manifest-version-format
{
    "name": "Empty module for tests",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA)",
    "version": "13.0.1.0.0",
    "depends": ["base", "dependency_module"],  # test dependency repo installation
    "data": ["security/ir.model.access.csv"],
}
