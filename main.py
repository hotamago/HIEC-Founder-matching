# System
import os
import json
from random import randint
import json
from io import StringIO

# Time and data
import datetime
import pandas as pd

# Chart
import matplotlib.pyplot as plt
import plotly.graph_objects as plotly_go

# Hota Lib
from module.readData import CsvData
from module.apiPyController import ApiCController
from module.mangerStatus import MangerStatus

# Hota config
from mainConfig import *

# Webapp
import streamlit as st

# Init page
st.set_page_config(
    page_title="Techstart matching",
    # page_icon="D:\hotamago\HIEC project\Founder matching\relesese\logo.jpg",
    layout="wide"
)

# Cache
@st.cache_resource
def load_model_0():
    apiCController = ApiCController()
    csvData = CsvData()
    return apiCController, csvData

@st.cache_resource
def load_model_1():
    apiCController = ApiCController()
    csvData = CsvData()
    return apiCController, csvData

# Loading model
with st.spinner('Load model 0...'):
    apiCController, csvData = load_model_0()

def makeEmptyStatus():
    df = csvData.read(namesCol).to_json(orient='records')
    dfDict = json.loads(df)

    cntMemTeam = {}
    cntTryUser = {}
    isHustInTeam = {}
    isUserAreHust = {}

    # Function check if user is hust
    def checkHust(s):
        return checkExitStringInString(s, [
            "HUST", "hanoi university of science and technology", "Bách Khoa Hà Nội"
        ])

    # Build list
    for i in dfDict:
        if i[namesCol[1]] == nameRoleTeam:
            cntMemTeam[i["id"]] = max(int(i[namesCol[10]]), maxOfMemberPerTeam - int(i[namesCol[13]]))
            isHustInTeam[i["id"]] = checkHust(i[namesCol[7]])

        if i[namesCol[1]] == nameRoleUser:
            cntTryUser[i["id"]] = 0
            isUserAreHust[i["id"]] = checkHust(i[namesCol[-6]])

    return {
        "df": df,
        "nodesDel": [],
        "edegesDel": [],
        "cntMemTeam": cntMemTeam,
        "isHustInTeam": isHustInTeam,
        "isUserAreHust": isUserAreHust,
        "cntTryUser": cntTryUser,
        "svOption": dict(),
    }

with st.spinner('Load model 1...'):
    mStatus = MangerStatus(makeEmptyStatus())

# Helper function
def make_pair(a, b):
    return [a, b]
def read_df():
    return json.loads(mStatus.get_value("df"))
def write_df(df):
    mStatus.set_value("df", json.dumps(df))
def addNodesDel(edge):
    if edge[1] not in mStatus._data['nodesDel']:
        mStatus._data['nodesDel'].append(edge[1])
def addEdgesDel(edge):
    if edge not in mStatus._data['edegesDel']:
        mStatus._data['edegesDel'].append(edge)

# Read data and constant
mStatus._get()
df = read_df()
modeUI = "Matching"
# st.write(pd.read_json(StringIO(json.dumps(df))))
# st.write(mStatus._data)

# UI slider
with st.sidebar:
    # Rebuild data
    if st.button('Rebuild'):
        svOp = mStatus._data['svOption']
        for x in svOp:
            edge = list(map(str, x.split(',')))
            option = svOp[x]

            if option == 'Match':
                addNodesDel(edge)
                addEdgesDel(edge)

                # Update cntMemTeam and cntTryUser
                mStatus._data['cntMemTeam'][edge[0]] += 1
                mStatus._data['cntTryUser'][edge[1]] += 1

                # Update isHustInTeam by isUserAreHust
                if mStatus._data['isUserAreHust'][edge[1]]:
                    mStatus._data['isHustInTeam'][edge[0]] = True

                mStatus._set()

            if option == 'Not match':
                addEdgesDel(edge)
                mStatus._data['cntTryUser'][edge[1]] += 1
                mStatus._set()

            if option == 'Error':
                addEdgesDel(edge)

        mStatus._set()
        write_df(df)
        st.rerun()

    # Upload file
    with st.form("my-form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Choose a csv file", type='csv')
        submitted = st.form_submit_button("submit")

        if submitted and uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            with open('list.csv', 'wb') as tempf:
                tempf.write(bytes_data)

            st.cache_resource.clear()
            mStatus._data["df"] = csvData.read(namesCol).to_json(orient='records')
            mStatus._set()
            st.rerun()

    # Clear cache
    if st.button('Clear all cache'):
        st.cache_resource.clear()
        mStatus._data = makeEmptyStatus()
        mStatus._set()
        st.rerun()

    # Select mode
    modeUI = st.radio(
        "Chọn mode",
        ('Matching', 'Result', 'Table'))

# st.write(mStatus.get_value("nodesDel"))
# st.write(mStatus.get_value("edegesDel"))

