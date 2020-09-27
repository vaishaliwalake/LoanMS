

from django.shortcuts import render


from django.http import HttpResponse
from django.template import loader
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='loan')
cursor = conn.cursor()

def BankMngr(request):

    return render( request, 'bankmgr.html')

# Reading multiple datatypes and print to screen
def LoanValidation(request):
    cursor.execute ("select c.cust_id,c.first_name,c.last_name,c.email,c.CreditScore, "
                    "c.RequestedLoanAmount, c.DurationInMonths, cl.application_status as Status from selfserv_customers c left join cust_loans cl on cl.cust_id=c.cust_id")
# use fetchall() to get the list of row data
    l_data = []

    for cust_id,first_name,last_name,email,CreditScore, RequestedLoanAmount, DurationInMonths,Status  in cursor.fetchall ():
     l_data.append ({"id":cust_id,
                    "first_name":first_name,
                    "last_name":last_name,
                    "email":email
                       , "CreditScore": CreditScore
                       , "RequestedLoanAmount": RequestedLoanAmount
                       , "DurationInMonths": DurationInMonths
                     , "Status" : Status})


     #print (l_data)

# Create Template Object
    template = loader.get_template ('reviewloan.html')
    context = { 'l_data': l_data}
    return HttpResponse (template.render (context, request))

def ApproveLoanRequest(request):
    id = request.GET['id']
    print ("-----> inside  id",id)
    sqlGetCustDetails = "select CreditScore,RequestedLoanAmount,DurationInMonths from " \
                        "selfserv_customers where cust_id=%s"
    cursor.execute(sqlGetCustDetails, id)
    custValues = cursor.fetchone()
    print(custValues)
   # cursor.close()

    sqlLoanMDM = "select loan_mdm_lookup_id,CreditScoreMin,CreditScoreMax,LoanAmountMin,LoanAmountMax,IntrestRatePct,DurationMonths from  loan_mdm_lookup where  %s between CreditScoreMin and CreditScoreMax and  %s between LoanAmountMin and LoanAmountMax limit 10"
    values = [custValues[0], custValues[1]]
    print(values)
    cursor.execute(sqlLoanMDM,values)

    insert_custt = "insert into cust_loans (cust_loan_id, loan_mdm_lookup_id, cust_id, req_date, req_loan_amount,req_DurationMonths, apprvd_loan_amt, apprvd_DurationMonths, application_status, application_notes) values ("

    if (cursor.rowcount > 0):
        for loan_mdm_lookup_id, CreditScoreMin, CreditScoreMax, LoanAmountMin, LoanAmountMax, IntrestRatePct, DurationMonths in cursor.fetchall ():

            application_status = '"Approved"'
            application_notes = '"your application is approved"'
            apprvd_loan_amt = round ((custValues[1] + (custValues[1] * IntrestRatePct / 100)), 2)

            vl = str (id) + ',' + str (loan_mdm_lookup_id) + ',' + str ( id) + ',' + "20200425" + ',' +\
                 str (custValues[1]) + ',' + str (custValues[2]) + ',' + str ( apprvd_loan_amt) + ',' + str (0) + \
                 ',' + str (application_status) + ',' + str (application_notes)
            #print (insert_custt + vl + ');')
            cursor.execute (insert_custt + vl + ');')
            conn.commit ()
            cursor.execute (
                "select c.cust_id,c.first_name, last_name, email, CreditScore, RequestedLoanAmount, DurationInMonths, cl.application_status as Status from selfserv_customers c left join cust_loans cl on cl.cust_id=c.cust_id")
            # use fetchall() to get the list of row data
            l_data = []

            for cust_id ,first_name, last_name, email, CreditScore, RequestedLoanAmount, DurationInMonths, Status  in cursor.fetchall ():
                l_data.append ({"id": cust_id,
                                "first_name": first_name,
                                "last_name": last_name,
                                "email": email
                                   , "CreditScore": CreditScore

                                   , "RequestedLoanAmount": RequestedLoanAmount
                                   , "DurationInMonths": DurationInMonths
                                   , "Status": Status})
            #custValues = cursor.fetchone ()
            template = loader.get_template ('reviewloan.html')
            context = {'home_url': 'bankmgr', 'l_data': l_data}
            return HttpResponse (template.render (context, request))
    else:
        insert_custt = "insert into cust_loans (cust_loan_id, loan_mdm_lookup_id, cust_id, req_date, req_loan_amount,req_DurationMonths, apprvd_loan_amt, apprvd_DurationMonths, application_status, application_notes) values ("
        application_status = '"Not Approved"'
        application_notes = '"your application is not approved"'
        apprvd_loan_amt = "0"

        vl = str (id) + ',' + str ("0") + ',' + str (id) + ',' + "20200425" + ',' + str (custValues[1]) + ',' + str (custValues[2]) + ',' + str (apprvd_loan_amt) + ',' + str (0) + \
             ',' + str (application_status) + ',' + str (application_notes)
        # print (insert_custt + vl + ');')
        cursor.execute (insert_custt + vl + ');')
        conn.commit ()
        cursor.execute (
            "select c.cust_id, c.first_name, c.last_name, c.email, c.CreditScore, c.RequestedLoanAmount, c.DurationInMonths, cl.application_status as Status from selfserv_customers c left join cust_loans cl on cl.cust_id=c.cust_id")
        # use fetchall() to get the list of row data
        l_data = []

        for cust_id, first_name, last_name, email, CreditScore, RequestedLoanAmount, DurationInMonths, Status in cursor.fetchall ():
            l_data.append ({"id": cust_id,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email
                               , "CreditScore": CreditScore

                               , "RequestedLoanAmount": RequestedLoanAmount
                               , "DurationInMonths": DurationInMonths
                               , "Status": Status})
        # custValues = cursor.fetchone ()
        template = loader.get_template ('reviewloan.html')
        context = {'home_url': 'bankmgr', 'l_data': l_data}
        return HttpResponse (template.render (context, request))
        print("no criteria matched for applied loan request ")

    return LoanValidation(request)

def loanMDMChartView(request):
    sqlLoanMDM = "select CreditScoreMin as minscore,CreditScoreMax as maxscore,LoanAmountMin as minamount,LoanAmountMax as maxamount from  loan_mdm_lookup"
    cursor.execute (sqlLoanMDM)



    # Step 3: Send the chart object to the template.
    template = loader.get_template ('mdmChart.html')
    context = {'loanmdm': None}
    return HttpResponse (template.render (context, request))


