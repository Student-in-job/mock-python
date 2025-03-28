from fastapi import APIRouter, Request, Response, status

# import app.models as models
# from app.DTO import DTOContract, DTOError, DTOResponse, DTOReturnContract, DTOReturnSchedule, DTOContractConfirm, \
#     DTOReturnContractInfo, DTOReturnScheduleInfo, DTOMerchant
# from app.settings import Settings
# from app.helpers import DatesUtils
import models as models
from DTO import DTOContract, DTOError, DTOResponse, DTOReturnContract, DTOReturnSchedule, DTOContractConfirm, \
    DTOContractConfirm, DTOReturnContractInfo, DTOReturnScheduleInfo, DTOMerchant
from settings import Settings
from helpers import DatesUtils

import math
from datetime import datetime, timedelta

settings = Settings()
router = APIRouter()


@router.post('/contracts')
async def contract_add(contract: DTOContract, session: models.SessionDep, response: Response):
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
            period = tariff.period
            total_amount = int(contract.amount * (100 + tariff.markup_rate) / 100)
            profit_amount = total_amount - contract.amount
            schedule_amount = math.floor(total_amount / period)
            schedule_profit_amount = math.floor(profit_amount / period)
            last_schedule_amount = total_amount - schedule_amount * (period - 1)
            last_schedule_profit_amount = profit_amount - schedule_profit_amount * (period - 1)
            session.statement = models.select(models.LimitBalance).where(models.LimitBalance.client_id == client_id)
            results = session.exec(session.statement)
            limit: models.LimitBalance = results.first()
            if limit is not None:
                if limit.value > last_schedule_amount:
                    found = True
                    limit.value = limit.value - last_schedule_amount
                    session.add(limit)
                    session.commit()
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
                        status=new_contract.status,
                        date=new_contract.created_at.strftime('%Y-%m-%d'),
                        totalAmount=new_contract.total_amount,
                        prepaidAmount=0,
                        paymentsSchedule=[]
                    )
                    session.add(new_contract)
                    new_limit_balance_transaction = models.LimitBalanceTransaction(
                        client_id,
                        - last_schedule_amount,
                        models.LimitTransactionTypes.HOLD,
                        contract_id
                    )
                    session.add(new_limit_balance_transaction)
                    new_merchant: models.ContractMerchant = models.ContractMerchant(
                        contract.merchant.inn,
                        contract.merchant.brandName,
                        contract.merchant.legalName,
                        contract_id
                    )
                    session.add(new_merchant)
                    session.commit()
                    new_schedules: list[models.ContractSchedule] = []
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
                        last_schedule_amount,
                        last_schedule_profit_amount,
                        DatesUtils.start_date(start_date, now_date.day)
                    )
                    schedule_record: DTOReturnSchedule = DTOReturnSchedule(
                        paymentDate=DatesUtils.start_date(start_date, now_date.day).strftime('%Y-%m-%d'),
                        amount=total_amount - schedule_amount * (period-1)
                    )
                    contract_record.paymentsSchedule.append(schedule_record)
                    new_schedules.append(new_schedule)
                    new_schedule: models.ContractSchedule = models.ContractSchedule(
                        contract_id, 0, 0, schedule_type=1)
                    new_schedules.append(new_schedule)
                    new_schedule: models.ContractSchedule = models.ContractSchedule(
                        contract_id, 0, 0, schedule_type=2)
                    new_schedules.append(new_schedule)
                    for date_schedule in new_schedules:
                        session.add(date_schedule)
                    session.commit()
                else:
                    result = DTOError(5019, 'The given contract amount exceeds available limit')
            else:
                result = DTOError(5019, 'The given contract amount exceeds available limit')
        else:
            result = DTOError(5018, 'The given tariff plan is not exists')
    else:
        result = DTOError(5002, 'Can\'t find client')

    if found:
        result = DTOResponse('', data={"contract": contract_record})
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result


@router.post('/contracts/confirm')
async def contract_confirm(contract: DTOContractConfirm, session: models.SessionDep, response: Response):
    found = False
    session.statement = models.select(models.Contract).where(models.Contract.id == int(contract.operationId))
    results = session.exec(session.statement)
    new_contract = results.first()
    if new_contract is not None:
        found = True
        contract_id = new_contract.id
        contract_record: DTOReturnContract = DTOReturnContract(
            operationId=str(new_contract.id),
            duration=new_contract.period,
            status=2,
            date=new_contract.created_at.strftime('%Y-%m-%d'),
            totalAmount=new_contract.total_amount,
            prepaidAmount=0,
            paymentsSchedule=[]
        )
        new_contract.status = 2
        session.add(new_contract)
        session.commit()
        session.statement = models.select(models.ContractSchedule).where(
            models.ContractSchedule.contract_id == contract_id).where(
            models.ContractSchedule.schedule_type == 0
        )
        results = session.exec(session.statement)
        for item in results:
            contract_record.paymentsSchedule.append(
                DTOReturnSchedule(
                    paymentDate=item.payment_date.strftime('%Y-%m-%d'),
                    amount=item.amount
                )
            )

    else:
        result = DTOError(5020, 'Can\'t find contract')

    if found:
        result = DTOResponse('', data={"contract": contract_record})
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result


@router.get('/contracts/{contract_id}')
async def contracts_get(session: models.SessionDep, response: Response, contract_id:int):
    found = False
    session.statement = models.select(models.Contract).where(models.Contract.id == int(contract_id))
    results = session.exec(session.statement)
    new_contract = results.first()
    if new_contract is not None:
        found = True
        contract_record: DTOReturnContractInfo = DTOReturnContractInfo(
            id=str(new_contract.id),
            actUrl='',
            status=new_contract.status,
            date=new_contract.created_at.strftime('%Y-%m-%d'),
            duration=new_contract.period,
            totalAmount=new_contract.total_amount,
            originAmount=new_contract.total_amount-new_contract.profit_amount,
            prepaidAmount=0,
            overdueDays=new_contract.overdue_days,
            overdueAmount=new_contract.overdue_amount,
            paymentsSchedule=[]
        )
        session.statement = models.select(models.ContractMerchant).where(
            models.ContractMerchant.contract_id == contract_id)
        results = session.exec(session.statement)
        new_merchant = results.first()
        merchant_record: DTOMerchant = DTOMerchant(
            inn=new_merchant.inn,
            brandName=new_merchant.brand_name,
            legalName=new_merchant.legal_name
        )
        contract_record.merchant = merchant_record
        session.statement = models.select(models.ContractSchedule).where(
            models.ContractSchedule.contract_id == contract_id).where(
            models.ContractSchedule.schedule_type == 0
        )
        results = session.exec(session.statement)
        for item in results:
            contract_record.paymentsSchedule.append(
                DTOReturnScheduleInfo(
                    paymentDate=item.payment_date.strftime('%Y-%m-%d'),
                    amount=item.amount,
                    paidAmount=item.paid_amount,
                    status=item.status
                )
            )

    else:
        result = DTOError(5020, 'Can\'t find contract')

    if found:
        result = DTOResponse('', data={"contract": contract_record})
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result
