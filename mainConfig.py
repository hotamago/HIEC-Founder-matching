maxOfMemberPerTeam = 6
maxOfTeamPerUsers = 3

# Name of role
nameRoleUser = "Cá nhân mong muốn tìm được đội thi phù hợp"
nameRoleTeam = "Đội thi và đang tìm kiếm thêm thành viên"

namesCol = """
Dấu thời gian
Bạn đăng ký tham gia ghép đội với vai trò là
Họ và tên nhóm trưởng
SĐT nhóm trưởng
Email nhóm trưởng
Facebook nhóm trưởng
Lĩnh vực của dự án
Thông tin về cơ cấu nhân sự của dự án
Mô tả sơ lược ý tưởng của dự án
Giai đoạn phát triển của dự án
Số thành viên hiện có
Thông tin về kỹ năng của các thành viên trong đội
Thông tin về thành tựu của các thành viên trong đội (nếu có)
Số thành viên mong muốn kết nạp
Mô tả chân dung thành viên mong muốn kết nạp vào đội
Thời gian dự kiến đồng hành
Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 1)
Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 2)
Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 3)
Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 4):
Họ và tên của bạn
Ngày tháng năm sinh của bạn
SĐT của bạn
Email của bạn
Facebook của bạn
Trường (Đại học) hiện đang theo học
CV của bạn
3 lĩnh vực bạn tự tin nhất ở bản thân
Mô tả các kỹ năng mà bạn thông thạo nhất
3 lĩnh vực của đội thi mà bạn mong muốn được ghép cặp
Trình bày ý tưởng mà bản thân đang ấp ủ. Nếu không có, điền N/A
"""
namesCol = namesCol.split("\n")[1:-1]

# Alice name to index
iN2Id = {
    "time": 0,
    "role": 1,
    "numMemCur": 10,
    "numMemWant": 13,
    "hustInTeam": 7,
    "userAreHust": -6,
}

# Check vaild type data rule
vaildTypeRule = {
    "time": "str",
    "role": "str",
    "numMemCur": "int",
    "numMemWant": "int",
    "hustInTeam": "int",
    "userAreHust": "int",
}
def checkJSONVaildType(jsonData):
    for iraw in jsonData.keys():
        i = iN2Id.get(iraw, None)
        if i is None:
            continue
        if vaildTypeRule.get(i, None) is not None:
            if vaildTypeRule[i] == "int":
                try:
                    int(jsonData[i])
                except:
                    return False
            elif vaildTypeRule[i] == "str":
                if type(jsonData[i]) != str:
                    return False
    return True

# Split data
listTypeSingle = [*namesCol[:2], *namesCol[-11:]]
listTypeTeam = [*namesCol[:-11]]

# Split data for cv
listTypeSingleCV = [*namesCol[-11:-9], *namesCol[-6:]]
listTypeTeamCV = [*namesCol[2:3], *namesCol[6:-11]]


# Helper function
# Function to lower case, remove space and remove special character, remove accent, replace vietnamese character to english character
def goodString2Cmp(s):
    sLow = s.lower()
    listChar2Replace = {
        "a": "áàảãạăắằẳẵặâấầẩẫậ",
        "d": "đ",
        "e": "éèẻẽẹêếềểễệ",
        "i": "íìỉĩị",
        "o": "óòỏõọôốồổỗộơớờởỡợ",
        "u": "úùủũụưứừửữự",
        "y": "ýỳỷỹỵ",
        # Special character
        "": ".,;:?!@#$%^&*()_+-=[]{}|\/<>\"\'",
        # Space
        "": " \t\n",
    }

    for i in listChar2Replace.keys():
        for j in listChar2Replace[i]:
            sLow = sLow.replace(j, i)

    return sLow
                                      
# Check if any string in list is in another string
def countExitStringInString(smain, listSub):
    cnt = 0
    for i in listSub:
        cnt += goodString2Cmp(smain).count(goodString2Cmp(i))
    return cnt

# Compare function
def default_caculate_match(a, b, isHustInTeam, isUserAreHust):
    ajson = a
    bjson = b

    # a, b is data of row
    # a is team, b is single user
    listAHave = [bjson[namesCol[6]]]
    listAWantB = [ajson[i] for i in ajson.keys() if i in namesCol[16:20]]
    listBHave = bjson[namesCol[-4]].split(", ")
    listBWantA = bjson[namesCol[-2]].split(", ")

    pointValue = 0.0

    # If A want B then add 2 point
    for i in listAWantB:
        if i in listBHave:
            pointValue += 2
            break

    # If B want A then add 1 point
    for i in listBWantA:
        if i in listAHave:
            pointValue += 1

    
    if isHustInTeam <= 0 and isUserAreHust >= 1:
        pointValue += 4

    return pointValue