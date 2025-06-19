from flask import Flask, render_template, request, redirect, url_for
import math
import caculation_air 
import caculation_h2

app = Flask(__name__)

# 主页面
@app.route('/')
def index():
    return render_template('index.html')

# 电堆空气侧计算页面
@app.route('/Air.html', methods=['GET', 'POST'])
def Air():
    results = {
        'result1': None,
        'result2': None,
        'result3': None,
        'result4': None,
        'result5': None,
        'result6': None,
        'result7': None
    }

    if request.method == 'POST':
        try:
            # 获取用户输入
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            num3 = float(request.form['num3'])
            num4 = float(request.form['num4'])
            num5 = float(request.form['num5'])
            num6 = float(request.form['num6'])
            num7 = float(request.form['num7'])
            num8 = float(request.form['num8'])
            num9 = float(request.form['num9'])

            # 执行计算
            results['result1'] = caculation_air.calculate_air_result1(num1, num2, num3, num4)
            results['result2'] = caculation_air.calculate_air_result2(num6)
            results['result3'] = caculation_air.calculate_air_result3(num5, results['result1'], results['result2'], num7)
            results['result4'] = caculation_air.calculate_air_result4(results['result1'], num3)
            results['result5'] = caculation_air.calculate_air_result5(results['result1'])
            results['result6'] = caculation_air.calculate_air_result6(num8, num9, results['result4'], results['result5'])
            results['result7'] = caculation_air.calculate_air_result7(num1, num2, num4)

        except ValueError:
            results = {key: "输入无效，请输入数字!" for key in results}

    return render_template('Air.html', results=results)


# 电堆氢气侧计算页面
@app.route('/H2.html', methods=['GET', 'POST'])
def H2():
    results = {
        'result1': None,
        'result2': None,
        'result3': None,
        'result4': None,
        'result5': None    
    }
    
    if request.method == 'POST':
        try:
            # 从表单中获取用户输入的数字
            number1 = float(request.form['number1'])
            number2 = float(request.form['number2'])
            number3 = float(request.form['number3'])
            number4 = float(request.form['number4'])
            number5 = float(request.form['number5'])
            number6 = float(request.form['number6'])
            number7 = float(request.form['number7'])
            number8 = float(request.form['number8'])
            number9 = float(request.form['number9'])
            #执行计算
            results['result1']=caculation_h2.calculate_h2_result1(number1,number2,number4)
            results['result2'] = caculation_h2.calculate_h2_result2(number6)
            results['result3'] = caculation_h2.calculate_h2_result3(number1, number3, number5, results['result2'], number7)
            results['result4'] = caculation_h2.calculate_h2_result4(results['result1'], number3)
            results['result5'] = caculation_h2.calculate_h2_result5(number9, results['result1'], number3, number8)
            
        except ValueError:
            results = {key: "输入无效，请输入数字!" for key in results}
            
    return render_template('H2.html', results=results)
        
if __name__ == '__main__':
    app.run(debug=True)