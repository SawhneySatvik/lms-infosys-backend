import secrets, string


def generate_random_password(length=12):
    """Generate a secure random password meeting complexity requirements."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = (
        secrets.choice(string.ascii_uppercase) +  # Ensure at least one uppercase
        secrets.choice(string.digits) +  # Ensure at least one digit
        ''.join(secrets.choice(characters) for _ in range(length - 2))
    )
    # Shuffle to ensure randomness
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)