import csv, io

from django.core.checks import messages
from django.shortcuts import render
import datetime

from django.template import Template, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from mysql.connector import cursor
import pymysql
from  .forms import UploadCsvfile
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='loan')
cursor = conn.cursor()

def uploadPage(request):
    print('load upload page')
    template = loader.get_template ('uploadcsv.html')
    return HttpResponse(template.render( request))

def UploadCsv(request):
    print ("Start file upload view")

    if request.method == 'POST' :
        print ("after if Start file upload view")
        form=UploadCsvfile(request.POST)
        print ("start validation file upload view")
        csvfile = request.FILES['file']
        print(csvfile)

        # let's check if it is a csv file
        #if not csvfile.name.endswith ('.csv'):
            #messages.error (request, 'THIS IS NOT A CSV FILE')
        data_set = csvfile.read().decode ('UTF-8')
        io_string = io.StringIO(data_set)


        reader = csv.reader (io_string, delimiter=",", quotechar="|")
        l_ins_script = "INSERT INTO loan_mdm_lookup( loan_mdm_lookup_id, CreditScoreMin,CreditScoreMax,LoanAmountMin,LoanAmountMax ,IntrestRatePct," \
                       "DurationMonths,eff_from_date,eff_to_date) VALUES(%s,%s ,%s ,%s,%s,%s,%s,%s,%s)"

        for row in reader:
            print(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            insertVal =  ( row[0], row[1] ,row[2] , row[3] , row[4] ,row[5] ,row[6] , row[7] , row[8])
            cursor.execute(l_ins_script,insertVal)
            conn.commit()
        return HttpResponse('File Uploaded')