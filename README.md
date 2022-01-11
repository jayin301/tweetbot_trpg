# tweetbot_trpg

## auth.py
* twitter developer account로부터 key, secret, access token 및 secret을 받아서 auth를 얻어옴
* google spread로부터 drive 사용을 인가받은 secret의 json 파일을 넘겨 auth를 얻어옴

## main.py
* google spread로부터 필요한 데이터를 일괄 다운로드함
* 봇에서 수용할 키워드 목록을 바탕으로 update tweet를 작동시켜 실시간으로 키워드를 포함한 멘션에 답하도록함

## UpdateTweet.py
* 실시간으로 키워드를 분석하여 입력받은 키워드에 따라 알맞은 명령을 수행
* 키워드에 따라 유저의 재화를 확인해야할 경우 해당 정보를 담고 있는 구글 스프레드 시트의 주소에 접속, 확인 및 업데이트하는 작업을 수행

## Activities.py
* UpdateTweet에서 수행하는 모든 함수에 대한 정의를 포함

## RWData.py
* 외부 텍스트 파일 혹은 구글스프레드시트로부터 데이터를 읽어오는 모든 함수에 대한 정의를 
