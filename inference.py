import streamlit as st
import pickle
import pandas as pd
import datetime

with open('best_rfr_model.pkl','rb') as file_1:
  model = pickle.load(file_1)

# pembuatan form

def run():
    with st.form(key='form_fifa_2022_rmt_057'):
        img = st.text_input('Url Image', value='--Url Image--')
        title = st.text_input('Judul Video Game', value='Judul Video Game')
        console = st.radio('Console', ('PS3','PS4','PS2','X360','XOne','PC','PSP','Wii','PS','DS','2600','GBA','NES','XB','PSN','GEN','PSV','DC','N64','SAT','SNES','GBC','GC','NS','3DS','GB','WiiU','WS','VC','NG','WW','SCD','PCE','XBL','3DO','GG','OSX','Mob','PCFX','Series','All','iOS','5200','And','DSiW','Lynx','Linux','MS','ZXS','ACPC','Amig','7800','DSi','AJ','WinP','iQue','GIZ','VB','Ouya','NGage','AST','MSD','S32X','XS','PS5','Int','CV', 'Arc', 'C64', 'FDS', 'MSX','OR', 'C128', 'CDi', 'CD32', 'BRW', 'FMT', 'ApII', 'Aco', 'BBCM', 'TG16'),index =1)
        genre = st.selectbox('Genre', ('Action','Shooter','Role-Playing','Sports','Platform','Racing','Adventure','Strategy','Misc','Fighting','Puzzle','Simulation','Action-Adventure','Music','Party','MMO','Visual Novel','Education','Sandbox','Board Game'), index=2)
        today = datetime.date.today()
        developer = st.text_input('Developer Game', value='Developer Game')
        publisher = st.text_input('Penerbit Game', value='Penerbit Game')
        na_sales= st.number_input('Prediksi penjualan di Amerika Utara', min_value= 0.0, value=0.0)
        jp_sales = st.number_input('Prediksi penjualan di Jepang', min_value= 0.0, value=0.0)
        pal_sales = st.number_input('Prediksi penjualan di Eropa dan Afrika', min_value= 0.0, value=0.0)
        other_sales = st.number_input('Prediksi penjualan di daerah lain', min_value= 0.0, value=0.0)
        release_date = st.date_input(label="Select a date",value=today,key="release_date")
        last_update = st.date_input(label="Select a date",value=release_date,max_value=release_date,key="last_update")

        total_sales = na_sales + jp_sales + pal_sales + other_sales

        data_inf1 = {
            'img': img,
            'title': title,
            'console': console,
            'genre': genre,
            'publisher': publisher,
            'developer': developer,
            'total_sales': total_sales,
            'na_sales': na_sales,
            'jp_sales': jp_sales,
            'pal_sales': pal_sales,
            'other_sales': other_sales,
            'release_date': release_date,
            'last_update': last_update
        }

        data_inf = pd.DataFrame([data_inf1])
        data_inf

        # Kurangi jumlah data unik di kolom developer

        data_inf.loc[((data_inf['developer'].str.contains('EA ', na=False)|data_inf['developer'].str.contains('Electronic Arts', na=False))&~data_inf['developer'].str.contains('SCEA', na=False)), 'developer'] = 'Electronic Arts'

        data_inf.loc[((data_inf['developer'].str.contains('Bandai', na=False)|data_inf['developer'].str.contains('Namco', na=False))), 'developer'] = 'Bandai Namco Games'

        data_inf.loc[data_inf['developer'].str.contains('Ubisoft', na=False), 'developer'] = 'Ubisoft'

        data_inf.loc[data_inf['developer'].str.contains('Rockstar', na=False), 'developer'] = 'Rockstar'

        data_inf.loc[data_inf['developer'].str.contains('Activision', na=False), 'developer'] = 'Activision'

        data_inf.loc[((data_inf['developer'].str.contains('Sony', na=False)|data_inf['developer'].str.contains('SCEA', na=False))|(data_inf['developer'].str.contains('SCEE', na=False))), 'developer'] = 'Sony'

        data_inf.loc[data_inf['developer'].str.contains('Sega', na=False), 'developer'] = 'Sega'

        data_inf.loc[data_inf['developer'].str.contains('Konami', na=False), 'developer'] = 'Konami'

        data_inf.loc[data_inf['developer'].str.contains('Microsoft', na=False), 'developer'] = 'Microsoft'

        data_inf.loc[data_inf['developer'].str.contains('Koei', na=False) | data_inf['developer'].str.contains('Tecmo', na=False), 'developer'] = 'Koei Tecmo Games'

        data_inf.loc[data_inf['developer'].str.contains('Capcom', na=False), 'developer'] = 'Capcom'

        data_inf.loc[data_inf['developer'].str.contains('Atari', na=False), 'developer'] = 'Atari'

        data_inf.loc[data_inf['developer'].str.contains('SNK', na=False), 'developer'] = 'SNK'

        data_inf.loc[data_inf['developer'].str.contains('Atlus', na=False), 'developer'] = 'Atlus'

        data_inf.loc[data_inf['developer'].str.contains('Marvelous', na=False), 'developer'] = 'Marvelous'

        data_inf.loc[data_inf['developer'].str.contains('Taito', na=False), 'developer'] = 'Taito'

        data_inf.loc[((data_inf['developer'].str.contains('Nippon Ichi', na=False)|data_inf['developer'].str.contains('Gust', na=False))&~(data_inf['developer'].str.contains('Gusto', na=False) | data_inf['developer'].str.contains('Gustav', na=False))), 'developer'] = 'Nippon Ichi / Gust'

        data_inf.loc[data_inf['developer'].str.contains('Square Enix', na=False), 'developer'] = 'Square Enix'

        data_inf.loc[data_inf['developer'].str.contains('Hudson', na=False), 'developer'] = 'Hudson'

        data_inf.loc[data_inf['developer'].str.contains('Nihon Falcom', na=False), 'developer'] = 'Nihon Falcom'

        data_inf.loc[data_inf['developer'].str.contains('THQ', na=False), 'developer'] = 'THQ'

        data_inf.loc[data_inf['developer'].str.contains('Idea Factory', na=False), 'developer'] = 'Idea Factory'

        data_inf.loc[~(
                        data_inf['developer'].str.contains('Electronic Arts', na=False)|
                        data_inf['developer'].str.contains('Bandai Namco Games', na=False)|
                        data_inf['developer'].str.contains('Ubisoft', na=False)|
                        data_inf['developer'].str.contains('Rockstar', na=False)|
                        data_inf['developer'].str.contains('Activision', na=False)|
                        data_inf['developer'].str.contains('Sony', na=False)|
                        data_inf['developer'].str.contains('Sega', na=False)|
                        data_inf['developer'].str.contains('Microsoft', na=False)|
                        data_inf['developer'].str.contains('Koei Tecmo Games', na=False)|
                        data_inf['developer'].str.contains('Capcom', na=False)|
                        data_inf['developer'].str.contains('Atari', na=False)|
                        data_inf['developer'].str.contains('SNK', na=False)|
                        data_inf['developer'].str.contains('Atlus', na=False)|
                        data_inf['developer'].str.contains('Marvelous', na=False)|
                        data_inf['developer'].str.contains('Taito', na=False)|
                        data_inf['developer'].str.contains('Nippon Ichi / Gust', na=False)|
                        data_inf['developer'].str.contains('Square Enix', na=False)|
                        data_inf['developer'].str.contains('Hudson', na=False)|
                        data_inf['developer'].str.contains('Nihon Falcom', na=False)|
                        data_inf['developer'].str.contains('THQ', na=False)|
                        data_inf['developer'].str.contains('Idea Factory', na=False)|
                        data_inf['developer'].str.contains('Unknown', na=False)
                )| data_inf['developer'].str.contains('Unknown Worlds Entertainment', na=False), 'developer'] = 'Others'

        data_inf.drop(['img', 'last_update','release_date', 'total_sales', 'publisher', 'title'], axis=1, inplace=True)
        submitted = st.form_submit_button('Predict')
    if submitted:
        predict = model.predict(data_inf)

        st.write('## Prediksi nilai kritik: ',str(float(predict)))
       
if __name__ == '__main__':
  run()