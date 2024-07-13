import requests
import json
from tabulate import tabulate
from datetime import datetime, timedelta
import re
#hh-mm的时间变成dd-hh-mm
#last和running搞反了
def time_convert(last_running_time,running_time):
    #print(running_time,last_running_time)
    if running_time == "":
        return ""
    if last_running_time == "":
        last_running_time = "00:00"
    running_time_h = int(running_time.split(':')[0])
    running_time_m = int(running_time.split(':')[1])
    last_running_time_h = int(last_running_time.split(':')[0])
    last_running_time_m = int(last_running_time.split(':')[1])
    running_d = 0
    if int(last_running_time_h) - int(running_time_h) >= 24:
        running_d = int(last_running_time_h - running_time_h) // 24
    lishi_h = last_running_time_h - running_time_h - running_d *24
    lishi_m = last_running_time_m - running_time_m
    if lishi_m < 0:
        lishi_h -= 1
        lishi_m += 60
    if running_d == 0 and lishi_h == 0 and lishi_m == 0:
        return ""
    if running_d == 0:
        return str(lishi_h) + "小时" + str(lishi_m) + "分"
    else:
        return str(f"{running_d}天{lishi_h}小时{lishi_m}分")

#判断是不是一个正确的日期
def is_valid_date(date_str):
    # 定义正则表达式模式来匹配 "年-月-日" 格式
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    # 使用正则表达式检查字符串是否匹配模式
    if date_pattern.match(date_str):
        return True
    else:
        return False
#计算时间差
def calculate_duration(previous_departure_time, current_arrive_time, previous_day_count, current_day_count):
    # 定义时间格式
    if previous_departure_time =="" or current_arrive_time =="":
        return ""
    
    time_format = "%H:%M"
    
    # 将时间字符串转换为 datetime 对象
    previous_departure = datetime.strptime(previous_departure_time, time_format)
    current_arrive = datetime.strptime(current_arrive_time, time_format)
    
    # 计算跨天数
    days_diff = current_day_count - previous_day_count
    
    # 如果跨天数大于0，则需要加上相应的天数
    if days_diff > 0:
        current_arrive += timedelta(days=days_diff)
    
    # 计算历时
    duration = current_arrive - previous_departure
    
    # 将历时转换为小时和分钟
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    # 返回历时字符串
    if hours == 0:
        return f"{minutes}分钟"
    else:
        return f"{hours}小时{minutes}分钟"
