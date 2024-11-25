import streamlit as st
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import layout
import numpy as np
import pandas as pd
import time
from datetime import date
from matplotlib import pyplot as plt
import seaborn as sns
# MySQL 데이터베이스 연결 설정

config1 = {
    'user': '',#DB접속 유저 이름 
    'password': '', # 비밀번호
    'host': '', #호스트의 주소
    'database': 'target_real' #데이터베이스의 테이블명
}
config2 = {
    'user': '',#DB접속 유저 이름 
    'password': '', # 비밀번호
    'host': '', #호스트의 주소
    'database': 'category_news' #데이터베이스의 테이블명
}
config3 = {
    'user': '',#DB접속 유저 이름 
    'password': '', # 비밀번호
    'host': '', #호스트의 주소
    'database': 'team1_project' #데이터베이스의 테이블명
}
config4 = {
    'user': '',#DB접속 유저 이름 
    'password': '', # 비밀번호
    'host': '', #호스트의 주소
    'database': 'news_outlook' #데이터베이스의 테이블명
}
config5 = {
    'user': '',#DB접속 유저 이름 
    'password': '', # 비밀번호
    'host': '', #호스트의 주소
    'database': 'target' #데이터베이스의 테이블명
}
config6 = {
    'user': '',#DB접속 유저 이름 
    'password': '', # 비밀번호
    'host': '', #호스트의 주소
    'database': 'realtime_market' #데이터베이스의 테이블명
}
ticker_dict = {
            # 추가 옵션 및 티커값 추가
            "삼익THK":"004380",
            "이엠넷":"123570" ,
            "모헨즈":"006920" ,
            "앤씨앤":"092600" ,
            "EDGC":"245620" ,
            "인터플렉스":"051370" ,
            "오픈엣지테크놀로지":"394280" ,
            "씨씨에스":"066790", 
            "갤럭시아에스엠":"011420" ,
            "플레이디":"237820" ,
            "엔켐":"348370",
            "이수스폐셜티케미컬":"457190" ,
            "우리기술투자":"041190",
            "에브리봇":"270660",
            "큐알티":"405100",
            "알테오젠":"196170",
            "SK하이닉스":"000660",
            "삼성전자":"005930"} 

today = date.today() #오늘 날짜
today_str = today.strftime("%Y%m%d") 

st.sidebar.title('주가 및 전망예측시스템')
selected_option = st.sidebar.selectbox("원하시는 항목을 선택해주세요", ["예측값","category_news","News", "Option 4","종목별 뉴스의 긍정,부정"])#,"18개종목"

