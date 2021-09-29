import logging

import auth

logger = logging.Logger


def get_sheet(client, spread_name, sheet_name, col_num):
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    google_sheet = client.open(spread_name)
    # Extract and print all of the values
    sheet = google_sheet.worksheet(sheet_name)
    sheet_data = []
    for i in range(0, col_num):
        col_values = sheet.col_values(i + 1)
        col_values.pop(0)
        sheet_data.append(col_values)

    return sheet_data


def update_user_inven(user_list, user_name, equip_list):
    EQUIPB = 5
    EQUIPC = 6
    num_B = 0
    num_C = 0

    num_B = get_user_data(user_list, user_name, EQUIPB)
    num_C = get_user_data(user_list, user_name, EQUIPC)

    update_user_data(user_list, user_name, EQUIPB, int(num_B) + equip_list[2])
    update_user_data(user_list, user_name, EQUIPC, int(num_C) + equip_list[3])

    return


def open_file(filename):
    with open(filename, 'r') as f:
        last_line = f.readlines()[-1]
    return last_line


def update_file(filename, value):
    with open(filename, 'w') as f:
        f.write("%s\n" % value)
    return


def get_user_data(user_list, user_name, status_name):
    client = auth.google_auth()
    user_number = -1

    # search the # of user name
    for name in user_list:
        if name == user_name:
            user_number = user_list.index(name)

    if user_number == -1:
        print("존재하지 않는 유저명입니다.")
        return 0
    else:
        # 크리스탈=2, 스테미나=3, 떡밥=4
        return client.open("플레이어").worksheet("player_data").cell(user_number + 2, status_name).value


def update_user_data(user_list, user_name, status_name, value):
    client = auth.google_auth()
    user_number = -1

    # search the # of user name
    for i, name in enumerate(user_list):
        if name == user_name:
            user_number = i

    if user_number == -1:
        print("존재하지 않는 유저명입니다.")

    else:
        # 크리스탈=2, 스테미나=3, 떡밥=4
        client.open("플레이어").worksheet("player_data").update_cell(user_number + 2, status_name, value)
    return
