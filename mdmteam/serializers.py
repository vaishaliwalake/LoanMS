from rest_framework import serializers

class MdmSerializer(serializers.Serializer):
    loan_mdm_lookup_id = serializers.IntegerField()
    CreditScoreMin = serializers.IntegerField()
    CreditScoreMax=serializers.IntegerField()
    LoanAmountMin=serializers.IntegerField()
