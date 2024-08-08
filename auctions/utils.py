from .models import Message

def send_auction_end_message(user, listing, role):
    if role == "seller":
        subject = f"Your auction for {listing.title} has ended"
        body = f"Your auction for {listing.title} has ended. The winning bid was ${listing.current_price}. Please prepare to ship the item to the winner."
    else:  # buyer
        subject = f"You won the auction for {listing.title}"
        body = f"Congratulations! You won the auction for {listing.title} with a bid of ${listing.current_price}. Please prepare to complete the payment and receive the item."
    
    Message.objects.create(
        sender=None,  # System message
        recipient=user,
        subject=subject,
        body=body
    )
