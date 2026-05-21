import logging
from fastmcp import FastMCP
from .client import get_client

logger = logging.getLogger(__name__)


async def calculate_statistics(numbers: list[float]) -> dict:
    """Calculate descriptive statistics for a list of numbers.

    Args:
        numbers: List of numeric values to analyze
    """
    async with get_client() as client:
        r = await client.post("/stats", json={"numbers": numbers})
        r.raise_for_status()
        logger.info(f"calculate_statistics: n={len(numbers)} status={r.status_code}")
        return r.json()


async def amortize_loan(principal: float, annual_rate: float, months: int) -> dict:
    """Calculate loan amortization schedule and payment totals.

    Args:
        principal: Loan amount
        annual_rate: Annual interest rate as decimal (e.g. 0.06 = 6%)
        months: Loan term in months
    """
    async with get_client() as client:
        r = await client.post(
            "/amortize",
            json={"principal": principal, "annual_rate": annual_rate, "months": months},
        )
        r.raise_for_status()
        logger.info(f"amortize_loan: principal={principal} rate={annual_rate} months={months} status={r.status_code}")
        return r.json()


def register(mcp: FastMCP) -> None:
    mcp.tool()(calculate_statistics)
    mcp.tool()(amortize_loan)