#路路通数据库查询
def get_train_info_llt(train, date):
    #print(f"进入路路通查询{train}")
    while True:
        try:
            url_number = "https://rail.moefactory.com/api/trainNumber/query"

            data_number = {
                "date": f"{date}",
                "trainNumber": f"{train}"
            }
            headers_number = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post(url_number, data=data_number, headers=headers_number)  # requests会自动把data中的键值对进行编码

            if response.status_code != 200:
                err_string = "1,出现请求故障："+str(response.status_code)
                return err_string
            train_info_query_result = response.json()

            if 'data' in train_info_query_result and isinstance(train_info_query_result['data'], dict) and 'data' in train_info_query_result['data'] and isinstance(train_info_query_result['data']['data'], list) and len(train_info_query_result['data']['data']) > 0:
                train_data = train_info_query_result['data']['data'][0]  # 提取列表中的第一个字典
                train_index = train_data['trainIndex']
                train_number = train_data['trainNumber']
                begin_station = train_data['beginStationName']
                departure_time = train_data['departureTime']
                end_station_name = train_data['endStationName']
                arrival_time = train_data['arrivalTime']
                day_count = train_data['dayCount']
                duration_minutes = train_data['durationMinutes']
                distance = train_data['distance']
                train_type = train_data['trainType']
                cr_type = train_data['crType']

                #print(train_index, train_number, begin_station, departure_time, end_station_name, arrival_time, day_count, duration_minutes, distance, train_type, cr_type)
            else:
                err_string = str(1)+","+f"未查询到{train}的时刻信息"
                return err_string

            url_detail = "https://rail.moefactory.com/api/trainDetails/query"


            data_detail = {
                "trainIndex": f"{train_index}",
                "date": "20240705"
            }
            #print(data_detail)
            headers_detail = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response_detail = requests.post(url_detail, data=data_detail, headers=headers_detail)

            if response_detail.status_code != 200:
                return response_detail.status_code


            # 解析 JSON 数据
            data_detail = response_detail.json()

            # 获取 data 部分
            train_data = data_detail['data']
            #print(train_data)
            # 输出 trainNumber, trainType, companyName, foodCoachName
            #if train_data['trainNumber'] != train:
                #return 1
            
            print(f"查询到车次： {train_data['trainNumber']}, {train_data['trainType']}, 担当: {train_data['companyName']}, 餐车: {train_data['foodCoachName']}")
            if cr_type == 1:
                #红色内容
                print("\033[1;31m复兴号CR400\033[0m")
            elif cr_type == 2:
                #蓝色内容
                print("\033[1;34m复兴号CR300\033[0m")
            elif cr_type == 3:
                #垃圾桶
                print("\033[1;32m“复兴号”CR200J\033[0m")
            
            header = [["车站", "车次", "到达时间", "出发时间", "停留", "区间历时", "里程", "均速", "车站地点"]]
            data_rows = []
            # 输出 viaStations 中的每一组
            print("时刻表:")
            previous_departure_time = None  # 用于存储上一个循环的departure_time
            previous_day_count = 0  # 用于存储上一个循环的day_count
            for station in train_data['viaStations']:

                current_arrive_time = station['arrivalTime']
                current_departure_time = station['departureTime']
                current_day_count = station['dayIndex']
                if previous_departure_time is not None:
                    lishi = calculate_duration(previous_departure_time, current_arrive_time, previous_day_count, current_day_count)
                else:
                    lishi = ""

                new_row = f"{station['stationName']}, {station['trainNumber']}, {station['arrivalTime']}, {station['departureTime']}, {station['stopMinutes']}分, {lishi}, {station['distance']}km, {station['speed']}km/h, {station['district']}"
                new_row = new_row.split(", ")
                data_rows.append(new_row)

                # 更新previous_departure_time和previous_day_count

                previous_departure_time = current_departure_time
                previous_day_count = current_day_count

            #检查data_rows元素
            for i in range(len(data_rows)):
                for j in range(len(data_rows[i])):
                    if data_rows[i][j] == "None":
                        data_rows[i][j] = ""
                    if data_rows[i][j] == "Nonekm/h":
                        data_rows[i][j] = ""
            # 将表头和数据组合成一个表格
            table = header + data_rows

            # 使用 tabulate 打印表格，tablefmt 可选择 "grid" 或 "fancy_grid" 或 "pipe" 等样式来形成实线
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid", colalign=("center")*len(header), maxcolwidths=[20]*len(header[0])))

            #清空表格
            data_rows.clear()

            # 输出 routingItems 中的每一组
            data_rows_jiaolu = []
            #print(train_data['routing'])
            if train_data['routing'] is None:
                jiaolu_llt = 0

            else:
                jiaolu_llt = 1
            if jiaolu_llt == 1:
                print("交路表:")
                print(train_data['routing']['trainModel'])
                header_jiaolu = [["车次", "始发站", "发车时间", "终到车站", "到达时间"]]
                for routing in train_data['routing']['routingItems']:
                    new_row_jiaolu = f"{routing['trainNumber']}, {routing['beginStationName']}, {routing['departureTime']}, {routing['endStationName']}, {routing['arrivalTime']}"
                    new_row_jiaolu = new_row_jiaolu.split(", ")
                    data_rows_jiaolu.append(new_row_jiaolu)

                #检查data_rows_jiaolu
                for i in range(len(data_rows_jiaolu)):
                    for j in range(len(data_rows_jiaolu[i])):
                        if data_rows_jiaolu[i][j] == "None":
                            data_rows_jiaolu[i][j] = ""

                # 将表头和数据组合成一个表格
                table_jiaolu = header_jiaolu + data_rows_jiaolu

                # 使用 tabulate 打印表格，tablefmt 可选择 "grid" 或 "fancy_grid" 或 "pipe" 等样式来形成实线
                print(tabulate(table_jiaolu, headers="firstrow", tablefmt="fancy_grid", colalign=("center",)*len(header_jiaolu[0])))

                #清空表格
                data_rows_jiaolu.clear()
                get_train_zhengwandian(train,date)
            if jiaolu_llt == 0:
                jiaolu_result = get_train_bureau(train, date)
                jiaolu_result_type = jiaolu_result.split('#')[0]
                jiaolu_result_str = jiaolu_result.split('#')[1]
                if jiaolu_result_type == "0":
                    jiaolu_result = jiaolu_result_str.split('&')[0]+jiaolu_result_str.split('&')[1]
                    #print(jiaolu_result)
                    get_train_zhengwandian(train,date)
                    #return "0,success"
                else:
                    err_string = str(3)+","+f"未查询到{train}的交路信息"
                    return err_string
            return "0,success"
        except requests.exceptions.RequestException as e:
            err_string = str(2)+","+f"Request error: {e}"
            return (err_string)
        except json.JSONDecodeError as e:
            err_string = str(2)+","+f"JSON decode error: {e}"
            return (err_string)
        except KeyError as e:
            err_string = str(2)+","+f"Key error: {e}"
            return (err_string)
        except Exception as e:
            err_string = str(2)+","+f"An unexpected error occurred: {e}"
            return (err_string)
