# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julius Network Solutions SARL <contact@julius.fr>
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright (C) 2018 Razumovskyi Yurii <garazdcreation@gmail.com>
{
    'name': 'Garazd SMS Client',
    'version': '10.0.1.0.1',
    'category': 'Uncategorized',
    'author': 'Garazd Creation',
    'website': "https://garazd.biz",
    'license': 'AGPL-3',
    'summary': """Common SMS Client for Ukrainian SMS Services.""",
    'description': 'Extends the capabilities of the "Partner" and "SMS message" models.',
    'images': ['static/description/banner.png'],
    'depends': [
        'base_sms_client',
        'base_suspend_security',
        'keychain'
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sms_sms_views.xml',
        'wizard/mass_sms_views.xml',
    ],
    'application': False,
    'installable': True,
}
