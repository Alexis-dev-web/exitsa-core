import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.middlewares import permission_required

from order.dto import GetOrdersReportDTO
from order.use_case import OrderReportsUseCase
from order.serializers import OrderReportSerializer


class ReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.order_report_use_case = OrderReportsUseCase()

    def get(self, request, *args, **kwargs):
        self.logger.info(f"ReportView#get START - Get report orders - orderAgent={request.META.get('HTTP_order_AGENT', None)}")

        try:
            serializer = OrderReportSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)
            
            report = self.order_report_use_case.execute(GetOrdersReportDTO.from_json(serializer.data))

            self.logger.info(f"ReportView#post SUCCESS - Get report orders")

            return Response(report, status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'ReportView#get FAILURE - error to get report orders - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ReportView#get FAILURE - error to get report orders - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)
