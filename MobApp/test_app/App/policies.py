from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from database import get_db_connection

router = APIRouter()

class PolicySummary(BaseModel):
    policy_id: int
    policy_number: str
    policy_type: str
    start_date: str
    end_date: str
    premium_amount: float
    status: str

class PolicyDetail(PolicySummary):
    details: str | None = None


@router.get("/customers/{customer_id}/policies", response_model=List[PolicySummary])
def get_policies_for_customer(customer_id: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        query = """
            SELECT policy_id, policy_number, policy_type, start_date, end_date, premium_amount, status
            FROM Policies
            WHERE customer_id = ?
        """
        cursor.execute(query, (customer_id,))
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No policies found for this customer")
        policies = [
            PolicySummary(
                policy_id=row[0],
                policy_number=row[1],
                policy_type=row[2],
                start_date=str(row[3]),
                end_date=str(row[4]),
                premium_amount=float(row[5]),
                status=row[6]
            )
            for row in rows
        ]
        return policies
    finally:
        cursor.close()
        conn.close()


@router.get("/policies/{policy_no}", response_model=PolicyDetail)
def get_policy_detail(policy_no: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        query = """
            SELECT policy_id, policy_number, policy_type, start_date, end_date, premium_amount, status, details
            FROM Policies
            WHERE policy_number = ?
        """
        cursor.execute(query, (policy_no))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Policy not found")
        policy = PolicyDetail(
            policy_id=row[0],
            policy_number=row[1],
            policy_type=row[2],
            start_date=str(row[3]),
            end_date=str(row[4]),
            premium_amount=float(row[5]),
            status=row[6],
            details=row[7]
        )
        return policy
    finally:
        cursor.close()
        conn.close()
