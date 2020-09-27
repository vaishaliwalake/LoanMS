if request.method == 'GET' or 'POST':
    print ("request")
    TestForm1 = TestForm (request.POST)
    if TestForm1.is_valid ():
        LoanID = TestForm1.cleaned_data.get ('LoanID')
        CreditScoreMin = TestForm1.cleaned_data.get ('CreditScoreMin')
        CreditScoreMax = TestForm1.cleaned_data.get ('CreditScoreMax')
        LoanAmountMin = TestForm1.cleaned_data.get ('LoanAmountMin')
        LoanAmountMax = TestForm1.cleaned_data.get ('LoanAmountMax')
        IntrestRatePct = TestForm1.cleaned_data.get ('IntrestRatePct')
        DurationMonths = TestForm1.cleaned_data.get ('DurationMonths')
        eff_from_date = TestForm1.cleaned_data.get ('eff_from_date')
        eff_to_date = TestForm1.cleaned_data.get ('eff_to_date')

        dateVal = datetime.datetime.strptime (str (eff_to_date), '%Y%m%d')
        toDate = '"' + datetime.date.strftime (dateVal, '%Y-%m-%d') + '"'

        dateVal2 = datetime.datetime.strptime (str (eff_from_date), '%Y%m%d')
        toDate2 = '"' + datetime.date.strftime (dateVal2, '%Y-%m-%d') + '"'
        update_st = ('UPDATE loan_mdm_lookup SET CreditScoreMin=%s,CreditScoreMax=%s, LoanAmountMin=%s,'
                     'LoanAmountMax=%s,IntrestRatePct=%s, '
                     'DurationMonths=%s,eff_from_date=%s, eff_to_date=%s WHERE LoanID==loan_mdm_lookup_id ('
                     + str (LoanID) + ',' + str (CreditScoreMin) + ',' + str (CreditScoreMax) + ',' + str (
                    LoanAmountMin) + ',' + str (LoanAmountMax) + ',' + str (IntrestRatePct) + ',' + str (
                    DurationMonths) + ',' + str (toDate2) + \
                     ',' + str (toDate) + ')')
        cursor.execute (update_st)
        print ("updated", LoanID)
        conn.commit ()
             return HttpResponse ("updated", LoanID)

    # return HttpResponse('data updated')
else:
    template = 'mdm_single_loan_entry.html'
    context = {'home_url': 'http://127.0.0.1:8002', }
    return HttpResponse ("error")
