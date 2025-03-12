from pydantic import BaseModel


class MyIDProfileCommonData(BaseModel):
    first_name: str
    middle_name: str
    last_name: str | None
    pinfl: str
    gender: str
    birth_place: str
    birth_country: str
    birth_country_id: str
    birth_country_id_cbu: str | None
    birth_date: str
    nationality: str | None
    nationality_id: str | None
    nationality_id_cbu: str | None
    citizenship: str
    citizenship_id: str | None
    citizenship_id_cbu: str | None
    doc_type: str
    doc_type_id: str | None
    doc_type_id_cbu: str | None
    sdk_hash: str
    last_update_pass_data: str
    last_update_address: str


class MyIDProfileDocData(BaseModel):
    pass_data: str
    issued_by: str
    issued_by_id: str | None
    issued_date: str
    expiry_date: str
    doc_type: str
    doc_type_id: str | None
    doc_type_id_cbu: str | None


class MyIDProfileAddressItem(BaseModel):
    address: str | None
    region: str | None
    region_id: str | None
    region_id_cbu: str | None
    country: str | None
    country_id: str | None
    country_id_cbu: str | None
    district: str | None
    district_id: str | None
    district_id_cbu: str | None
    cadastre: str | None
    registration_date: str | None


class MyIDProfileAddress(BaseModel):
    permanent_address: str | None
    temporary_address: str | None
    permanent_registration: MyIDProfileAddressItem | None
    temporary_registration: MyIDProfileAddressItem | None


class ReportMYID(BaseModel):
    common_data: MyIDProfileCommonData | None
    doc_data: MyIDProfileDocData | None
    address: MyIDProfileAddress | None
    contacts: dict | None
    authentication_method: str | None