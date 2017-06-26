#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for
from reportdb import get_popular_articles,get_popular_authors,get_error_log

app = Flask(__name__)

# HTML template for the report page
HTML_WRAP = """
<!DOCTYPE html>
<html>
  <meta charset="utf-8">
  <meta name="viewport" content="initial-scale=1,user-scalable=yes">
  <head>
    <title>DB Forum</title>
    {0}
  </head>
  <body>
        <div class="center">
        <form action="" method="post">
            Report Name:
            <select name="preport">
                <option value="0"></option>
                <option value="1">Most Popular Articles Report</option>
                <option value="2">Most Popular Aurthors Report</option>
                <option value="3">Error Request Report (threshold 1%)</option>
            </select>
            <input type="submit" value="submit">
        </form>
        </div>
        <br>
        <hr>
        <div class="center">
    <!-- report content  -->
     
            {1}     
        </div>
  </body>
</html>
"""

style = """
<style type="text/css">
        .center {
            margin: auto;
            width: 60%;
            padding: 10px;
            }
        .tg  {
            border-collapse:collapse;
            border-spacing:0;
            }
        .tg td{
            font-family:Arial, sans-serif;
            font-size:14px;
            padding:10px 5px;
            border-style:solid;
            border-width:1px;
            overflow:hidden;
            word-break:normal;
            }
        .tg th{
            font-family:Arial, sans-serif;
            font-size:14px;
            font-weight:normal;
            padding:10px 5px;
            border-style:solid;
            border-width:1px;
            overflow:hidden;
            word-break:normal;
            background-color:#cccccc;
            color:#000000
            }
    </style>
"""


@app.route('/', methods=['GET'])
def main():
    '''Main page of the Reporting page.'''
    return HTML_WRAP.format(style, '')

@app.route('/', methods=['POST'])
def post():
    '''Submit Report Type.'''
    report_type = request.form['preport']
    # preport is the drop downlist
    # Value 1: popular article report 
    if report_type=="1":
        report=get_popular_articles()
    # Value 2: popular author report
    if report_type=="2":
        report=get_popular_authors()
    # Value 3: error request rate that exceeds 1%
    if report_type=="3":
        report=get_error_log()
    report_html=HTML_WRAP.format(style, report)
    return report_html

# Default port number 8000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)