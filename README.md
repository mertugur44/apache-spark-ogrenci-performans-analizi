# Apache Spark ile Öğrenci Akademik Performans Analizi

Apache Spark (PySpark) kullanarak öğrenci akademik performansıyla ilişkili faktörleri büyük veri yaklaşımıyla analiz ettiğim bir veri analizi projesidir.

Projede tanımlayıcı istatistikler, Pearson korelasyon analizi ve K-Means kümeleme kullanılarak öğrencilerin akademik başarıları ve davranışsal özellikleri incelenmiştir.

## Veri Seti

Projede kullanılan `Student Academic Performance` veri seti ders kapsamında öğretim elemanı tarafından sağlanmıştır ve 250 öğrenci kaydından oluşmaktadır.

Apache Spark ile ölçeklenebilir veri işleme yaklaşımını uygulamak amacıyla veri seti **çoğaltma (replication)** yöntemiyle 100.000 kayda ölçeklendirilmiştir.

> Analizde kullanılan 100.000 kayıt, orijinal 250 kaydın tekrarlarından oluşmaktadır; yeni veya benzersiz öğrenci verisi üretilmemiştir.

## Uygulanan Analizler

- Apache Spark (PySpark) ile veri işleme
- 250 kaydın 100.000 kayda ölçeklendirilmesi
- Tanımlayıcı istatistikler
- Pearson korelasyon analizi
- Korelasyon matrisi ve heatmap görselleştirmesi
- StandardScaler ile özellik ölçeklendirme
- K-Means (k=3) ile öğrenci profillerinin oluşturulması

## Öne Çıkan Bulgular

- GPA ile en güçlü doğrusal ilişkiler `Final_Score` (**r = 0.77**) ve `Midterm_Score` (**r = 0.59**) değişkenlerinde görüldü.
- Günlük çalışma süresi, derse devam oranı ve uyku süresi GPA ile güçlü doğrusal ilişkiler göstermedi.
- K-Means analiziyle derse devam, uyku ve günlük çalışma süresine göre üç farklı davranışsal öğrenci profili oluşturuldu.
- Profillerin GPA ortalamaları birbirine yakın olmakla birlikte en yüksek devam ve çalışma değerlerine sahip profilin GPA ortalaması **7.33** olarak elde edildi.

## Kullanılan Teknolojiler

`Python` `Apache Spark` `PySpark` `Spark DataFrame` `Spark ML` `K-Means` `StandardScaler` `Pandas` `Matplotlib` `Seaborn`

## Dosyalar

- [`student_performance_analysis.py`](./student_performance_analysis.py) — Analizin çalıştırılabilir PySpark kodu
- [`Apache_Spark_Ogrenci_Performans_Analizi.pdf`](./Apache_Spark_Ogrenci_Performans_Analizi.pdf) — Projenin detaylı raporu
