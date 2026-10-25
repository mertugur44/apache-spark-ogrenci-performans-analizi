# Apache Spark ile Öğrenci Akademik Performans Analizi

Apache Spark (PySpark) kullanarak öğrenci akademik performansıyla ilişkili faktörleri büyük veri yaklaşımıyla analiz ettiğim bir veri analizi projesidir.

Projede tanımlayıcı istatistikler, Pearson korelasyon analizi ve K-Means kümeleme kullanılarak akademik başarı ile davranışsal özellikler arasındaki ilişkiler incelenmiştir.

## Veri Seti

Projede kullanılan `Student Academic Performance` veri seti ders kapsamında öğretim elemanı tarafından sağlanmıştır ve **250 kayıttan** oluşmaktadır.

Apache Spark ile ölçeklenebilir veri işleme yaklaşımını uygulamak amacıyla veri seti **çoğaltma (replication)** yöntemiyle **100.000 satıra** ölçeklendirilmiştir.

> Analizde kullanılan 100.000 satır, orijinal 250 kaydın tekrarlarından oluşmaktadır; yeni veya benzersiz öğrenci verisi üretilmemiştir.

## Uygulanan Analizler

- Apache Spark (PySpark) ile veri işleme
- 250 kaydın replication yöntemiyle 100.000 satıra ölçeklendirilmesi
- Tanımlayıcı istatistikler
- Pearson korelasyon analizi
- Korelasyon matrisi ve heatmap görselleştirmesi
- StandardScaler ile özellik ölçeklendirme
- K-Means (k=3) ile öğrenci profillerinin oluşturulması

## Öne Çıkan Bulgular

- GPA ile en güçlü pozitif doğrusal ilişkiler `Final_Score` (**r = 0.77**) ve `Midterm_Score` (**r = 0.59**) değişkenlerinde görüldü.
- Stres seviyesi ile GPA arasında **r = -0.18** düzeyinde negatif ilişki gözlemlendi.
- K-Means analizinde `Attendance_%`, `Sleep_Hours` ve `Study_Hours_per_Day` değişkenleri kullanılarak üç farklı davranışsal profil oluşturuldu.
- GPA kümeleme girdisi olarak kullanılmadı; oluşturulan profillerin akademik performanslarını karşılaştırmak amacıyla sonradan değerlendirildi.
- En yüksek ortalama GPA, **7.33/10** ile dengeli ve yüksek çalışma düzeyine sahip profilde gözlemlendi.

## Kullanılan Teknolojiler

`Python` `Apache Spark` `PySpark` `Spark DataFrame` `Spark ML` `K-Means` `StandardScaler` `Pandas` `Matplotlib` `Seaborn`

## Dosyalar

- [`student_academic_performance.csv`](./student_academic_performance.csv) — Projede kullanılan 250 kayıtlık temel veri seti
- [`student_performance_analysis.py`](./student_performance_analysis.py) — Analizin çalıştırılabilir PySpark kodu
- [`Apache_Spark_Ogrenci_Performans_Analizi.pdf`](./Apache_Spark_Ogrenci_Performans_Analizi.pdf) — Projenin detaylı raporu
