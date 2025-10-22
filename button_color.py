#değişkenler:
#User_ID: Kullanıcı kimliği
#Variant: A veya B (örneğin: kırmızı buton / mavi buton)
#Clicks: Kullanıcının yaptığı tıklama sayısı
#Conversioans: Kullanıcı dönüşüm yaptı mı (örneğin 0/1) veya toplam dönüşüm sayısı



# soru: B varyantı (treatment), A varyantına göre dönüşüm oranını artırıyor mu?”

# Her varyant için:
# Kullanıcı sayısı
# Dönüşüm sayısı
#
# Dönüşüm oranı = sum(Conversions) / count(User_ID)
#
# İki oranın farkını istatistiksel olarak test etmek (z-test)
# H₀: pₐ = p_b
# H₁: pₐ ≠ p_b
#
# (Opsiyonel) “Clicks” üzerinden yardımcı metrikler:
#
# Ortalama tıklama sayısı
# Click başına dönüşüm oranı (CTR veya CVR)


import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt
# 1.soru  Hazırlık & veri yükleme ilk 5 veri
df=pd.read_csv("ab_data.csv")
df.head()
#Toplam kaç satır var?
df.shape # 2000 satır 4 sutun
len(df) # 2000 satır

#Boş/missing değer var mı? Hangi sütunlarda?
df.isnull().sum()
#User_ID benzersiz mi? kaç tekrar var?
df["User_ID"].nunique() #2000
df["Conversions"].nunique() #2

#Variant sadece A ve B içeriyor mu? Varsa farklı değerler hangileri?
df["Variant"].unique()
df["Variant"].value_counts() #Her bir değerden kaç tane var (kontrol için)

#Conversions sadece 0/1 mi? Varsa farklı değerleri listeler misin?
df["Conversions"].unique()
df["Conversions"].value_counts()

#butonların tıklanma sayısı ?
df.groupby("Variant")["Clicks"].sum()

#Grupların(A ve B - Variant) Ana dönüşüm(conversions) oranlarını hesapla:
df.groupby("Variant").agg({"Conversions": "mean"})  # A:0.0270  B:0.0422

#1.hipotezleri kur:
# İki oranın farkını istatistiksel olarak test etmek :
#H0:İki değişken arasında anlamlı bir fark yoktur.
#H1:İki değişken arasında anlamlı bir fark vardır .

# H₀: p1 = p2
# H₁: p1 ≠ p2
#p-value < 0.05 → H₀ reddedilir → istatistiksel olarak anlamlı fark var
#p-value ≥ 0.05 → H₀ kabul edilir → fark anlamlı değil.

#3.Conversions kategorik bir veri olduğu için z_test: Dönüşüm oranı = sum(Conversions) / count(User_ID) toplam başarı sayısı/toplam kullanıcı sayısı
from statsmodels.stats.proportion import proportions_ztest

# Başarı sayıları (dönüşüm sayıları)
A_success = df.loc[df["Variant"]=="A", "Conversions"].sum()
B_success = df.loc[df["Variant"]=="B", "Conversions"].sum()

# Her grubun toplam kullanıcı sayısı
A_n = df.loc[df["Variant"]=="A", "Conversions"].count()
B_n = df.loc[df["Variant"]=="B", "Conversions"].count()

# Z-test count:başarı sayıları , nobs= her grubun gözlem sayıları
test_stat, pvalue = proportions_ztest(count=[A_success, B_success], nobs=[A_n, B_n])
print("test stat =%4f,p-value=%4f"%(test_stat,pvalue))

# Grupların conversion rate'leri
A_rate = df.loc[df["Variant"]=="A", "Conversions"].mean()
B_rate = df.loc[df["Variant"]=="B", "Conversions"].mean()
#plot
plt.bar(["A (Control)", "B (Treatment)"], [A_rate, B_rate], color=["red", "blue"])
plt.ylabel("Conversion Rate")
plt.title("A/B Test: Conversion Rate Karşılaştırması")
plt.ylim(0, max(A_rate, B_rate)*1.2)  # Y eksenini biraz boşluk bırakacak şekilde ayarladık
plt.show()


#Yorumlayalım:Z-test istatistiği: -5.88 → B grubunun oranı A’dan yüksek olduğu için negatif işaretli (sıralama farkıyla ilgili).
#p-value: 4.08 × 10⁻⁹ → çok küçük, yani neredeyse 0.
#p < 0.05 → istatistiksel olarak anlamlı fark var
# H0 reddedilir → A ve B dönüşüm oranları eşit değil
#B grubunun dönüşüm oranı daha yüksek → Yeni buton (B) kullanıcıları daha fazla dönüştürmüş
#Bu A/B testi sonucunda B butonunu uygulamak mantıklı çünkü kullanıcı davranışını olumlu yönde etkiliyor.
