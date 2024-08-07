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

def autoVaildNewFile():
    try:
        df = csvData.read(namesCol).to_json(orient='records')
        dfDict = json.loads(df)

        # Check vaild type data rule
        for i in dfDict:
            if not checkJSONVaildType(i):
                raise ValueError("File list.csv is not vaild type data rule")
    except Exception as e:
        csvData.resetFile()
        df = csvData.read(namesCol).to_json(orient='records')
        dfDict = json.loads(df)
        st.write("File list.csv is have error, reset file to default. Error: {0}".format(e))
        raise ValueError("File list.csv is have error, reset file to default. Error: {0}".format(e))

# Function check if user is hust
def checkHust(s):
    return countExitStringInString(s, [
        "HUST", "hanoi university of science and technology", "Bách Khoa Hà Nội"
    ])

def makeEmptyStatus():
    try:
        df = csvData.read(namesCol).to_json(orient='records')
        dfDict = json.loads(df)

        # Check vaild type data rule
        for i in dfDict:
            if not checkJSONVaildType(i):
                raise ValueError("File list.csv is not vaild type data rule")
    except Exception as e:
        csvData.resetFile()
        df = csvData.read(namesCol).to_json(orient='records')
        dfDict = json.loads(df)
        raise ValueError("File list.csv is have error, reset file to default. Error: {0}".format(e))

    cntMemTeam = {}
    cntTryUser = {}
    isHustInTeam = {}
    isUserAreHust = {}

    # Build list
    for i in dfDict:
        if i[namesCol[iN2Id["role"]]] == nameRoleTeam:
            cntMemTeam[i["id"]] = max(int(i[namesCol[iN2Id["numMemCur"]]]), maxOfMemberPerTeam - int(i[namesCol[iN2Id["numMemWant"]]]))
            isHustInTeam[i["id"]] = checkHust(i[namesCol[iN2Id["hustInTeam"]]])

        if i[namesCol[iN2Id["role"]]] == nameRoleUser:
            cntTryUser[i["id"]] = 0
            isUserAreHust[i["id"]] = checkHust(i[namesCol[iN2Id["userAreHust"]]])

    return {
        "df": df,
        "nodesDel": [],
        "edegesDel": [],
        "resultEdges": [],
        "cntMemTeam": cntMemTeam,
        "isHustInTeam": isHustInTeam,
        "isUserAreHust": isUserAreHust,
        "cntTryUser": cntTryUser,
        "svOption": dict(),
        "svOptionPrev": dict(),
    }

def update_account_status(mStatus):
    cntMemTeam = mStatus._data['cntMemTeam']
    cntTryUser = mStatus._data['cntTryUser']
    isHustInTeam = mStatus._data['isHustInTeam']
    isUserAreHust = mStatus._data['isUserAreHust']

    dfDict = json.loads(mStatus.get_value("df"))

    # Build list
    for i in dfDict:
        if i[namesCol[iN2Id["role"]]] == nameRoleTeam:
            if i["id"] not in cntMemTeam:
                cntMemTeam[i["id"]] = max(int(i[namesCol[iN2Id["numMemCur"]]]), maxOfMemberPerTeam - int(i[namesCol[iN2Id["numMemWant"]]]))
            if i["id"] not in isHustInTeam:
                isHustInTeam[i["id"]] = checkHust(i[namesCol[iN2Id["hustInTeam"]]])

        if i[namesCol[iN2Id["role"]]] == nameRoleUser:
            if i["id"] not in cntTryUser:
                cntTryUser[i["id"]] = 0
            if i["id"] not in isUserAreHust:
                isUserAreHust[i["id"]] = checkHust(i[namesCol[iN2Id["userAreHust"]]])
    
    # Update status
    mStatus._data['cntMemTeam'] = cntMemTeam
    mStatus._data['cntTryUser'] = cntTryUser
    mStatus._data['isHustInTeam'] = isHustInTeam
    mStatus._data['isUserAreHust'] = isUserAreHust

    mStatus._set()

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
def addSingleNodeDel(node):
    if node not in mStatus._data['nodesDel']:
        mStatus._data['nodesDel'].append(node)
