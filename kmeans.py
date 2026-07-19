import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os


# =====================================================
# FUNGSI PROSES K-MEANS
# =====================================================
def proses_kmeans():

    # ==============================================
    # MEMBACA DATASET
    # ==============================================
    file_csv = "data_kualitas_udara.csv"

    # cek file tersedia
    if not os.path.exists(file_csv):
        raise FileNotFoundError(
            "File data_kualitas_udara.csv tidak ditemukan!"
        )

    # membaca csv
    df = pd.read_csv(file_csv)

    # ==============================================
    # MENAMPILKAN DATA AWAL
    # ==============================================
    print("\nDATASET AWAL")
    print(df.head())

    # ==============================================
    # MEMILIH FITUR
    # ==============================================
    fitur = [
        'pm25',
        'co',
        'suhu',
        'kelembapan'
    ]

    X = df[fitur]

    # ==============================================
    # NORMALISASI DATA
    # ==============================================
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # ==============================================
    # MEMBUAT MODEL K-MEANS
    # ==============================================
    model = KMeans(

        n_clusters=3,

        init='k-means++',

        max_iter=300,

        n_init=10,

        random_state=42

    )

    # ==============================================
    # PROSES TRAINING
    # ==============================================
    model.fit(X_scaled)

    # ==============================================
    # HASIL CLUSTER
    # ==============================================
    cluster = model.predict(X_scaled)

    # simpan cluster ke dataframe
    df['cluster'] = cluster

    # ==============================================
    # MENENTUKAN LABEL KATEGORI
    # ==============================================
    kategori_cluster = {}

    # centroid
    centroid = model.cluster_centers_

    # mencari rata-rata pm25 tiap cluster
    rata_pm25 = {}

    for i in range(3):

        rata = df[df['cluster'] == i]['pm25'].mean()

        rata_pm25[i] = rata

    # urutkan cluster berdasarkan pm25
    urut_cluster = sorted(
        rata_pm25,
        key=rata_pm25.get
    )

    # cluster pm25 kecil = udara baik
    kategori_cluster[urut_cluster[0]] = 'Udara Baik'

    # cluster tengah
    kategori_cluster[urut_cluster[1]] = 'Udara Sedang'

    # cluster terbesar
    kategori_cluster[urut_cluster[2]] = 'Udara Buruk'

    # mapping kategori
    df['kategori'] = df['cluster'].map(
        kategori_cluster
    )

    # ==============================================
    # MENAMPILKAN HASIL
    # ==============================================
    print("\nHASIL CLUSTERING")
    print(df.head())

    # ==============================================
    # MENAMPILKAN CENTROID
    # ==============================================
    print("\nCENTROID")
    print(model.cluster_centers_)

    # ==============================================
    # MEMBUAT FOLDER HASIL
    # ==============================================
    if not os.path.exists('hasil'):
        os.makedirs('hasil')

    # ==============================================
    # MENYIMPAN HASIL CSV
    # ==============================================
    output_csv = 'hasil/hasil_cluster.csv'

    df.to_csv(
        output_csv,
        index=False
    )

    print(f"\nHasil clustering disimpan ke: {output_csv}")

    # ==============================================
    # RETURN DATAFRAME
    # ==============================================
    return df


# =====================================================
# MENJALANKAN FILE LANGSUNG
# =====================================================
if __name__ == '__main__':

    hasil = proses_kmeans()

    print("\nPROGRAM SELESAI")
