# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julius Network Solutions SARL <contact@julius.fr>
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <garazdcreation@gmail.com>
{
    'name': 'TurboSMS Client',
    'version': '10.0.2.0.1',
    'category': 'Partner Management',
    'author': 'Garazd Creation',
    'website': "https://garazd.biz",
    'license': 'AGPL-3',
    'summary': """Allows send SMS messages to partners.""",
    'description': 'Allows send SMS messages to partners via TurboSMS service.',
    'images': ['static/description/banner.png'],
    'depends': [
        'garazd_sms_client',
    ],
    'application': True,
    'data': [
        'data/keychain.xml',
        'views/sms_sms_views.xml',
        'views/sms_gateway_views.xml',
        'wizard/mass_sms_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
