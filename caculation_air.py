# calculation_air.py
import math

# 空气侧计算函数
def calculate_air_result1(number1, number2, number3, number4):
    return round(number1 * number2 / 4 / 96485 * number3 / 0.21 * 28.85 * number4, 4)

def calculate_air_result2(number6):
    return round(0.61078 * math.exp(17.08085 * (number6 - 273.15) / (234.175 + number6 - 273.15)), 4)

def calculate_air_result3(number5, result1, result2, number7):
    if number5 > result2:
        return round(result1 / 28.85 / (number5 - result2 * number7/ 100) * result2 * number7 / 100 * 18, 4)
    else:
        return "计算错误，空气入口压力小于饱和蒸汽压！"

def calculate_air_result4(result1, number3):
    return round(result1/ 4.25 / number3 * (number3 - 1), 4)

def calculate_air_result5(result1):
    return round(result1 / 4.25 * 3.25, 4)

def calculate_air_result6(number8, number9, result4, result5):
    return round(0.61078 * math.exp(17.08085 * (number9 - 273.15) / (234.175 + number9 - 273.15)) * 18 * (result4 / 32 + result5 / 28) / (number8 - 0.61078 * math.exp(17.08085 * (number9 - 273.15) / (234.175 + number9 - 273.15))), 4)

def calculate_air_result7(number1, number2, number4):
    return round((number1 * number2/ 4 / 96485 * 2 * 18 * number4), 4)

