import datetime
from django.template import Template, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from mysql.connector import cursor
import pymysql
from rest_framework import views

from mdmteam.forms import TestForm, DeleteForm, UpdateForm
from django.shortcuts import render, redirect
import csv, io

from django.shortcuts import render
import datetime
from users.ConnpoolUser import  GetConn, db3,   db3curr

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='loan')
cursor = conn.cursor()

def mdm(request):

    template = loader.get_template('mdm.html')

    username=""
    context = {'home':'http://127.0.0.1:8001'}
    print(username)
    return render (request, 'mdm.html')
    #return HttpResponse(template.render(context, request))



# Create your views here.
def reports(request):
    import pymysql

    # Create Connection Object
    # ##############################################################################
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='loan')
    cursor = conn.cursor()


    # Reading multiple datatypes and print to screen
    cursor.execute("select * from loan_mdm_lookup;")
    # use fetchall() to get the list of row data
    l_data = []
    
    for loan_mdm_lookup_id, CreditScoreMin, CreditScoreMax, LoanAmountMin, LoanAmountMax, IntrestRatePct, DurationMonths, eff_from_date, eff_to_date in cursor.fetchall():
        l_data.append({  "loan_mdm_lookup_id": loan_mdm_lookup_id
                        ,"CreditScoreMin": CreditScoreMin
                        ,"CreditScoreMax": CreditScoreMax
                        ,"LoanAmountMin" : LoanAmountMin
                        ,"LoanAmountMax" : LoanAmountMax
                        ,"IntrestRatePct": IntrestRatePct
                        ,"DurationMonths": DurationMonths
                        ,"eff_from_date" : eff_from_date
                        ,"eff_to_date"   : eff_to_date})


    print(l_data)
    
    # Create Template Object
    template = loader.get_template('mdm_report.html')
    context = { 'l_data':l_data }
    return HttpResponse(template.render(context, request))


def loanManager(request):
    if request.method == 'POST':

        # Create Template Object
        template = loader.get_template ('mdm_single_loan_entry.html')
        testForm = TestForm (request.POST)

        if testForm.is_valid ():
            LoanID = testForm.cleaned_data.get ('LoanID')
            CreditScoreMin = testForm.cleaned_data.get ('CreditScoreMin')
            CreditScoreMax = testForm.cleaned_data.get ('CreditScoreMax')
            LoanAmountMin = testForm.cleaned_data.get ('LoanAmountMin')
            LoanAmountMax = testForm.cleaned_data.get ('LoanAmountMax')
            IntrestRatePct = testForm.cleaned_data.get ('IntrestRatePct')
            DurationMonths = testForm.cleaned_data.get ('DurationMonths')

            print("before reading dates")
            eff_from_date = testForm.cleaned_data.get ('eff_from_date')
            eff_to_date = testForm.cleaned_data.get ('eff_to_date')

            dateVal = datetime.datetime.strptime (str (eff_to_date), '%Y%m%d')
            toDate = '"'+datetime.date.strftime (dateVal, '%Y-%m-%d')+'"'

            print ('formated date ----->', toDate)

            dateVal2 = datetime.datetime.strptime (str (eff_from_date), '%Y%m%d')
            toDate2 = '"'+datetime.date.strftime (dateVal2, '%Y-%m-%d') +'"'

            print ('formated date ----->', toDate2)

            print (LoanID)
            l_ins_script = 'INSERT INTO loan_mdm_lookup( loan_mdm_lookup_id,CreditScoreMin,CreditScoreMax,' \
                           'LoanAmountMin,LoanAmountMax ,IntrestRatePct, DurationMonths,eff_from_date,eff_to_date) ' \
                           'VALUES ('+str(LoanID )+','+\
                           str(CreditScoreMin)+','+str(CreditScoreMax)+',' +str(LoanAmountMin) \
                           +','+str(LoanAmountMax) +','+str(IntrestRatePct) +','+str(DurationMonths) +','+str(toDate2) +\
                           ',' +str(toDate)+')'

            print(l_ins_script)
            cursor.execute(l_ins_script)
            conn.commit()

        # Use the "context" to render the HTML Template to display values
        # return HttpResponse(template.render(context, request))
        return render (request, 'mdm_single_loan_entry.html')
    else:
        form = TestForm ()
        return render (request, 'mdm_single_loan_entry.html', {'form': form})

def deletereport (request):
    print ("-----> inside delete report function")
    conn=GetConn()
    db3curr=db3.cursor()
    if request.method == 'POST' or request.method == 'GET' :

        testForm = DeleteForm (request.GET)
        if testForm.is_valid():
         print ("-----> inside delete report form")
         LoanID = testForm.cleaned_data.get('LoanID')

         db3curr.execute("delete from loan_mdm_lookup where loan_mdm_lookup_id=" + (str (LoanID)))
         print ("deleted loanid", LoanID)
         db3.commit()
         db3curr.close()

        return HttpResponse ('data deleted')
    else:
        template = loader.get_template ('mdm_single_loan_entry.html')

        render(request, template)