def addEdgesDel(edge):
    if edge not in mStatus._data['edegesDel']:
        mStatus._data['edegesDel'].append(edge)
def addResultEdges(edge):
    if edge not in mStatus._data['resultEdges']:
        mStatus._data['resultEdges'].append(edge)
def delNodesDel(edge):
    if edge[1] in mStatus._data['nodesDel']:
        mStatus._data['nodesDel'].remove(edge[1])
def delSingleNodeDel(node):
    if node in mStatus._data['nodesDel']:
        mStatus._data['nodesDel'].remove(node)
def delEdgesDel(edge):
    if edge in mStatus._data['edegesDel']:
        mStatus._data['edegesDel'].remove(edge)
def delResultEdges(edge):
    if edge in mStatus._data['resultEdges']:
        mStatus._data['resultEdges'].remove(edge)

# Read data and constant
mStatus._get()
df = read_df()
modeUI = "Matching"
# st.write(pd.read_json(StringIO(json.dumps(df))))
# st.write(mStatus._data)

# UI slider
with st.sidebar:
    # Rebuild data
    if st.button('Update and find new'):
        svOp = mStatus._data['svOption']
        svOptionPrev = mStatus._data['svOptionPrev']

        # Reverse status by svOptionPrev
        for x in svOptionPrev:
            edge = list(map(str, x.split(',')))
            option = svOptionPrev[x]

            if option == 'Match':
                delNodesDel(edge)
                delEdgesDel(edge)
                delResultEdges(edge)

                # Update cntMemTeam and cntTryUser
                mStatus._data['cntMemTeam'][edge[0]] -= 1
                mStatus._data['cntTryUser'][edge[1]] -= 1

                # Update isHustInTeam by isUserAreHust
                mStatus._data['isHustInTeam'][edge[0]] -= mStatus._data['isUserAreHust'][edge[1]]

            if option == 'Not match':
                delEdgesDel(edge)
                mStatus._data['cntTryUser'][edge[1]] -= 1
            
            if option == 'Error':
                delEdgesDel(edge)

        # Update status for new matching
        for x in svOp:
            edge = list(map(str, x.split(',')))
            option = svOp[x]

            if option == 'Match':
                addNodesDel(edge)
                addEdgesDel(edge)
                addResultEdges(edge)

                # Update cntMemTeam and cntTryUser
                mStatus._data['cntMemTeam'][edge[0]] += 1
                mStatus._data['cntTryUser'][edge[1]] += 1

                # Update isHustInTeam by isUserAreHust
                mStatus._data['isHustInTeam'][edge[0]] += mStatus._data['isUserAreHust'][edge[1]]

            if option == 'Not match':
                addEdgesDel(edge)
                mStatus._data['cntTryUser'][edge[1]] += 1

            if option == 'Error':
                addEdgesDel(edge)

            mStatus._data['svOptionPrev'] = mStatus._data['svOption']

        mStatus._set()
        write_df(df)
        st.rerun()

    with st.expander("See tutorial"):
        st.markdown('Sau khi đã đặt trạng thái ("match", "not match", "Error") cho 1 hoặc nhiều cạnh, nhấn "Update and find new" để cập nhật dữ liệu matching và tìm matching mới nếu có.')
        st.markdown('Một số matching không hiện vì đã có đủ matching cho team hoặc user đó. Và cần phải đặt trạng thái cho các matching đang hiện trước khi tìm matching mới.')
        st.markdown('Lưu ý: Các trạng thái đã đặt sẽ hiện ở mục menu "Result".')
        st.markdown('Trạng thái "Unknow" sẽ không thay đổi khi nhấn "Update and find new". Và cạnh đấy sẽ tiếp tục hiện ở lần tìm matching tiếp theo.')
        st.markdown('Trạng thái "Match" sẽ tăng số lượng thành viên trong team lên 1 đơn vị (hiện tại số thành viên team tối đa là 6), đặt trạng thái cho user là đã có team và cập nhật trạng thái "isHustInTeam" của team.')
        st.markdown('Trạng thái "Not Match" sẽ tăng số lần thử của user lên 1 đơn vị (số lần user được thử mathcing là 3).')
        st.markdown('Trạng thái "Error" dùng cho các cạnh lỗi logic hoặc sự cố hi hữu, matching trạng thái sẽ này sẽ bị xóa khỏi danh sách matching nhưng không làm thay đổi bất kỳ trạng thái hay thông tin nào khác.')

    with st.expander("Which matching not show"):
        st.markdown('- Các cạnh đã được đặt trạng thái "Match" hoặc "Not match" hoặc "Error".')
        st.markdown('- Mỗi user chỉ hiện 1 lần mỗi đợt matching.')
        st.markdown('- Các cạnh mà số cạnh đã hiện đủ số lần thử hoặc đã đủ số thành viên trong team.')
        st.markdown('- Các cạnh mà 1 trong 2 node đã bị xóa.')
        st.markdown('- Các cạnh mà team chưa có thành viên là HUST và user không phải là HUST (Tức bắt buộc phải đảm bảo team có HUST hoặc cạnh có user là HUST còn nếu không thì không cho matching với bất kỳ ai khác, tránh việc team sau khi matching thì lại không có HUST để match không đủ điều kiện tham gia và gây lãng phí tài nguyên).')

    with st.expander("Copyright"):
        st.markdown('- Developed by HotaMago')
        st.markdown('- Facebook Author: [HotaMago](https://www.facebook.com/hotamago)')
        st.markdown('- The project was built for HIEC club and Techstart event.')

    st.divider()

    # Select mode
    modeUI = st.radio(
        "Chọn mode",
        ('Matching', 'Final match', 'Deleted match', 'Table', 'List Node', 'Team non HUST', 'Bad matching', 'Cache status'))
    
    st.divider()

    # Upload file
    with st.form("my-form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Choose a csv file", type='csv')
        submitted = st.form_submit_button("submit")

        if submitted and uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()

            with open('list.csv', 'wb') as tempf:
                tempf.write(bytes_data)

            try:
                autoVaildNewFile()
                mStatus._data["df"] = csvData.read(namesCol).to_json(orient='records')
                mStatus._set()
            except:
                pass

            update_account_status(mStatus)

            st.cache_resource.clear()
            st.rerun()

    st.divider()

    # Clear cache
    if st.button('Clear all cache'):
        st.cache_resource.clear()
        mStatus._data = makeEmptyStatus()
        mStatus._set()
        st.rerun()

