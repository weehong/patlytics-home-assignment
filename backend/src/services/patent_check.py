import json
from typing import List, Optional, Tuple
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from services.grok_service import GrokService
from utils.file import get_data_path

llm_service = GrokService()


class PatentCheck:
    def __init__(self, fuzzy_threshold: int = 80):
        """
        Initialize PatentCheck with configurable fuzzy matching threshold.

        Args:
            fuzzy_threshold (int): Minimum similarity score (0-100) for fuzzy matching
        """
        self.fuzzy_threshold = fuzzy_threshold

    def check_patent(self, patent_id: str, company_name: str) -> dict:
        patents = self._get_patent_data(patent_id)
        companies = self._get_company_data(company_name)

        if not patents or not companies:
            closest_patent = (
                self._find_closest_patent(patent_id) if not patents else None
            )
            closest_company = (
                self._find_closest_company(company_name) if not companies else None
            )

            suggestion_msg = self._build_suggestion_message(
                closest_patent, closest_company
            )

            return {
                "message": f"Relevant patent or company not found. {suggestion_msg}",
                "data": {
                    "suggested_patents": closest_patent[0] if closest_patent else None,
                    "suggested_companies": (
                        closest_company[0] if closest_company else None
                    ),
                },
                "status": False,
            }

        return {
            "message": "Patent check successful",
            "data": {
                "patent_id": patent_id,
                "company_name": company_name,
                "analysis": self._analyze_infridgement(patents, companies),
            },
            "status": True,
        }

    def _find_closest_patent(self, patent_id: str) -> Optional[Tuple[str, int]]:
        """Find the closest matching patent ID using fuzzy matching."""
        file_path = get_data_path() / "patents.json"
        with open(file_path, "r", encoding="utf-8") as f:
            patents = json.load(f)
            patent_ids = [p["publication_number"] for p in patents]

        matches = process.extractBests(
            patent_id,
            patent_ids,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=self.fuzzy_threshold,
            limit=3,
        )
        return matches if matches else None

    def _find_closest_company(self, company_name: str) -> Optional[Tuple[str, int]]:
        """Find the closest matching company name using fuzzy matching."""
        file_path = get_data_path() / "company_products.json"
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            company_names = [c["name"] for c in data["companies"]]

        matches = process.extractBests(
            company_name,
            company_names,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=self.fuzzy_threshold,
            limit=3,
        )
        return matches if matches else None

    def _build_suggestion_message(
        self,
        patent_matches: Optional[List[Tuple]],
        company_matches: Optional[List[Tuple]],
    ) -> str:
        """Build a suggestion message based on fuzzy match results."""
        suggestions = []

        if patent_matches:
            patents_str = ", ".join(
                [f"'{p[0]}' ({p[1]}% match)" for p in patent_matches]
            )
            suggestions.append(f"Similar patents found: {patents_str}")

        if company_matches:
            companies_str = ", ".join(
                [f"'{c[0]}' ({c[1]}% match)" for c in company_matches]
            )
            suggestions.append(f"Similar companies found: {companies_str}")

        return " ".join(suggestions)

    def _get_patent_data(self, patent_id: str) -> Optional[dict]:
        """Get patent data with fuzzy matching support."""
        file_path = get_data_path() / "patents.json"
        with open(file_path, "r", encoding="utf-8") as f:
            patents = json.load(f)

            # Exact match first
            exact_match = next(
                (p for p in patents if p["publication_number"] == patent_id), None
            )
            if exact_match:
                return exact_match

            # Fuzzy match if no exact match
            for patent in patents:
                if (
                    fuzz.token_sort_ratio(patent["publication_number"], patent_id)
                    >= self.fuzzy_threshold
                ):
                    return patent

            return None

    def _get_company_data(self, company_name: str) -> Optional[dict]:
        """Get company data with fuzzy matching support."""
        file_path = get_data_path() / "company_products.json"
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            companies = data["companies"]

            # Exact match first (case-insensitive)
            exact_match = next(
                (c for c in companies if c["name"].lower() == company_name.lower()),
                None,
            )
            if exact_match:
                return exact_match

            # Fuzzy match if no exact match
            for company in companies:
                if (
                    fuzz.token_sort_ratio(company["name"].lower(), company_name.lower())
                    >= self.fuzzy_threshold
                ):
                    return company

            return None

    def _analyze_infridgement(self, patent: List[dict], company: List[dict]):
        infringing_products = []

        for product in company["products"]:
            analysis = llm_service.analyze_infringement(patent, product)
            result = llm_service.parse_llm_output(analysis)

            infringing_products.append(
                {
                    "product_name": product["name"],
                    "infringement_likelihood": result["likelihood"],
                    "relevant_claims": result["relevant_claims"],
                    "specific_features": result["specific_features"],
                    "explanation": result["explanation"],
                    "risk_assessment": result["risk_assessment"],
                }
            )

        sorted_products = sorted(
            infringing_products,
            key=lambda x: (
                self._get_likelihood_priority(x["infringement_likelihood"]),
                len(x["relevant_claims"]),
            ),
            reverse=True,
        )

        return sorted_products[:2]

    def _get_likelihood_priority(self, likelihood: str):
        priority_map = {"High": 3, "Moderate": 2, "Low": 1}
        return priority_map.get(likelihood, 0)
