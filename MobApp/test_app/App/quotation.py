from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

router = APIRouter()

# ----- Input Schemas -----

class HeaderItem(BaseModel):
    WFCATEGORY: str
    POLICYNUMBER: str
    SOURCE: str

class DataItem(BaseModel):
    PRODUCT: str
    PRODUCTID: str
    BENEFITCODE: str
    ANNUALPREMIUM: Optional[str] = ""
    AGE: str
    GENDER: str
    PPT: str
    PREMIUMFREQUENCY: str
    TERM: str
    DOB: str
    RCD: str
    SUMASSURED: str

class QuotationRequest(BaseModel):
    header: List[HeaderItem]
    data: List[DataItem]

# ----- Output Schemas -----

class TranxStatus(BaseModel):
    TransactionID: str
    Status: str
    Error_Code: Optional[str] = ""
    Error_Description: Optional[str] = ""

class TranxResponseItem(BaseModel):
    PREMIUMRATE: str
    PREMIUM: str

class QuotationResponse(BaseModel):
    TranxStatus: TranxStatus
    TranxResponse: List[TranxResponseItem]

# ----- API Route -----

@router.post("/quotation/calculate", response_model=QuotationResponse)
async def calculate_quotation(request: QuotationRequest):
    try:
        # Mock Logic: Premium = SUMASSURED * 0.1086 (for demo)
        data = request.data[0]  # assuming only one for now
        sum_assured = float(data.SUMASSURED)
        rate = 0.1086
        premium = round(sum_assured * rate, 2)

        return {
            "TranxStatus": {
                "TransactionID": "37647",
                "Status": "Success",
                "Error_Code": "",
                "Error_Description": ""
            },
            "TranxResponse": [
                {
                    "PREMIUMRATE": f"{rate}",
                    "PREMIUM": f"{premium:.0f}"
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