# st.write(mStatus.get_value("nodesDel"))
# st.write(mStatus.get_value("edegesDel"))

# Component
def matchingInteractive(edge, pointEdge, isHustInTeam, isUserAreHust):
    with st.container():
        st.text("Edge ({0}) -> ({1}), weight ({2}), isHustInTeam ({3}), isUserAreHust ({4}), numMember ({5}), numTriedOfUser ({6})".format(edge[0], edge[1], pointEdge, isHustInTeam, isUserAreHust, mStatus._data["cntMemTeam"][edge[0]], mStatus._data["cntTryUser"][edge[1]]))
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

            cvDict = teamsCV[edge[0]]
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

            cvDict = singleUsersCV[edge[1]]
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
        st.divider()

# UI main
with st.container():
    # Get all node
    # Split data to team and single user
    singleUsers = {
        str(i["id"]): {
            k: i[k] for k in i if k in listTypeSingle
        } for i in df if i[namesCol[iN2Id["role"]]] == nameRoleUser
    }
    teams = {
        str(i["id"]): {
            k: i[k] for k in i if k in listTypeTeam
        } for i in df if i[namesCol[iN2Id["role"]]] == nameRoleTeam
    }
    # Split data to team and single user with delete info data
    singleUsersCV = {
        str(i["id"]): {
            k: i[k] for k in i if k in listTypeSingleCV
        } for i in df if i[namesCol[iN2Id["role"]]] == nameRoleUser
    }
    teamsCV = {
        str(i["id"]): {
            k: i[k] for k in i if k in listTypeTeamCV
        } for i in df if i[namesCol[iN2Id["role"]]] == nameRoleTeam
    }
    # index data
    singleUsersList = [str(i["id"]) for i in df if i[namesCol[iN2Id["role"]]] == nameRoleUser]
    teamList = [str(i["id"]) for i in df if i[namesCol[iN2Id["role"]]] == nameRoleTeam]

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

            matchingInteractive(edge, pointEdge, isHustInTeam, isUserAreHust)

    elif modeUI == "Final match":
        listEdges = mStatus.get_value("resultEdges")

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

            matchingInteractive(edge, pointEdge, isHustInTeam, isUserAreHust)

    elif modeUI == "Deleted match":
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

            matchingInteractive(edge, pointEdge, isHustInTeam, isUserAreHust)

    elif modeUI == "Table":
        st.write(pd.read_json(StringIO(json.dumps(df))))

    elif modeUI == "List Node":
        def nodeStatusCompoment(nameRow, index, key_prefix, dataFrame):
            st.write(nameRow)
            with st.container():
                col1, col2 = st.columns([5, 2])
                with col1:
                    st.dataframe(dataFrame, width=600, height=200)

                indexOx = 0
                if index in mStatus._data["nodesDel"]:
                    indexOx = 1
                dictOp = {
                    "Active": 0,
                    "Delete": 1,
                }
                with col2:
                    option = st.selectbox('Select', dictOp, index=indexOx, key="{0}_{1}".format(key_prefix, index))

                # st.write("{0} - {1}".format(indexOx, dictOp[option]))

                # Reverse status
                if indexOx == 1:
                    delSingleNodeDel(index)
                
                # Update status
                if dictOp[option] == 1:
                    addSingleNodeDel(index)

                mStatus._set()
            st.divider()

        for i in teamList:
            nodeStatusCompoment("Team {0}".format(i), i, "node_status_t_", teams[i])

        for i in singleUsersList:
            nodeStatusCompoment("Member {0}".format(i), i, "node_status_m_", singleUsers[i])

    elif modeUI == "Team non HUST":
        for i in teamList:
            if mStatus._data["isHustInTeam"][i] <= 0:
                with st.container():
                    col1, col2 = st.columns([6, 1])
                    with col1:
                        st.dataframe(teams[i], width=600, height=200)
                    with col2:
                        cvDict = teamsCV[i]
                        strCvTeam = ""
                        for x in cvDict:
                            strCvTeam += "{0}: {1}\n".format(x, cvDict[x])

                        st.download_button(
                            label="CV Teams",
                            data=strCvTeam,
                            file_name='cvTeams_{0}.txt'.format(i),
                            mime='text',
                            key=i + "_cvteam",
                        )

                    st.divider()

    elif modeUI == "Bad matching":
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
        listEdges = apiCController.badRes

        # Show list edges for matching
        for edgeRaw in listEdges:
            edge = edgeRaw["edge"]
            pointEdge = edgeRaw["point"]
            isHustInTeam = edgeRaw["isHustInTeam"]
            isUserAreHust = edgeRaw["isUserAreHust"]
            # Check edge is valid
            if (edge[0] not in teamList) or (edge[1] not in singleUsersList):
                continue

            matchingInteractive(edge, pointEdge, isHustInTeam, isUserAreHust)

    elif modeUI == "Cache status":
        st.json(mStatus._data)