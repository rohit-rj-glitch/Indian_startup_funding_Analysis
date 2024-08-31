import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='StartUp Analysis', layout='wide')

df = pd.read_csv('startup_cleaned.csv')
investorsdf = pd.read_csv('investors.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    # Define a function to create a card-like layout
    def card(title, content):
        st.markdown(
            f"""
            <div style='padding: 3px 7px; border: 1px solid #e6e6e6; border-radius: 10px;'>
                <h5>{title}</h5>
                <p>{content}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        card('Total Investment',str(total) + ' Cr')
    with col2:
        card('Max Investment', str(max_funding) + ' Cr')

    with col3:
        card('Avg Investment',str(round(avg_funding)) + ' Cr')

    with col4:
        card('Total Startups',num_startups)

    st.header('Month by month graph')
    selected_option = st.selectbox('Select Type',['Total investment in every months','Count of investment in every months'])
    if selected_option == 'Total investment in every months':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    
    # Specify the nth value you want to show
    nth_value = 5
    
    # Set tick positions and labels
    x_values = temp_df['x_axis'][::nth_value]
    x_labels = temp_df['x_axis'].iloc[::nth_value]
    ax3.set_xticks(x_values)
    ax3.set_xticklabels(x_labels, rotation=45)  # Rotate x-axis labels for better readability
    # Show plot inStreamlit
    st.pyplot(fig3)

    col5,col6 = st.columns(2)
    with col5:
        st.header('Top 10 Startups')
        df['startup'] = df['startup'].str.replace('Flipkart.com','Flipkart')
        
        tpstr = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        
        fig4, ax4 = plt.subplots()
        ax4.bar(tpstr.index, tpstr.values)
        
        # Customize plot
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('startups')
        plt.ylabel('Values (in Cr.)')
        
        # Display chart in Streamlit
        st.pyplot(fig4)
        
    with col6:
        st.header('Top 10 Investor')
        investorsdf['index'] = investorsdf['index'].str.replace('and existing envestors',' ')
        tpinvestors = investorsdf.groupby('index')['amount'].sum().sort_values(ascending=False).head(10)
        fig5, ax5 = plt.subplots()
        ax5.bar(tpinvestors.index, tpinvestors.values)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig5)
    col7,col8 = st.columns(2)
    with col7:
        st.header('Top Sectors')
        df['vertical']=df['vertical'].str.replace('eCommerce','E-commerce')
        df['vertical']=df['vertical'].str.replace('ECommerce','E-commerce')
        df['vertical']=df['vertical'].str.replace('E-Commerce & M-Commerce platform','E-commerce')
        df['vertical']=df['vertical'].str.replace('E-Commerce','E-commerce')
        sanalysis = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(6)
        # Create column chart
        fig4, ax4 = plt.subplots()
        ax4.pie(sanalysis.values, labels=sanalysis.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig4)
    with col8:
        st.header('Top Cities')
        tpcity = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(6)
        
        fig4, ax4 = plt.subplots()
        ax4.bar(tpcity.index, tpcity.values)
        
        # Customize plot
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('City')
        plt.ylabel('Values (in Cr.)')
        
        # Display chart in Streamlit
        st.pyplot(fig4)
        
   
    
           
def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)
        
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)


def load_startup_details(select_startup):
    st.header(select_startup)
    st.subheader('1. About Startup')
    startabout = df[df['startup'].str.contains(select_startup)][['year','vertical','subvertical','city','round']]
    st.dataframe(startabout)

    st.subheader('1. Investors')
    inv_series = df[df['startup'].str.contains(select_startup)][['date','investors','round','amount']]
    st.dataframe(inv_series)
    
    col1, col2 = st.columns(2)
    with col1:
        sub_series = df[df['startup'].str.contains(select_startup)].groupby('subvertical')['year'].sum()
        st.subheader('subindustry')
        fig9, ax9 = plt.subplots()
        ax9.pie(sub_series, labels=sub_series.index, autopct="%0.01f%%")
        st.pyplot(fig9)
    with col2:
        ver_series = df[df['startup'].str.contains(select_startup)].groupby('vertical')['year'].sum()
        st.subheader('industry')
        fig10, ax10 = plt.subplots()
        ax10.pie(ver_series, labels=ver_series.index, autopct="%0.01f%%")
        st.pyplot(fig10)
    

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    select_startup = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(select_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum()),reverse=True))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
