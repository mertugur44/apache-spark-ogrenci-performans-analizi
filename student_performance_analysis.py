from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.stat import Correlation
from pyspark.ml.clustering import KMeans

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ---------------------------------------------------------
# 1. Spark oturumunu başlat
# ---------------------------------------------------------

spark = (
    SparkSession.builder
    .appName("StudentAcademicPerformance")
    .config("spark.sql.crossJoin.enabled", "true")
    .getOrCreate()
)


# ---------------------------------------------------------
# 2. Veri setini oku
# ---------------------------------------------------------

# Veri seti ders kapsamında öğretim elemanı tarafından sağlanmıştır.
# Dosyayı script ile aynı dizine ekleyerek bu yolu kullanabilirsiniz.
CSV_PATH = "student_academic_performance.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(CSV_PATH)
)

df.printSchema()
df.show(5, truncate=False)

print("Orijinal satır sayısı:", df.count())


# ---------------------------------------------------------
# 3. Veri setini 100.000 satıra ölçeklendir
# ---------------------------------------------------------

base_count = df.count()
target_n = 100000
repeat_factor = (target_n + base_count - 1) // base_count

df_big = (
    spark.range(repeat_factor)
    .crossJoin(df)
    .drop("id")
    .limit(target_n)
)

print("Ölçeklendirilmiş satır sayısı:", df_big.count())


# ---------------------------------------------------------
# 4. Tanımlayıcı istatistikler
# ---------------------------------------------------------

desc_cols = [
    "GPA",
    "Attendance_%",
    "Study_Hours_per_Day",
    "Sleep_Hours",
    "Stress_Level_(1-10)",
    "Social_Media_Hours",
    "Assignments_Completed_%",
    "Midterm_Score",
    "Final_Score",
    "Age",
]

print("\nTABLO 1: DESCRIBE (count / mean / stddev / min / max)\n")
df_big.select(desc_cols).describe().show()

print("\nTABLO 2: QUARTILES (Q1=25%, Median=50%, Q3=75%)\n")
df_big.select(desc_cols).summary("25%", "50%", "75%").show()


# ---------------------------------------------------------
# 5. GPA ile diğer değişkenler arasındaki Pearson korelasyonu
# ---------------------------------------------------------

corr_targets = [
    "Age",
    "Study_Hours_per_Day",
    "Sleep_Hours",
    "Attendance_%",
    "Assignments_Completed_%",
    "Midterm_Score",
    "Final_Score",
    "Stress_Level_(1-10)",
    "Social_Media_Hours",
]

corr_rows = [
    (column, df_big.stat.corr("GPA", column))
    for column in corr_targets
]

corr_df = (
    spark.createDataFrame(
        corr_rows,
        ["Variable", "Corr_with_GPA"]
    )
    .orderBy(F.abs(F.col("Corr_with_GPA")).desc())
)

print("\nGPA ile diğer değişkenler arasındaki korelasyonlar (Pearson)\n")
corr_df.show(truncate=False)


# ---------------------------------------------------------
# 6. Korelasyon matrisi ve heatmap
# ---------------------------------------------------------

matrix_cols = ["GPA"] + corr_targets

assembler = VectorAssembler(
    inputCols=matrix_cols,
    outputCol="features"
)

vec_df = (
    assembler
    .transform(df_big.select(matrix_cols))
    .select("features")
)

corr_matrix = Correlation.corr(
    vec_df,
    "features",
    "pearson"
).head()[0]

corr_array = corr_matrix.toArray()

corr_pd = pd.DataFrame(
    corr_array,
    columns=matrix_cols,
    index=matrix_cols
)

plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_pd,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)
plt.title("Korelasyon Matrisi (Pearson)")
plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# 7. K-Means için özellikleri hazırla ve ölçeklendir
# ---------------------------------------------------------

cluster_features = [
    "Attendance_%",
    "Sleep_Hours",
    "Study_Hours_per_Day",
]

assembler_k = VectorAssembler(
    inputCols=cluster_features,
    outputCol="features"
)

tmp = assembler_k.transform(
    df_big.select(cluster_features + ["GPA"])
)

scaler = StandardScaler(
    inputCol="features",
    outputCol="scaled_features",
    withMean=True,
    withStd=True,
)

scaled = scaler.fit(tmp).transform(tmp)


# ---------------------------------------------------------
# 8. K-Means kümeleme
# ---------------------------------------------------------

kmeans = KMeans(
    k=3,
    seed=42,
    featuresCol="scaled_features"
)

model = kmeans.fit(scaled)

clustered = (
    model.transform(scaled)
    .withColumnRenamed("prediction", "cluster")
)


# ---------------------------------------------------------
# 9. Küme dağılımı
# ---------------------------------------------------------

print("\nKÜME DAĞILIMI\n")

clustered.groupBy("cluster") \
    .count() \
    .orderBy("cluster") \
    .show()


# ---------------------------------------------------------
# 10. Öğrenci profillerinin ortalama değerleri
# ---------------------------------------------------------

print("\nKÜME PROFİL ÖZETİ (Ortalamalar)\n")

(
    clustered.groupBy("cluster")
    .agg(
        F.avg("Attendance_%").alias("avg_Attendance"),
        F.avg("Sleep_Hours").alias("avg_Sleep"),
        F.avg("Study_Hours_per_Day").alias("avg_StudyHours"),
        F.avg("GPA").alias("avg_GPA"),
    )
    .orderBy("cluster")
    .show(truncate=False)
)


# Spark oturumunu kapat
spark.stop()
