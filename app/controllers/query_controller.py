from fastapi import APIRouter

from app.dtos.query_request_dto import QueryRequestDto
from app.dtos.query_response_dto import QueryResponseDto

from app.services.query_service import QueryService

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)

query_service = QueryService()


@router.post(
    "",
    response_model=QueryResponseDto,
)
def generate_sql(
    request: QueryRequestDto,
) -> QueryResponseDto:

    return query_service.generate_sql(request)