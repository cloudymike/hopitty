from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      for key, value in result.items():
          print key, value
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)
   