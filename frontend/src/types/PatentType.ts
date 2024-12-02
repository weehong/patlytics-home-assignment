import { ApiError } from "./ErrorType";

export type ResultProps = {
  isLoading: boolean;
  result?: PatentAnalysisData | undefined;
  error: ApiError | null;
};

export type PatentCheckResponse = {
  message: string;
  data: PatentAnalysisData;
  status: boolean;
};

export type PatentAnalysisData = {
  patent_id: string;
  company_name: string;
  analysis: PatentAnalysis[];
};

type PatentAnalysis = {
  product_name: string;
  infringement_likelihood: "High" | "Moderate" | "Low";
  relevant_claims: string[];
  explanation: string;
  specific_features: string[];
  risk_assessment: string;
};
