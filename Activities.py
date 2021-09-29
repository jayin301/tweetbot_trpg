from random import randint
import RWData

def todays_fortune():
    value = randint(0, 1000)

    if value == 1:
        return "축하합니다!!! 0.01%의 확률을 뚫은 불운!!!"
    elif value < 50:
        return "[대흉] 대흉과 대길은 확률이 같습니다. 힘내세요 ㅠ^ㅠ"
    elif value < 200:
        return "[중흉] 오늘은 조금 주의해야겠어요."
    elif value < 500:
        return "[흉] 이 정도면 나쁘지 않은 운이네요"
    elif value < 800:
        return "[길] 상쾌한 하루가 되겠네요!"
    elif value < 950:
        return "[중길] 0.5% 확률을 뚫은 행운아!"
    else:
        return "[대길] 축하합니다!! 로또보단 낮지만 어쨌든 엄청난 확률을 손에 쥐셨습니다!"

def generate_eqip_list(sheet_data, user_name):
    equip_list = [0, 0, 0, 0, "normal.png"]

    # get gotcha result
    for i in range(0, 10):
        value = randint(1, 100)
        if value == 100:
            equip_list[0] += 1
            equip_list[4] = "special.png"
        elif value > 89:
            equip_list[1] += 1
            equip_list[4] = "special.png"
        elif value > 53:
            equip_list[2] += 1
        else:
            equip_list[3] += 1
    return equip_list

def print_gotcha_result(sheet_data, sheet_name, equip_list, equip_class):
    # equip class: S=0 A=1 B=2 C=3
    class_name = ["[S급]", "[A급]", "[B급]", "[C급]"]
    col_num = 2 * (equip_class)

    equip_data = sheet_data[sheet_name]
    result_comment = ""

    name = equip_data[col_num]
    detail = equip_data[col_num + 1]

    for i in range(0, equip_list[equip_class]):
        value = randint(0, len(name) - 1)
        if len(name) != len(detail):
            print("google sheet error occur")
            print(value)
            print(len(detail), detail)
            new_value = randint(4, 8)
            result_comment += class_name[equip_class] + name[new_value] + ": " + detail[new_value] + "\n"
        else:
            result_comment += class_name[equip_class] + name[value] + ": " + detail[value] + "\n"

    return result_comment

def print_S_equip(sheet_data, sheet_name, equip_list):
    equip_data = sheet_data[sheet_name]
    result_comment = ""
    image_name = []

    name = equip_data[0]
    detail = equip_data[1]
    image = equip_data[8]

    for i in range(0, equip_list[0]):
        value = randint(0, len(name) - 1)
        if len(name) != len(detail):
            print("google sheet error occur")
            print(value)
            print(len(detail), detail)
            new_value = randint(4, 8)
            result_comment += "[S급]" + name[new_value] + ": " + detail[new_value] + "\n"
            if image[value] != "None":
                image_name.append(image[new_value])
        else:
            result_comment += "[S급]" + name[value] + ": " + detail[value] + "\n"
            if image[value] != "None":
                image_name.append(image[value])
    print(image_name)
    return [image_name, result_comment]


def check_user_status(user_list, user_name, status_name, price):
    status_figure = RWData.get_user_data(user_list, user_name, status_name)

    if int(status_figure) < price:
        return False
    else:
        RWData.update_user_data(user_list, user_name, status_name, int(status_figure) - price)
        return True

