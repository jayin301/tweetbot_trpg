import auth
import logging
import RWData
import UpdateTweet
import time

activity_list = ["오늘의운세", "[낚시]", "[사냥]", "[요리]", "[장비뽑기]", "[tmi보기]", "[하급장비판매]", "[일괄판매]", "[중급장비판매]"]
logger = logging.Logger

def main():
    # get all spreadsheet data from google spreadsheet
    client = auth.google_auth()
    sheet_data = dict(food_data=RWData.get_sheet(client, "server_burangza", "요리", 4),
                      hunt_data=RWData.get_sheet(client, "server_burangza", "사냥", 15),
                      feature_data=RWData.get_sheet(client, "server_burangza", "랜덤 설정", 1),
                      )
    print("first bulk end")
    time.sleep(10)
    sheet_data.update({"equip_data": RWData.get_sheet(client, "server_burangza", "장비뽑기", 9)})
    sheet_data.update({"fish_data": RWData.get_sheet(client, "server_burangza", "낚시", 15)})
    sheet_data.update({"user_names": RWData.get_sheet(client, "플레이어", "player_data", 1)})
    print("data is ready")
    time.sleep(10)

    # operate tweet bot
    api = auth.tweeter_auth()
    latest_mention = RWData.open_file("replied_mention_ids.txt")
    since_id = int(latest_mention)
    while True:
        since_id = UpdateTweet.check_mentions(api, activity_list, since_id, sheet_data)
        time.sleep(15)

if __name__ == "__main__":
    main()