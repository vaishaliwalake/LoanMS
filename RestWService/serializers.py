from rest_framework import serializers
from selfserv import models
class CustomersSerializer(serializers.ModelSerializer):

    class Meta:
        model =models.Customers
        fields = ('first_name' ,'last_name','email', 'CreditScore', 'DurationInMonths',  'cust_id')
