from flask import Flask, request, render_template_string, redirect, url_for
import math

app = Flask(__name__)

# 主页面
@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>主页面</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-image: url('/static/bg_cacu.png');
                    background-size: cover;
                    background-position: center;
                    opacity: 0.8;
                }
                .container {
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }
                button {
                    padding: 10px;
                    margin: 5px;
                    font-size: 16px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>计算工具</h1>
                <button onclick="window.location.href='/air'">电堆空气侧计算</button>
                <button onclick="window.location.href='/anode'">电堆氢气侧计算</button>
                <button onclick="window.location.href='/mixture'">常见混合气体计算</button>
                <button onclick="window.location.href='/purge'">理想气体一维绝热流动计算(<=音速)</button>
            </div>
        </body>
        </html>
    ''')

# 电堆空气侧计算页面

# 定义 HTML 模板字符串
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>电堆空气侧计算</title>
    <style>
        /* 简单的样式设置 */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-image: url('/static/bg_cacu.png'); /* 设置本地背景图片路径 */
            background-size: cover; /* 背景图片覆盖整个页面 */
            background-position: center; /* 背景图片居中 */
            opacity: 0.8; /* 设置背景图片透明度为80% */
        }
        .container {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        input[type="number"], button {
            padding: 10px;
            margin: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            margin-top: 20px;
        }
        .left-results, .right-results {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }  

        .result-label {
            font-size: 16px;
            color: #0000FF; /* 标准蓝色 */
            margin-right: 10px;
        }
        .result-box {
            font-size: 16px;
            color: #0000FF; /* 标准蓝色 */
            background-color: white; /* 背景填充白色 */
            border: 1px solid black; /* 黑色边框 */
            padding: 10px; /* 与输入框相同的内边距 */
            border-radius: 4px; /* 圆角边框 */
            width: 300px; /* 固定宽度 */
            text-align: center; /* 文本居中 */
            margin-bottom: 10px; /* 添加间距 */
            margin-right: 20px; /* 添加间距 */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>电堆空气侧计算</h1>
        <!-- 表单用于接收用户输入 -->
        <form method="post">
            <input type="number" name="number1" placeholder="电流密度 A/cm2" step="0.001" required>
            <input type="number" name="number2" placeholder="单片活性面积 cm2" step="0.001" required>
            <input type="number" name="number3" placeholder="计量比" step="0.001" required>
            <input type="number" name="number4" placeholder="电堆片数 片" step="0.001" required>
            <input type="number" name="number5" placeholder="空气入堆压力 kPa.a" step="0.001" required>
            <input type="number" name="number6" placeholder="入堆温度 K" step="0.001" required>
            <input type="number" name="number7" placeholder="入堆相对湿度 %" step="0.001" required>
            <input type="number" name="number8" placeholder="空气出堆压力 kPa.a" step="0.001" required>
            <input type="number" name="number9" placeholder="出堆温度 K" step="0.001" required>
            <button type="submit">计算</button>
        </form>
        <!-- 如果有结果，则显示结果 -->
        <div class="result-container">
            <div class="left-results">
                {% if result1 %}
                    <div>
                        <div class="result-label">电堆入堆空气质量流量：</div>
                        <div class="result-box">{{ result1 }} g/s</div>
                    </div>
                {% endif %}
                {% if result2 %}
                    <div>
                        <div class="result-label">电堆入堆饱和蒸汽压：</div>
                        <div class="result-box">{{ result2 }} kPa</div>
                    </div>
                {% endif %}
                {% if result3 %}
                    <div>
                        <div class="result-label">电堆入堆水蒸气质量流量：</div>
                        <div class="result-box">{{ result3 }} g/s</div>
                    </div>
                {% endif %}
            </div>
            <div class="right-results">
                {% if result4 %}
                    <div>
                        <div class="result-label">电堆出堆剩余未消耗氧气：</div>
                        <div class="result-box">{{ result4 }} g/s</div>
                    </div>
                {% endif %}
                {% if result5 %}
                    <div>
                        <div class="result-label">电堆出堆氮气：</div>
                        <div class="result-box">{{ result5 }} g/s</div>
                    </div>
                {% endif %}
                {% if result6 %}
                    <div>
                        <div class="result-label">电堆出堆饱和水蒸气：</div>
                        <div class="result-box">{{ result6 }} g/s</div>
                    </div>
                {% endif %}
                {% if result7 %}
                    <div>
                        <div class="result-label">电堆出堆反应生成水：</div>
                        <div class="result-box">{{ result7 }} g/s</div>
                    </div>
                {% endif %}
            </div>
        </div>
        
</body>
</html>
'''
# 定义路由和视图函数
@app.route('/air', methods=['GET', 'POST'])
def air():

    result1 = 1  # 初始化第一个结果变量
    result2 = 1  # 初始化第二个结果变量
    result3 = 1  # 初始化第二个结果变量
    result4 = 1  # None初始化第一个结果变量
    result5 = 1  # 初始化第二个结果变量
    result6 = 1  # 初始化第二个结果变量
    result7 = 1  # 初始化第一个结果变量
 
    if request.method == 'POST':  # 如果是 POST 请求
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
            # 计算1 入堆空气流量
            result1 = round(number1 * number2 / 4 / 96485 * number3 / 0.21 * 28.85 * number4, 4)
            
            # 计算2 入堆饱和蒸汽压
            
            #方法2
            result2 = round(0.61078*math.exp(17.08085*(number6-273.15)/(234.175+number6-273.15)), 4)
            
            #方法1
            #result2 = round(math.exp(-5800.2206 / number6 + 1.3914993 - 0.048640239 * number6 + 4.1764768e-5 * number6**2 - 1.44521e-8 * number6**3 + 6.5459673 * math.log(number6))/1000, 4)
            
            # 计算3 入堆水蒸气流量
            if number5 > result2:
                result3 = round(result1 / 28.85 / (number5 - result2*number7/100) * result2*number7/100 * 18, 4)
            else:
                result3 = "计算错误，空气入口压力小于饱和蒸汽压！"
          
            #计算4 出堆未消耗氧气流量 
            result4 = round(result1 /4.25 / number3 * (number3-1), 4)
            
            #计算5电堆出堆氮气
            result5 = round(result1/4.25*3.25,4)
            #计算6 电堆出堆饱和水蒸气流量
            result6 = round(0.61078*math.exp(17.08085*(number9-273.15)/(234.175+number9-273.15))*18*(result4/32+result5/28)/(number8-0.61078*math.exp(17.08085*(number9-273.15)/(234.175+number9-273.15))), 4)
        
            #计算7 电堆生成水流量            
            result7 = round((number1 * number2 / 4 / 96485 *2*18*number4), 4)
                 
        except ValueError:  # 如果输入无效，捕获 ValueError
            result1 = "输入无效，请输入数字!"
            result2 = "输入无效，请输入数字!"
            result3 = "输入无效，请输入数字!"
            result4 = "输入无效，请输入数字!"
            result5 = "输入无效，请输入数字!"
            result6 = "输入无效，请输入数字!"
            result7 = "输入无效，请输入数字!"
    # 渲染 HTML 模板，并将结果传递给模板
    return render_template_string(html_template, result1=result1, result2=result2, result3=result3, result4=result4,result5=result5, result6=result6, result7=result7)
    

# 电堆氢气侧计算页面
@app.route('/anode', methods=['GET', 'POST'])
def anode():
    result1 = 1  # 初始化第一个结果变量
    result2 = 1  # 初始化第二个结果变量
    result3 = 1  # 初始化第二个结果变量
    result4 = 1  # None初始化第一个结果变量
    result5 = 1  # None初始化第一个结果变量
    
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

            #计算1 入堆新鲜氢气流量
            result1 = round(number1 * number2 / 2 / 96485 * 2* number4, 4)
        
            # 计算2 入堆饱和蒸汽压  
            #方法2
            result2 = round(0.61078*math.exp(17.08085*(number6-273.15)/(234.175+number6-273.15)), 4)
        
            #计算3 入堆水蒸气含量
            if number5 > result2:
                result3 = round(result1 * (number3-1) / 2 / (number5 - result2*number7/100) * result2*number7/100 * 18, 4)
            else:
                result3 = "计算错误，空气入口压力小于饱和蒸汽压！"
        
            #计算4 出口循环氢气流量
            result4 = round(result1*(number3-1), 4)
        
            #计算5 出堆饱和水蒸气含量
            result5 = round(0.61078*math.exp(17.08085*(number9-273.15)/(234.175+number9-273.15))*18*(result1*(number3-1)/2)/(number8-0.61078*math.exp(17.08085*(number9-273.15)/(234.175+number9-273.15))), 4)
        
        except ValueError:  # 如果输入无效，捕获 ValueError
            result1 = "输入无效，请输入数字!"
            result2 = "输入无效，请输入数字!"
            result3 = "输入无效，请输入数字!"
            result4 = "输入无效，请输入数字!"
            resulr5 = "输入无效，请输入数字!"
            
        
    anode_html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>电堆氢气侧计算</title>
        <style>
            /* 简单的样式设置 */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url('/static/bg_cacu.png'); /* 设置本地背景图片路径 */
                background-size: cover; /* 背景图片覆盖整个页面 */
                background-position: center; /* 背景图片居中 */
                opacity: 0.8; /* 设置背景图片透明度为80% */
            }
            .container {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            input[type="number"], button {
                padding: 10px;
                margin: 5px;
                font-size: 16px;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .result-container {
                display: flex;
                justify-content: center;
                align-items: flex-start;
                margin-top: 20px;
            }
            .left-results, .right-results {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            }  
            .result-label {
                font-size: 16px;
                color: #0000FF; /* 标准蓝色 */
                margin-right: 10px;
            }
            .result-box {
                font-size: 16px;
                color: #0000FF; /* 标准蓝色 */
                background-color: white; /* 背景填充白色 */
                border: 1px solid black; /* 黑色边框 */
                padding: 10px; /* 与输入框相同的内边距 */
                border-radius: 4px; /* 圆角边框 */
                width: 300px; /* 固定宽度 */
                text-align: center; /* 文本居中 */
                margin-bottom: 10px; /* 添加间距 */
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>电堆氢气侧计算</h1>
            <form method="post">
                <input type="number" name="number1" placeholder="电流密度 A/cm2" step="0.001" required>
                <input type="number" name="number2" placeholder="单片活性面积 cm2" step="0.001" required>
                <input type="number" name="number3" placeholder="计量比" step="0.001" required>
                <input type="number" name="number4" placeholder="电堆片数 片" step="0.001" required>
                <input type="number" name="number5" placeholder="入堆压力 kPa.a" step="0.001" required>
                <input type="number" name="number6" placeholder="入堆温度 K" step="0.001" required>
                <input type="number" name="number7" placeholder="入堆相对湿度 %" step="0.001" required>
                <input type="number" name="number8" placeholder="出堆压力 kPa.a" step="0.001" required>
                <input type="number" name="number9" placeholder="出堆温度 K" step="0.001" required>
                <button type="submit">计算</button>
                
            </form>
                <div class="result-container">
                    <div class="left-results">
                        {% if result1 %}
                            <div>
                                <div class="result-label">电堆入堆新鲜氢气质量流量：</div>
                                <div class="result-box">{{ result1 }} g/s</div>
                            </div>
                        {% endif %}
                        {% if result2 %}
                            <div>
                                <div class="result-label">电堆入堆饱和蒸汽压：</div>
                                <div class="result-box">{{ result2 }} kPa</div>
                            </div>
                        {% endif %}
                        {% if result3 %}
                            <div>
                                <div class="result-label">电堆入堆水蒸气流量(按照循环氢气流量折算)：</div>
                                <div class="result-box">{{ result3 }} g/s</div>
                            </div>
                        {% endif %}
                    </div>
                    <div class="right-results">
                        {% if result4 %}
                            <div>
                                <div class="result-label">出堆循环氢气质量流量：</div>
                                <div class="result-box">{{ result4 }} g/s</div>
                            </div>
                        {% endif %}
                        {% if result5 %}
                            <div>
                                <div class="result-label">出堆饱和水蒸气流量：</div>
                                <div class="result-box">{{ result5 }} g/s</div>
                            </div>
                        {% endif %}            
                </div>
    </body>
    </html>
    '''
    return render_template_string(anode_html_template, result1=result1,result2=result2,result3=result3,result4=result4,result5=result5)
     
    


# 常见混合气体计算页面
@app.route('/mixture', methods=['GET', 'POST'])
def mixture():
    result1 = 1  # 初始化第一个结果变量
    result2 = 1  # 初始化第二个结果变量
    result3 = 1  # 初始化第二个结果变量
    result4 = 1  # None初始化第一个结果变量
    
    if request.method == 'POST':  # 如果是 POST 请求
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
            # 检查摩尔组分之和是否为1
            
            if not math.isclose(number1 + number2 + number3 + number4 + number5 + number6 + number7, 1.0, rel_tol=1e-3):        
    
                result1 = result2 = result3 = result4 = "摩尔组分之和不为1，请检查输入！"        
    
                return render_template_string(html_template, result1=result1, result2=result2, result3=result3,result4=result4)
     
            # 计算1 混合物粘度
            result1 = round(number1*17.16*((number9+273.15)/273)**1.5*(273+111)/(number9+273+111)+
            number2*16.63*((number9+273.15)/273)**1.5*(273+107)/(number9+273+107)+
            number3*19.19*((number9+273.15)/273)**1.5*(273+139)/(number9+273+139)+
            number4*13.7*((number9+273.15)/273)**1.5*(273+222)/(number9+273+222)+
            number5*16.57*((number9+273.15)/273)**1.5*(273+136)/(number9+273+136)+
            number6*8.411*((number9+273.15)/273)**1.5*(273+47)/(number9+273+47)+
            number7*11.2*((number9+273.15)/273)**1.5*(273+1064)/(number9+273+1064), 4)      
            # 计算2 混合物的分子量
            result2 = round(number1*28.97+number2*28.02+number3*32+number4*44.01+number5*28.01+number6*2.01+number7*18.02, 4)      
            # 计算3 混合物的气体常数
            result3 = round(8.31447/(result2/1000),4)
            # 计算4 混合物的密度
            result4 = round(number8*100000/(result3*(number9+273.15)),4)
                                
        except ValueError:  # 如果输入无效，捕获 ValueError
            result1 = "输入无效，请输入数字!"
            result2 = "输入无效，请输入数字!"
            result3 = "输入无效，请输入数字!"
            result4 = "输入无效，请输入数字!"
                
   
    # 定义 HTML 模板字符串
    mixture_html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>常见混合气体计算</title>
        <style>
            /* 简单的样式设置 */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url('/static/bg_cacu.png'); /* 设置本地背景图片路径 */
                background-size: cover; /* 背景图片覆盖整个页面 */
                background-position: center; /* 背景图片居中 */
                opacity: 0.8; /* 设置背景图片透明度为80% */
            }
            .container {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            input[type="number"], button {
                padding: 10px;
                margin: 5px;
                font-size: 14px;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .result-container {
                display: flex;
                justify-content: center;
                align-items: flex-start;
                margin-top: 20px;
            }
            .left-results, .right-results {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
            }  
    
            .result-label {
                font-size: 16px;
                color: #0000FF; /* 标准蓝色 */
                margin-right: 10px;
            }
            .result-box {
                font-size: 16px;
                color: #0000FF; /* 标准蓝色 */
                background-color: white; /* 背景填充白色 */
                border: 1px solid black; /* 黑色边框 */
                padding: 10px; /* 与输入框相同的内边距 */
                border-radius: 4px; /* 圆角边框 */
                width: 300px; /* 固定宽度 */
                text-align: center; /* 文本居中 */
                margin-bottom: 10px; /* 添加间距 */
                margin-right: 20px; /* 添加间距 */
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>常见混合气体计算</h1>
            <!-- 表单用于接收用户输入 -->
            <form method="post">
                <input type="number" name="number1" placeholder="Air摩尔组分" step="0.001" required style="width:100px;">
                <input type="number" name="number2" placeholder="N2摩尔组分" step="0.001" required style="width:100px;">
                <input type="number" name="number3" placeholder="O2摩尔组分" step="0.001" required style="width:100px;">
                <input type="number" name="number4" placeholder="CO2摩尔组分" step="0.001" required style="width:100px;">
                <input type="number" name="number5" placeholder="CO摩尔组分" step="0.001" required style="width:100px;">
                <input type="number" name="number6" placeholder="H2摩尔组分" step="0.001" required style="width:100px;">
                <input type="number" name="number7" placeholder="H2O(气态)摩尔组分" step="0.001" required style="width:150px;">
                <br> <!-- 换行 -->
                <input type="number" name="number8" placeholder="指定压力 bar.a" step="0.001" required>
                <input type="number" name="number9" placeholder="指定温度 ℃" step="0.001" required>
                <button type="submit">计算</button>
            </form>
            <!-- 如果有结果，则显示结果 -->
            <div class="result-container">
                <div class="left-results">
                    {% if result1 %}
                        <div>
                            <div class="result-label">混合物粘度(加权平均） ：</div>
                            <div class="result-box">{{ result1 }} e-6Pa s </div>
                        </div>
                    {% endif %}
                    {% if result2 %}
                        <div>
                            <div class="result-label">混合物分子量：</div>
                            <div class="result-box">{{ result2 }} g/mol </div>
                        </div>
                    {% endif %}
                    {% if result3 %}
                        <div>
                            <div class="result-label">混合物气体常数：</div>
                            <div class="result-box">{{ result3 }} J/(kg K) </div>
                        </div>
                    {% endif %}
                    {% if result4 %}
                        <div>
                            <div class="result-label">混合物气体密度：</div>
                            <div class="result-box">{{ result4 }} kg/m3 </div>
                        </div>
                    {% endif %}
                </div>
            </div>
            
    </body>
    </html>
    '''
   # 渲染 HTML 模板，并将结果传递给模板
    return render_template_string(mixture_html_template, result1=result1, result2=result2, result3=result3, result4=result4)

# 理想气体一维绝热流动计算
@app.route('/purge', methods=['GET', 'POST'])
def purge():
    result1 = 1  # 初始化第一个结果变量
    result2 = 1  # 初始化第二个结果变量
    result3 = 1  # 初始化第二个结果变量
  
    
    if request.method == 'POST':  # 如果是 POST 请求
        try:
             # 从表单中获取用户输入的数字
            number1 = float(request.form['number1'])
            number2 = float(request.form['number2'])
            number3 = float(request.form['number3'])
            number4 = float(request.form['number4'])
            number5 = float(request.form['number5'])
            number6 = float(request.form['number6'])
            number7 = float(request.form['number7'])
       
            
     
            # 计算1 计算流通面积
            result1 = round(number3**2*3.1415926/4/1000000, 8)  
                
            # 计算2 计算上下游压比
            result2 = round(number5/number4, 4)      
            
            # 计算3 预估质量流量
            if result2 >0.528:
            
              result3 = round(result1*number4/number7*math.sqrt(2/(number6+273.15)/(8.31447/number1*1000))*math.sqrt(number2/(number2-1)*((number5/number4)**(2/number2)-(number5/number4)**((number2+1)/number2))), 8)
            
            elif result2 <= 0.528:
            
              result3 = round(result1*number4/number7*math.sqrt(1/(number6+273.15)/(8.31447/number1*1000))*math.sqrt(number2*(2/(number2+1))**((number2+1)/(number2-1))),8)
            
                                
        except ValueError:  # 如果输入无效，捕获 ValueError
            result1 = "输入无效，请输入数字!"
            result2 = "输入无效，请输入数字!"
            result3 = "输入无效，请输入数字!"
            result4 = "输入无效，请输入数字!"
                
   
    # 定义 HTML 模板字符串
    purge_html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>常见混合气体计算</title>
        <style>
            /* 简单的样式设置 */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url('/static/bg_cacu.png'); /* 设置本地背景图片路径 */
                background-size: cover; /* 背景图片覆盖整个页面 */
                background-position: center; /* 背景图片居中 */
                opacity: 0.8; /* 设置背景图片透明度为80% */
            }
            .container {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            input[type="number"], button {
                padding: 10px;
                margin: 5px;
                font-size: 14px;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .result-container {
                display: flex;
                justify-content: center;
                align-items: flex-start;
                margin-top: 20px;
            }
            .left-results, .right-results {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
            }  
    
            .result-label {
                font-size: 16px;
                color: #0000FF; /* 标准蓝色 */
                margin-right: 10px;
            }
            .result-box {
                font-size: 16px;
                color: #0000FF; /* 标准蓝色 */
                background-color: white; /* 背景填充白色 */
                border: 1px solid black; /* 黑色边框 */
                padding: 10px; /* 与输入框相同的内边距 */
                border-radius: 4px; /* 圆角边框 */
                width: 300px; /* 固定宽度 */
                text-align: center; /* 文本居中 */
                margin-bottom: 10px; /* 添加间距 */
                margin-right: 20px; /* 添加间距 */
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>理想气体一维绝热流动计算(<=音速)</h1>
            <!-- 表单用于接收用户输入 -->
            <form method="post">
                <input type="number" name="number1" placeholder="分子量(摩尔质量)" step="0.001" required style="width:150px;">
                <input type="number" name="number2" placeholder="绝热指数(默认1.4)" step="0.001" required style="width:150px;">
                <br> <!-- 换行 -->
                <input type="number" name="number3" placeholder="喉口直径(参考)mm" step="0.001" required style="width:150px;">
               
                <br> <!-- 换行 -->
                <input type="number" name="number4" placeholder="上游滞止压力Pa" step="0.001" required style="width:100px;">
                <input type="number" name="number5" placeholder="下游静压Pa" step="0.001" required style="width:100px;">
                <br> <!-- 换行 -->
                <input type="number" name="number6" placeholder="上游滞止温度℃" step="0.001" required style="width:150px;">
                <input type="number" name="number7" placeholder="流量系数" step="0.001" required>
                <br> <!-- 换行 -->
                <button type="submit">计算</button>
            </form>
            <!-- 如果有结果，则显示结果 -->
            <div class="result-container">
                <div class="left-results">
                    {% if result1 %}
                        <div>
                            <div class="result-label">计算流通面积 ：</div>
                            <div class="result-box">{{ result1 }} m2 </div>
                        </div>
                    {% endif %}
                    {% if result2 %}
                        <div>
                            <div class="result-label">上下游压比：</div>
                            <div class="result-box">{{ result2 }}  </div>
                        </div>
                    {% endif %}
                </div>
                <div class="right-results"> 
                    {% if result3 %}
                        <div>
                            <div class="result-label">预估质量流量：</div>
                            <div class="result-box">{{ result3 }} kg/s </div>
                        </div>
                    {% endif %}
                </div>
            </div>
            
    </body>
    </html>
    '''
   # 渲染 HTML 模板，并将结果传递给模板
    return render_template_string(purge_html_template, result1=result1, result2=result2, result3=result3)          
        

if __name__ == '__main__':
    app.run(debug=True)

