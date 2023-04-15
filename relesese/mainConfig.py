maxOfMemberPerTeam = 6
maxOfTeamPerUsers = 3
nameRoleUser = "Cá nhân mong muốn tìm được đội thi phù hợp"
nameRoleTeam = "Đội thi và đang tìm kiếm thêm thành viên"

namesCol = {
    'Timestamp': 'time',
    'Bạn đăng ký tham gia ghép đội với vai trò là': 'role',
    'Họ và tên nhóm trưởng': 'nameLeader',
    'SĐT nhóm trưởng': 'sdtLeader',
    'Email nhóm trưởng': 'emailLeader',
    'Facebook nhóm trưởng': 'facebookLeader',
    'Lĩnh vực của dự án': 'typeProject',
    'Thông tin về cơ cấu nhân sự của dự án': 'infoMemberStruct',
    'Mô tả sơ lược ý tưởng của dự án': 'shortIdea',
    'Giai đoạn phát triển của dự án:': 'statusProject',
    'Số thành viên hiện có': 'numberMember',
    'Thông tin về kĩ năng của các thành viên trong đội': 'infoMemberSill',
    'Thông tin về thành tựu của các thành viên trong đội (nếu có)': 'infoGoalMember',
    'Số thành viên mong muốn kết nạp': 'numberRequestAddin',
    'Mô tả chân dung thành viên mong muốn kết nạp vào đội': 'profileRequest',
    'Thời gian dự kiến đồng hành': 'thoigiandonghanh',
    'Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 1)': 'request01',
    'Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 2)': 'request02',
    'Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 3)': 'request03',
    'Thế mạnh chuyên môn của thành viên mong muốn kết nạp (thành viên 4)': 'request04',

    'Họ và tên của bạn': 'name_re',
    'Ngày tháng năm sinh của bạn': 'birth_re',
    'SĐT của bạn': 'sdt_re',
    'Email của bạn': 'email_re',
    'Facebook của bạn': 'facebook_re',
    '3 lĩnh vực bạn tự tin nhất ở bản thân': 'nicework_re',
    '3 thành tích ấn tượng nhất bạn đã đạt được ': 'profile_re',
    '3 lĩnh vực của đội thi mà bạn mong muốn được ghép cặp': 'teamRequest_re',
    'Bạn đã có ý tưởng rõ ràng chưa? Nếu có hãy mô tả sơ lược về ý tưởng mong muốn theo đổi là gì?': 'idea_re',
}

listTypeSingle = ['id', 'time', 'role', 'name_re', 'birth_re', 'sdt_re', 'email_re', 'facebook_re', 'nicework_re',
             'profile_re', 'teamRequest_re', 'idea_re']
listTypeTeam = ['id', 'time', 'role', 'nameLeader', 'sdtLeader', 'emailLeader', 'facebookLeader', 'typeProject',
             'infoMemberStruct', 'shortIdea', 'statusProject', 'numberMember', 'numberRequestAddin', 'profileRequest', 'thoigiandonghanh', 'request01', 'request02', 'request03', 'request04']

dtypesCol = {
    "time": str,
    "role": str,
    "nameLeader": str,
    "sdtLeader": str,
    "emailLeader": str,
    "facebookLeader": str,
    "typeProject": str,
    "infoMemberStruct": str,
    "shortIdea": str,
    "statusProject": str,
    "numberMember": 'Int64',
    "numberRequestAddin": 'Int64',
    "profileRequest": str,
    "thoigiandonghanh": str,
    "request01": str,
    "request02": str,
    "request03": str,
    "request04": str,

    "name_re": str,
    "birth_re": str,
    "sdt_re": str,
    "email_re": str,
    "facebook_re": str,
    "nicework_re": str,
    "profile_re": str,
    "teamRequest_re": str,
    "idea_re": str,
}

idLabel = [
    'Cơ khí & Chế tạo máy',
    'Công nghệ sinh học',
    'Công nghệ thông tin',
    'Công nghệ môi trường',
    'Công nghệ vật liệu',
    'Công nghệ hóa học',
    'Công nghệ điện - điện tử',
    'Quản lý',
    'Kinh doanh',
    'Tài chính',
    'Truyền thông'
]

valueNan = {
    "thoigiandonghanh": "",
    "request01": "",
    "request02": "",
    "request03": "",
    "request04": "",

    "nicework_re": "",
    "teamRequest_re": "",
    "idea_re": "",
}
