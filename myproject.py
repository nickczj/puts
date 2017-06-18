from flask import Flask, render_template, request, redirect, url_for, send_file
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")
    
@app.route("/", methods=['POST'])
def handle_data(excelfile):
    text = request.form['text']
    
    import StringIO
    import requests
    import re
    import openpyxl
    import datetime
    from bs4 import BeautifulSoup

    soup=BeautifulSoup(text,"html.parser")
    # print(soup.prettify())
    # e=open("test3.html",encoding="utf8").read()
    # soup2=BeautifulSoup(e,"html.parser")

    default_date=datetime.date.today().strftime("%d/%m/%Y")

    dates=[]
    sites=[]
    amount=[]

    for string in soup.stripped_strings:
        if "Total: SGD " in string:
            temp=repr(string)[len("Total: SGD ")+1:-1]
            amount.append(float(temp))
            
    for string in soup.stripped_strings:
        if "Placed on " in string:
            temp=repr(string)[len("Placed on ")+1:-1]
            dates.append(temp)
            
    # all=soup2.find_all("strong",{"class":"totalamount"})
    # amount.append(float(all[0].string))
    # dates.append(default_date)

    wb=openpyxl.Workbook()
    sheet=wb.create_sheet()
    sheet.title='Expenses'
    sheet['A1']='Date'
    sheet['B1']='Website'
    sheet['C1']='Amount'
    wb.remove_sheet(wb.get_sheet_by_name('Sheet'))

    for i in range(len(dates)):
        sheet['A{}'.format(i+2)]=dates[i]
        
    for i in range(len(amount)):
        sheet['C{}'.format(i+2)]=amount[i]
        
    wb.save(excelfile)
    strIO = StringIO.StringIO()
    strIO.write('test')
    strIO.seek(0)
    return send_file(strIO, attachment_filename=filename, as_attachment=True)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
