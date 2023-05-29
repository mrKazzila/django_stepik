import logging

import stripe
from django.conf import settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def create_checkout_session(line_items, order_id, success_page, cancel_page):
    return stripe.checkout.Session.create(
        line_items=line_items,
        metadata={'order_id': order_id},
        mode='payment',
        success_url=success_page,
        cancel_url=cancel_page,
    )


def handle_stripe_webhook(payload, sig_header, order_model):
    logger.debug(f'Stripe webhook {payload}, {sig_header}, {order_model}')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        logger.error(f'Invalid payload: {e}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f'Invalid signature: {e}')
        return HttpResponse(status=400)

    logger.debug(f'Stripe event {type(event)}, {dir(event)}, {event}')

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response,
        # you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )
        logger.debug(f'Stripe session {type(session)}, {dir(session)}, {session}')

        # Fulfill the purchase...
        _fulfill_order(
            session=session,
            order_model=order_model,
        )


def _fulfill_order(session, order_model):
    order_id = int(session.metadata.order_id)
    order = order_model.objects.get(id=order_id)
    order.update_after_payment()
