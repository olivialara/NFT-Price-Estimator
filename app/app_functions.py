import streamlit as st
import pandas as pd
import numpy as np
#plotly imports
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json


###############HOME PAGE##############################################################################

def set_home():
    st.title('Search By Punk ID')
    # st.header("Search By Punk ID")
    st.subheader("Get the estimated value, rarity score, similar punks, and transaction data.")

    trans = pd.read_csv('../data/clean_transactions.csv')
    rarity = pd.read_csv('../data/clean_rarity.csv')
    nearest_neighbors = pd.read_csv('../data/clean_nearest_neighbors.csv')
    estimates = pd.read_csv('../data/nn_preds.csv')

    id = st.number_input('CryptoPunk ID', 0, 9999)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(id) + '.png', use_column_width=True)
        details_url = 'https://www.larvalabs.com/cryptopunks/details/' + str(id)
        st.markdown(f"See all info on this Punk [here]({details_url}).")
    with col3:
        st.write("")
    
    st.write(f"Estimated Value of Punk: ${get_rarity_score(rarity, id)}K")
    st.write(f"Rarity Score of Punk: {get_estimated_value(estimates, id)}")

    st.write(f"10 Most Similar Punks: ")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    similar_punks = get_similar_punks(nearest_neighbors, id)
    urls = []
    for i in range(len(similar_punks)):
        url = 'https://www.larvalabs.com/cryptopunks/details/' + str(similar_punks[i][0]) 
        urls.append(url)

    
    with col1:
        st.markdown(f"#{0+1}: [Punk {similar_punks[0][0]}] ({urls[0]})")
        st.markdown(f"Similarity Score: {similar_punks[0][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[0][0]) + '.png', use_column_width=True)
        st.markdown(f"#{5+1}: [Punk {similar_punks[5][0]}] ({urls[5]})")
        st.markdown(f"Similarity Score:  {similar_punks[5][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[5][0]) + '.png', use_column_width=True)
    with col2:
        st.markdown(f"#{1+1}: [Punk {similar_punks[1][0]}] ({urls[1]})")
        st.markdown(f"Similarity Score: {similar_punks[1][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[1][0]) + '.png', use_column_width=True)
        st.markdown(f"#{6+1}: [Punk {similar_punks[6][0]}] ({urls[6]})")
        st.markdown(f"Similarity Score: {similar_punks[6][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[6][0]) + '.png', use_column_width=True)
    with col3:
        st.markdown(f"#{2+1}: [Punk {similar_punks[2][0]}] ({urls[2]})")
        st.markdown(f"Similarity Score: {similar_punks[2][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[2][0]) + '.png', use_column_width=True)
        st.markdown(f"#{7+1}: [Punk {similar_punks[7][0]}] ({urls[7]})")
        st.markdown(f"Similarity Score:  {similar_punks[7][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[7][0]) + '.png', use_column_width=True)
    with col4:
        st.markdown(f"#{3+1}: [Punk {similar_punks[3][0]}] ({urls[3]})")
        st.markdown(f"Similarity Score: {similar_punks[3][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[3][0]) + '.png', use_column_width=True)
        st.markdown(f"#{8+1}: [Punk {similar_punks[8][0]}] ({urls[8]})")
        st.markdown(f"Similarity Score: {similar_punks[8][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[8][0]) + '.png', use_column_width=True)
    with col5:
        st.markdown(f"#{4+1}: [Punk {similar_punks[4][0]}] ({urls[4]})")
        st.markdown(f"Similarity Score: {similar_punks[4][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[4][0]) + '.png', use_column_width=True)
        st.markdown(f"#{9+1}: [Punk {similar_punks[9][0]}] ({urls[9]})")
        st.markdown(f"Similarity Score:  {similar_punks[9][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(similar_punks[9][0]) + '.png', use_column_width=True)

    st.write(graph_all_punk_transactions(trans, id))
    
    my_expander = st.expander(label='View Sales Only Graph')
    with my_expander:
        st.write(graph_sales_punk_transactions(trans, id))
            
    my_expander_2 = st.expander(label='View Bids Only Graph')
    with my_expander_2:
        st.write(graph_bids_punk_transactions(trans, id))

    my_expander_3 = st.expander(label = 'View Offers Only Graph')
    with my_expander_3:
        st.write(graph_offers_punk_transactions(trans, id))

def get_estimated_value(estimates, id):
    return(estimates['rounded_preds'].iloc[id])

def get_rarity_score(rarity, id):
    return round(rarity['total_rarity_score'].iloc[id], 2)

def get_similar_punks(nearest_neighbors, id):
    return(json.loads(nearest_neighbors['neighbors'].iloc[id]))

def graph_all_punk_transactions(trans, id):
    pio.templates.default = "plotly_dark"
    trans.rename(columns = {'punk_id': 'id'}, inplace = True)
    # dataframe for single punk
    punk = trans[trans['id'] == id]
    punk['date'] = pd.to_datetime(punk['date'])
    punk_trans = punk[(punk['trans'] == 'Sold') | (punk['trans'] == 'Bid') | (punk['trans'] == 'Offered')]

    # separate dataframes sales, bids, and offers
    punk_sold = punk_trans[punk_trans['trans'] == 'Sold']
    punk_bid = punk_trans[punk_trans['trans'] == 'Bid']
    punk_offered = punk_trans[punk_trans['trans'] == 'Offered']
    
    df = punk_trans
    fig = px.line(df, x="date", y=df['usd'].apply(pd.to_numeric),
                  hover_data={"date": "|%B %d, %Y"},
                  labels={'y': 'USD(K)', 'date': 'Date', 'trans': 'Transaction'},
                  #text = df['usd']
                  markers = True,
                  color = 'trans',
                  color_discrete_map = {'Sold': '#99c2ff', 'Bid': '#bfacff', 'Offered': '#ffa7ab'}
                 )

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        rangeslider_visible=True,
        rangeselector=dict(
        buttons=list([dict(count=3, label="3 months", step="month", stepmode="backward"),
                          dict(count=6, label="6 months", step="month", stepmode="backward"),
                          dict(count=1, label="Year to Date", step="year", stepmode="todate"),
                          dict(count=1, label="1 Year", step="year", stepmode="backward"),
                          dict(label= 'All', step="all")])
        ))
    
    fig.update_layout(title = 'All Transactions', title_x=.5, )
    fig.update_layout(updatemenus=[{'bgcolor': '#99c2ff'}])
    
    #fig.update_layout(width=1000,height=400)
    return fig

def graph_sales_punk_transactions(trans, id):
    pio.templates.default = "plotly_dark"
    # first plot: sales
    trans.rename(columns = {'punk_id': 'id'}, inplace = True)
    # dataframe for single punk
    punk = trans[trans['id'] == id]
    punk['date'] = pd.to_datetime(punk['date'])
    punk_trans = punk[(punk['trans'] == 'Sold') | (punk['trans'] == 'Bid') | (punk['trans'] == 'Offered')]

    # separate dataframes sales, bids, and offers
    punk_sold = punk_trans[punk_trans['trans'] == 'Sold']
    df_1 = punk_sold
    fig_1 = px.line(df_1, x="date", y=df_1['usd'].apply(pd.to_numeric),
                  hover_data={"date": "|%B %d, %Y"},
                  labels={'y': 'USD(K)', 'date': 'Date'},
                  #text = df['usd']
                  markers = True,
                 )

    fig_1.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([dict(count=3, label="3 months", step="month", stepmode="backward"),
                          dict(count=6, label="6 months", step="month", stepmode="backward"),
                          dict(count=1, label="Year to Date", step="year", stepmode="todate"),
                          dict(count=1, label="1 Year", step="year", stepmode="backward"),
                          dict(label= 'All', step="all")])
        ))

    fig_1.update_traces(line_color='#99c2ff') 
    fig_1.update_layout(title = 'Sold Transactions', title_x=.5)
    return fig_1

def graph_bids_punk_transactions(trans, id):
    pio.templates.default = "plotly_dark"
    trans.rename(columns = {'punk_id': 'id'}, inplace = True)
    # dataframe for single punk
    punk = trans[trans['id'] == id]
    punk['date'] = pd.to_datetime(punk['date'])
    punk_trans = punk[(punk['trans'] == 'Sold') | (punk['trans'] == 'Bid') | (punk['trans'] == 'Offered')]

    # separate dataframes sales, bids, and offers
    punk_bid = punk_trans[punk_trans['trans'] == 'Bid']
    
    # second plot: bids
    df_2 = punk_bid
    fig_2 = px.line(df_2, x="date", y=df_2['usd'].apply(pd.to_numeric),
                  hover_data={"date": "|%B %d, %Y"},
                  labels={'y': 'USD(K)', 'date': 'Date'},
                  #text = df['usd']
                  markers = True,
                 )

    fig_2.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([dict(count=3, label="3 months", step="month", stepmode="backward"),
                          dict(count=6, label="6 months", step="month", stepmode="backward"),
                          dict(count=1, label="Year to Date", step="year", stepmode="todate"),
                          dict(count=1, label="1 Year", step="year", stepmode="backward"),
                          dict(label= 'All', step="all")])
        ))

    fig_2.update_traces(line_color='#bfacff')
    fig_2.update_layout(title = 'Bid Transactions', title_x=.5)
    return fig_2
    
def graph_offers_punk_transactions(trans, id):
    pio.templates.default = "plotly_dark"
    trans.rename(columns = {'punk_id': 'id'}, inplace = True)
    # dataframe for single punk
    punk = trans[trans['id'] == id]
    punk['date'] = pd.to_datetime(punk['date'])
    punk_trans = punk[(punk['trans'] == 'Sold') | (punk['trans'] == 'Bid') | (punk['trans'] == 'Offered')]

    # separate dataframes sales, bids, and offers
    punk_offered = punk_trans[punk_trans['trans'] == 'Offered']

    # third plot: offers
    df_3 = punk_offered
    fig_3 = px.line(df_3, x="date", y=df_3['usd'].apply(pd.to_numeric),
                  hover_data={"date": "|%B %d, %Y"},
                  labels={'y': 'USD(K)', 'date': 'Date'},
                  #text = df['usd']
                  markers = True,
                 )

    fig_3.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([dict(count=3, label="3 months", step="month", stepmode="backward"),
                          dict(count=6, label="6 months", step="month", stepmode="backward"),
                          dict(count=1, label="Year to Date", step="year", stepmode="todate"),
                          dict(count=1, label="1 Year", step="year", stepmode="backward"),
                          dict(label= 'All', step="all")])
        ))

    fig_3.update_traces(line_color='#ffa7ab')
    fig_3.update_layout(title = 'Offered Transactions', title_x=.5)
    return fig_3

###############HIGHEST ESTIMATED VALUE PAGE##############################################################################
def set_value():
    st.title('Top Ten Highest Estimated Values')
    
    estimates = pd.read_csv('../data/nn_preds.csv')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    high_punks = get_high_punks(estimates)
    #st.write(rare_punks)
    
    urls = []
    for i in range(len(high_punks)):
        url = 'https://www.larvalabs.com/cryptopunks/details/' + str(high_punks[i][0]) 
        urls.append(url)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        #st.write("      ")
        st.markdown(f"#{0+1}: [Punk {high_punks[0][0]}] ({urls[0]})")
        st.markdown(f"Estimated Value: ${high_punks[0][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[0][0]) + '.png')            #st.write("      ")
        st.markdown(f"#{5+1}: [Punk {high_punks[5][0]}] ({urls[5]})")
        st.markdown(f"Estimated Value: ${high_punks[5][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[5][0]) + '.png')
                    #st.write("      ")
    with col2:
        #st.write("      ")            
        st.markdown(f"#{1+1}: [Punk {high_punks[1][0]}] ({urls[1]})")
        st.markdown(f"Estimated Value: ${high_punks[1][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[1][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{6+1}: [Punk {high_punks[6][0]}] ({urls[6]})")
        st.markdown(f"Estimated Value: ${high_punks[6][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[6][0]) + '.png')
        #st.write("      ")
    with col3:
        #st.write("      ")
        st.markdown(f"#{2+1}: [Punk {high_punks[2][0]}] ({urls[2]})")
        st.markdown(f"Estimated Value: ${high_punks[2][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[2][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{7+1}: [Punk {high_punks[7][0]}] ({urls[7]})")
        st.markdown(f"Estimated Value: ${high_punks[7][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[7][0]) + '.png')
        #st.write("      ")
    with col4:
        #st.write("      ")
        st.markdown(f"#{3+1}: [Punk {high_punks[3][0]}] ({urls[3]})")
        st.markdown(f"Estimated Value: ${high_punks[3][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[3][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{8+1}: [Punk {high_punks[8][0]}] ({urls[8]})")
        st.markdown(f"Estimated Value: ${high_punks[8][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[8][0]) + '.png')
        #st.write("      ")
    with col5:
        #st.write("      ")
        st.markdown(f"#{4+1}: [Punk {high_punks[4][0]}] ({urls[4]})")
        st.markdown(f"Estimated Value: ${high_punks[4][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[4][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{9+1}: [Punk {high_punks[9][0]}] ({urls[9]})")
        st.markdown(f"Estimated Value: ${high_punks[9][1]}K")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(high_punks[9][0]) + '.png')
        #st.write("      ")

def get_high_punks(estimates):
    ten_high = estimates.sort_values(by = 'nn_preds', ascending=False).head(10)
    ten_high_ids = list(ten_high['punk_id'])
    ten_high_preds = list(ten_high['rounded_preds'])
    return (list(zip(ten_high_ids, ten_high_preds)))

###############HIGHEST RARITY SCORES PAGE##############################################################################

def set_rarity():
    st.title('Top Ten Rarest Punks')
    #st.subheader(f" The 10 most rariest punks are: ")

    rarity = pd.read_csv('../data/clean_rarity.csv')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    rare_punks = get_rare_punks(rarity)
    
    urls = []
    for i in range(len(rare_punks)):
        url = 'https://www.larvalabs.com/cryptopunks/details/' + str(rare_punks[i][0]) 
        urls.append(url)
    
    #col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        #st.write("      ")
        st.markdown(f"#{0+1}: [Punk {rare_punks[0][0]}] ({urls[0]})")
        st.markdown(f"Rarity Score: {rare_punks[0][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[0][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{5+1}: [Punk {rare_punks[5][0]}] ({urls[5]})")
        st.markdown(f"Rarity Score: {rare_punks[5][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[5][0]) + '.png')
        #st.write("      ")
    with col2:
        #st.write("      ")
        st.markdown(f"#{1+1}: [Punk {rare_punks[1][0]}] ({urls[1]})")
        st.markdown(f"Rarity Score: {rare_punks[1][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[1][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{6+1}: [Punk {rare_punks[6][0]}] ({urls[6]})")
        st.markdown(f"Rarity Score: {rare_punks[6][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[6][0]) + '.png')
        #st.write("      ")
    with col3:
        #st.write("      ")
        st.markdown(f"#{2+1}: [Punk {rare_punks[2][0]}] ({urls[2]})")
        st.markdown(f"Rarity Score: {rare_punks[2][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[2][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{7+1}: [Punk {rare_punks[7][0]}] ({urls[7]})")
        st.markdown(f"Rarity Score: {rare_punks[7][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[7][0]) + '.png')
        #st.write("      ")
    with col4:
        #st.write("      ")
        st.markdown(f"#{3+1}: [Punk {rare_punks[3][0]}] ({urls[3]})")
        st.markdown(f"Rarity Score: {rare_punks[3][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[3][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{8+1}: [Punk {rare_punks[8][0]}] ({urls[8]})")
        st.markdown(f"Rarity Score: {rare_punks[8][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[8][0]) + '.png')
        #st.write("      ")
    with col5:
        #st.write("      ")
        st.markdown(f"#{4+1}: [Punk {rare_punks[4][0]}] ({urls[4]})")
        st.markdown(f"Rarity Score: {rare_punks[4][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[4][0]) + '.png')
        #st.write("      ")
        st.markdown(f"#{9+1}: [Punk {rare_punks[9][0]}] ({urls[9]})")
        st.markdown(f"Rarity Score: {rare_punks[9][1]}")
        st.image('https://www.larvalabs.com/cryptopunks/cryptopunk' + str(rare_punks[9][0]) + '.png')
        #st.write("      ")

def get_rare_punks(rarity):
    ten_rare = rarity.sort_values(by = 'total_rarity_score', ascending=False).head(10)
    ten_rare_ids = list(ten_rare['punk_id'])
    ten_rare_scores = list(ten_rare['rounded_scores'])
    return (list(zip(ten_rare_ids, ten_rare_scores)))

###############AVERAGES OF TYPES AND ACCESSORIES PAGE##############################################################################

def set_averages():
    st.title('Averages of Punks Based on Types and Accessories')
    types = pd.read_csv('../data/type.csv')
    accessory = pd.read_csv('../data/clean_accessory.csv')
    indiv = pd.read_csv('../data/clean_individual.csv')
    
    menu_set_averages = st.radio("", ("Types", "Accessories"),)

    if menu_set_averages == "Types":
        #st.markdown('### Graphs')
        #st.markdown('.')
        st.write(graph_punk_type_rarity(types))
        st.write(graph_punk_type_sale(indiv))
        st.write(graph_punk_type_bid(indiv))
    elif menu_set_averages  == "Accessories":
        #st.markdown('### Graphs')
        #st.markdown('.')
        st.write(graph_punk_accessory_rarity(accessory))
        st.write(graph_punk_accessory_sales(indiv))
        st.write(graph_punk_accessory_bids(indiv))
    
def graph_punk_type_rarity(types):
    #sorted types dataframe
    type_sorted = types.sort_values(by = 'amount')

    # bar plot of punk type counts
    fig = px.bar(type_sorted, 
                x=type_sorted['type'],
                y= type_sorted['amount'],
                text = type_sorted['amount'],
                color_discrete_sequence = ['#19d3f3'],
                labels={'type': 'Punk Type', 'amount': 'Frequency'})
    fig.update_layout(title = 'Type Counts', title_x=.5)
    return fig

def graph_punk_accessory_rarity(accessory):
    # sort values by amount
    acc_sorted = accessory.sort_values(by = 'amount')

    # top ten most rare accessories
    rare_acc = acc_sorted[0:5]

    # converting rare info to lists for bar plot
    accessories = list(rare_acc['accessory'])
    acc_rarity = list(rare_acc['rarity'])

    # converting rare info to lists for bar plot
    accessories = list(rare_acc['accessory'])
    acc_amount = list(rare_acc['amount'])

    # bar plot of punk type counts
    fig = px.bar(rare_acc, 
             x= accessories,
             y= acc_amount,  
             text = acc_amount,
             color_discrete_sequence = ['#9DEA2E'],
             labels={'x': 'Punk Accessory', 'y': 'Amount'})
    fig.update_layout(title = "Rare Accessories' Counts", title_x=.5)
    return fig

def graph_punk_accessory_sales(indiv):
    rare_acc_names = ['beanie', 'choker', 'pilot', 'tiara', 'orange side']
    fig = px.bar(indiv, 
             x= rare_acc_names,
             y= [675.83, 286.70, 579.64, 377.84, 324.99],
             text = [675.83, 286.70, 579.64, 377.84, 324.99],
             color_discrete_sequence = ['#99c2ff'],
             labels={'x': 'Punk Type', 'y': 'USD(K)'})
    fig.update_layout(title = 'Average Sales for Punks w/ Rare Punk Accessories', title_x=.5)
    return fig

def graph_punk_accessory_bids(indiv):
    rare_acc_names = ['beanie', 'choker', 'pilot', 'tiara', 'orange side']
    fig = px.bar(indiv, 
             x= rare_acc_names,
             y= [668.65, 306.05, 468.97, 190.01, 332.17],
             text = [668.65, 306.05, 468.97, 190.01, 332.17],
             color_discrete_sequence = ['#bfacff'],
             labels={'x': 'Punk Type', 'y': 'USD(K)'})
    fig.update_layout(title = 'Average Bids for Punks w/ Rare Punk Accessories', title_x=.5)
    return fig

def graph_punk_type_sale(indiv):
    # bar plot of average sales (in last 6 months) per punk type
    type_names = ['alien', 'ape', 'zombie', 'female', 'male']

    fig = px.bar(indiv, 
                x= type_names,
                y= [0, 4605.00, 2315.91, 478.06, 226.48],
                text = [0, 4605, 2315.91, 478.06, 226.48],
                color_discrete_sequence = ['#99c2ff'],
                labels={'x': 'Punk Type', 'y': 'USD(K)'})
    fig.update_layout(title = 'Average Sales per Type', title_x=.5)
    return fig

def graph_punk_type_bid(indiv):
    # bar plot of average bids (in last 6 months) per punk type
    type_names = ['alien', 'ape', 'zombie', 'female', 'male']
    
    fig = px.bar(indiv, 
                x= type_names,
                y= [12421.31, 808.40, 681.77, 174.60, 220.03],
                text = [12421.31, 808.40, 681.77, 174.60, 220.03],
                color_discrete_sequence = ['#bfacff'],
                labels={'x': 'Punk Type', 'y': 'USD(K)'})
    fig.update_layout(title = 'Average Bids per Type', title_x=.5)
    return fig


###############ABOUT PROJECT PAGE##############################################################################
def set_about():
    st.title('Project Terms and Information')

    st.subheader("Genesis")
    st.write('The CryptoPunks are undoubtebly one of the most sought after NFTs. Unfortunately, attempting to estimate the value of an individual punk can be confusing,  as only 30% of punks have recent (past 6 months) sale data and many have no transaction data since they were claimed. This project was created to aid potential CryptoPunk buyers in estimating the value of a particular punk based on punks with similar accessories, accessory counts, and types, regardless of whether they have recent sale data or not.')
    st.markdown('##')
    
    st.subheader("Estimated Value")
    st.write("The estimated value of each punk was estimated using deep neural networks. The model incorporated more than 100 features, such as the accessories list and transaction history of each punk.")
    st.markdown('##')

    st.subheader("Rarity Score")
    st.write("The rarity score of a punk explains how rare a punk is and was calculated based on how rare all of the attributes of the particular punk are. The higher the score, the more rare the punk is. The accessories (87 possible accessories), types (alien, ape, zombie, female, male), skin (teal, ape shade, green, human shade), and total accessories (0-8) are all utilized in this calculation.")
    st.write("The minimum rarity score is 19.95 and the maximum is 10,336.34. Punks with a rarity score lower than 88.47 fall in the lower half of rarity scores, where as punks with a rarity score of 88.47 or higher fall in the upper half of rarity scores.")
    st.markdown('##')

    st.subheader("Similarity Score")
    st.write("The similarity score of a punk explains how similar it is to the inputted punk. Similarity scores closer to 1 imply strong similarity to the inputted punk. This similarity scores were calculated using a recommender system supported by natural language processing algorithms and cosine distances.")
    st.markdown('##')

    st.subheader("The Data Source")
    st.write("The data for this project was collected using three different sounces: OpenSea API for the accessory and type counts, LarvaLabs for all the transaction data, and Kaggle for a list of each individual punk's accessories and type. Below are links to the location of the data.")
    st.markdown("""<a href="https://docs.opensea.io/reference/retrieving-a-single-collection"> OpenSea API </a>""", unsafe_allow_html=True)
    st.markdown("""<a href="https://www.larvalabs.com/cryptopunks"> Larva Labs </a>""", unsafe_allow_html=True)
    st.markdown("""<a href="https://www.kaggle.com/tunguz/cryptopunks-simple-visualization/data"> Kaggle Dataset </a>""", unsafe_allow_html=True)