def loadEditreportById (request):

    id = request.GET['id']
    print ("-----> inside load edit report form", id)
    conn=GetConn()
    db3curr=db3.cursor()

    cursor.execute ("select * from loan_mdm_lookup where loan_mdm_lookup_id=" + (str (id)))
    # use fetchall() to get the list of row data
    l_data = ""

    for loan_mdm_lookup_id, CreditScoreMin, CreditScoreMax, LoanAmountMin, LoanAmountMax, IntrestRatePct, DurationMonths, eff_from_date, eff_to_date in cursor.fetchall():
        l_data={"LoanID": loan_mdm_lookup_id
                           , "CreditScoreMin": CreditScoreMin
                           , "CreditScoreMax": CreditScoreMax
                           , "LoanAmountMin": LoanAmountMin
                           , "LoanAmountMax": LoanAmountMax
                           , "IntrestRatePct": IntrestRatePct
                           , "DurationMonths": DurationMonths
                           , "eff_from_date": eff_from_date
                           , "eff_to_date": eff_to_date}

    print (l_data)
    editForm = UpdateForm (l_data)

    db3curr.close()
    return render ( request,'mdm_delete_report.html', {'form': editForm})


def report_update(request):
    print("before requset")

    if request.method == 'GET' or  request.method == 'POST' :
        TestForm1=UpdateForm(request.POST)
        print("request",request)
        print ("fileds------> ",TestForm1.is_valid())

        if TestForm1.is_valid ():
            print ('LoanID')

            LoanID = TestForm1.cleaned_data.get ('LoanID')
            CreditScoreMin = TestForm1.cleaned_data.get ('CreditScoreMin')
            CreditScoreMax = TestForm1.cleaned_data.get ('CreditScoreMax')
            LoanAmountMin = TestForm1.cleaned_data.get ('LoanAmountMin')
            LoanAmountMax = TestForm1.cleaned_data.get ('LoanAmountMax')
            IntrestRatePct = TestForm1.cleaned_data.get ('IntrestRatePct')
            DurationMonths = TestForm1.cleaned_data.get ('DurationMonths')
            eff_from_date = TestForm1.cleaned_data.get ('eff_from_date')
            eff_to_date = TestForm1.cleaned_data.get ('eff_to_date')
            print ("date values-----> fromdate ", eff_from_date, " to date " ,eff_to_date)
            dateVal = datetime.datetime.strptime (str (eff_to_date), '%Y-%m-%d')
            toDate =  datetime.date.strftime (dateVal, '%Y-%m-%d')

            dateVal2 = datetime.datetime.strptime (str (eff_from_date), '%Y-%m-%d')
            toDate2 =  datetime.date.strftime (dateVal2, '%Y-%m-%d')
            updateSqlstr = 'UPDATE loan_mdm_lookup SET CreditScoreMin=%s,CreditScoreMax=%s, LoanAmountMin=%s,LoanAmountMax=%s,IntrestRatePct=%s, DurationMonths=%s,eff_from_date=%s, eff_to_date=%s WHERE loan_mdm_lookup_id=%s '
            updateValues=   ( CreditScoreMin , CreditScoreMax , LoanAmountMin ,LoanAmountMax , IntrestRatePct , DurationMonths, toDate2 , toDate, LoanID )
            cursor.execute (updateSqlstr, updateValues)
            print ("updated", LoanID)
            conn.commit ()
            return HttpResponse("Updated")


cursor = conn.cursor()

def uploadPage(request):
    print('load upload page')
    template = loader.get_template ('uploadcsv.html')
    context = {'uploadPage': 'http://127.0.0.1:8002'}
    return HttpResponse(template.render(context, request))

def UploadCsv(request):
    print ("Start file upload view")
    template = loader.get_template ('uploadcsv.html')

    if request.method == 'POST' :
        print ("after if Start file upload view")
        print ("start validation file upload view")
        csvfile = request.FILES['file']
        print(csvfile)
        # let's check if it is a csv file
        #if not csvfile.name.endswith ('.csv'):
            #messages.error (request, 'THIS IS NOT A CSV FILE')
        data_set = csvfile.read().decode ('UTF-8')
        io_string = io.StringIO(data_set)
        next (io_string)

        reader = csv.reader (io_string, delimiter=",", quotechar="|")
        l_ins_script = "INSERT INTO loan_mdm_lookup( loan_mdm_lookup_id, CreditScoreMin,CreditScoreMax,LoanAmountMin,LoanAmountMax ,IntrestRatePct, " \
                       "DurationMonths,eff_from_date,eff_to_date) VALUES(%s,%s ,%s ,%s,%s,%s,%s,%s,%s)"
        valuse=[]
        for row in reader:
            print(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            insertVal =  ( row[0], row[1] ,row[2] , row[3] , row[4] ,row[5] ,row[6] , row[7] , row[8])
            valuse.append(insertVal)
           ## cursor.execute(l_ins_script,insertVal)
           ## conn.commit()
        cursor.executemany(l_ins_script, valuse)
        conn.commit()
        return HttpResponse('file uploaded,Thank you')

from rest_framework.response import Response

from .serializers import MdmSerializer

class RestView(views.APIView):

    def get(self, request):
        cursor.execute ("select * from loan_mdm_lookup;")
        # use fetchall() to get the list of row data
        l_data = []

        for loan_mdm_lookup_id, CreditScoreMin, CreditScoreMax, LoanAmountMin, LoanAmountMax, IntrestRatePct, DurationMonths, eff_from_date, eff_to_date in cursor.fetchall ():
            l_data.append ({"loan_mdm_lookup_id": loan_mdm_lookup_id
                               , "CreditScoreMin": CreditScoreMin
                               , "CreditScoreMax": CreditScoreMax
                               , "LoanAmountMin": LoanAmountMin
                               , "LoanAmountMax": LoanAmountMax
                               , "IntrestRatePct": IntrestRatePct
                               , "DurationMonths": DurationMonths
                               , "eff_from_date": eff_from_date
                               , "eff_to_date": eff_to_date})


        yourdata= l_data
        results = yourdata
        return HttpResponse(results)