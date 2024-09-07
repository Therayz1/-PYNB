import pandas as pd
import re

# Veri setini oku
data = pd.read_csv("house_sales.csv")

# 1. house_id: Bu sütunda herhangi bir temizleme işlemi gerekmiyor.
data['house_id'] = data['house_id'].astype('int64')

# 2. city: Eksik değerleri ve geçersiz değerleri "Unknown" ile değiştir
data['city'].fillna("Unknown", inplace=True)
data['city'] = data['city'].str.replace('--', 'Unknown')  # "--" değerlerini "Unknown" ile değiştir
# city değerlerini temizle (fazladan boşlukları/noktaları kaldır)
data['city'] = data['city'].str.strip().str.replace('.', '')
# Geçersiz şehirleri "Unknown" ile değiştir
valid_cities = ['Silvertown', 'Riverford', 'Teasdale', 'Poppleton']
data.loc[~data['city'].isin(valid_cities), 'city'] = "Unknown"

# 3. sale_price: Eksik girişleri kaldır ve negatif/sıfır değerleri filtrele
data.dropna(subset=['sale_price'], inplace=True)
data = data[data['sale_price'] > 0]
data['sale_price'] = data['sale_price'].astype('float64')

# 4. sale_date: Eksik değerleri "2023-01-01" ile değiştir ve geçerli tarihe dönüştür
data['sale_date'] = pd.to_datetime(data['sale_date'], errors='coerce')
data['sale_date'].fillna(pd.to_datetime("2023-01-01"), inplace=True)

# 5. months_listed: Eksik değerleri ortalama ile değiştir, negatif değerleri düzelt ve bir ondalık basamağa yuvarla
mean_months_listed = round(data['months_listed'].mean(), 1)
data['months_listed'].fillna(mean_months_listed, inplace=True)
data['months_listed'] = data['months_listed'].apply(lambda x: max(0, round(x, 1)))
data['months_listed'] = data['months_listed'].astype('float64')

# 6. bedrooms: Eksik değerleri ortalama ile değiştir, negatif değerleri düzelt ve en yakın tam sayıya yuvarla
mean_bedrooms = round(data['bedrooms'].mean())
data['bedrooms'].fillna(mean_bedrooms, inplace=True)
data['bedrooms'] = data['bedrooms'].apply(lambda x: max(0, round(x)))
data['bedrooms'] = data['bedrooms'].astype('int64')

# 7. house_type: Eksik değerleri en yaygın ev tipi ile değiştir ve geçersiz değerleri düzelt
most_common_house_type = data['house_type'].mode()[0]
data['house_type'].fillna(most_common_house_type, inplace=True)
data['house_type'] = data['house_type'].str.replace('[^a-zA-Z\s]', '', regex=True) 
# house_type değerlerini temizle (fazladan boşlukları/noktaları kaldır)
data['house_type'] = data['house_type'].str.strip().str.replace('.', '')
# Geçersiz ev tiplerini en yaygın ev tipiyle değiştir
valid_house_types = ['Terraced', 'Semi-detached', 'Detached'] 
data.loc[~data['house_type'].isin(valid_house_types), 'house_type'] = most_common_house_type

# 8. area: Sayısal değeri ayıkla, eksik değerleri ortalama ile değiştir, negatif değerleri düzelt ve bir ondalık basamağa yuvarla
data['area'] = data['area'].str.extract(r'(\d+\.?\d*)').astype(float)
mean_area = round(data['area'].mean(), 1)
data['area'].fillna(mean_area, inplace=True)
data['area'] = data['area'].apply(lambda x: max(0, round(x, 1)))
data['area'] = data['area'].astype('float64')

# Temizlenmiş veri çerçevesini "clean_data" olarak kaydet
clean_data = data

# Temizlenmiş veri çerçevesinin özetini yazdır
print(clean_data.info())
print(clean_data.describe())

# Temizlenmiş veri çerçevesini CSV dosyasına kaydet
clean_data.to_csv("house_data_cleaned.csv", index=False)
