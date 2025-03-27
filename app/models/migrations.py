from datetime import datetime
from sqlmodel import Session
from sqlalchemy import Engine

from .client import *
from .partner import *
from .limit import *


def init_limit_types(engine: Engine):
    with Session(engine) as session:
        item1 = LimitTransactionType(
            id=1, code='HOLD', description='Замораживает лимит при подтверждении контракта',
            created_at=datetime.now())
        item2 = LimitTransactionType(
            id=2, code='UNHOLD', description='Освобождает лимит при отмене контракта',
            created_at=datetime.now())
        item3 = LimitTransactionType(
            id=3, code='ACTIVATE', description='Активирует лимит при активации контракта',
            created_at=datetime.now())
        item4 = LimitTransactionType(
            id=4, code='CLOSE/CANCEL', description='Возвращает лимит закрытии или отмене контракта',
            created_at=datetime.now())
        item5 = LimitTransactionType(
            id=5, code='SCORE/RESCORE', description='Назначает лимит при скоринге/перескоринге',
            created_at=datetime.now())
        session.add(item1)
        session.add(item2)
        session.add(item3)
        session.add(item4)
        session.add(item5)
        session.commit()
        session.close()


def init_partners(engine: Engine):
    with Session(engine) as session:
        item_partner = Partner(
            name='Credit Broker', inn='311734464', mfo='00421', bank_name='Мирзо-Улугбекский филиал АИКБ Ипак Йули',
            bank_account='20208000507169380001', vat_number='123456789012', oked='25687',
            description='Кредитный брокер, через который регистрируются контракты',
            access_token = '131d4e35d60e8d6fac4815a01c612ba0', created_at=datetime.now()
        )
        session.add(item_partner)
        item_tariff_1 = TariffPlan(
            name='Тариф 0-3-12', period=3, markup_rate=12, created_at=datetime.now()
        )
        item_tariff_2 = TariffPlan(
            name='Тариф 0-6-26', period=6, markup_rate=26, created_at=datetime.now()
        )
        item_tariff_3 = TariffPlan(
            name='Тариф 0-12-44', period=12, markup_rate=44, created_at=datetime.now()
        )
        session.add(item_tariff_1)
        session.add(item_tariff_2)
        session.add(item_tariff_3)
        session.commit()
        item_partner_tariff_plan1 = PartnerTariffPlan(
            partner_id=1, tariff_plan_id=1, activate_at=datetime.now(), created_at=datetime.now()
        )
        item_partner_tariff_plan2 = PartnerTariffPlan(
            partner_id=1, tariff_plan_id=2, activate_at=datetime.now(), created_at=datetime.now()
        )
        item_partner_tariff_plan3 = PartnerTariffPlan(
            partner_id=1, tariff_plan_id=3, activate_at=datetime.now(), created_at=datetime.now()
        )
        session.add(item_partner_tariff_plan1)
        session.add(item_partner_tariff_plan2)
        session.add(item_partner_tariff_plan3)
        session.commit()
        session.close()


def init_clients(engine: Engine):
    with Session(engine) as session:
        item_legal_report_type1 = LegalReportType(
            code='MYID', description='Данные от MyID', created_at=datetime.now()
        )
        item_legal_report_type2 = LegalReportType(
            code='KATM_UNIVERSAL', description='Отчет универсал от КАТМ', created_at=datetime.now()
        )
        item_legal_report_type3 = LegalReportType(
            code='KATM_UZCARD', description='Отчет UZCARD Scoring от КАТМ', created_at=datetime.now()
        )
        item_legal_report_type4 = LegalReportType(
            code='KATM_HUMO', description='Отчет HUMO Scoring от КАТМ', created_at=datetime.now()
        )
        session.add(item_legal_report_type1)
        session.add(item_legal_report_type2)
        session.add(item_legal_report_type3)
        session.add(item_legal_report_type4)
        session.commit()
        session.close()