#12306数据库查询
def fetch_train_info(train_no, date):
    """
    :train_no: 车次12306加密编码
    :date: 出发日期
    :return: 返回的JSON数据
    """
    train_no = train_no.split(',')[0]
    url = f"https://kyfw.12306.cn/otn/queryTrainInfo/query?leftTicketDTO.train_no={train_no}&leftTicketDTO.train_date={date}&rand_code="
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            raise Exception(f"Failed to parse JSON for train {train_no}")
    else:
        raise Exception(f"Failed to fetch data for train {train_no}, status code: {response.status_code}")
#12306表头查询
def extract_and_format_data(json_data,train_no):
    """
    提取并格式化数据
    :json_data: 请求返回的json数据
    :return: 格式化后的字符串
    """
    data = json_data.get('data', {}).get('data', [])
    if not data:
        raise Exception("Data field is empty or missing in JSON response.")
    
    first_station = data[0]['station_name']
    start_time = data[0]['start_time']
    last_station = data[-1]['station_name']
    arrive_time = data[-1]['arrive_time']
    running_time = data[-1]['running_time']
    service_type = data[0]['service_type']

    #print(service_type)
    
    #把running_time转化为天-小时-分钟
    running_time_list = running_time.split(':')
    running_time_hour = int(running_time_list[0])
    running_time_minute = int(running_time_list[1])
    running_time_day = 0
    if running_time_hour >= 24:
        running_time_day = running_time_hour // 24
        running_time_hour = running_time_hour % 24
    running_time_str = f"{running_time_day}天{running_time_hour}小时{running_time_minute}分钟"
    running_time = running_time_str
    
    # 去除重复的站名和车次号
    station_train_codes = []
    for entry in data:
        station_train_codes.append(entry['station_train_code'])
    
    # 判断是否都相同，不同用/分割
    unique_station_train_code = '/'.join(sorted(set(station_train_codes)))
    
    total_stations = len(data)
    if train_no[0] in ['D', 'G', 'C', 'S', 'Z', 'T', 'Y']:
        train_type_mapping = {
            'D': '动车',
            'G': '高速',
            'C': '城际',
            'S': '市郊',
            'Z': '直达特快',
            'T': '特快',
            'Y': '旅游'
        }
        if train_no[0] == 'D' and train_no[1:].isdigit() and int(train_no[1:]) < 300:
            train_type = "\033[32m复兴号\033[0m动车组列车" 
        else:
            train_type = train_type_mapping.get(train_no[0], '')
    elif train_no[0] == 'K':
        if service_type != '0':
            train_type = "新空调"+data[0]['train_class_name']
        else:
            train_type = "\033[33m**非空**\033[0m" +data[0]['train_class_name']
    elif train_no[0] == 'L':
        if service_type != '0':
            train_type = "新空调"+data[0]['train_class_name']
        else:
            train_type = "\033[33m**非空**\033[0m" +data[0]['train_class_name']
    elif train_no[0].isdigit():
        if service_type == '1' or service_type == '2':
            train_type = "新空调"+data[0]['train_class_name']
        elif service_type == '0':
            train_type = "\033[33m**非空**\033[0m"+data[0]['train_class_name']
    else:
        train_type = ""
    #train_type = +","+train_type

    #train_type = train_type + train_level
    #print(train_type)

    formatted_str = f"{unique_station_train_code},{first_station}-{last_station},{train_type},共{total_stations}站,出发时间：{start_time},到达时间：{arrive_time},行驶{running_time}"
    return formatted_str
