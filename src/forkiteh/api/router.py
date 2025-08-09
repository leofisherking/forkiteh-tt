import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from forkiteh.core.exceptions.tron import TronInvalidApiKey, TronWalletNotFound
from forkiteh.domain.use_cases.get_requests_history import GetRequestsUseCase
from forkiteh.domain.use_cases.get_wallet_info import GetWalletInfoUseCase
from forkiteh.schemas.api.pagination import Pagination
from forkiteh.schemas.api.requests_history import RequestsHistoryRequest
from forkiteh.schemas.api.wallet_info import GetWalletInfoPayload
from forkiteh.schemas.wallet_info import WalletInfoSchema
from forkiteh.schemas.wallet_request import WalletRequestSchema

router = APIRouter(prefix="/tron")

logger = logging.getLogger(__name__)


@router.post("", response_model=WalletInfoSchema)
@inject
async def request_wallet_info(
    payload: GetWalletInfoPayload,
    use_case: FromDishka[GetWalletInfoUseCase],
) -> WalletInfoSchema:
    try:
        return await use_case.execute(wallet_address=payload.wallet_address)
    except TronWalletNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except TronInvalidApiKey as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)


@router.get("", response_model=Pagination[WalletRequestSchema])
@inject
async def get_requests_history(
    use_case: FromDishka[GetRequestsUseCase],
    request: RequestsHistoryRequest = Depends(),
) -> Pagination[WalletRequestSchema]:
    items, total = await use_case.execute(
        limit=request.limit,
        offset=request.offset,
    )

    return Pagination(
        total=total,
        items=items,
        limit=request.limit,
        offset=request.offset,
    )
