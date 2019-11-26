# -*- coding: utf-8 -*-
# Copyright (C) 2018 Razumovskyi Yurii <GarazdCreation@gmail.com>
{
    'name': 'CRM SMS Client',
    'version': '10.0.1.0.1',
    'category': 'CRM',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz',
    'license': 'AGPL-3',
    'summary': """Allows to send SMS messages to CRM Leads.""",
    'description': 'Adds ability to send SMS to CRM Leads/opportunities.',
    'images': ['static/description/banner.png'],
    'depends': [
        'garazd_sms_client',
        'crm',
        'sales_team'
    ],
    'data': [
        'views/crm_lead_views.xml',
        'views/sms_sms_views.xml',
        'wizard/mass_sms_views.xml',
    ],
    'price': 10.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
