# calculation_h2.py
import math

# 氢气侧计算函数
def calculate_h2_result1(number1, number2, number4):
    try:
        result1 = round(number1 * number2 / 2 / 96485 * 2 * number4, 4)
        return result1
    except Exception as e:
        return "计算错误，请检查输入!", e

def calculate_h2_result2(number6):
    try:
        result2 = round(0.61078 * math.exp(17.08085 * (number6 - 273.15) / (234.175 + number6 - 273.15)), 4)
        return result2
    except Exception as e:
        return "计算错误，请检查输入!", e

def calculate_h2_result3(number1, number3, number5, result2, number7):
    try:
        if number5 > result2:
            result3 = round(number1 * (number3 - 1) / 2 / (number5 - result2 * number7 / 100) * result2 * number7 / 100 * 18, 4)
            return result3
        else:
            return "计算错误，空气入口压力小于饱和蒸汽压！"
    except Exception as e:
        return "计算错误，请检查输入!", e

def calculate_h2_result4(result1, number3):
    try:
        result4 = round(result1 * (number3 - 1), 4)
        return result4
    except Exception as e:
        return "计算错误，请检查输入!", e

def calculate_h2_result5(number9, result1, number3, number8):
    try:
        temp = 0.61078 * math.exp(17.08085 * (number9 - 273.15) / (234.175 + number9 - 273.15))
        result5 = round(temp * 18 * (result1 * (number3 - 1) / 2) / (number8 - temp), 4)
        return result5
    except Exception as e:
        return "计算错误，请检查输入!", e