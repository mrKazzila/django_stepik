import stripe
from django.http import HttpResponse
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(line_items, order_id, success_page, cancel_page):
    return stripe.checkout.Session.create(
        line_items=line_items,
        metadata={'order_id': order_id},
        mode='payment',
        success_url=success_page,
        cancel_url=cancel_page,
    )


def handle_stripe_webhook(payload, sig_header, order_model):
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            stripe.api_key,
        )
    except ValueError as e:
        print(f'Invalid payload, error: {e}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f'Invalid signature, error: {e}')
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response,
        # you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # Fulfill the purchase...
        _fulfill_order(
            session=session,
            order_model=order_model,
        )


def _fulfill_order(session, order_model):
    order_id = int(session.metadata.order_id)
    order = order_model.objects.get(id=order_id)
    order.update_after_payment()
