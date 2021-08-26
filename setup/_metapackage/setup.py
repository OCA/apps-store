import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-apps-store",
    description="Meta package for oca-apps-store Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-apps_download',
        'odoo14-addon-apps_product_creator',
        'odoo14-addon-website_apps_store',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