#经停信息
def get_stop_info(json_data):
    """
    获取列车的停站信息
    :param json_data: 请求返回的json数据
    :return: 停站信息的字符串列表
    """
    data = json_data.get('data', {}).get('data', [])
    if not data:
        raise Exception("Data field is empty or missing in JSON response.")
    
    stop_info_list = []
    null_info = ""
    last_running_time = ""
    for index, stop in enumerate(data, start=1):
        station_train_code = stop['station_train_code']
        station_name = stop['station_name']
        arrive_time = stop['arrive_time'] if stop['arrive_time'] != "----" else ""
        start_time = stop['start_time']
        running_time = time_convert(stop['running_time'],last_running_time)
        stay_time = calculate_duration(arrive_time, start_time, 0, 0)
        stop_info = f"{station_name},{station_train_code},{arrive_time},{start_time},{stay_time},{running_time},{null_info},{null_info},{null_info}"
        #print(stop_info)
        last_running_time = stop['running_time']
        stop_info_list.append(stop_info)
    
    #print(stop_info_list)
    return stop_info_list
#缺省查找
def train_code_to_12306(train_code,date_str):
    #去掉date中的-变成一串数字
    date = date_str.replace("-","")
    # 发送请求的网址
    url = f"https://search.12306.cn/search/v1/train/search?keyword={train_code}&date={date}"

    # 发送GET请求
    response = requests.get(url)

    # 解析返回的JSON数据
    data = json.loads(response.text)

    #print(response.text)
    #如果json数据中没有data字段，说明没有找到该车次信息
    if "data" not in data:
        return -1
        #raise Exception(f"{train_code}在{date}可能没有开行，或已经停运")
    
    # 解析 data 数据中的列车信息
    train_info_list = []
    for item in data["data"]:
        train_info_list.append({
            "station_train_code": item["station_train_code"],
            "from_station": item["from_station"],
            "to_station": item["to_station"],
            "train_no": item["train_no"]
        })

    if len(train_info_list) > 2:
        print("请选择列车：")
        data_rows_choose = []
        new_row_choose = ""
        choose_count = 1
        data_count = 0
        for i, info in enumerate(train_info_list):
            new_row_choose_temp = (f"{i + 1},{info['station_train_code']},{info['from_station']},{info['to_station']},")
            new_row_choose += new_row_choose_temp
            choose_count += 1
            i += 1
            #new_row_choose_temp += ","
            data_count += 1
            if choose_count == 4:
                data_rows_choose.append(new_row_choose.split(",")) 
                #删除空白元素
                data_rows_choose[-1] = list(filter(lambda x: x != "", data_rows_choose[-1]))
                new_row_choose = ""
                choose_count = 1
        

        #print(data_rows_choose)
        header_choose = [["序号", "车次", "出发站", "到达站", "序号", "车次", "出发站", "到达站","序号", "车次", "出发站", "到达站"]]
        # 将表头和数据组合成一个表格
        table_choose = header_choose + data_rows_choose
            # 使用 tabulate 打印表格，tablefmt 可选择 "grid" 或 "fancy_grid" 或 "pipe" 等样式来形成实线
        print(tabulate(table_choose, headers="firstrow", tablefmt="fancy_grid", colalign=("center",)*len(header_choose), maxcolwidths=[20]*len(header_choose[0])))

            #清空表格
        data_rows_choose.clear()
        choice = int(input("请输入选择的列车号码："))
        selected_train_no = train_info_list[choice - 1]["train_no"]
        selected_train_code = train_info_list[choice - 1]["station_train_code"]
    elif len(train_info_list) == 2:
        print("请选择列车：")
        data_rows_choose = []
        new_row_choose = ""
        choose_count = 1
        data_count = 0
        for i, info in enumerate(train_info_list):
            new_row_choose_temp = (f"{i + 1},{info['station_train_code']},{info['from_station']},{info['to_station']},")
            new_row_choose += new_row_choose_temp
            choose_count += 1
            i += 1
            #new_row_choose_temp += ","
            data_count += 1
            if choose_count == 3:
                data_rows_choose.append(new_row_choose.split(",")) 
                #删除空白元素
                data_rows_choose[-1] = list(filter(lambda x: x != "", data_rows_choose[-1]))
                new_row_choose = ""
                choose_count = 1
        
        #print(data_rows_choose)
        header_choose = [["序号", "车次", "出发站", "到达站", "序号", "车次", "出发站", "到达站","序号", "车次", "出发站", "到达站"]]
        # 将表头和数据组合成一个表格
        table_choose = header_choose + data_rows_choose
            # 使用 tabulate 打印表格，tablefmt 可选择 "grid" 或 "fancy_grid" 或 "pipe" 等样式来形成实线
        print(tabulate(table_choose, headers="firstrow", tablefmt="fancy_grid", colalign=("center",)*len(header_choose), maxcolwidths=[20]*len(header_choose[0])))

            #清空表格
        data_rows_choose.clear()
        choice = int(input("请输入选择的列车号码："))
        selected_train_no = train_info_list[choice - 1]["train_no"]
        selected_train_code = train_info_list[choice - 1]["station_train_code"]
    elif train_info_list:
        selected_train_no = train_info_list[0]["train_no"]
        selected_train_code  = train_info_list[0]["station_train_code"]
    else:
        print(f"{train_code}可能已经停运")
        selected_train_no = "-1"
        selected_train_code = "-1"
    selected_train = selected_train_no +","+ selected_train_code
    return selected_train