def sell_equips(user_list, user_name, sell_B, sell_C):
    EQUIPB = 5
    EQUIPC = 6
    GOLD = 7
    num_B = 0
    num_C = 0

    if sell_B is True:
        num_B = RWData.get_user_data(user_list, user_name, EQUIPB)
        RWData.update_user_data(user_list, user_name, EQUIPB, 0)
    if sell_C is True:
        num_C = RWData.get_user_data(user_list, user_name, EQUIPC)
        RWData.update_user_data(user_list, user_name, EQUIPC, 0)

    if int(num_B) + int(num_C) == 0:
        return "장비가 없습니다. 인벤토리를 확인해주세요."
    else:
        current_gold = RWData.get_user_data(user_list, user_name, GOLD)
        sell_total = 5000 * int(num_B) + 1000 * int(num_C)
        gold_total = int(current_gold) + sell_total
        RWData.update_user_data(user_list, user_name, GOLD, gold_total)
        return "[장비판매]\nB급장비개수: " + str(num_B) + "\nC급장비개수: " + str(num_C) + "\n총가격: " + str(sell_total)

def update_user_inven(user_list, user_name, equip_list):
    EQUIPB = 5
    EQUIPC = 6
    num_B = 0
    num_C = 0

    num_B = RWData.get_user_data(user_list, user_name, EQUIPB)
    num_C = RWData.get_user_data(user_list, user_name, EQUIPC)

    RWData.update_user_data(user_list, user_name, EQUIPB, int(num_B) + equip_list[2])
    RWData.update_user_data(user_list, user_name, EQUIPC, int(num_C) + equip_list[3])

    return

# print result of cooking and hunting
def activity_result(sheet_data, sheet_name):
    activity_data = sheet_data[sheet_name]
    # 시작용 코맨트 랜덤 리스트
    comment_list = activity_data[10]
    image_name = ""

    # 초희귀 10% 희귀 30% 일반 40% 허탕 20%
    value = randint(1, 101)

    if value < 20:
        result_list = activity_data[9]
        comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n" + result_list[
            randint(0, len(result_list) - 1)] + "\n[꽝]"
        return [image_name, comment]

    elif value < 60:
        name = activity_data[6]
        detail = activity_data[7]
        recommend = activity_data[8]
        num = randint(0, len(name) - 1)
        comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n[평범]" + name[num] + "\n" + \
                  detail[num] + "\n\n추천 레시피: " + recommend[num]
        return [image_name, comment]

    elif value < 90:
        name = activity_data[3]
        detail = activity_data[4]
        recommend = activity_data[5]
        num = randint(0, len(name) - 1)
        comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n[희귀]" + name[num] + "\n" + \
                  detail[num] + "\n\n추천 레시피: " + recommend[num]
        return [image_name, comment]

    elif value < 100:
        name = activity_data[0]
        detail = activity_data[1]
        recommend = activity_data[2]
        num = randint(0, len(name) - 1)
        if name[num] == "???":
            current_count = RWData.open_file("event_count.txt")
            RWData.update_file("event_count.txt", int(current_count)+1)
        comment = comment_list[randint(0, len(comment_list) - 1)] + "\n . \n . \n . \n[초희귀]" + name[num] + "\n" + \
                  detail[num] + "\n\n추천 레시피: " + recommend[num]
        return [image_name, comment]

    else:
        name = activity_data[11]
        detail = activity_data[12]
        recommend = activity_data[13]
        num = randint(0, len(name) - 1)
        image_name = activity_data[14][num]
        comment = comment_list[3] + "\n . \n . \n . \n[전설]" + name[num] + "\n" + \
                  detail[num] + "\n\n추천 레시피: " + recommend[num]
        return [image_name, comment]


def random_feature(sheet_data, user_name):
    feature_data = sheet_data['feature_data']
    feature_list = feature_data[0]

    return "[" + user_name + "의 tmi]\n" + feature_list[randint(0, len(feature_list) - 1)]


def cooking(sheet_data):
    food_data = sheet_data['food_data']
    food_names = food_data[0]
    food_details = food_data[1]
    food_materials = food_data[2]
    evaluation = food_data[3]

    list_num = len(food_names)
    value = randint(0, list_num - 1)
    return "[" + food_names[value] + "]\n들어간 재료: " + food_materials[value] + "\n" + food_details[value] + "\n\n한줄평: " + \
           evaluation[randint(0, len(evaluation) - 1)]
