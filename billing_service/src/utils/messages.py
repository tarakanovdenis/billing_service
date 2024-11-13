from dataclasses import dataclass


@dataclass
class Messages:
    INVALID_TOKEN_ERROR = "Invalid token error."

    USER_PROFILE_WAS_NOT_FOUND = (
        "Profile of the authenticated user was not found."
    )
    USER_PROFILES_WERE_NOT_FOUND = (
        "User profiles were not found."
    )
    USER_PROFILE_WITH_THAT_EMAIL_WAS_NOT_FOUND = (
        "User profile with the specified email was not found."
    )
    PROFILE_WAS_NOT_FOUND = (
        "Profile with the specified ID was not found."
    )

    USER_PROFILE_BANK_ACCOUNTS_WERE_NOT_FOUND = (
        "User doesn\'t have bank accounts."
    )
    USER_PROFILE_BANK_ACCOUNT_WITH_CURRENCY_ENTERED_WAS_NOT_FOUND = (
        "User doesn\'t have bank accounts with the specified currency."
    )
    BANK_ACCOUNT_WITH_THAT_ID_WAS_NOT_FOUND = (
        "Bank account with the specified ID was not found."
    )
    USER_DOES_NOT_HAVE_APPROPRIATE_PERMISSIONS = (
        "User doesn\'t have the appropriate permissions."
    )
    BANK_ACCOUNTS_WERE_NOT_FOUND = (
        "Bank accounts were not found."
    )
    PROFILE_WITH_SPECIFIED_ID_DOES_NOT_HAVE_BANK_ACCOUNT_WITH_THAT_CURRENCY = (
        "Profile with specified ID doesn\'t have "
        "bank account with that currency"
    )
    PROFILE_WITH_SPECIFIED_ID_DOES_NOT_HAVE_BANK_ACCOUNT_WITH_THAT_ID = (
        "Profile with specified ID doesn\'t have "
        "bank account with that ID"
    )

    CURRENCY_WITH_THAT_ID_WAS_NOT_FOUND = (
        "Currency with the specified ID was not found"
    )
    CURRENCY_ENTRIES_WERE_NOT_FOUND = (
        "Currency entries were not found."
    )
    SPECIFIED_CURRENCY_WAS_NOT_FOUND = "The specified currency was not found."

    CURRENCY_PAIRS_WERE_NOT_FOUND = (
        "Currency pair enries were not found."
    )
    CURRENCY_PAIR_WITH_THAT_ID_NOT_FOUND = (
        "Currency pair entry with the specified ID was not found."
    )
    CURRENCY_PAIR_WITH_THAT_BASE_CURRENCY_ID_WAS_NOT_FOUND = (
        "Currency pair entry with the specified base currency ID was not found."
    )

    CURRENCY_PRICE_FOR_THAT_CURRENCY_WAS_NOT_FOUND = (
        "Currency price entry for the specified currency was not found."
    )

    INVALID_REQUEST_PAYLOAD_DURING_CONSTRUCT_STRIPE_EVENT = (
        "Invalid payload."
    )
    INVALID_SIGNATURE_DURING_CONSTRUCT_STRIPE_EVENT = (
        "Invalid signature."
    )

    TRANSACTION_HISTORY_ENTRY_WAS_CREATED = (
        "Transaction history entry was created successfully."
    )


messages = Messages()
