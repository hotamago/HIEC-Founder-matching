import pandas as pd
import os
import datetime
import numpy as np

from mainConfig import *


def replanceLabel(_df, irow, col):
    arr = _df[irow][col].split(",")
    for j in range(len(arr)):
        ss = arr[j].strip()
        if ss in idLabel:
            arr[j] = idLabel.index(ss)
        else:
            arr[j] = -1
    _df[irow][col] = ','.join(map(str, arr))
    # _df[0, _df.columns.get_loc('id')] = ','.join(map(str, arr))
    # _df.at[irow, col] = ','.join(map(str, arr))


def replanceLabels(_df, cols):
    for i in range(len(_df)):
        for col in cols:
            replanceLabel(_df, i, col)


def fileWritelabels(tempf, line):
    labels = line.split(",")
    tempf.write("{0} ".format(len(labels)))
    for label in labels:
        tempf.write("{0} ".format(label))


class ApiCController():
    def __init__(self, exePath="hotaMatching.exe", nameTemp="temp"):
        self.exePath = exePath
        self.nameTemp = nameTemp

    def write(self, df, nodesDel, edgesDel):
        singleUsers = df.query("`role` == '{0}'".format(nameRoleUser)).loc[:, [
            'id', 'time', 'nicework_re', 'teamRequest_re']]
        teams = df.query("`role` == '{0}'".format(nameRoleTeam)).loc[:, [
            'id', 'time', 'typeProject', 'numberMember', 'numberRequestAddin', 'request01', 'request02', 'request03', 'request04']]
        # print(len(singleUsers), "| ", len(teams))

        line_singleUsers = singleUsers.values.tolist()
        line_teams = teams.values.tolist()

        replanceLabels(line_singleUsers, [2, 3])
        replanceLabels(line_teams, [2, 5, 6, 7, 8])

        for i in range(len(line_singleUsers)):
            line_singleUsers[i][1] = int(datetime.datetime.strptime(
                line_singleUsers[i][1], '%m/%d/%Y %H:%M:%S').timestamp())
            line_singleUsers[i].append(maxOfTeamPerUsers)

        line_teams_std = []
        for team in line_teams:
            arr = []
            arr.append(team[0])
            arr.append(int(datetime.datetime.strptime(
                team[1], '%m/%d/%Y %H:%M:%S').timestamp()))
            arr.append(team[2])
            request_temp = []
            for i in range(4, len(team)):
                if team[i] != '-1':
                    request_temp.append(team[i])
            arr.append(
                min([maxOfMemberPerTeam - team[3], team[4], len(request_temp)]))
            arr.append(','.join(map(str, request_temp)))
            line_teams_std.append(arr)

        with open('{0}.inp'.format(self.nameTemp), "wt") as tempf:
            # Users
            tempf.write("{0}\n".format(len(line_singleUsers)))
            for line in line_singleUsers:
                tempf.write("{0} {1} {2}\n".format(line[0], line[1], line[4]))
                fileWritelabels(tempf, line[2])
                tempf.write("\n")
                fileWritelabels(tempf, line[3])
                tempf.write("\n")

            # Teams
            tempf.write("{0}\n".format(len(line_teams_std)))
            for line in line_teams_std:
                tempf.write("{0} {1} {2}\n".format(line[0], line[1], line[3]))
                fileWritelabels(tempf, line[2])
                tempf.write("\n")
                fileWritelabels(tempf, line[4])
                tempf.write("\n")

            # Del node
            tempf.write("{0}\n".format(len(nodesDel)))
            for ele in nodesDel:
                tempf.write("{0}\n".format(ele))

            # Del edge
            tempf.write("{0}\n".format(len(edgesDel)))
            for ele in edgesDel:
                tempf.write("{0} {1}\n".format(ele[0], ele[1]))

    def run(self):
        os.system(self.exePath)

    def read(self):
        with open("{0}.out".format(self.nameTemp), "rt") as tempf:
            result = tempf.read()
        if result.strip() == "":
            return []
        result = result.strip().split("\n")
        for i in range(len(result)):
            result[i] = result[i].strip().split(" ")

        return np.asarray(result, dtype='int').tolist()
