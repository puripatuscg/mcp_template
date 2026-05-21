import math
import statistics
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Math Platform Mock")


class StatsRequest(BaseModel):
    numbers: list[float]


class AmortizeRequest(BaseModel):
    principal: float = Field(gt=0)
    annual_rate: float
    months: int = Field(gt=0)


@app.post("/stats")
def calculate_stats(req: StatsRequest):
    if not req.numbers:
        raise HTTPException(status_code=422, detail="numbers must not be empty")
    nums = req.numbers
    return {
        "mean": round(statistics.mean(nums), 4),
        "median": round(statistics.median(nums), 4),
        "std": round(statistics.stdev(nums), 4) if len(nums) > 1 else 0.0,
        "min": min(nums),
        "max": max(nums),
        "count": len(nums),
    }


@app.post("/amortize")
def amortize_loan(req: AmortizeRequest):
    monthly_rate = req.annual_rate / 12
    n = req.months
    p = req.principal

    if monthly_rate == 0:
        monthly_payment = p / n
    else:
        monthly_payment = (
            p * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)
        )

    schedule = []
    balance = p
    for month in range(1, n + 1):
        interest = balance * monthly_rate
        principal_paid = monthly_payment - interest
        balance = max(balance - principal_paid, 0.0)
        schedule.append({
            "month": month,
            "payment": round(monthly_payment, 2),
            "principal": round(principal_paid, 2),
            "interest": round(interest, 2),
            "balance": round(balance, 2),
        })

    total_paid = monthly_payment * n
    return {
        "monthly_payment": round(monthly_payment, 2),
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_paid - p, 2),
        "schedule": schedule,
    }
