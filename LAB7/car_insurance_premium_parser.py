def normalize_registration(plate):
    """
    Removes spaces, dashes and dots from a registration number and upper-cases it.
    Returns "" if the input is not a string.
    """
    if not isinstance(plate, str):
        return ""
    plate = plate.strip().upper()
    for ch in [' ', '-', '.']:
        plate = plate.replace(ch, '')
    return plate

def total_claim_amount(text):
    """
    Adds up claim amounts separated by semicolons.
    Returns None if the input is not a string, or if any amount is not
    a valid non-negative whole number.
    """
    if not isinstance(text, str):
        return None
    total = 0
    for piece in text.split(';'):
        try:
            amount = int(piece)
        except ValueError:
            return None
        if amount < 0:
            return None
        total += amount
    return total

def driver_age(dob, current_year=2026):
    """
    Works out the driver's age from a DD/MM/YYYY date of birth.
    Returns None if the input is not a string, is not in DD/MM/YYYY form,
    or has a birth year outside 1900 to current_year.
    """
    if not isinstance(dob, str):
        return None
    parts = dob.split('/')
    if len(parts) != 3:
        return None
    try:
        birth_year = int(parts[2])
    except ValueError:
        return None
    if not (1900 <= birth_year <= current_year):
        return None
    return current_year - birth_year

def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    print("Normalized registration:", normalize_registration(value))

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    print("Total claimed:", total_claim_amount(value))

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    print("Driver age in 2026:", driver_age(value))

if __name__ == "__main__":
    main()