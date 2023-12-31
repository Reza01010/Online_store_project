from django.shortcuts import render

from django.conf import settings
import requests
import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse

from cart.tasks import send_order_confirmation_email
from orders.models import Order














def payment_process_sandbox(request):
    # get order id from session
    order_id = request.session.get('order_id')
    # ger the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    request_data = {
        'MerchantID': 'dddddddddddddddddddddddddddddddddddd',
        'Amount': rial_total_price,
        'Description': f"#{order.id} : {order.user.first_name}  {order.user.first_name}",
        # 'CallbackURL': '127.0.0.1:8000' + reverse("payment:payment_callback_sandbox"),
        'CallbackURL': request.build_absolute_uri(reverse("payment:payment_callback_sandbox")),
        # 'CallbackURL': f'127.0.0.1:8000{reverse("payment:payment_callback_sandbox")}',
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    # print('>>>  ',res.json()['data'])###برای مثال ممکنه در حالت واقعی متفاوت باشه#
# >>>   {'code':100, 'message':'Success', 'zarinpal_authority':'A00000000000000000000000000350631138', 'fee_type':'Merchant', 'fee':'15000'}

    data = res.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get("Authority")
    payment_status = request.GET.get("Status")

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':

        request_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        request_data = {
            'MerchantID': 'dddddddddddddddddddddddddddddddddddd',
            'Amount': rial_total_price,
            'Authority':payment_authority,

        }
        res = requests.post(url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json', data=json.dumps(request_data),
                            headers=request_header, )

        if 'errors' not in res.json():
            data = res.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()
                
                send_order_confirmation_email.delay(email=request.user.email,text='پرداخت با موفقیت انجام شد.')
                return HttpResponse('پرداخت با موفقیت انجام شد.')
                
            elif payment_code ==101:
                return HttpResponse('پرداخت با موفقیت انجام شد. البته این تراکنش قبلا ثبت شده!')

            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                send_order_confirmation_email.delay(email=request.user.email,text=f'تراکنش ناموفق بود.  {error_code}     {error_message}')
                return HttpResponse(f'تراکنش ناموفق بود.  {error_code}     {error_message}')
    else:
        send_order_confirmation_email.delay(email=request.user.email,text='تراکنش ناموفق بود.')
        return HttpResponse('تراکنش ناموفق بود.')



