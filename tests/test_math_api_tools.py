import pytest
from pytest_httpx import HTTPXMock
from tools.api_tools.math_platform import calculate_statistics, amortize_loan


async def test_calculate_statistics_posts_to_stats_endpoint(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/stats",
        json={"mean": 3.0, "median": 3.0, "std": 1.5811, "min": 1.0, "max": 5.0, "count": 5},
    )
    result = await calculate_statistics([1.0, 2.0, 3.0, 4.0, 5.0])
    assert result["mean"] == 3.0
    assert result["count"] == 5


async def test_calculate_statistics_sends_correct_payload(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/stats",
        json={"mean": 7.0, "median": 7.0, "std": 0.0, "min": 7.0, "max": 7.0, "count": 1},
    )
    result = await calculate_statistics([7.0])
    requests = httpx_mock.get_requests()
    import json
    body = json.loads(requests[0].content)
    assert body == {"numbers": [7.0]}


async def test_amortize_loan_posts_to_amortize_endpoint(httpx_mock: HTTPXMock):
    mock_response = {
        "monthly_payment": 5551.0,
        "total_paid": 666120.0,
        "total_interest": 166120.0,
        "schedule": [],
    }
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/amortize",
        json=mock_response,
    )
    result = await amortize_loan(500000.0, 0.06, 120)
    assert result["monthly_payment"] == 5551.0
    assert result["total_interest"] == 166120.0


async def test_amortize_loan_sends_correct_payload(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/amortize",
        json={"monthly_payment": 1000.0, "total_paid": 12000.0, "total_interest": 2000.0, "schedule": []},
    )
    await amortize_loan(10000.0, 0.05, 12)
    requests = httpx_mock.get_requests()
    import json
    body = json.loads(requests[0].content)
    assert body == {"principal": 10000.0, "annual_rate": 0.05, "months": 12}
