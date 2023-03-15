import streamlit as st
import pickle
import plotly.express as px
import pandas as pd

with open('data/dic_pca.pkl', 'rb') as f:
    dic_pcas = pickle.load(f)

with open('data/df_weights.pkl', 'rb') as f:
    df_weights = pickle.load(f)

# Define the years that can be selected
years = dic_pcas.keys()

st.write('## Weights matrix')

df_weights = df_weights.style.applymap(lambda v: f'background-color: darkorange; opacity: {int(v*100)+40}%;')

html = df_weights.to_html(escape=False)

st.markdown(
    html,
    unsafe_allow_html=True
)

st.write('## Compare Years')

# Create a layout with two columns
col1, col2 = st.columns(2)

# Add dropdowns to each column to select the year
with col1:
    year1 = st.selectbox('Select a year', years, key='year1')

    df_pca_1 = dic_pcas[year1]

    fig1_3d = px.scatter_3d(data_frame=df_pca_1, x='PC1', y='PC2',
                z='PC3', color='Cluster', hover_name=df_pca_1.index)
    st.plotly_chart(fig1_3d, use_container_width=True)

with col2:
    year2 = st.selectbox('Select a year', years, key='year2')

    df_pca_2 = dic_pcas[year2]

    fig2_3d = px.scatter_3d(data_frame=df_pca_2, x='PC1', y='PC2',
                z='PC3', color='Cluster', hover_name=df_pca_2.index)
    st.plotly_chart(fig2_3d, use_container_width=True)

pc = st.selectbox('Select a Principal Component', df_pca_2.columns[2:], key='pc')

print(pc)

df_year1_pc = dic_pcas[year1][[pc, 'Year']].reset_index()
df_year2_pc = dic_pcas[year2][[pc, 'Year']]
df_year2_pc = df_year2_pc.reset_index()

dff = pd.concat([df_year1_pc, df_year2_pc])

dff['Change %'] = dff.groupby('Country')[pc].pct_change()*100
dff_pivot = dff.pivot_table(index='Country', columns='Year', values=['PC1', 'Change %'])
dff_pivot = dff_pivot.sort_values((pc, year2), ascending=False)

df_ranking = dff_pivot.style.background_gradient('Greens', subset=['PC1']).bar(subset=['Change %'])

df_ranking_html = df_ranking.to_html(escape=False)

st.markdown(
    df_ranking_html,
    unsafe_allow_html=True
)