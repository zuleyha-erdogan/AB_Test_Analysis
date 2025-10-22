# 🎯 A/B Test Analysis – Button Color Experiment

Bu proje, bir web sitesindeki **buton renginin** kullanıcı davranışlarını (tıklama ve dönüşüm oranlarını) etkileyip etkilemediğini analiz etmek için yapılmış bir **A/B test çalışmasıdır**.

---

## 📊 Proje Özeti

Bir web sitesi, satış veya kayıt gibi bir hedef aksiyona yönlendiren bir **butonun tasarımını (rengini)** değiştirmek istemektedir.  
Yeni buton renginin (örneğin kırmızıdan maviye geçiş) kullanıcıların dikkatini daha fazla çekip **tıklama (click)** ve **dönüşüm (conversion)** oranlarını artırıp artırmadığı merak edilmektedir.

Bu nedenle, kullanıcılar rastgele iki gruba ayrılmıştır:

- **A (Control):** Mevcut buton tasarımı (örneğin kırmızı)
- **B (Treatment):** Yeni buton tasarımı (örneğin mavi)

Her iki gruptaki kullanıcıların tıklama ve dönüşüm davranışları ölçülmüş, ardından bu iki grubun **ortalama dönüşüm oranları karşılaştırılmıştır.**

Projenin amacı, buton rengindeki değişikliğin **istatistiksel olarak anlamlı bir fark yaratıp yaratmadığını** belirlemektir.  
Eğer fark anlamlıysa, yeni tasarım (B) kullanıcı deneyimini iyileştiriyor demektir.  
Değilse, mevcut tasarım korunabilir.

- **Veri Seti:** `ab_data.csv` (sentetik veri seti – Kaggle'dan alınmıştır)  
- **Analiz Aracı:** Python (pandas, matplotlib, statsmodels)  

Bu proje, A/B testlerinin nasıl uygulanacağını, hipotezlerin nasıl kurulacağını ve istatistiksel anlamlılığın nasıl test edileceğini öğretmek amacıyla hazırlanmıştır.  
Gerçek kullanıcı verisi içermez.

---

## 🧮 Değişkenler

| Değişken | Açıklama |
|-----------|-----------|
| `User_ID` | Kullanıcı kimliği (benzersiz) |
| `Variant` | A veya B (kontrol / yeni tasarım) |
| `Clicks` | Kullanıcının yaptığı tıklama sayısı |
| `Conversions` | 0 veya 1 — hedef davranışı gerçekleştirdi mi |

---

## 🧠 Hipotezler

**H₀ (Null):** A ve B varyantlarının dönüşüm oranları arasında anlamlı bir fark yoktur.  
**H₁ (Alternative):** A ve B varyantlarının dönüşüm oranları arasında anlamlı bir fark vardır.

- p-value < 0.05 → **H₀ reddedilir** → Anlamlı fark vardır.  
- p-value ≥ 0.05 → **H₀ kabul edilir** → Fark istatistiksel olarak anlamlı değildir.

---

## ⚗️ Kullanılan Test

Dönüşüm oranı (categorical success rate) için **iki oran z-testi** kullanılmıştır:

```python
from statsmodels.stats.proportion import proportions_ztest

test_stat, pvalue = proportions_ztest(
    count=[A_success, B_success],
    nobs=[A_n, B_n]
)

🧩 Kullanılan Kütüphaneler
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest

📁 Dosya Yapısı
AB_Test_Button_Color/
│
├── button_color.py       # A/B test analiz kodu
├── ab_data.csv           # Sentetik veri seti
└── README.md             # Proje açıklaması
    nobs=[A_n, B_n]
)

📈 Sonuçlar
Metrik	A (Control)	B (Treatment)
Dönüşüm Oranı	0.0270	0.0422

Z-test istatistiği: -5.88

p-value: 4.08 × 10⁻⁹

Karar: p < 0.05 → H₀ reddedilir

Yorum: B varyantının dönüşüm oranı A varyantına göre istatistiksel olarak anlamlı şekilde daha yüksektir.

✅ Sonuç: Yeni buton tasarımı (B) kullanıcı davranışını olumlu yönde etkilemiştir.
Bu nedenle, yeni buton rengi siteye uygulanabilir.

![button_color](https://github.com/user-attachments/assets/21401b9d-a571-4b04-9fee-4a9ac2e81c30)