if selected_option == "예측값":
    
    # 데이터베이스 연결
    cnx = mysql.connector.connect(**config6)
    cursor = cnx.cursor()
    option = st.selectbox("원하는 종목을 골라주세요", list(ticker_dict.keys()))
    ticker = ticker_dict.get(option)
    # 데이터베이스에서 데이터 가져오기
    if option:
        # option가 선택된 경우에만 데이터베이스에서 데이터를 가져옵니다.
        #여긴 모델 나오면 공사할거에요.
        query1 = f"SELECT time,hname,price FROM realtime_market.`{today_str}`  WHERE shcode='{ticker}' and time BETWEEN '202403111337' AND '202403111517'" #실제값
        cursor = cnx.cursor()
        cursor.execute(query1)
        result1 = cursor.fetchall()
        query2 = f"SELECT time,predict_price FROM temp WHERE shcode='A{ticker}' and time BETWEEN '202403111334' AND '202403111517'" #예측값
        cursor.execute(query2)
        result2 = cursor.fetchall()
        result_date=[row[0] for row in result1]
        result1_value= [row[2] for row in result1]
        result2_date= [row[0] for row in result2]
        result2_value= [row[1] for row in result2]
        df_real = pd.DataFrame({
            "date": result_date,
            "value1": result1_value
        })
        df_predict=pd.DataFrame({
            "date":result2_date,
            "value2": result2_value
        })
        df_real['date'] = pd.to_datetime(df_real['date'])
        df_predict['date'] = pd.to_datetime(df_predict['date'])
        fig, axs = plt.subplots(3, 1, sharex=True)
        df_predict['value2'] = df_predict['value2'].astype(int)
        def format_value(value):
            rounded_value = round(value, -2)
            if rounded_value % 100 == 0:
                return f'{int(rounded_value):,d}'
            else:
                return f'{rounded_value:.2f}'

        df_predict['value2'] = df_predict['value2'].apply(format_value)
        
        st.dataframe(df_real)
      # 첫 번째 그래프
        axs[0].plot(df_real['date'], df_real['value1'], label='value1')
        axs[0].set_ylabel('REAL')
        
        # 두 번째 그래프
        axs[1].plot(df_predict['date'], df_predict['value2'], label='value2')
        axs[1].set_ylabel('PREDICT')
    

        # 세 번째 그래프
        sns.lineplot(x='date', y='value1', data=df_real, ax=axs[2], label='REAL')
        sns.lineplot(x='date', y='value2', data=df_predict, ax=axs[2], label='PREDICT')
        axs[2].set_xticklabels(df_predict['date'], rotation=270, ha='left')
        axs[2].set_ylabel('REAL & PREDICT')
        

        # 첫 번째와 두 번째 그래프 x축 레이블 설정
        for ax in axs[:2]:
            ax.set_xlabel('Date')

        # 그래프 간격 조정
        plt.subplots_adjust(hspace=0.5)

        # Streamlit에 표시
        st.pyplot(fig)






if selected_option == "category_news":
    cnx = mysql.connector.connect(**config2)
    cursor = cnx.cursor()
    option = st.selectbox("원하는 종목을 골라주세요", list(ticker_dict.keys()))
    ticker = ticker_dict.get(option)
    today_str = '20240220' #db에 자료가 없어서 임시적으로 날짜를 부여
    if option:
        # option가 선택된 경우에만 데이터베이스에서 데이터를 가져옵니다.
        query = f"SELECT date,subject,url FROM `{ticker}` WHERE date LIKE '%{today_str}%'"
        #category_news db에서 날짜가 오늘인걸로, 선택된 종목의 년월일시분과 제목과 URL을 가져옴
        cursor.execute(query)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=['날짜', '제목','url'])
        #데이터 프레임에 날짜,제목,url이라고 이름을 부여
        new_data = pd.DataFrame({
            "날짜": result['날짜'],
            "제목": result['제목'],
            "URL": result['url']
        }) #날짜와 제목과 URL을 가지고 한번더 데이터프레임을 생성
        new_data.set_index(['날짜'], inplace=True) # 날짜로 처음 인덱스를 수정
        column_config = {"URL": st.column_config.LinkColumn()}  # URL에 하이퍼 링크를 성정
        st.dataframe(new_data, column_config=column_config) #보여주기!
             
            

