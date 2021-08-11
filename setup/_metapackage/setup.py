import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-apps-store",
    description="Meta package for oca-apps-store Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-apps_product_creator',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
