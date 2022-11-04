from flask import Flask, render_template, request
import pandas as pd
import datetime
# from macpath import split
from load_model import predict_ans
app = Flask(__name__)

app._static_folder="static"

@app.route('/')
def found(endpoint='assets'):
	title = "首頁"
	return render_template('1Firstpage.html', title=title)
						   
@app.route('/1Firstpage')
def Firstpage():
	title = "首頁"
	return render_template('1Firstpage.html', title=title)

@app.route('/2Dashboard')
def Dash():
	title = "互動式介面"
	return render_template('2Dashboard.html', title=title)

x=pd.read_csv('data/x4.csv')
z=0
@app.route("/result", methods=['POST', 'GET'])
def result_json():
    date = request.form['date'] #出發日期
    Quarter = 4
    DayOfWeek = 5
    CRSDepTime = 1714
    CRSArrTime = 1940
    DistanceGroup = 2
    WT18_x = 0
    startcontinent = request.form['startcontinent'] #出發州
    startairport = request.form['startairport'] #出發機場
    endcontinent = request.form['endcontinent'] #抵達州
    endairport = request.form['endairport'] #抵達機場
    AWND_x = request.form.get('awnd') #平均風速
    PRCP_x = request.form.get('prcp') #降水量
    TMAX_x = request.form.get('tmax') #最高溫
    TMIN_x = request.form.get('tmin') #最低溫
    WSF2_x = request.form.get('wsf2') #2min風速
    WSF5_x = request.form.get('wsf5') #5sec風速
    SNOW_x = request.form.get('snow') #降雪量
    WT01_x = request.form.get('wt01')
    WT02_x = request.form.get('wt02')
    WT03_x = request.form.get('wt03')
    WT04_x = request.form.get('wt04')
    WT05_x = request.form.get('wt05')
    WT06_x = request.form.get('wt06')
    WT07_x = request.form.get('wt07')
    WT08_x = request.form.get('wt08')
    WT09_x = request.form.get('wt09')
    WT10_x = request.form.get('wt10')
    WT11_x = request.form.get('wt11')

    if WT01_x == None:
        WT01_x = 0
    if WT02_x == None:
        WT02_x = 0
    if WT03_x == None:
        WT03_x = 0    
    if WT04_x == None:
        WT04_x = 0
    if WT05_x == None:
        WT05_x = 0   
    if WT06_x == None:
        WT06_x = 0     
    if WT07_x == None:
        WT07_x = 0
    if WT08_x == None:
        WT08_x = 0
    if WT09_x == None:
        WT09_x = 0
    if WT10_x == None:
        WT10_x = 0
    if WT11_x == None:
        WT11_x = 0

    WT01_y = 1
    WT02_y = 0
    WT03_y = 0   
    WT04_y = 1
    WT05_y = 0 
    WT06_y = 1    
    WT07_y = 0
    WT08_y = 1
    WT09_y = 0
    WT10_y = 0
    WT11_y = 0
    WT18_y = 0
    AWND_y = 0
    PRCP_y = 0
    TMAX_y = 0
    TMIN_y = 0
    WSF2_y = 0
    WSF5_y = 0
    SNOW_y = 0
    IATA_Code_Marketing_Airline = 3
    Year = date.split('-')[0]
    Month = date.split('-')[1]
    DayofMonth = date.split('-')[2]
    Origin = 6
    Dest = 2
    input_list = [Year, Quarter, Month, DayofMonth, DayOfWeek,
           IATA_Code_Marketing_Airline, Origin, Dest, CRSDepTime,
           CRSArrTime, DistanceGroup,
           
           AWND_x, PRCP_x, TMAX_x, TMIN_x, WSF2_x,
           WSF5_x, SNOW_x, WT01_x, WT02_x, WT03_x, WT04_x, WT05_x,
           WT06_x, WT07_x, WT08_x, WT09_x, WT10_x, WT11_x, WT18_x,
           
           AWND_y, PRCP_y, TMAX_y, TMIN_y, WSF2_y, 
           WSF5_y, SNOW_y, WT01_y, WT02_y, WT03_y, WT04_y, WT05_y, 
           WT06_y, WT07_y, WT08_y, WT09_y, WT10_y, WT11_y, WT18_y,
           ]
    file_name = []
    for i in input_list:
        if isinstance(i,str):
            i = float(i)
        file_name.append(i)
    df_pred = predict_ans(file_name)
    

    # filt = (x['ea'] == str(endairport)) & (x['DATE'] == str(date))
    # y=x[filt].at[0,'AWND']
        
    status_val = -1
    dic={-1:"判別異常",0:"準時抵達",1:"delay 0 ~ 30 分鐘",2:"delay 30 ~ 60 分鐘",3:"delay 60 ~ 90 分鐘",
        4:"delay 90 ~ 120 分鐘",5:"delay 120 ~ 150 分鐘",6:"delay 150 分鐘以上"}
    
    status_val = df_pred.at[0, 0]
    colorDic={-1:"#D7A1FF",0:"#ABFFAB",1:"#FFE1AB",2:"#FFE1AB",3:"#FFE1AB",4:"#FFE1AB",5:"#FFE1AB",6:"#FFABAB"}   

    e1=endairport
    filt =(x['DATE']==date)&(x['NAME']==e1)
    y=x[filt]['AWND'].values
    return render_template("2Dashboard.html", startcontinent=startcontinent,startairport=startairport,
    endcontinent=endcontinent,endairport=endairport,date=date,y=y,AWND_x=AWND_x,PRCP_x=PRCP_x,TMAX_x=TMAX_x,
    TMIN_x=TMIN_x,WSF2_x=WSF2_x,WSF5_x=WSF5_x,SNOW_x=SNOW_x,
    WT01_x=WT01_x,WT02_x=WT02_x,WT03_x=WT03_x,WT04_x=WT04_x,WT05_x=WT05_x,WT06_x=WT06_x,WT07_x=WT07_x,
    WT08_x=WT08_x,WT09_x=WT09_x,WT10_x=WT10_x,WT11_x=WT11_x,Quarter=Quarter,DayOfWeek=DayOfWeek,CRSDepTime=CRSDepTime,
    CRSArrTime=CRSArrTime,DistanceGroup=DistanceGroup,WT18_x=WT18_x,Year=Year,Month=Month,DayofMonth=DayofMonth,answer=dic[status_val],CCcolor=colorDic[status_val])
    
@app.route('/3Chart')
def Chart():
	title = "分析圖表"
	return render_template('3Chart.html', title=title)

@app.route('/4Member')
def Member():
	title = "組員簡介"
	return render_template('4Member.html', title=title)

if __name__=="__main__":
	app.run(debug=True, port=5002)