if selected_option == "News":
    
    # # 데이터베이스 연결
    cnx = mysql.connector.connect(**config3)
    cursor = cnx.cursor()  

    tab1,tab2=st.tabs(['UP',"DOWN"])
    with tab1:
        query = "SELECT * FROM testbye WHERE Updown='up'"
        #testbye라는 실험용 db에서 상승하락중 상승인것의 전체 데이터를 가져와서
        cursor.execute(query)
        result = cursor.fetchall()

        # 데이터를 DataFrame으로 변환
        data = pd.DataFrame(result, columns=['날짜', '제목', 'URL', 'UPDown'])
        #데이터 프레임으로 만들고
        new_data = pd.DataFrame({
        "날짜": data["날짜"],
        "제목": data["제목"],
        "UPDown": data["UPDown"],
        "URL": data["URL"]
        }) #열 이름을 날짜 제목 UPDown URL로 지정
        column_config={"URL": st.column_config.LinkColumn()} #URL에 하이퍼링크 부여
        st.dataframe(new_data, column_config=column_config) #새로운 데이터프레임 생성
    
    with tab2:

        query = "SELECT * FROM testbye WHERE Updown='down'" 
        #testbye라는 실험용 db에서 상승하락중 하락인것의 전체 데이터를 가져와서               
        cursor.execute(query)
        result = cursor.fetchall()
        # 데이터를 DataFrame으로 변환
        data = pd.DataFrame(result, columns=['날짜', '제목', 'URL', 'UPDown'])
        #데이터 프레임으로 만들고
        new_data = pd.DataFrame({
        "날짜": data["날짜"],
        "제목": data["제목"],
        "UPDown": data["UPDown"],
        "URL": data["URL"]
        })#열 이름을 날짜 제목 UPDown URL로 지정
        column_config={"URL": st.column_config.LinkColumn()} #URL에 하이퍼링크 부여
        st.dataframe(new_data, column_config=column_config) #새로운 데이터프레임 생성
    
                
            
            

if selected_option == "Option 4":

    # 데이터베이스 연결
    cnx = mysql.connector.connect(**config4)
    cursor = cnx.cursor()

    # 사용자 선택
    option = st.selectbox("원하는 종목을 골라주세요", list(ticker_dict.keys()))
    ticker = ticker_dict.get(option)

    # SQL 쿼리 생성 및 실행
    if option:
        query = f"SELECT curent_time ,outlook_0, outlook_1, outlook_2 FROM today_sokbo_outlook_signal WHERE code_outlook='{ticker}_outlook' and curent_time LIKE'{today_str}%'"
        #현재시간,하락,보합,상승을 오늘 속보 데이터베이스에서 선택한 항목의 table을 오늘자로 넣어져있는걸 가져옴
        cursor.execute(query)
        result = cursor.fetchall()
        result_dict = {
            '하락': [row[1] for row in result], 
            '보합': [row[2] for row in result], 
            '상승': [row[3] for row in result]
        }

        # 데이터 유무 확인 및 오류 처리
        if len(result_dict) > 0:
           # 데이터 변환
            values = []
            for key in result_dict.keys():
                values.extend([float(value) for value in result_dict[key]])

            # Outlook 카테고리에 대한 사용자 정의 색상 정의
            category_colors = ['blue', 'lightgray', 'red'] # 원하는대로 조정  

            # 원형 그래프 그리기
            fig = go.Figure(data=[go.Pie(labels=list(result_dict.keys()), values=values, marker={'colors': category_colors})])

            # 데이터프레임 보여주기
            st.plotly_chart(fig)
            result = pd.DataFrame(result)
            result.columns = ['날짜', '하락', '보합','상승']
            result['날짜'] = pd.to_datetime(result['날짜']) #날짜의 데이터 타입(str)을 'datetime(날짜)로 변환
            result.set_index('날짜', inplace=True)

            st.dataframe(result)
        else:
            st.write("데이터가 없습니다.")



if selected_option == "종목별 뉴스의 긍정,부정":
    
    cnx = mysql.connector.connect(**config4)
    cursor = cnx.cursor()
    option = st.selectbox("원하는 종목을 골라주세요", list(ticker_dict.keys()))
    ticker = ticker_dict.get(option)
    if option: # option가 선택된 경우에만 데이터베이스에서 데이터를 가져옵니다.
        query = f"SELECT rdate,summary,{ticker}_outlook FROM today_sokbo_outlook;"
        cursor.execute(query)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=['날짜', '본문내용','종목'])
        new_data = pd.DataFrame({
        "날짜": result["날짜"],
        "본문내용": result["본문내용"],
        "UDH": result["종목"]
        })
        new_data['UDH'] = new_data['UDH'].apply(lambda x: {0: '부정', 1: '보합', 2: '긍정'}.get(x, 'Unknown'))
        new_data.set_index(['날짜'], inplace=True)
        st.dataframe(new_data)
