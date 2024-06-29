import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..models import Subscription
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(login_required, name='dispatch')
class SubscriptionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'subscription/subscription.html', {
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })

@method_decorator(login_required, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            # Create a Stripe Customer
            customer = stripe.Customer.create(
                email=user.email
            )

            # Create a Subscription
            checkout_session = stripe.checkout.Session.create(
                customer=customer.id,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Pro Monthly Subscription',
                            },
                            'unit_amount': 2000,
                            'recurring': {
                                'interval': 'month',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url='http://127.0.0.1:8000/subscription/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/subscription/cancel/',
            )

            return JsonResponse({'id': checkout_session.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class SubscriptionSuccessView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)
        customer = stripe.Customer.retrieve(session.customer)

        # Get the subscription
        subscription = stripe.Subscription.retrieve(session.subscription)

        # Save the subscription info to the database
        Subscription.objects.create(
            user=request.user,
            stripe_subscription_id=subscription.id,
            stripe_customer_id=customer.id,
            active=True
        )

        return render(request, 'subscription/subscription_success.html')

class SubscriptionCancelView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'subscription/subscription_cancel.html')



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'invoice.payment_succeeded':
        session = event['data']['object']
        # Handle the successful subscription payment here

    if event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        stripe_subscription_id = subscription['id']
        try:
            user_subscription = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
            user_subscription.active = False
            user_subscription.save()
        except Subscription.DoesNotExist:
            pass

    return HttpResponse(status=200)
