# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 18:59:23 2024

@author: Dell
"""
import sys

BG_IMG_PATH = "sunny.jpg"
GPS_IMG_PATH = "gps.png"
file_path = "city_name.txt"
BTN_STYLE_SHEET = """
    QPushButton {
        border: none;               /* 移除边框 */
        padding: 0px;               /* 去掉内边距 */
        background: transparent;    /* 背景透明 */
        outline: none;              /* 去掉焦点边框 */
    }
    QPushButton::hover {
        border: none;               /* 悬停时无边框 */
        background: transparent;    /* 背景透明 */
    }
    QPushButton::pressed {
        border: none;               /* 按下时无边框 */
        background: transparent;    /* 背景透明 */
    }
    QPushButton::focus {
        border: none;               /* 焦点时无边框 */
        outline: none;              /* 去掉焦点虚线 */
    }
    QPushButton::menu-indicator {
        image: none;                /* 隐藏默认的下拉箭头 */
        width: 0px;
        height: 0px;
    }
"""
def GET_CURRENT_CITY_NAME():
    # TODO
    return "南京"

def GET_CITY_NAME():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines   
    except Exception as e:
        print("error: {0}".format(e), flush=True)
        sys.exit(-1)

def IS_REPUSH_CITY(city_name):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return city_name in content
    except Exception as e:
        print("error: {0}".format(e), flush=True)
        sys.exit(-1)

def ADD_CITY(new_name):
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write("\n" + new_name)
    except Exception as e:
        print("error: {0}".format(e), flush=True)
        sys.exit(-1)

def DEL_CITY(city_name):
    try:
        print(f"try opening \"{file_path}\"", flush=True)
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        print(f"\"{file_path}\" open successfully, contents read", flush=True)
        updated_lines = [line for line in lines if line.strip() != city_name]

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)
        print("del success：\"{0}\"".format(city_name), flush=True)
    except Exception as e:
        print("error: {0}".format(e), flush=True)
        sys.exit(-1)

def TOP_CITY(city_idx):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    
        line_to_move = lines.pop(city_idx)
        lines.insert(1, "\n")
        lines.insert(1, line_to_move)
    
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
    except Exception as e:
        print("error: {0}".format(e), flush=True)
        sys.exit(-1)
    
def BOTTOM_CITY(city_idx):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        line_to_move = lines.pop(city_idx)
        lines.append(line_to_move)
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
    except Exception as e:
        print("error: {0}".format(e), flush=True)
        sys.exit(-1)

def CHECK_CITY():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        non_empty_lines = [line for line in lines if line.strip() != ""]
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(non_empty_lines)
    except Exception as e:
        print("error: {0}".format(e), flush=True)
        sys.exit(-1)

def GET_CURRENT_TEMPERATURE(city_name):
    # TODO
    return "23"

def GET_CURRENT_WEATHER(city_name):
    # TODO
    return "晴"

def GET_CURRENT_TEMPERATURE_RANGE(city_name):
    # TODO
    return "24 / 17°C"

def GET_CURRENT_TIME():
    # TODO
    return 

def GET_PREDICT_TIME(city_name, cur_time=GET_CURRENT_TIME()):
    # TODO
    return ["下午3:00", "下午3:30", "下午4:00"]

def GET_PREDICT_WEATHER(city_name, time):
    # TODO
    if time == "下午3:30":
        return "sun&cloud"
    else:
        return "sun"
    
def GET_PREDICT_TEMPERATURE(city_name, time):
    # TODO
    if time == "下午3:30":
        return 22
    else:
        return 23
    
def GET_HUMIDITY(city_name, cur_time=GET_CURRENT_TIME()):
    # TODO
    humidity = 0.7
    text = ""
    if humidity > 0.6:
        text = "较高"
    elif humidity < 0.4:
        text = "较低"
    else:
        text = "正常"
    return humidity, text

def GET_DRESSING_GUIDE(city_name):
    cur_weather = GET_CURRENT_WEATHER(city_name)
    cur_temperature = GET_CURRENT_TEMPERATURE(city_name)
    # TODO
    return [["clothes", "短袖"], ["uv", "紫外线强"], ["flower", "易过敏"]]
    