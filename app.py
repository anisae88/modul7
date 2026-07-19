from flask import Flask, render_template
import pandas as pd
import folium
import os

from kmeans import proses_kmeans

app = Flask(__name__)

# =====================================================
# HALAMAN UTAMA
# =====================================================
@app.route('/')
def index():
    return render_template('index.html')


# =====================================================
# PROSES CLUSTERING
# =====================================================
@app.route('/proses')
def proses():

    # menjalankan proses kmeans
    df = proses_kmeans()

    # =================================================
    # MEMBUAT PETA FOLIUM
    # =================================================
    
    # koordinat pusat map (Jawa Tengah)
    map_center = [-7.43, 109.24]

    # membuat map
    m = folium.Map(
        location=map_center,
        zoom_start=8,
        tiles='OpenStreetMap'
    )

    # warna tiap cluster
    warna_cluster = {
        0: 'green',
        1: 'orange',
        2: 'red'
    }

    # =================================================
    # MENAMBAHKAN MARKER
    # =================================================
    for index, row in df.iterrows():

        # popup informasi
        popup_text = f"""
        <div style="width:200px;">
            <h5>{row['lokasi']}</h5>

            <hr>

            <b>PM2.5 :</b> {row['pm25']}<br>
            <b>CO :</b> {row['co']}<br>
            <b>Suhu :</b> {row['suhu']} °C<br>
            <b>Kelembapan :</b> {row['kelembapan']} %<br>

            <hr>

            <b>Kategori :</b> {row['kategori']}
        </div>
        """

        # menentukan warna marker
        warna = warna_cluster[row['cluster']]

        # membuat marker
        folium.Marker(
            location=[
                row['latitude'],
                row['longitude']
            ],

            popup=folium.Popup(
                popup_text,
                max_width=300
            ),

            tooltip=row['lokasi'],

            icon=folium.Icon(
                color=warna,
                icon='cloud'
            )

        ).add_to(m)

    # =================================================
    # MEMBUAT CIRCLE MARKER
    # =================================================
    for index, row in df.iterrows():

        if row['cluster'] == 0:
            color = 'green'

        elif row['cluster'] == 1:
            color = 'orange'

        else:
            color = 'red'

        folium.CircleMarker(

            location=[
                row['latitude'],
                row['longitude']
            ],

            radius=row['pm25'] / 10,

            color=color,

            fill=True,

            fill_color=color,

            fill_opacity=0.4,

            popup=f"""
            Lokasi: {row['lokasi']}<br>
            PM2.5: {row['pm25']}<br>
            Status: {row['kategori']}
            """

        ).add_to(m)

    # =================================================
    # MENYIMPAN PETA
    # =================================================

    # membuat folder templates jika belum ada
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # simpan map
    m.save('templates/map.html')

    # =================================================
    # MEMBUAT TABEL HTML
    # =================================================
    tabel = df.to_html(

        classes="""
        table
        table-bordered
        table-striped
        table-hover
        """,

        index=False

    )

    # =================================================
    # HITUNG STATISTIK CLUSTER
    # =================================================
    jumlah_cluster = df['kategori'].value_counts().to_dict()

    udara_baik = jumlah_cluster.get('Udara Baik', 0)
    udara_sedang = jumlah_cluster.get('Udara Sedang', 0)
    udara_buruk = jumlah_cluster.get('Udara Buruk', 0)

    total_data = len(df)

    # =================================================
    # KIRIM KE HALAMAN HASIL
    # =================================================
    return render_template(

        'hasil.html',

        tabel=tabel,

        total_data=total_data,

        udara_baik=udara_baik,

        udara_sedang=udara_sedang,

        udara_buruk=udara_buruk

    )


# =====================================================
# HALAMAN PETA
# =====================================================
@app.route('/map.html')
def map_view():
    return render_template('map.html')


# =====================================================
# MAIN PROGRAM
# =====================================================
if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