#担当路局返回
def get_train_bureau(train, date):
    url_app_detail = "https://mobile.12306.cn/wxxcx/wechat/main/travelServiceQrcodeTrainInfo"

    post_data_app_detail = {
        'trainCode': f'{train}',
        'startDay': f'{date}',
        'startTime': '',
        'endDay': '',
        'endTime': ''
    }

    headers_app_detail = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b11)XWEB/9185'
    }

    result_app_detail = requests.post(url_app_detail, data=post_data_app_detail, headers=headers_app_detail)
    data = result_app_detail.json()
    stop_times = data['data']['trainDetail']['stopTime']

    # 交路信息提取
    if stop_times:
        stop_time = stop_times[0]
        jiaolu_train_style = stop_time['jiaolu_train_style']  # 交路列车类型
        jiaolu_dept_train = stop_time['jiaolu_dept_train']  # 交路担当客运段
        if 'jiaolu_corporation_code' in stop_time:
            jiaolu_corporation_code = stop_time['jiaolu_corporation_code']  # 担当客运段代码

        #print("担当：" + jiaolu_corporation_code)
        #print("车底：" + jiaolu_dept_train + "的" + jiaolu_train_style)
        if jiaolu_train_style == "" or jiaolu_dept_train == "" or jiaolu_corporation_code == "":
            jiaolu_result = str(-1)+"#无担当数据"
            return jiaolu_result
        jiaolu_result = "1#担当：" + jiaolu_corporation_code+"&车底：" + jiaolu_dept_train + "的" + jiaolu_train_style
        #print(jiaolu_result)
        return jiaolu_result

