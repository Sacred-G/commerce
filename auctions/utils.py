from .models import Message

def send_auction_message(sender, recipient, listing, message_type, additional_info=None):
    """
    Send a message related to an auction.
    :param sender: User object of the sender (None for system messages)
    :param recipient: User object of the recipient
    :param listing: AuctionListing object (can be None for deletion messages)
    :param message_type: String indicating the type of message
    :param additional_info: Dictionary containing any additional information needed for the message
    """
    subject = ""
    body = ""

    if message_type == "auction_deleted":
        title = additional_info.get('title', 'your auction') if additional_info else 'your auction'
        subject = "Auction Deletion Confirmation"
        body = f"Your auction '{title}' has been successfully deleted from the system."

    elif message_type == "new_bid_seller":
        bid_amount = additional_info.get('bid_amount', 'an undisclosed amount')
        bidder = additional_info.get('bidder', 'A user')
        subject = f"New Bid Received for {listing.title}"
        body = f"Your auction '{listing.title}' has received a new bid of ${bid_amount} from {bidder}."

    elif message_type == "new_bid_buyer":
        bid_amount = additional_info.get('bid_amount', 'an undisclosed amount')
        subject = f"Bid Confirmation for {listing.title}"
        body = f"Your bid of ${bid_amount} for the auction '{listing.title}' has been successfully placed."

    elif message_type == "auction_end_seller":
        subject = f"Your auction for {listing.title} has ended"
        body = f"Your auction for {listing.title} has ended. The winning bid was ${listing.current_price}. Please prepare to ship the item to the winner."

    elif message_type == "auction_end_buyer":
        subject = f"An auction you bid on has ended: {listing.title}"
        body = f"The auction for {listing.title} has ended. The winning bid was ${listing.current_price}."

    elif message_type == "auction_won":
        subject = f"Congratulations! You won the auction for {listing.title}"
        body = f"You won the auction for {listing.title} with a bid of ${listing.current_price}. Please prepare to complete the payment and receive the item."

    else:
        raise ValueError("Invalid message type")

    Message.objects.create(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body
    )