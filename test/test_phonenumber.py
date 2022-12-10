import phonenumbers as PN


def isValidPhoneNumber(phone_number: str) -> bool:
    return PN.is_possible_number(phone_number)


def getPhonenumber(numberlist: list) -> str:

    filtered_number = []

    for number in numberlist:
        number = PN.parse(number, region="IN")
        if isValidPhoneNumber(number):
            international_format = PN.format_number(number, PN.PhoneNumberFormat.E164)
            filtered_number.append(international_format)

    # return filtered_number

    return filtered_number[0] if filtered_number else None


numberlist = [
    "+91-1122334455",
    "+44 1122334455",
    "+911122334455",
    "911122334455",
]

print(getPhonenumber(numberlist))
