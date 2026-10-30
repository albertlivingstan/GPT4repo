
def get_customer_details():
    """Collect customer details from the user."""

    print("\n===== Intelligent Email Assistant =====")

    customer_name = input("Enter Customer Name: ").strip()
    subject = input("Enter Email Subject: ").strip()
    customer_email = input("Enter Customer Email: ").strip()

    # Validate the input fields
    if not customer_name:
        print("Error: Customer name cannot be empty.")
        return None

    if not subject:
        print("Error: Email subject cannot be empty.")
        return None

    if not customer_email:
        print("Error: Customer email cannot be empty.")
        return None

    # Store the details in a dictionary
    customer_details = {
        "customer_name": customer_name,
        "subject": subject,
        "customer_email": customer_email
    }

    return customer_details


def display_customer_details(details):
    """Display the entered customer details."""

    if details is None:
        return

    print("\n===== Customer Email Details =====")
    print("Customer Name :", details["customer_name"])
    print("Subject       :", details["subject"])
    print("Customer Email:", details["customer_email"])


# Test this module independently
if __name__ == "__main__":
    details = get_customer_details()
    display_customer_details(details)
