import { PDFViewer } from "@react-pdf/renderer";
import { ResultProps } from "../types/PatentType";
import MyDocument from "./MyDocument";

export default function Viewer({ isLoading, result, error }: ResultProps) {
  if (isLoading) {
    return <div>Searching for patent...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error: {error.message}</div>;
  }

  if (result) {
    return (
      <PDFViewer style={{ width: "100%", height: "100%" }}>
        <MyDocument data={result} />
      </PDFViewer>
    );
  }

  return <div>No data available</div>;
}
