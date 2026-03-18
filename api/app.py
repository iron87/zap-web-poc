from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="ZAP API Playground",
    description="Simple API playground used for OpenAPI-driven ZAP scans.",
    version="1.0.0",
)


class TransferRequest(BaseModel):
    from_account: str = Field(min_length=3, max_length=32)
    to_account: str = Field(min_length=3, max_length=32)
    amount: float = Field(gt=0)
    currency: Literal["EUR", "USD"] = "EUR"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: int) -> dict[str, object]:
    if customer_id <= 0:
        raise HTTPException(status_code=400, detail="customer_id must be > 0")

    return {
        "id": customer_id,
        "name": f"Customer {customer_id}",
        "tier": "standard" if customer_id % 2 == 0 else "premium",
    }


@app.get("/api/accounts")
def get_accounts() -> dict[str, list[dict[str, object]]]:
    return {
        "accounts": [
            {"id": "ACC-1001", "balance": 1450.25, "currency": "EUR"},
            {"id": "ACC-2002", "balance": 220.0, "currency": "USD"},
        ]
    }


@app.post("/api/transfer")
def transfer(payload: TransferRequest) -> dict[str, object]:
    return {
        "status": "accepted",
        "transaction_id": "TX-0001",
        "from_account": payload.from_account,
        "to_account": payload.to_account,
        "amount": payload.amount,
        "currency": payload.currency,
    }
