from mainConfig import *
from functools import cmp_to_key
from datetime import datetime

def convertStr2Unix(timestr):
    return datetime.strptime(timestr, '%d/%m/%Y %H:%M:%S').timestamp()

class ApiCController():
    def __init__(self):
        pass

    def write(self, df, nodesDel, edgesDel, cntMemTeam, cntTryUser, isHustInTeam, isUserAreHust):
        self.df = df
        self.nodesDel = nodesDel
        self.edgesDel = edgesDel
        self.cntMemTeam = cntMemTeam
        self.cntTryUser = cntTryUser
        self.isHustInTeam = isHustInTeam
        self.isUserAreHust = isUserAreHust

    def run(self):
        singleUsersList = [str(i["id"]) for i in self.df if i[namesCol[iN2Id["role"]]] == nameRoleUser]
        teamList = [str(i["id"]) for i in self.df if i[namesCol[iN2Id["role"]]] == nameRoleTeam]

        # Prepare data
        edges = []
        for i in range(len(teamList)):
            for j in range(len(singleUsersList)):
                # Check if node or edge is deleted
                if teamList[i] in self.nodesDel or singleUsersList[j] in self.nodesDel:
                    continue
                # Check if edge is deleted
                if ([teamList[i], singleUsersList[j]] in self.edgesDel):
                    continue
                # Add edge
                edges.append([teamList[i], singleUsersList[j]])

        # Compare function
        def compare_pair(ea, eb):
            ea_0 = self.df[int(ea[0])]
            ea_1 = self.df[int(ea[1])]
            eb_0 = self.df[int(eb[0])]
            eb_1 = self.df[int(eb[1])]

            # Sort by time of register
            timeA_0 = convertStr2Unix(ea_0[namesCol[iN2Id["time"]]])
            timeA_1 = convertStr2Unix(ea_1[namesCol[iN2Id["time"]]])
            timeB_0 = convertStr2Unix(eb_0[namesCol[iN2Id["time"]]])
            timeB_1 = convertStr2Unix(eb_1[namesCol[iN2Id["time"]]])

            # calculate point
            pointValueA = default_caculate_match(ea_0, ea_1, self.isHustInTeam[ea[0]], self.isUserAreHust[ea[1]])
            pointValueB = default_caculate_match(eb_0, eb_1, self.isHustInTeam[eb[0]], self.isUserAreHust[eb[1]])

            if timeA_0 != timeB_0:
                return timeA_0 - timeB_0
            else:
                # Compare greater point first
                if pointValueA != pointValueB:
                    return pointValueB - pointValueA
                else:
                    return timeA_1 - timeB_1

        # Sort
        edges.sort(key=cmp_to_key(compare_pair))

        # Filler
        self.res = []
        # Copy of cntMemTeam and cntTryUser
        cntMemTeam = self.cntMemTeam.copy()
        cntTryUser = self.cntTryUser.copy()
        for edge in edges:
            # Check if team or user is full
            if cntMemTeam[edge[0]] >= maxOfMemberPerTeam or cntTryUser[edge[1]] >= maxOfTeamPerUsers:
                continue
            # Check if team or user one of them is hust
            if (not self.isHustInTeam[edge[0]]) and (not self.isUserAreHust[edge[1]]):
                continue
            # Add edge
            self.res.append({
                "edge": edge,
                "point": default_caculate_match(
                    self.df[int(edge[0])],
                    self.df[int(edge[1])],
                    self.isHustInTeam[edge[0]],
                    self.isUserAreHust[edge[1]]
                ),
                "isHustInTeam": self.isHustInTeam[edge[0]],
                "isUserAreHust": self.isUserAreHust[edge[1]]
            })
            # Increase cntMemTeam and cntTryUser
            cntMemTeam[edge[0]] += 1
            cntTryUser[edge[1]] += 1

    def read(self):
        return self.res