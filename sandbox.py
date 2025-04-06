def simulate_brute_force(password):
    # Calculate strength and crack time
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_number = any(c.isdigit() for c in password)
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    has_symbol = any(c in symbols for c in password)

    # Strength factor
    strength = length
    if has_upper:
        strength += 5
    if has_number:
        strength += 5
    if has_symbol:
        strength += 10

    # Crack time in seconds
    if strength < 10:
        crack_time = 0.5  # Weak
    elif strength < 20:
        crack_time = 2.0  # Moderate
    else:
        crack_time = 5.0  # Strong

    return crack_time  # Return time for GUI to handle
