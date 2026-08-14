from typing import Annotated
import re

from fastapi import APIRouter, Depends, HTTPException, Path

from app.dependencies import get_stock_summary_service
from app.models.summary import StockSummaryResponse
from app.services.stock_summary import StockSummaryService, NoNewsFoundError

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

@router.get("/{ticker}/summary", response_model=StockSummaryResponse)
async def get_stock_summary(
    ticker: Annotated[str, Path(..., description="The stock ticker symbol")],
    service: Annotated[StockSummaryService, Depends(get_stock_summary_service)]
):
    if not re.match(r"^[A-Za-z0-9]+$", ticker):
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")

    try:
        return await service.get_summary(ticker.upper(), limit=10)
    except NoNewsFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
