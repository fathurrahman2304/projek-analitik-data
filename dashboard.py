import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# from babel.numbers import format_currency
# sns.set(style='dark')

def create_rent_df(df):
    daily_orders_df = df.resample(rule='D', on='Date').agg({
        "total_rent": "sum"
    })    
    return daily_orders_df

def create_bycasual_df(df):
    # data_pertahun_casual = df.groupby(by='Year')['casual'].sum().sort_values(ascending=False).reset_index()
    data_pertahun_casual = df.groupby(by=['Season','Year'])['casual'].sum().sort_values(ascending=False).reset_index()
    return data_pertahun_casual
def create_byregist_df(df):
    data_pertahun_registered = df.groupby(by=['Season','Year'])['registered'].sum().sort_values(ascending=False).reset_index()
    return data_pertahun_registered
def barplot(df,kolom):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=kolom, y='Season', hue='Year',data=df,ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title(f'Jumlah Penyewaan {kolom.capitalize()}', loc="center")
    ax.tick_params(axis='both')
    st.pyplot(fig)

Bike_df = pd.read_csv("Bike_rent.csv")
Bike_df['Date'] = pd.to_datetime(Bike_df['Date'])
min_date = Bike_df["Date"].min()
max_date = Bike_df["Date"].max()

page=st.sidebar.radio("Pilih Menu Halaman",["DataSet","Visualisasi"])
if page == "DataSet":
    html_temp = """ 
    <div style ="background-color:White;padding:13px"> 
    <h1 style ="color:black;text-align:center;">DataSet Bike</h1> 
    </div> 
    """
    st.markdown(html_temp, unsafe_allow_html = True) 
    st.dataframe(Bike_df)
    st.text(Bike_df.shape)
elif page == "Visualisasi":
    html_temp = """ 
    <div style ="background-color:White;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Visualitation Data Dashboard</h1> 
    </div> 
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    with st.sidebar:
        # Mengambil start_date & end_date dari date_input
        start_date, end_date = st.date_input(
            label='Rentang Waktu',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    main_df = Bike_df[(Bike_df["Date"] >= str(start_date)) & 
                    (Bike_df["Date"] <= str(end_date))]

    daily_orders_df = create_rent_df(main_df)
    # st.header('Visualitation Data Dashboard :sparkles:')

    # Menampilkan data harian dalam satu kolom
    st.subheader('Total Rent Metric')
    total_rent = main_df.total_rent.sum()
    st.metric("Total Rent", value=total_rent) 
    
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(
        daily_orders_df,
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20)
    
    st.pyplot(fig)
    data_pertahun_casual = create_bycasual_df(main_df)
    data_pertahun_registered = create_byregist_df(main_df)

    selected_feature = st.selectbox('Rent Option:', ['registered', 'casual'])
    if selected_feature == 'casual':
        barplot(data_pertahun_casual,selected_feature)
    else:
        barplot(data_pertahun_registered,selected_feature)

    
    fig , ax = plt.subplots(figsize=(12,6))
    ax.pie(main_df.groupby(by='Year')['total_rent'].sum(), 
            labels=main_df['Year'].unique(),
            autopct='%1.1f%%',
            startangle=90)
    ax.set_title('Persen Total Penyewaan  Sepeda')
    st.pyplot(fig)