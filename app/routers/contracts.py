from fastapi import APIRouter, Request, Response, status

# import app.models as models
# from app.DTO import DTOContract, DTOError, DTOResponse, DTOReturnContract, DTOReturnSchedule
# from app.settings import Settings
# from app.helpers import DatesUtils
import models as models
from DTO import DTOContract, DTOError, DTOResponse, DTOReturnContract, DTOReturnSchedule
from settings import Settings
from helpers import DatesUtils

import math
from datetime import datetime, timedelta

settings = Settings()
router = APIRouter()


@router.post('/contracts')
async def client_set_client(contract: DTOContract, session: models.SessionDep, response: Response):
    session.statement = models.select(models.Client).where(models.Client.id == contract.clientId)
    results = session.exec(session.statement)
    found: bool = False
    client: models.Client = results.first()
    if client is not None:
        client_id = client.id
        session.statement = models.select(models.TariffPlan).where(models.TariffPlan.id == contract.tariffPlanId)
        results = session.exec(session.statement)
        tariff: models.TariffPlan = results.first()
        if tariff is not None:
            response_schedules = []
            found = True
            period = tariff.period
            total_amount = int(contract.amount * (100 + tariff.markup_rate) / 100)
            profit_amount = total_amount - contract.amount
            new_contract: models.Contract = models.Contract(
                client_id,
                total_amount,
                profit_amount,
                period,
                tariff.id,
                1
            )
            session.add(new_contract)
            session.commit()
            session.refresh(new_contract)
            contract_id = new_contract.id
            new_contract.contract_uid = settings.CORE_MFO + '-' + str(new_contract.id)
            contract_record: DTOReturnContract = DTOReturnContract(
                operationId=str(new_contract.id),
                duration=new_contract.period,
                date=new_contract.created_at.strftime('%Y-%m-%d'),
                totalAmount=new_contract.total_amount,
                prepaidAmount=0,
                paymentsSchedule=[]
            )
            session.add(new_contract)
            session.commit()
            new_merchant: models.ContractMerchant = models.ContractMerchant(
                contract.merchant.inn,
                contract.merchant.brandName,
                contract.merchant.legalName,
                contract_id
            )
            session.add(new_merchant)
            session.commit()
            new_schedules: list[models.ContractSchedule] = []
            schedule_amount = math.floor(total_amount / period)
            schedule_profit_amount = math.floor(profit_amount / period)
            now_date = datetime.now()
            start_date = DatesUtils.start_date(DatesUtils.next_month(now_date), now_date.day)
            for index in range(1, period):
                new_schedule: models.ContractSchedule = models.ContractSchedule(
                    contract_id,
                    schedule_amount,
                    schedule_profit_amount,
                    DatesUtils.start_date(start_date, now_date.day)
                )
                new_schedules.append(new_schedule)
                schedule_record: DTOReturnSchedule = DTOReturnSchedule(
                    paymentDate=DatesUtils.start_date(start_date, now_date.day).strftime('%Y-%m-%d'),
                    amount=schedule_amount
                )
                contract_record.paymentsSchedule.append(schedule_record)
                start_date = DatesUtils.next_month(start_date)
            new_schedule: models.ContractSchedule = models.ContractSchedule(
                contract_id,
                total_amount - schedule_amount * (period - 1),
                profit_amount - schedule_profit_amount * (period - 1),
                DatesUtils.start_date(start_date, now_date.day)
            )
            schedule_record: DTOReturnSchedule = DTOReturnSchedule(
                paymentDate=DatesUtils.start_date(start_date, now_date.day).strftime('%Y-%m-%d'),
                amount=total_amount - schedule_amount * (period-1)
            )
            contract_record.paymentsSchedule.append(schedule_record)
            new_schedules.append(new_schedule)
            new_schedule: models.ContractSchedule = models.ContractSchedule(contract_id, 0, 0, schedule_type=1)
            new_schedules.append(new_schedule)
            new_schedule: models.ContractSchedule = models.ContractSchedule(contract_id, 0, 0, schedule_type=2)
            new_schedules.append(new_schedule)
            for date_schedule in new_schedules:
                session.add(date_schedule)
            session.commit()

    if found:
        result = DTOResponse('', data={"contract": contract_record})
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result = DTOError(1001, 'Can\'t find client')
    return result
