import tweepy
import logging
import time
import Activities
import RWData
import random

logging.basicConfig(level=logging.INFO)

CRYSTAL = 2
STAMINA = 3
BAIT = 4
EQUIPB = 5
EQUIPC = 6
GOLD = 7

def check_mentions(api, keywords, since_id, sheet_data):
    latest_id = since_id
    user_names = sheet_data['user_names'][0]
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        if (int(latest_id) <= tweet.id):
            latest_id = tweet.id
        task_name = ""

        if tweet.in_reply_to_status_id is not None:
            continue

        for keyword in keywords:
            if keyword in tweet.text.lower():
                task_name = keyword
        if task_name != "":
            print(f"Answering to {tweet.user.name}")
            print(tweet.id)
            # save replied tweet's id

            if task_name == "오늘의운세":
                api.update_status(
                    status="@%s" % tweet.user.screen_name + Activities.todays_fortune(),
                    in_reply_to_status_id=tweet.id,
                )

            elif task_name == "[낚시]":
                print("낚시 시작")
                has_enough_bait = Activities.check_user_status(user_names, tweet.user.name, BAIT, 1)
                if has_enough_bait is True:
                    fish_result = Activities.activity_result(sheet_data, "fish_data")
                    if fish_result[0] != "":
                        api.update_with_media(fish_result[0],
                                              status="@%s" % tweet.user.screen_name + fish_result[1],
                                              in_reply_to_status_id=tweet.id,
                                              )
                    else:
                        api.update_status(
                            status="@%s" % tweet.user.screen_name + fish_result[1],
                            in_reply_to_status_id=tweet.id,
                        )
                else:
                    api.update_status(
                        status="@%s" % tweet.user.screen_name
                               + "떡밥이 없거나 없는 유저명입니다. 상점에서 떡밥을 구입하거나 이름을 확인해주세요.",
                        in_reply_to_status_id=tweet.id,
                    )
                time.sleep(2)
            elif task_name == "[사냥]":
                print("사냥 시작")
                has_enough_stamina = Activities.check_user_status(user_names, tweet.user.name, STAMINA, 20)
                if has_enough_stamina is True:
                    hunt_result = Activities.activity_result(sheet_data, "hunt_data")
                    if hunt_result[0] != "":
                        api.update_with_media(hunt_result[0],
                                              status="@%s" % tweet.user.screen_name + hunt_result[1],
                                              in_reply_to_status_id=tweet.id,
                                              )
                    else:
                        api.update_status(
                            status="@%s" % tweet.user.screen_name + hunt_result[1],
                            in_reply_to_status_id=tweet.id,
                        )
                else:
                    api.update_status(
                        status="@%s" % tweet.user.screen_name
                               + "스테미나가 부족하거나 없는 유저명입니다. 상점에서 회복약을 구입하거나 스테미나가 회복될 때까지 기다려주세요.",
                        in_reply_to_status_id=tweet.id,
                    )
                time.sleep(2)
            elif task_name == "[요리]":
                print("요리 시작")
                api.update_status(
                    status="@%s" % tweet.user.screen_name + Activities.cooking(sheet_data),
                    in_reply_to_status_id=tweet.id,
                )

            elif task_name == "[장비뽑기]":
                print("장비 뽑기 시작")
                has_enough_crystal = Activities.check_user_status(user_names, tweet.user.name, CRYSTAL, 3000)
                if has_enough_crystal is True:

                    # check the number of each rate of equipment and upload the image
                    equip_list = Activities.generate_eqip_list(sheet_data, tweet.user.name)
                    api.update_with_media(equip_list[4], "@%s" % tweet.user.screen_name,
                                          in_reply_to_status_id=tweet.id,
                                          )
                    time.sleep(5)
                    # print B,C equipment
                    comment = Activities.print_gotcha_result(sheet_data, "equip_data", equip_list, 3) + Activities.print_gotcha_result(
                        sheet_data, "equip_data", equip_list, 2)
                    for i in range(0, len(comment) // 139 + 1):
                        if comment[i*139:(i + 1) * 139] != '\n':
                            api.update_status(status="@%s " % tweet.user.screen_name + comment[i * 139: (i + 1) * 139],
                                              in_reply_to_status_id=tweet.id,
                                              )
                    # print A,S equipment
                    S_equip = Activities.print_S_equip(sheet_data, "equip_data", equip_list)
                    comment = Activities.print_gotcha_result(sheet_data, "equip_data", equip_list, 1) + S_equip[1]
                    if len(S_equip[0]) != 0:
                        media_ids = []
                        for filename in S_equip[0]:
                            print(S_equip[0])
                            res = api.media_upload(filename)
                            media_ids.append(res.media_id)
                        api.update_status(media_ids=media_ids, status="@%s" % tweet.user.screen_name + comment[:139],
                                          in_reply_to_status_id=tweet.id,
                                          )
                        if len(comment) > 139:
                            for i in range(1, len(comment) // 139 + 1):
                                if comment[i*139:(i + 1) * 139] != '\n':
                                    api.update_status(
                                        status="@%s " % tweet.user.screen_name + comment[i * 139: (i + 1) * 139],
                                        in_reply_to_status_id=tweet.id,
                                        )
                    else:
                        if comment != "":
                            for i in range(0, len(comment) // 139 + 1):
                                if comment[i*139:(i + 1) * 139] != '\n':
                                    api.update_status(
                                        status="@%s " % tweet.user.screen_name + comment[i * 139: (i + 1) * 139],
                                        in_reply_to_status_id=tweet.id,
                                        )
                    Activities.update_user_inven(user_names, tweet.user.name, equip_list)
                else:
                    api.update_status(
                        status="@%s" % tweet.user.screen_name + "없는 유저이거나 크리스탈이 부족합니다. 가챠숍에서 크리스탈을 구매해주세요.",
                        in_reply_to_status_id=tweet.id,
                    )
                time.sleep(2)

            elif task_name == "[하급장비판매]":
                print("c등급 판매 시작")
                api.update_status(
                    status="@%s" % tweet.user.screen_name + Activities.sell_equips(user_names, tweet.user.name, False, True),
                    in_reply_to_status_id=tweet.id,
                )
                time.sleep(2)
            elif task_name == "[중급장비판매]":
                print("b등급 판매 시작")
                api.update_status(
                    status="@%s" % tweet.user.screen_name + Activities.sell_equips(user_names, tweet.user.name, True, False),
                    in_reply_to_status_id=tweet.id,
                )
                time.sleep(2)
            elif task_name == "[일괄판매]":
                print("일괄 판매 시작")
                api.update_status(
                    status="@%s" % tweet.user.screen_name + Activities.sell_equips(user_names, tweet.user.name, True, True),
                    in_reply_to_status_id=tweet.id,
                )
                time.sleep(2)
            elif task_name == "[tmi보기]":
                print("tmi 출력 시작")
                api.update_status(
                    status="@%s" % tweet.user.screen_name + Activities.random_feature(sheet_data, tweet.user.name),
                    in_reply_to_status_id=tweet.id,
                )

            else:
                api.update_status(
                    status="@%s 오류입니다. 해당 트윗과 봇에 보낸 트윗을 캡쳐해서 총괄계 디엠으로 보내주세요." % tweet.user.screen_name,
                    in_reply_to_status_id=tweet.id,
                )

    RWData.update_file("replied_mention_ids.txt", latest_id)
    return latest_id