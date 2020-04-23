import pandas as pd
from src.utils.customer_log import CustomerLog


def parse_transaction_details(transaction):
    offer_id = transaction['offer']
    current_timestamp = transaction['time']
    event_type = transaction['event']
    amount = transaction['amount']

    return offer_id, current_timestamp, event_type, amount


def get_customer_transcript(transcript, customer_id):
    return transcript[transcript['person'] == customer_id].to_dict(orient='records')


def parse_transcript(transcript, portfolio_validity):
    # Create a list to store transaction details
    transaction_list = []

    # List out informational offers
    informational_offers = ['3f207df678b143eea3cee63160fa8bed', '5a8bc65990b245e5a138643cd4eb9837']

    for customer_id in transcript['person'].unique():
        # Get events related to a customer
        customer_transcript = get_customer_transcript(transcript, customer_id)

        # Initialise customer tracker
        customer_log = CustomerLog(customer_id, portfolio_validity)

        for transaction in customer_transcript:
            # Parse details
            offer_id, current_timestamp, event_type, amount = parse_transaction_details(transaction)

            # Decay validity of all current offers
            if customer_log.last_timestamp != current_timestamp:
                customer_log.decay_offer_validity(current_timestamp)

            # Only track informational offers
            if offer_id in informational_offers:
                if event_type == 'offer received':
                    customer_log.receive_offer(offer_id)

                elif event_type == 'offer viewed':
                    customer_log.view_offer(offer_id)

            elif event_type == 'transaction':
                customer_log.money_spent = amount
                transaction_list.append(customer_log.record_transaction())

            elif event_type == 'offer completed':
                if customer_log.last_event == 'transaction':
                    # Remove the last transaction as it doesn't contain the offer it should have
                    transaction_list.pop()

                # Store transaction details
                transaction_list.append(customer_log.record_transaction(offer_id))

            # Store last event type for future reference
            customer_log.last_event = event_type

    return transaction_list


def get_transaction_dataframe(transaction_list):
    transaction_df = pd.DataFrame(transaction_list, columns=['person', 'amount', 'offer'])

    return transaction_df