# UI main
with st.container():
    # Split data to team and single user
    singleUsers = {
        str(i["id"]): {
            k: i[k] for k in i if k in listTypeSingle
        } for i in df if i[namesCol[1]] == nameRoleUser
    }
    teams = {
        str(i["id"]): {
            k: i[k] for k in i if k in listTypeTeam
        } for i in df if i[namesCol[1]] == nameRoleTeam
    }
    # index data
    singleUsersList = [str(i["id"]) for i in df if i[namesCol[1]] == nameRoleUser]
    teamList = [str(i["id"]) for i in df if i[namesCol[1]] == nameRoleTeam]

    backupStatus = mStatus._data

    idOp = {
        "Unknow": 0,
        "Match": 1,
        "Not match": 2,
        "Error": 3,
    }
    svOp = mStatus._data['svOption']

    # st.write(teamList)
    # st.write(singleUsersList)
    
    # Show to UI
    if modeUI == "Matching":
        # Write to temp file for exe
        apiCController.write(
            df,
            mStatus.get_value("nodesDel"),
            mStatus.get_value("edegesDel"),
            mStatus.get_value("cntMemTeam"),
            mStatus.get_value("cntTryUser"),
            mStatus.get_value("isHustInTeam"),
            mStatus.get_value("isUserAreHust"),
        )
        # Run matching
        apiCController.run()
        # Read result
        listEdges = apiCController.read()
        # st.write(apiCController.edges)

        # Show list edges for matching
        for edgeRaw in listEdges:
            edge = edgeRaw["edge"]
            pointEdge = edgeRaw["point"]
            isHustInTeam = edgeRaw["isHustInTeam"]
            isUserAreHust = edgeRaw["isUserAreHust"]
            # st.write(edge)
            # Check edge is valid
            if (edge[0] not in teamList) or (edge[1] not in singleUsersList):
                continue

            with st.container():
                st.text("Edge ({0}) -> ({1}), weight ({2}), isHustInTeam ({3}), isUserAreHust ({4})".format(edge[0], edge[1], pointEdge, isHustInTeam, isUserAreHust))
                col1, col2, col3 = st.columns([3, 3, 1])
                with col1:
                    st.dataframe(teams[edge[0]], width=600, height=200)
                with col2:
                    st.dataframe(
                        singleUsers[edge[1]], width=600, height=200)
                with col3:
                    indexOx = 0
                    edgeStr = ','.join(map(str, edge))
                    if svOp.get(edgeStr) is not None:
                        indexOx = idOp[svOp[edgeStr]]
                    option = st.selectbox(
                        'Select', idOp.keys(), index=indexOx, key=edgeStr)
                    mStatus._data['svOption'][edgeStr] = option
                    mStatus._set()

                    cvDict = teams[edge[0]]
                    strCvTeam = ""
                    for x in cvDict:
                        strCvTeam += "{0}: {1}\n".format(x, cvDict[x])

                    st.download_button(
                        label="CV Teams",
                        data=strCvTeam,
                        file_name='cvTeams_{0}.txt'.format(edge[0]),
                        mime='text',
                        key=edgeStr + "_cvteam",
                    )

                    cvDict = singleUsers[edge[1]]
                    strCvPer = ""
                    for x in cvDict:
                        strCvPer += "{0}: {1}\n".format(x, cvDict[x])

                    st.download_button(
                        label="CV Personal",
                        data=strCvPer,
                        file_name='cvPersonal_{0}.txt'.format(edge[1]),
                        mime='text',
                        key=edgeStr + "_cvpersonal",
                    )
                st.markdown("""---""")

    elif modeUI == "Result":
        listEdges = mStatus.get_value("edegesDel")

        for edge in listEdges:
            pointEdge = default_caculate_match(
                df[int(edge[0])], df[int(edge[1])],
                mStatus._data["isHustInTeam"][edge[0]], mStatus._data["isUserAreHust"][edge[1]]
            )
            isHustInTeam = mStatus._data["isHustInTeam"][edge[0]]
            isUserAreHust = mStatus._data["isUserAreHust"][edge[1]]

            # st.write(edge)
            if (edge[0] not in teamList) or (edge[1] not in singleUsersList):
                continue

            with st.container():
                st.text("Edge ({0}) -> ({1}), weight ({2}), isHustInTeam ({3}), isUserAreHust ({4})".format(edge[0], edge[1], pointEdge, isHustInTeam, isUserAreHust))
                col1, col2, col3 = st.columns([3, 3, 1])
                with col1:
                    st.dataframe(teams[edge[0]], width=600, height=200)
                with col2:
                    st.dataframe(singleUsers[edge[1]], width=600, height=200)
                with col3:
                    indexOx = 0
                    edgeStr = ','.join(map(str, edge))
                    if svOp.get(edgeStr) is not None:
                        indexOx = idOp[svOp[edgeStr]]
                    option = st.selectbox('Select', idOp.keys(), index=indexOx, key=edgeStr, disabled=True)

                    cvDict = teams[edge[0]]
                    strCvTeam = ""
                    for x in cvDict:
                        strCvTeam += "{0}: {1}\n".format(x, cvDict[x])

                    st.download_button(
                        label="CV Teams",
                        data=strCvTeam,
                        file_name='cvTeams_{0}.txt'.format(edge[0]),
                        mime='text',
                        key=edgeStr + "_cvteam",
                    )

                    cvDict = singleUsers[edge[1]]
                    strCvPer = ""
                    for x in cvDict:
                        strCvPer += "{0}: {1}\n".format(x, cvDict[x])

                    st.download_button(
                        label="CV Personal",
                        data=strCvPer,
                        file_name='cvPersonal_{0}.txt'.format(edge[1]),
                        mime='text',
                        key=edgeStr + "_cvpersonal",
                    )
                st.markdown("""---""")

    elif modeUI == "Table":
        st.write(pd.read_json(StringIO(json.dumps(df))))