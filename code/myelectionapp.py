import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["PRU15-PARLIMEN", "PRN14-DUN", "AHLI PARLIMEN", "PRU-HistoricalData", "PRN-HistoricalData"],
    icons=["bi-bank", "bi-house", "bar-chart-fill", "bi-clock-history", "bi-clock-history"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

@st.cache_data(persist=True)
def load_data_parlimen():
    df = pd.read_csv('/Users/mannitor/Documents/VScode/pru15_result_parlimen.csv')
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

def load_data_dun():
    df = pd.read_csv('/Users/mannitor/Documents/VScode/prn-2018.csv')
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

def load_data_ahli_parlimen():
    df = pd.read_csv('/Users/mannitor/Documents/VScode/Ahli_Parlimen_15.csv')
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

def load_data_parlimen_history():
    df = pd.read_csv('/Users/mannitor/Documents/VScode/parlimen_historical_data.csv')
    #df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

def load_data_dun_history():
    df = pd.read_csv('/Users/mannitor/Documents/VScode/dun_historical_data.csv')
    #df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

df_parlimen = load_data_parlimen()
df_dun = load_data_dun()
df_ahli = load_data_ahli_parlimen()
df_parlimen_hist = load_data_parlimen_history()
df_dun_hist = load_data_dun_history()


st.title(f"My Politiko")

if selected == "PRU15-PARLIMEN":
    
    st.markdown('### Keputusan PRU 15')
    state = list(df_parlimen['state'].drop_duplicates())
    state_choice = st.sidebar.multiselect(
        "Negeri:", state, default=state)

    parlimen_name = list(df_parlimen[df_parlimen['state'].isin(state_choice)]['seat_name'].drop_duplicates())
    parlimen_name_choice = st.sidebar.multiselect(
        'Nama Parlimen:', parlimen_name, default=parlimen_name)

    parti_name = list(df_parlimen[df_parlimen['seat_name'].isin(parlimen_name_choice)]['coalition'].drop_duplicates())
    parti_name_choice = st.sidebar.multiselect(
        'Nama Parti/Gabungan:', parti_name, default=parti_name)

    show_filtered = st.sidebar.checkbox("Show filtered data", value=True)

    # Calculate total wins by state and abbreviation
    count_wins = df_parlimen[df_parlimen['status'] == 'win'].pivot_table(index='state', columns='abbreviation', values='status', aggfunc='count', fill_value=0)

    # Calculate total wins for each abbreviation across all states
    total_wins = count_wins.sum().astype(int)

    # Add a row for total wins for all states for each abbreviation
    total_win = count_wins._append(total_wins.rename('TOTAL'))

    if show_filtered:
        st.dataframe(df_parlimen[
            df_parlimen['seat_name'].isin(parlimen_name_choice) &
            df_parlimen['state'].isin(state_choice) &
            df_parlimen['coalition'].isin(parti_name_choice)
        ].sort_values('seat_id', ascending=True).reset_index(drop=True))
    else:
        st.dataframe(df_parlimen.sort_values('seat_id', ascending=True).reset_index(drop=True))
    
    st.markdown('### Keputusan Setiap Negeri')
    st.dataframe(total_win, use_container_width=True)

    df_parlimen_filtered = df_parlimen[
        df_parlimen['seat_name'].isin(parlimen_name_choice) &
        df_parlimen['state'].isin(state_choice) &
        df_parlimen['coalition'].isin(parti_name_choice)
    ]

    

    d = alt.Chart(df_parlimen_filtered).mark_bar().encode(
        x=alt.X('candidate', sort=alt.EncodingSortField('-vote')),
        y=alt.Y('vote'),
        color=alt.Color('abbreviation'),
        tooltip=['candidate','vote','total_votes','type', 'majority']
    ).interactive()

    st.altair_chart(d, use_container_width=True, theme="streamlit")



if selected == "PRN14-DUN":
    
    st.markdown('### Keputusan PRN 14')
    dun_state = list(df_dun['NEGERI'].drop_duplicates())
    dun_state_choice = st.sidebar.multiselect(
        "Negeri:", dun_state, default=dun_state)

    dun_name = list(df_dun[df_dun['NEGERI'].isin(dun_state_choice)]['NAMA DUN'].drop_duplicates())
    dun_name_choice = st.sidebar.multiselect(
        'Nama DUN:', dun_name, default=dun_name)

    dun_parti_name = list(df_dun[df_dun['NAMA DUN'].isin(dun_name_choice)]['PARTI'].drop_duplicates())
    dun_parti_name_choice = st.sidebar.multiselect(
        'Nama Parti:', dun_parti_name, default=dun_parti_name)

    show_filtered = st.sidebar.checkbox("Show filtered data", value=True)

    if show_filtered:
        st.dataframe(df_dun[
            df_dun['NAMA DUN'].isin(dun_name_choice) &
            df_dun['NEGERI'].isin(dun_state_choice) &
            df_dun['PARTI'].isin(dun_parti_name_choice)
        ].sort_values('NEGERI', ascending=True).reset_index(drop=True))
    else:
        st.dataframe(df_dun.sort_values('NEGERI', ascending=True).reset_index(drop=True))

    df_dun_filtered = df_dun[
        df_dun['NAMA DUN'].isin(dun_name_choice) &
        df_dun['NEGERI'].isin(dun_state_choice) &
        df_dun['PARTI'].isin(dun_parti_name_choice)
    ]

    st.markdown('### Keputusan PRN 14')

    e = alt.Chart(df_dun_filtered).mark_bar().encode(
        x=alt.X('NAMA CALON', sort=alt.EncodingSortField('-BILANGAN UNDI')),
        y=alt.Y('BILANGAN UNDI'),
        color=alt.Color('PARTI'),
        tooltip=['BILANGAN UNDI','JUMLAH UNDI','STATUS']
    ).interactive()

    st.altair_chart(e, use_container_width=True, theme="streamlit")

if selected == "AHLI PARLIMEN":
    
    st.markdown('### Data Ahli Parlimen')
    ahli_state = list(df_ahli['Negeri'].drop_duplicates())
    ahli_state_choice = st.sidebar.multiselect(
         "Negeri:", ahli_state, default=ahli_state)

    ahli_parlimen_place = list(df_ahli[df_ahli['Negeri'].isin(ahli_state_choice)]['Kawasan Parlimen'].drop_duplicates())
    ahli_parlimen_place_choice = st.sidebar.multiselect(
         'Kawasan Parlimen:', ahli_parlimen_place, default=ahli_parlimen_place)

    ahli_parti_name = list(df_ahli[df_ahli['Kawasan Parlimen'].isin(ahli_parlimen_place_choice)]['Parti'].drop_duplicates())
    ahli_parti_name_choice = st.sidebar.multiselect(
         'Nama Parti:', ahli_parti_name, default=ahli_parti_name)

    show_filtered = st.sidebar.checkbox("Show filtered data", value=True)

    if show_filtered:
        st.dataframe(df_ahli[
            df_ahli['Kawasan Parlimen'].isin(ahli_parlimen_place_choice) &
            df_ahli['Negeri'].isin(ahli_state_choice) &
            df_ahli['Parti'].isin(ahli_parti_name_choice)
    ].sort_values('Negeri', ascending=True).reset_index(drop=True))
    else:
        st.dataframe(df_ahli.sort_values('Negeri', ascending=True).reset_index(drop=True))

    df_ahli_filtered = df_ahli[
        df_ahli['Kawasan Parlimen'].isin(ahli_parlimen_place_choice) &
        df_ahli['Negeri'].isin(ahli_state_choice) &
        df_ahli['Parti'].isin(ahli_parti_name_choice)
    ]

    st.markdown('### Keputusan PRN 14')

    
    # text_nama = df_ahli_filtered['Yang Berhormat'].tolist()[0]
    # text_jawatan = df_ahli_filtered['Jawatan'].tolist()[0]
    # text_adun = df_ahli_filtered['ADUN'].tolist()[0]
    # st.markdown(f"<p style='font-size:24px; font-family: Arial'>{text_nama}</p>", unsafe_allow_html=True)
    # st.markdown(f"<p style='font-size:24px; font-family: Arial'>{text_jawatan}</p>", unsafe_allow_html=True)
    # st.markdown(f"<p style='font-size:24px; font-family: Arial'>{text_adun}</p>", unsafe_allow_html=True)

    
    # f = alt.Chart(df_ahli_filtered).mark_bar().encode(
    #     x=alt.X('NAMA CALON', sort=alt.EncodingSortField('-BILANGAN UNDI')),
    #     y=alt.Y('BILANGAN UNDI'),
    #     color=alt.Color('PARTI'),
    #     tooltip=['BILANGAN UNDI','JUMLAH UNDI','STATUS']
    # ).interactive()

    # st.altair_chart(f, use_container_width=True, theme="streamlit")

if selected == "PRU-HistoricalData":
    
    st.markdown('### Keputusan PRU 2004-2018')
    parlimen_hist_year = list(df_parlimen_hist['Tahun'].drop_duplicates())
    parlimen_hist_year_choice = st.sidebar.multiselect(
        "Tahun:", parlimen_hist_year, default=parlimen_hist_year)

    parlimen_hist_state = list(df_parlimen_hist[df_parlimen_hist['Tahun'].isin(parlimen_hist_year_choice)]['Negeri'].drop_duplicates())
    parlimen_hist_state_choice = st.sidebar.multiselect(
        "Negeri:", parlimen_hist_state, default=parlimen_hist_state)

    parlimen_hist_name = list(df_parlimen_hist[df_parlimen_hist['Negeri'].isin(parlimen_hist_state_choice)]['Kawasan Parlimen'].drop_duplicates())
    parlimen_hist_name_choice = st.sidebar.multiselect(
        'Nama Parlimen:', parlimen_hist_name, default=parlimen_hist_name)

    parlimen_hist_parti_name = list(df_parlimen_hist[df_parlimen_hist['Kawasan Parlimen'].isin(parlimen_hist_name_choice)]['Parti'].drop_duplicates())
    parlimen_hist_parti_name_choice = st.sidebar.multiselect(
        'Nama Parti:', parlimen_hist_parti_name, default=parlimen_hist_parti_name)

    show_filtered = st.sidebar.checkbox("Show filtered data", value=True)

    # # Calculate total wins by state and abbreviation
    # count_wins = df_parlimen[df_parlimen['status'] == 'win'].pivot_table(index='state', columns='abbreviation', values='status', aggfunc='count', fill_value=0)

    # # Calculate total wins for each abbreviation across all states
    # total_wins = count_wins.sum().astype(int)

    # # Add a row for total wins for all states for each abbreviation
    # total_win = count_wins._append(total_wins.rename('TOTAL'))

    if show_filtered:
        st.dataframe(df_parlimen_hist[
            df_parlimen_hist['Tahun'].isin(parlimen_hist_year_choice) &
            df_parlimen_hist['Kawasan Parlimen'].isin(parlimen_hist_name_choice) &
            df_parlimen_hist['Negeri'].isin(parlimen_hist_state_choice) &
            df_parlimen_hist['Parti'].isin(parlimen_hist_parti_name_choice)
        ].sort_values('Kawasan Parlimen', ascending=True).reset_index(drop=True))
    else:
        st.dataframe(df_parlimen_hist.sort_values('Kawasan Parlimen', ascending=True).reset_index(drop=True))
    
    #st.markdown('### Keputusan Setiap Negeri')
    #st.dataframe(total_win, use_container_width=True)

    df_parlimen_hist_filtered = df_parlimen_hist[
        df_parlimen_hist['Tahun'].isin(parlimen_hist_year_choice) &
        df_parlimen_hist['Kawasan Parlimen'].isin(parlimen_hist_name_choice) &
        df_parlimen_hist['Negeri'].isin(parlimen_hist_state_choice) &
        df_parlimen_hist['Parti'].isin(parlimen_hist_parti_name_choice)
    ]

    

    f = alt.Chart(df_parlimen_hist_filtered).mark_bar().encode(
        x=alt.X('Nama Calon', sort=alt.EncodingSortField('')),
        y=alt.Y('Undi'),
        color=alt.Color('Parti'),
        tooltip=['Nama Calon','Undi','Jumlah Undi','Keputusan', 'Majoriti', 'Tahun']
    ).interactive()

    st.altair_chart(f, use_container_width=True, theme="streamlit")

if selected == "PRN-HistoricalData":
    
    st.markdown('### Keputusan PRN 2004-2018')
    dun_hist_year = list(df_dun_hist['Tahun'].drop_duplicates())
    dun_hist_year_choice = st.sidebar.multiselect(
        "Tahun:", dun_hist_year, default=dun_hist_year)

    dun_hist_state = list(df_dun_hist[df_dun_hist['Tahun'].isin(dun_hist_year_choice)]['Negeri'].drop_duplicates())
    dun_hist_state_choice = st.sidebar.multiselect(
        "Negeri:", dun_hist_state, default=dun_hist_state)

    dun_hist_name = list(df_dun_hist[df_dun_hist['Negeri'].isin(dun_hist_state_choice)]['Kawasan DUN'].drop_duplicates())
    dun_hist_name_choice = st.sidebar.multiselect(
        'Nama DUN:', dun_hist_name, default=dun_hist_name)

    dun_hist_parti_name = list(df_dun_hist[df_dun_hist['Kawasan DUN'].isin(dun_hist_name_choice)]['Parti'].drop_duplicates())
    dun_hist_parti_name_choice = st.sidebar.multiselect(
        'Nama Parti:', dun_hist_parti_name, default=dun_hist_parti_name)

    show_filtered = st.sidebar.checkbox("Show filtered data", value=True)

    # # Calculate total wins by state and abbreviation
    # count_wins = df_parlimen[df_parlimen['status'] == 'win'].pivot_table(index='state', columns='abbreviation', values='status', aggfunc='count', fill_value=0)

    # # Calculate total wins for each abbreviation across all states
    # total_wins = count_wins.sum().astype(int)

    # # Add a row for total wins for all states for each abbreviation
    # total_win = count_wins._append(total_wins.rename('TOTAL'))

    if show_filtered:
        st.dataframe(df_dun_hist[
            df_dun_hist['Tahun'].isin(dun_hist_year_choice) &
            df_dun_hist['Kawasan DUN'].isin(dun_hist_name_choice) &
            df_dun_hist['Negeri'].isin(dun_hist_state_choice) &
            df_dun_hist['Parti'].isin(dun_hist_parti_name_choice)
        ].sort_values('Kawasan DUN', ascending=True).reset_index(drop=True))
    else:
        st.dataframe(df_dun_hist.sort_values('Kawasan DUN', ascending=True).reset_index(drop=True))
    
    #st.markdown('### Keputusan Setiap Negeri')
    #st.dataframe(total_win, use_container_width=True)

    df_dun_hist_filtered = df_dun_hist[
        df_dun_hist['Tahun'].isin(dun_hist_year_choice) &
        df_dun_hist['Kawasan DUN'].isin(dun_hist_name_choice) &
        df_dun_hist['Negeri'].isin(dun_hist_state_choice) &
        df_dun_hist['Parti'].isin(dun_hist_parti_name_choice)
    ]

    

    g = alt.Chart(df_dun_hist_filtered).mark_bar().encode(
        x=alt.X('Nama Calon', sort=alt.EncodingSortField('')),
        y=alt.Y('Undi'),
        color=alt.Color('Parti'),
        tooltip=['Nama Calon','Undi','Jumlah Undi','Keputusan', 'Majoriti', 'Tahun', 'Kod Parlimen']
    ).interactive()

    st.altair_chart(g, use_container_width=True, theme="streamlit")


    


