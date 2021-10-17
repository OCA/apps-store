import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-apps-store",
    description="Meta package for oca-apps-store Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-apps_download',
        'odoo12-addon-apps_product_creator',
        'odoo12-addon-website_apps_store',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
