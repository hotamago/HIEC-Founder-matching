# System
import os
import json
from random import randint

# Time and data
import datetime
import pandas as pd

# Chart
import matplotlib.pyplot as plt
import plotly.graph_objects as plotly_go

# Hota Lib
from module.readData import CsvData
from module.apiCController import ApiCController
from module.mangerStatus import MangerStatus

# Hota config
from mainConfig import *

# Webapp
import streamlit as st

st.set_page_config(
    page_title="Techstart matching",
    page_icon="D:\hotamago\HIEC project\Founder matching\relesese\logo.jpg",
    layout="wide"
)


def make_pair(a, b):
    return [a, b]

# Cache
@st.cache_resource
def load_model():
    apiCController = ApiCController()
    csvData = CsvData()
    mStatus = MangerStatus({
        "df": csvData.read(namesCol, dtypesCol, valueNan).to_json(orient='records'),
        "nodesDel": [],
        "edegesDel": [],
        "svOption": dict(),
    })
    return mStatus, apiCController, csvData


with st.spinner('Loading...'):
    mStatus, apiCController, csvData = load_model()


def read_df():
    return pd.read_json(mStatus.get_value("df"), dtype=dtypesCol)


def write_df(df):
    mStatus.set_value("df", df.to_json(orient='records'))


mStatus._get()

df = read_df()

with st.sidebar:
    if st.button('Rebuild'):
        svOp = mStatus._data['svOption']
        for x in svOp:
            edge = list(map(int, x.split(',')))
            option = svOp[x]

            if option == 'Match':
                mStatus._data['nodesDel'].append(edge[1])
                df.at[edge[0], 'numberMember'] += 1
                df.at[edge[0], 'numberRequestAddin'] -= 1

            if option == 'Not match':
                mStatus._data["edegesDel"].append(edge)

        mStatus._data['svOption'] = dict()
        mStatus._set()
        write_df(df)
        st.experimental_rerun()

    with st.form("my-form", clear_on_submit=True):
        uploaded_file = st.file_uploader(
            "Choose a csv file", type='csv')
        submitted = st.form_submit_button("submit")

        if submitted and uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            with open('list.csv', 'wb') as tempf:
                tempf.write(bytes_data)

            st.cache_resource.clear()
            mStatus._data = {
                "df": csvData.read(namesCol, dtypesCol, valueNan).to_json(orient='records'),
                "nodesDel": [],
                "edegesDel": [],
                "svOption": dict(),
            }
            mStatus._set()
            st.experimental_rerun()

# st.write(mStatus.get_value("nodesDel"))
# st.write(mStatus.get_value("edegesDel"))

with st.container():
    apiCController.write(
        df,
        mStatus.get_value("nodesDel"),
        mStatus.get_value("edegesDel"),
    )
    apiCController.run()
    listEdges = apiCController.read()

    singleUsers = df.query("`role` == '{0}'".format(
        nameRoleUser)).loc[:, listTypeSingle]
    teams = df.query("`role` == '{0}'".format(
        nameRoleTeam)).loc[:, listTypeTeam]

    backupStatus = mStatus._data

    idOp = {
        "Unknow": 0,
        "Match": 1,
        "Not match": 2,
    }
    svOp = mStatus._data['svOption']

    for edge in listEdges:
        with st.container():
            st.text("Edge ({0}) -> ({1})".format(edge[0], edge[1]))
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                st.dataframe(teams.loc[edge[0]], width=600, height=200)
            with col2:
                st.dataframe(singleUsers.loc[edge[1]], width=600, height=200)
            with col3:
                indexOx = 0
                edgeStr = ','.join(map(str, edge))
                if svOp.get(edgeStr) is not None:
                    indexOx = idOp[svOp[edgeStr]]
                option = st.selectbox(
                    'Select', ('Unknow', 'Match', 'Not match'), index=indexOx, key=edgeStr)
                mStatus._data['svOption'][edgeStr] = option
                mStatus._set()

                # if st.button('Match'):
                #     mStatus._data['nodesDel'].append(edge[1])
                #     df.at[edge[0], 'numberMember'] += 1
                #     df.at[edge[0], 'numberRequestAddin'] -= 1

                # if st.button('Not match'):
                #     mStatus._data["edegesDel"].append(edge)

                cvDict = teams.loc[edge[0]].to_dict()
                strCvTeam = ""
                for x in cvDict:
                    strCvTeam += "{0}: {1}\n".format(x, cvDict[x])

                st.download_button(
                    label="CV Teams",
                    data=strCvTeam,
                    file_name='cvTeams_{0}.txt'.format(edge[0]),
                    mime='text',
                )

                cvDict = singleUsers.loc[edge[1]].to_dict()
                strCvPer = ""
                for x in cvDict:
                    strCvPer += "{0}: {1}\n".format(x, cvDict[x])

                st.download_button(
                    label="CV Personal",
                    data=strCvPer,
                    file_name='cvPersonal_{0}.txt'.format(edge[1]),
                    mime='text',
                )
            st.markdown("""---""")
