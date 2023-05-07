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
    options=["Parlimen", "DUN"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

@st.cache_data(persist=True)
def load_data_parlimen():
    df = pd.read_csv('./data/pru15_result_parlimen.csv')
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

def load_data_dun():
    df = pd.read_csv('./data/prn-2018.csv')
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

df_parlimen = load_data_parlimen()
df_dun = load_data_dun()

st.title(f"MY Election APP")

if selected == "Parlimen":
    
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

    if show_filtered:
        st.dataframe(df_parlimen[
            df_parlimen['seat_name'].isin(parlimen_name_choice) &
            df_parlimen['state'].isin(state_choice) &
            df_parlimen['coalition'].isin(parti_name_choice)
        ].sort_values('seat_id', ascending=True).reset_index(drop=True))
    else:
        st.dataframe(df_parlimen.sort_values('seat_id', ascending=True).reset_index(drop=True))

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



if selected == "DUN":
    
    st.markdown('### Keputusan PRN 14')
    dun_state = list(df_dun['NEGERI'].drop_duplicates())
    dun_state_choice = st.sidebar.multiselect(
        "Negeri:", dun_state, default=dun_state)

    dun_name = list(df_dun[df_dun['NEGERI'].isin(dun_state_choice)]['NAMA DUN'].drop_duplicates())
    dun_name_choice = st.sidebar.multiselect(
        'Nama DUN:', dun_name)

    dun_parti_name = list(df_dun[df_dun['NAMA DUN'].isin(dun_name_choice)]['PARTI'].drop_duplicates())
    dun_parti_name_choice = st.sidebar.multiselect(
        'Nama Parti:', dun_parti_name, default=dun_parti_name)

    show_filtered = st.sidebar.checkbox("Show filtered data", value=False)

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
