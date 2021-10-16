import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-apps-store",
    description="Meta package for oca-apps-store Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-apps_download',
        'odoo13-addon-apps_product_creator',
        'odoo13-addon-website_apps_store',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
