import { useState } from "react";
import Form from "./components/Form";
import Viewer from "./components/Viewer";
import { ApiError } from "./types/ErrorType";
import { PatentAnalysisData } from "./types/PatentType";

export default function App() {
  const [data, setData] = useState<PatentAnalysisData | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  const handleError = (err: unknown) => {
    if (err instanceof Response) {
      return {
        message: `Server error: ${err.statusText}`,
        status: err.status,
      };
    }
    if (err instanceof Error) {
      return {
        message: err.message,
        status: 500,
      };
    }
    return {
      message: "An unexpected error occurred",
      status: 500,
    };
  };

  const fetchData = async (patentId: string, companyName: string) => {
    try {
      setLoading(true);
      setError(null);

      const apiHost = import.meta.env.VITE_API_URL;
      const response = await fetch(`${apiHost}/api/v1/patent`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patent_id: patentId,
          company_name: companyName,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();

      if (result.status) {
        setData(result.data);
      } else {
        setError({
          message: result.message,
          status: response.status,
        });
        setData(undefined);
      }
    } catch (err: unknown) {
      const processedError = handleError(err);
      setError(processedError);
      setData(undefined);
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = (data: {
    patentId: string;
    companyName: string;
  }) => {
    fetchData(data.patentId, data.companyName);
  };

  return (
    <div className="h-full mx-auto max-w-7xl sm:px-6 lg:px-8">
      <h1 className="text-4xl font-bold text-center my-8">
        Patlytics Home Assignment
        <small className="block text-sm text-gray-500">By Vernon</small>
      </h1>
      <div className="h-full grid grid-cols-2 space-x-4">
        <Form onSubmit={handleFormSubmit} />
        <Viewer isLoading={loading} result={data} error={error} />
      </div>
    </div>
  );
}
