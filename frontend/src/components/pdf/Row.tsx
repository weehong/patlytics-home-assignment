import { StyleSheet, Text, View } from "@react-pdf/renderer";

const styles = StyleSheet.create({
  row: {
    flexDirection: "row",
    marginBottom: 0,
  },
  columnLeft: {
    width: "40%",
    padding: 5,
    border: "1px solid black",
    backgroundColor: "#f0f0f0",
  },
  columnRight: {
    width: "60%",
    padding: 5,
    border: "1px solid black",
    borderLeft: 0,
  },
  text: {
    fontSize: 12,
  },
});

export default function Row({
  title,
  value,
}: {
  title: string;
  value: string | string[];
}) {
  return (
    <View style={styles.row}>
      <View style={styles.columnLeft}>
        <Text style={styles.text}>{title}</Text>
      </View>

      <View style={styles.columnRight}>
        {Array.isArray(value) ? (
          <Text style={styles.text}>{value.join(", ")}</Text>
        ) : (
          <Text style={styles.text}>{value}</Text>
        )}
      </View>
    </View>
  );
}
