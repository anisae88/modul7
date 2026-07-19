import pandas as pd
import random

# daftar lokasi dummy
lokasi = [
    "Purwokerto",
    "Cilacap",
    "Banyumas",
    "Purbalingga",
    "Banjarnegara",
    "Kebumen",
    "Tegal",
    "Pemalang",
    "Brebes",
    "Slawi",
    "Wonosobo",
    "Magelang",
    "Semarang",
    "Solo",
    "Yogyakarta"
]

# koordinat dummy
latitudes = [
    -7.43, -7.72, -7.51, -7.39, -7.37,
    -7.67, -6.87, -6.89, -6.87, -6.98,
    -7.36, -7.47, -6.99, -7.56, -7.80
]

longitudes = [
    109.24, 109.01, 109.29, 109.36, 109.68,
    109.65, 109.14, 109.38, 109.04, 109.13,
    109.90, 110.22, 110.42, 110.82, 110.36
]

data = []

# generate data dummy
for i in range(len(lokasi)):
    
    pm25 = random.randint(10, 150)
    co = round(random.uniform(0.5, 8.0), 2)
    suhu = random.randint(24, 37)
    kelembapan = random.randint(60, 95)

    data.append({
        "lokasi": lokasi[i],
        "latitude": latitudes[i],
        "longitude": longitudes[i],
        "pm25": pm25,
        "co": co,
        "suhu": suhu,
        "kelembapan": kelembapan
    })

# membuat dataframe
df = pd.DataFrame(data)

# simpan ke csv
df.to_csv("data_kualitas_udara.csv", index=False)

print("Dataset berhasil dibuat!")
print(df)
