import {
  Document,
  Font,
  Page,
  StyleSheet,
  Text,
  View,
} from "@react-pdf/renderer";
import { PatentAnalysisData } from "../types/PatentType";
import Row from "./pdf/Row";

Font.register({
  family: "Ubuntu Sans Mono",
  fonts: [
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyc7mzgBHrR5yE7ZyRg0QRJMKI4zAbgjc1t-pKe27Ev_kYRiqcZu3n0.ttf",
      fontWeight: 400,
    },
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyc7mzgBHrR5yE7ZyRg0QRJMKI4zAbgjc1t-pKe27Ed_kYRiqcZu3n0.ttf",
      fontWeight: 500,
    },
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyc7mzgBHrR5yE7ZyRg0QRJMKI4zAbgjc1t-pKe27Hx-UYRiqcZu3n0.ttf",
      fontWeight: 600,
    },
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyc7mzgBHrR5yE7ZyRg0QRJMKI4zAbgjc1t-pKe27HI-UYRiqcZu3n0.ttf",
      fontWeight: 700,
    },
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyi7mzgBHrR5yE7ZyRg0QRJMKI45g_SchUEkQgw3KTnva5SgKM7vmn0BLE.ttf",
      fontWeight: 400,
      fontStyle: "italic",
    },
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyi7mzgBHrR5yE7ZyRg0QRJMKI45g_SchUEkQgw3KTnvZxSgKM7vmn0BLE.ttf",
      fontWeight: 500,
      fontStyle: "italic",
    },
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyi7mzgBHrR5yE7ZyRg0QRJMKI45g_SchUEkQgw3KTnvXBVgKM7vmn0BLE.ttf",
      fontWeight: 600,
      fontStyle: "italic",
    },
    {
      src: "https://fonts.gstatic.com/s/ubuntusansmono/v1/jVyi7mzgBHrR5yE7ZyRg0QRJMKI45g_SchUEkQgw3KTnvUlVgKM7vmn0BLE.ttf",
      fontWeight: 700,
      fontStyle: "italic",
    },
  ],
});

const styles = StyleSheet.create({
  page: {
    fontFamily: "Ubuntu Sans Mono",
    fontSize: 10,
    flexDirection: "column",
    paddingTop: 40,
    paddingBottom: 40,
    paddingHorizontal: 40,
  },
  text: {
    fontSize: 12,
  },
  header: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
  },
  tableHeader: {
    fontSize: 14,
    fontWeight: "bold",
    marginBottom: 5,
    marginTop: 20,
  },
  gap: {
    marginTop: 10,
  },
  tableContainer: {
    marginBottom: 20,
  },
});

export default function MyDocument({ data }: { data: PatentAnalysisData }) {
  const date = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
  });

  const itemsPerPage = 5;
  const pages = [];

  for (let i = 0; i < data.analysis.length; i += itemsPerPage) {
    pages.push(data.analysis.slice(i, i + itemsPerPage));
  }

  return (
    <Document
      title={`Patent Infringement Analysis - ${date}`}
      author="Wee Hong"
      subject={`Patent Infringement Analysis - ${date}`}
      language="en"
    >
      {pages.map((pageAnalysis, pageIndex) => (
        <Page size="A4" style={styles.page} key={pageIndex}>
          <Text style={styles.header}>Patent Infringement Analysis Result</Text>

          <Row title="Patent ID" value={data.patent_id} />
          <Row title="Company Name" value={data.company_name} />
          <Row title="Analysis Date" value={date} />

          <View style={styles.gap}>
            <Text style={styles.tableHeader}>Analysis Tables</Text>

            {pageAnalysis.map((item, index) => (
              <View key={index} style={styles.tableContainer}>
                <Text style={styles.tableHeader}>Analysis {index + 1}</Text>
                <Row title="Product Name" value={item.product_name} />
                <Row
                  title="Infringement Likelihood"
                  value={item.infringement_likelihood}
                />
                <Row title="Relevant Claims" value={item.relevant_claims} />
                <Row title="Specific Features" value={item.specific_features} />
                <Row title="Explanation" value={item.explanation} />
                <Row
                  title="Overall Risk Analysis"
                  value={item.risk_assessment}
                />
                {pageIndex < pages.length - 1 ||
                  index < pageAnalysis.length - 1 ? (
                  <View break />
                ) : null}
              </View>
            ))}
          </View>
        </Page>
      ))}
    </Document>
  );
}
