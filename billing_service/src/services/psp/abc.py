from abc import ABC, abstractmethod


class PaymentServiceProvider(ABC):
    @abstractmethod
    def get_top_up_bank_account_by_another_currency_checkout_session(self):
        pass

    @abstractmethod
    def get_subscription_payment_checkout_session(self):
        pass
