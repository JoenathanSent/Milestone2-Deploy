import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import plotly.express as px
import numpy as np

def run():
    # Membuat title 
    st.title('Aplikasi Prediksi Rating Kritik Video Game')

    # Membuat sub header
    st.subheader('Page ini berisi Exploratory Data Analysis (EDA) mengenai dataset Laporan Penjualan Video Game dan Rating Kritiknya')

    # Menampilkan teks
    st.write('Proyek ini dibuat untuk melakukan prediksi rating video game menggunakan model berbasis regularisasi. Algoritma machine learning yang akan digunakan adalah algoritma `Linear Regression`, `KNeighborRegressor`, `Support Vector Machine`, `Decision Tree`, dan `Random Forest`, yang kemudian akan dievaluasi dengan metode `Mean Absolute Error` (MAE) dan `R2 Score`. Harapannya dataset ini dapat berguna bagi perusahaan bidang hiburan berjenis *video game*.')
    st.write('Metrik evaluasi yang akan digunakan adalah RMSE (Root Mean Squared Evaluation) karena metode evaluasi ini lebih akurat saat terdapat outlier di data. Dataset yang digunakan adalah penjualan video game dimulai dari tahun 1971 sampai tahun 2024 dari website `vgchartz.com`. Model akan dibandingkan performanya dengan `cross validation` dan akan dilakukan `Hyperparameter Tuning` untuk menemukan parameter terbaik untuk tiap algoritma model')
    # Menampilkan gambar
    data = mpimage.imread('jeshoots-com-eCktzGjC-iU-unsplash-scaled.jpg')
    st.image(data, caption='EDA Kritik Video Game')

    st.write('# Import Library')
    # library untuk melakukan perhitungan statistik
    import numpy as np
    # library untuk menampilkan gambar grafik
    import matplotlib.pyplot as plt
    import seaborn as sns
    import statsmodels.api as sm
    # library untuk membaca csv dan fungsi pandas lainnya
    import pandas as pd
    # import library untuk perhitungan statistik
    from scipy import stats
    # library untuk memisahkan data untuk train-set dan test-set
    from sklearn.model_selection import train_test_split
    # library untuk feature scaling
    from sklearn.preprocessing import MinMaxScaler
    # library untuk feature encoding
    from sklearn.preprocessing import OneHotEncoder
    # library untuk latih model menggunakan Linear Regression, KNN, SVC, Decision Tree, Random Forest, dan Boosting. Karena target data berupa numerik, maka jenis algoritma yang akan digunakan adalah jenis regressor
    from sklearn.linear_model import LinearRegression
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.svm import SVR
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import AdaBoostRegressor
    # Library untuk evaluasi asumsi linear Regression
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.stats.stattools import durbin_watson
    # library untuk evaluasi model dengan metrik MAE
    from sklearn.metrics import mean_absolute_error, r2_score
    # library untuk memisahkan kolom kategori dan numerik untuk proses pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    # library untuk mencari model terbaik dan untuk hyperparameter tuning dengan target data numerik
    from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
    # import library untuk menyimpan model
    import pickle
    # library untuk menyembunyikan warning
    import warnings
    warnings.filterwarnings("ignore")

    st.write('# Data Loading')
    df = pd.read_csv('vgchartz-2024.csv')
    st.write('Tampilan dataframe')
    st.dataframe(df)
    st.write('# Exploratory Data Analysis')
    st.subheader('1. Meneliti apabila `na_sales`, `jp_sales`, `pal_sales`, dan `other_sales` mempengaruhi `critic_score`')
    st.write('Pertama, saya akan melakukan imputasi terhadap data kosong (*missing value*) di dataset supaya perhitungan korelasi bisa berjalan. ')
    st.write('Daftar kolom yang memiliki missing value:')
    st.write(df.columns[df.isna().any()])
    st.write('Jenis missing value untuk tiap kolom adalah:')
    st.write('- developer: Jenis missing value adalah MCAR karena tidak mungkin sebuah video game dibuat tanpa developer. Artinya informasi asli developer lupa diisi atau terlewat oleh pembuat dataset')
    st.write('- critic_score: Jenis missing value adalah MCAR karena mungkin saja memang tidak ada yang melakukan kritik terdapat video game tersebut')
    st.write('- total_sales: Jenis missing value adalah MNAR karena pasti ada yang membeli video game tersebut. Namun data di kolom ini bergantung dari jumlah penjualan dari kolom `na_sales`, `jp_sales`, `pal_sales`, dan `other_sales` jadi missing data disebabkan karena ketidak adaannya data dari setidaknya 1 dari 4 kolom tersebut.')
    st.write('- na_sales: Jenis missing value adalah MNAR karena mungkin saja memang video game-nya tidak dijual di daerah tersebut')
    st.write('- jp_sales: Sama seperti jenis missing value untuk kolom `na_sales`, jenis missing value adalah MNAR karena mungkin saja memang video game-nya tidak dijual di daerah tersebut')
    st.write('- pal_sales: Sama seperti jenis missing value untuk kolom `na_sales`, jenis missing value adalah MNAR karena mungkin saja memang video game-nya tidak dijual di daerah tersebut')
    st.write('- other_sales: Sama seperti jenis missing value untuk kolom `na_sales`, jenis missing value adalah MNAR karena mungkin saja memang video game-nya tidak dijual di daerah tersebut')
    st.write('- release_date: Jenis missing value adalah MCAR karena ada kemungkinan besar pembuat dataset lupa mengisi data untuk kolom ini atau tidak ada yang melakukan dokumentasi terhadap tanggal rilis video game tersebut atau dokumentasi video game tersebut memang sudah hilang.')
    st.write('- last_update: Jenis missing value adalah MNAR karena mungkin memang tidak ada update untuk data tersebut, jadi data untuk `last_update` bisa diisi dengan tanggal `release_date`')
    st.write('')
    st.write('Jadi untuk melakukan imputasi data, untuk data MCAR dan MAR bisa dilakukan dengan imputasi manual atau menghitung rata-rata, median, modus, atau imputasi 0 atau 1. Caranya akan ditentukan tergantung dari nilai skewness)')
    st.write('nilai skew pada kolom na_sales:',df['na_sales'].skew())
    st.write('nilai skew pada kolom jp_sales:',df['jp_sales'].skew())
    st.write('nilai skew pada kolom pal_sales:',df['pal_sales'].skew())
    st.write('nilai skew pada kolom other_sales:',df['other_sales'].skew())
    st.write('nilai skew pada kolom critic_score:',df['critic_score'].skew())
    st.write('Diketahui nilai *skew* pada kolom `na_sales`, `jp_sales`, `pal_sales`, dan `other_sales` condong ke kanan (lebih tinggi dari nilai rata-rata) dan nilainya ekstrim (lebih dari 1). Karena jenis missing value adalah MNAR, maka teknik imputasi adalah dengan memasukkan imputasi angka 0. Sedangkan untuk nilai *skew* pada kolom `critic_score` condong ke kiri (lebih rendah dari nilai rata-rata) dan nilainya sedang (lebih besar dari -1, tapi lebih kecil dari -0,5)')
    st.write('Diketahui nilai *skew* pada kolom `total_sales` condong ke kanan (lebih tinggi dari nilai rata-rata) dan nilainya ekstrim (lebih dari 1). Sedangkan untuk nilai *skew* pada kolom `critic_score` condong ke kiri (lebih rendah dari nilai rata-rata) dan nilainya sedang (lebih besar dari -1, tapi lebih kecil dari -0,5).')
    st.write('Untuk korelasi antara 2 kolom dengan tipe data yang sama-sama numerik dan diketahui terdapat *skew*, maka metode korelasi yang akan digunakan adalah metode spearman. Hasil dari perhitungan korelasi tersebut adalah sebagai berikut')
    temp_df = df.copy()
    temp_df['na_sales'] = temp_df['na_sales'].fillna(0)
    temp_df['jp_sales'] = temp_df['jp_sales'].fillna(0)
    temp_df['pal_sales'] = temp_df['pal_sales'].fillna(0)
    temp_df['other_sales'] = temp_df['other_sales'].fillna(0)
    temp_df['critic_score'] = temp_df['critic_score'].fillna(temp_df['critic_score'].median())
    st.write('')
    corr_rho, pval_s = stats.spearmanr(temp_df['na_sales'], temp_df['critic_score'])
    st.write(f"nilai korelasi kolom 'na_sales' dengan kolom 'critic_score': {corr_rho:.2f}, p-value: {pval_s}")
    corr_rho, pval_s = stats.spearmanr(temp_df['jp_sales'], temp_df['critic_score'])
    st.write(f"nilai korelasi kolom 'jp_sales' dengan kolom 'critic_score': {corr_rho:.2f}, p-value: {pval_s}")
    corr_rho, pval_s = stats.spearmanr(temp_df['pal_sales'], temp_df['critic_score'])
    st.write(f"nilai korelasi kolom 'pal_sales' dengan kolom 'critic_score': {corr_rho:.2f}, p-value: {pval_s}")
    corr_rho, pval_s = stats.spearmanr(temp_df['other_sales'], temp_df['critic_score'])
    st.write(f"nilai korelasi kolom 'other_sales' dengan kolom 'critic_score': {corr_rho:.2f}, p-value: {pval_s}")
    st.write('')
    st.write('Dari hasil diatas, diketahui bahwa nilai penjualan di tiap daerah tidak memiliki korelasi kuat dengan kolom `critic_score` karena nilai korelasinya dibawah 0.3. Kecuali untuk kolom `other_sales` tidak bisa dibuktikan apabila korelasinya nyata karena nilai p-value untuk korelasi `other_sales` dengan `critic_score` bernilai diatas 0.05')
    st.subheader('2. Meneliti apabila game di konsol PC umumnya memiliki rating lebih baik daripada game di konsol lainnya')
    st.write('Untuk meneliti ini, saya akan menggunakan teknik pengujian hipotesa `Two Sample Test` dengan hipotesa berikut:')
    st.write('- H0 (Hipotesa Null): Rata-rata `critic_score` untuk game di konsol PC > Rata-rata `critic_score` untuk game di konsol lainnya')
    st.write('- H1 (Hipotesa Alternatif): Rata-rata `critic_score` untuk game di konsol PC <= Rata-rata `critic_score` untuk game di konsol lainnya')
    df_pc_critic_score = temp_df[(temp_df['console'] == 'PC')].reset_index(drop=True)
    df_other_critic_score = temp_df[(temp_df['console'] != 'PC')].reset_index(drop=True)
    # perhitungan hipotesa
    t_stat, p_val = stats.ttest_ind(
        df_pc_critic_score['critic_score'],
        df_other_critic_score['critic_score'],
        alternative="less",
    )

    st.write("T-Statistic:", t_stat)
    st.write("P-value:", p_val)  
    st.write('Nilai T-Statistic yang positif menunjukkan bahwa ada benarnya nilai `critic_score` untuk konsol PC lebih besar daripada `critic_score` untuk konsol lainnya. Tapi, nilai P-value menunjukkan bahwa data yang didapatkan hanya kebetulan (bukti tidak cukup kuat) karena nilainya lebih dari 0.05, sehingga dari hasil ini hipotesa null (H0) yang berbunyi `Rata-rata critic_score untuk game di konsol PC lebih besar dari Rata-rata critic_score untuk game di konsol lainnya` **gagal ditolak**')

if __name__ == '__main__':
    run()