class CustomerLog:
    def __init__(self, person, portfolio_validity):
        self.last_timestamp = 0
        self.last_event = None
        self.current_timestamp = 0
        self.current_offers = {}
        self.money_spent = 0
        self.portfolio_validity = portfolio_validity
        self.person = person

    def receive_offer(self, offer_id):
        self.current_offers[offer_id] = {'time_left': self.portfolio_validity[offer_id]}

    def view_offer(self, offer_id):
        try:
            self.current_offers[offer_id]['viewed'] = True
        except KeyError:
            # If offer wasn't received before, consider the offer was received
            # and viewed at the same time.
            self.receive_offer(offer_id)

    def expire_offer(self, offer_id):
        del self.current_offers[offer_id]

    def decay_offer_validity(self, current_timestamp):
        # Create a list of offer to be expired
        expired_offers = []

        # Reduce the time left to the offer by how much time has passed
        for offer_id in self.current_offers:
            time_passed = current_timestamp - self.last_timestamp
            offer_time_left = self.current_offers[offer_id]['time_left'] - time_passed
            if offer_time_left < 0:
                expired_offers.append(offer_id)
            else:
                self.current_offers[offer_id]['time_left'] = offer_time_left

        # Remove expired offers
        for offer_id in expired_offers:
            self.expire_offer(offer_id)

        # Update last timestamp
        self.last_timestamp = current_timestamp

    def record_transaction(self, offer_id='no_offer'):
        if offer_id == 'no_offer':
            # Record the transaction value with any current informational offers
            viewed_offer = [
                offer_id
                for offer_id in self.current_offers
                if self.current_offers[offer_id].get('viewed')
            ]

            if viewed_offer:
                # It's fine to take the first element only because there can only be 1
                # informational offer at the same time
                offer_id = viewed_offer[0]

        return (self.person, self.money_spent, offer_id)