def get_train_zhengwandian(train, date):
    url_app_detail = "https://mobile.12306.cn/wxxcx/wechat/main/travelServiceQrcodeTrainInfo"

    post_data_app_detail = {
        'trainCode': f'{train}',
        'startDay': f'{date}',
        'startTime': '',
        'endDay': '',
        'endTime': ''
    }

    headers_app_detail = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b11)XWEB/9185'
    }

    result_app_detail = requests.post(url_app_detail, data=post_data_app_detail, headers=headers_app_detail)

    #print(result_app_detail.text)

    data = result_app_detail.json()
    #动车判断
    if train[0] in ['D', 'G', 'C', 'S']:
        if 'stopTime' in data['data']['trainDetail'] and data['data']['trainDetail']['stopTime'] != "":
            stop_times = data['data']['trainDetail']['stopTime']
        else:
            print("该列车暂无正晚点信息")
        data_list = []
        # 遍历每个停站信息
        for stop_time in stop_times:
            stationTrainCode = stop_time['stationTrainCode']#车次
            if 'channel' in stop_time:
                channel = stop_time['channel']#????
            stationName = stop_time['stationName']#停站名
            train_style = stop_time['train_style']#列车类型
            time_interval = stop_time['time_interval']#间隔？？？
            day_difference = stop_time['dayDifference']#日期差
            center_notice_code = stop_time['center_notice_code']#中心公告
            arrive_date = stop_time['arraiveDate']#到达日期（这里12306拼错了）
            bureau_code = stop_time['bureau_code']#路局代码
            disp_train_code = stop_time['dispTrainCode']#显示车次
            station_corporation_code = stop_time['station_corporation_code']#车站路局代码
            running_time = stop_time['runningTime']#运行时间
            arriveTime = stop_time['arriveTime']#到达时间
            
            arrive_difference = stop_time['arraiveDifference']#到达日期差（这里又拼错了）
            start_train_date = stop_time['startTrainDate']#发车日期
            start_time = stop_time['startTime']#发车时间
            station_name = stop_time['stationName']#车站名
            #正晚点信息部分
            if 'ticketDelay' in stop_time:
                train_zhuangtai = stop_time['ticketDelay'] # 晚点
                if int(train_zhuangtai) != 0:
                    train_zhuangtai = "晚点"+train_zhuangtai+"分"
                else:
                    train_zhuangtai = "正点到达"
            if 'ticketEraly' in stop_time:
                train_zhuangtai = stop_time['ticket_eraly']#提前
                #去掉提前的-
                if train_zhuangtai.startswith('-'):
                    train_zhuangtai = train_zhuangtai.lstrip('-')
                if int(train_zhuangtai) != 0:
                    train_zhuangtai = "早点"+train_zhuangtai+"分"
                else:
                    train_zhuangtai = "正点到达"
            ticket_delay_data_flag = stop_time['ticketDelayDataFlag']#与晚点相关数据？？？

            corporation_code = stop_time['corporation_code']#路局代码
            train_flag = stop_time['train_flag']#列车标识
            station_no = stop_time['stationNo']#车站序号
            waiting_room = stop_time['waitingRoom']#候车室
            check_channel = stop_time['wicket']#检票口
            local_start_time = stop_time['local_start_time']#本地发车时间
            stopover_time = stop_time['stopover_time']#停车时间
            startTime = stop_time['startTime']
            if 'exit' in stop_time:
                exit_kou = stop_time['exit']#出站口
            #交路信息提取
            jiaolu_train_style = stop_time['jiaolu_train_style']#交路列车类型
            jiaolu_dept_train = stop_time['jiaolu_dept_train']#交路担当客运段
            jiaolu_corporation_code = stop_time['jiaolu_corporation_code']#担当客运段代码
            
            #为出发到达添加：
            arriveTime = arriveTime[:2] + ":" +arriveTime[2:]
            startTime = startTime[:2] + ":" +startTime[2:]
            
            new_row = [stationTrainCode, stationName, waiting_room + "\n" + check_channel, exit_kou, arriveTime + "\n" + startTime, train_zhuangtai]
            data_list.append(new_row)

        header = [["车次", "站名", "候车室\n检票口", "出站口", "时刻表到达\n时刻表出发", "正晚点"]]

        table = header + data_list
        print("正晚点及检票口、出站口信息：")
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid", colalign=("center",)*len(header[0]), maxcolwidths=[20]*len(header[0])))
    elif train[0] in ['K', 'T', 'Z', 'L', 'Y'] or train[0].isdight:
        # 获取停站信息
        #if 'stop_time' in data['data']['trainDetail']:
        stop_times = data['data']['trainDetail']['stopTime']
            #print(stop_times)
        data_list = []
        # 输出停站信息
        for stop in stop_times:
            station_name = stop['stationName']#车站名
            station_train_code = stop['stationTrainCode']#车站车次
            station_tips = stop['stationTips']#车站提示
            arrive_time = stop['arriveTime']#到达时间
            start_train_code = stop['startTrainCode']#出发车次
            arraive_difference = stop['arraiveDifference']#到达日期差
            day_difference = stop['dayDifference']#日期差
            start_train_date = stop['startTrainDate']#开车日期
            start_time = stop['startTime']#开车时间

            #正晚点信息
            if 'ticketDelay' in stop:
                if int(stop['ticketDelay']) !=0:
                    train_zhengwandian = "晚点"+stop['ticketDelay']+"分"
                else:
                    train_zhengwandian = "正点"
            if 'ticketEarly' in stop:
                train_zhengwandian = stop['ticketEarly']
                #去掉提前的-
                if train_zhengwandian.startswith('-'):
                    train_zhengwandian = train_zhengwandian.lstrip('-')
                if int(stop['ticketEarly']) !=0:
                    train_zhengwandian = "早点"+train_zhengwandian+"分"
                else:
                    train_zhengwandian = "正点"
            ticket_delay_data_flag = stop['ticketDelayDataFlag']#不知道是啥晚点相关的
            
            center_notice_code = stop['center_notice_code']#中心公告代码
            corporation_code = stop['corporation_code']#担当路局代码
            train_flag = stop['train_flag']#不知道是个啥
            station_no = stop['stationNo']#停站序号
            arraive_date = stop['arraiveDate']#到达日期
            bureau_code = stop['bureau_code']#路局代码
            station_corporation_code = stop['station_corporation_code']#车站所属车务段
            stopover_time = stop['stopover_time']#停车时间
            running_time = stop['runningTime']#运行时间
            pass_flag = stop['passFlag']#不知道是啥
            check_channel = stop['wicket']#检票口
            station_status_color = stop['stationStatusColor']#车站状态颜色
            exit_kou = stop['exit']#出站口
            train_date = stop['trainDate']#到达终点日期
            end_station_name = stop['end_station_name']#终点站名
            waiting_room = stop['waitingRoom']#候车室

        

            #交路信息提取
            jiaolu_corporation_code = stop['jiaolu_corporation_code']#交路担当局代码
            jiaolu_train_style = stop['jiaolu_train_style']#交路车底类型
            jiaolu_dept_train = stop['jiaolu_dept_train']#交路担当客运段

            """
            print(f"车站: {station_name}")
            print(f"当前站车次: {station_train_code}")
            print(f"到达时间: {arrive_time}")
            print(f"出发时间: {start_time}")
            print(f"停留时间: {stopover_time}分钟")
            print(f"运行时间: {running_time}分钟")
            if station_tips:
                print(f"提示: {station_tips}")
            print("-" * 40)
            """
            #为出发到达添加：
            arrive_time = arrive_time[:2] + ":" +arrive_time[2:]
            start_time = start_time[:2] + ":" +start_time[2:]
            
            new_row = [station_train_code, station_name, waiting_room + "\n" + check_channel, exit_kou, arrive_time + "\n" + start_time, train_zhengwandian]
            data_list.append(new_row)

        header = [["车次", "站名", "候车室\n检票口", "出站口", "时刻表到达\n时刻表出发", "正晚点"]]

        table = header + data_list
        print("正晚点及检票口、出站口信息：")
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid", colalign=("center",)*len(header[0]), maxcolwidths=[20]*len(header[0])))
    

