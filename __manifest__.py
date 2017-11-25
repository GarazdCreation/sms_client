# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julius Network Solutions SARL <contact@julius.fr>
# Copyright (C) 2015 Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright (C) 2017 Razumovskyi Yurii <garazdcreation@gmail.com>
{
    'name': 'TurboSMS Client',
    'version': '10.0.1.0.1',
    'license': 'AGPL-3',
    'category': 'Tools',
    'description': 'Client for sending SMS via TurboSMS service (https://turbosms.ua). ',
    'author': 'Garazd Creation',
    'website': "https://garazd.biz",
    'depends': ['mail', 'base_sms_client', 'base_suspend_security', 'keychain'],
    'application': True,
    'data': [
        'data/keychain.xml',
        'views/res_partner_views.xml',
        'views/sms_sms_views.xml',
        'wizard/mass_sms_view.xml',
    ],
    'installable': True,
}
