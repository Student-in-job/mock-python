from pydantic import BaseModel


class ReportKatmUniversal(BaseModel):
    contingent_liabilities: dict | None
    overview: dict | None
    subscriptions: dict | None
    blacklist: str | None
    open_contracts: dict | None
    contracts: dict | None
    dynamics_of_scoring_ball: dict | None
    incomes_info : dict | None
    scorring: dict | None
    sysinfo: dict | None
    credit_requests: dict | None
    client: dict | None
    claims_wo_contracts: dict | None