if __name__ == '__main__':
    while True:
        train = input("请输入车次：")
        if re.match(r'^(D|Z|T|K|N|L|A|Y|G|S|C)\d{1,4}|\d{1,4}|\d{5}$', train):
            date_str = input("请输入日期(2024-07-12)，空白则获取今天为时间：")
        else:
            print(f"{train}不是一个有效的车次 ")
            continue
        #date_str = input("请输入日期(2024-07-12)，空白则获取今天为时间：")
        if date_str == "":
            # 获取当前系统时间
            current_time = datetime.now()
            # 格式化为年-月-日
            date_str = current_time.strftime("%Y-%m-%d")
            #print(f"查询{date_str}的{train}时刻表")
        if is_valid_date(date_str):
            today = datetime.now().date()
            # 将 data_str 转换为日期对象
            data_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            # 计算今天之后的14天和3天前的日期
            future_date = today + timedelta(days=14)
            past_date = today - timedelta(days=3)
            if past_date <= data_date <= future_date:
                print(f"查询{date_str}的{train}时刻表")
            else:
                choice = input(f"{date_str}不在预售期内或者前3天，无法在线查询，是否进入本地数据库查询历史信息？(y/n)：")
                if choice.lower() == 'y':
                    print("进入本地数据库查询")
                    continue
                else:
                    continue
        else:
            print(f"{date_str} 不是一个有效的日期格式（年-月-日）")
            continue
        
        date = date_str.replace("-", "")
        #print(get_train_bureau(train, date))
        train_code_12306 = train_code_to_12306(train, date_str)
        train_code_12306_result = train_code_12306.split(',')[0]
        #print(train_code_12306_result)
        if train_code_12306_result == "-1":
            choice = input("查询列车可能已经停运，是否进入本地数据库查询历史信息？(y/n)：")
            if choice.lower() == 'y':
                print("进入本地数据库查询")
                continue
            else:
                continue
        else:
            #print(train_code_12306)
            train = train_code_12306.split(',')[1]
        get_train_info_llt_result = get_train_info_llt(train, date)
        get_train_info_llt_type = int(get_train_info_llt_result.split(',')[0])
        get_train_info_llt_msg = get_train_info_llt_result.split(',')[1]
        #print(get_train_info_llt_result)
        if get_train_info_llt_type ==0:
            continue
        elif get_train_info_llt_type == 1 or get_train_info_llt_type == 2:
            #进入12306api实时查询
            print("路路通无数据，进入12306api实时查询")
            try:
                json_data = fetch_train_info(train_code_12306, date_str)
                formatted_str = extract_and_format_data(json_data,train)
                print(formatted_str)
                train_code = formatted_str.split(',')[0]
                # 取/前面的部分
                train_code = train_code.split('/')[0]
                stop_info_list = get_stop_info(json_data)
                data_rows_12306 = []
                header_12306 = [["车站","车次","到达时间","出发时间","停留","区间历时","里程","均速","车站地点"]]
                print("时刻表：")
                for stop_info in stop_info_list:
                    #print(stop_info_list)
                    data_rows_12306.append(stop_info.split(','))
                # 将表头和数据组合成一个表格
                table_12306 = header_12306 + data_rows_12306
                # 使用 tabulate 打印表格，tablefmt 可选择 "grid" 或 "fancy_grid" 或 "pipe" 等样式来形成实线
                print(tabulate(table_12306, headers="firstrow", tablefmt="fancy_grid", colalign=("center",)*len(header_12306), maxcolwidths=[20]*len(header_12306[0])))
            except Exception as e:
                print(f"Error processing train {train}: {e}")
                continue
            continue
        else:
            print(get_train_info_llt_msg)
            continue
        
        