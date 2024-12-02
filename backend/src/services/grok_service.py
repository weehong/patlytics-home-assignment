import re

from anthropic import Anthropic

from config.config import get_settings


class GrokService:
    def __init__(self):
        self.client = Anthropic(
            api_key=get_settings().LLM_API_KEY,
            base_url="https://api.x.ai",
        )

    def analyze_infringement(self, patent: dict, product: dict) -> dict:
        prompt = f"""
            You are a patent analysis expert. Analyze the potential infringement based on the given patent and product information.

            Patent Title: {patent['title']}
            Patent Claims: {patent['claims']}
            Product Name: {product['name']}
            Product Description: {product['description']}

            Provide your analysis in the exact format below. Do not deviate from this structure:

            Likelihood: High/Moderate/Low
            (Must be exactly one of the values above)

            Relevant Claims:
            Provide only comma-separated claim numbers (e.g., 1, 4, 7, 12)

            Specific Features:
            Provide only comma-separated with relevant specific features (e.g., "Direct advertisement-to-list functionality", "Mobile app integration", "Shopping list synchronization", "Digital weekly ads integration", "Product data payload handling")

            Explanation:
            Provide a single concise sentence explaining the key reason for potential infringement.

            Overall Risk Assessment:
            Provide a conclusion after risk assessment. (e.g., High risk of infringement due to implementation of the core patent.)

            Remember:
            1. Relevant Claims must only contain numbers separated by commas
            2. Explanation must be exactly one sentence
            3. Overall Risk Assessment must be exactly one sentence
            4. Do not add any additional formatting or sections
            5. Do not include any analysis beyond the requested format
            """

        response = self.client.messages.create(
            model="grok-beta",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        return response

    def parse_llm_output(self, response: str) -> dict:
        try:
            text = response.content[0].text if response.content else ""

            likelihood_match = re.search(r"Likelihood:\s*(\w+)", text)
            likelihood = likelihood_match.group(1) if likelihood_match else ""

            claims_match = re.search(r"Relevant Claims:\s*([\d\s*,]+)", text)
            if claims_match:
                claims_text = claims_match.group(1)
                claims = [num.strip() for num in claims_text.split(",")]
            else:
                claims = []

            features_match = re.search(
                r"Specific Features:(.*?)Explanation:", text, re.DOTALL
            )
            if features_match:
                features_text = features_match.group(1).strip()
                features = [feature.strip() for feature in features_text.split(",")]
            else:
                features = []

            explanation_match = re.search(r"Explanation:(.*?)Overall", text, re.DOTALL)
            explanation = (
                explanation_match.group(1).strip() if explanation_match else ""
            )

            risk_match = re.search(
                r"Overall Risk Assessment:\s*(.+?)(?=\n|\Z)", text, re.DOTALL
            )
            risk_assessment = risk_match.group(1).strip() if risk_match else ""

            return {
                "likelihood": likelihood,
                "relevant_claims": claims,
                "specific_features": features,
                "explanation": explanation,
                "risk_assessment": risk_assessment,
            }
        except (AttributeError, IndexError) as e:
            return {
                "likelihood": "",
                "relevant_claims": [],
                "specific_features": [],
                "explanation": "",
                "risk_assessment": "",
            }
