import logging
import traceback

from fastapi import APIRouter, HTTPException
from config.config import get_settings
from schemas.request import PatentRequest
from schemas.response import CompanyResponse
from services.patent_check import PatentCheck

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class PatentAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/api/v1/patent", tags=["analysis"])
        self.settings = get_settings()
        self.patent_service = PatentCheck(
            fuzzy_threshold=self.settings.fuzzy_match_threshold
        )
        self._setup_routes()

    def _setup_routes(self):
        """Initialize API routes"""
        self.router.add_api_route(
            "", self.analyze_patent, methods=["POST"], response_model=CompanyResponse
        )

    async def analyze_patent(self, request: PatentRequest) -> CompanyResponse:
        """
        Analyze patent and company data with optional fuzzy matching support.

        Args:
            request: PatentRequest containing patent_id and company_name
            fuzzy_threshold: Optional threshold for fuzzy matching (0-100)

        Returns:
            CompanyResponse with analysis results or suggestions for similar matches

        Raises:
            HTTPException: For invalid inputs or internal errors
        """
        try:
            logger.debug(f"Received request: {request.model_dump()}")
            logger.debug(f"Settings loaded: {self.settings}")

            if not request.patent_id or not request.company_name:
                raise HTTPException(
                    status_code=400,
                    detail="Both patent_id and company_name are required",
                )

            try:
                analysis_result = self.patent_service.check_patent(
                    patent_id=request.patent_id, company_name=request.company_name
                )
                logger.debug(f"Analysis result: {analysis_result}")
            except FileNotFoundError as e:
                logger.error(f"Data file not found: {str(e)}")
                raise HTTPException(
                    status_code=500, detail=f"Data file not found: {str(e)}"
                )
            except Exception as e:
                logger.error(f"Analysis error: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise HTTPException(
                    status_code=500, detail=f"Error during analysis: {str(e)}"
                )

            if not analysis_result:
                raise HTTPException(
                    status_code=500, detail="Analysis returned no results"
                )

            return CompanyResponse(
                message=analysis_result.get("message", "Analysis completed"),
                data=analysis_result.get("data", {}),
                status=analysis_result.get("status", False),
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
