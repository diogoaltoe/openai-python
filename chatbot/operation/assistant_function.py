def validate_promotional_code(args):
    code = args.get("code")

    match code:
        case "COUPON_ECO":
            return "05/01/2024"
        case "COUPON_ECO10":
            return "11/01/2024"
        case "COUPON_OUT":
            return "12/01/2024"
        case "COUPON_FAS":
            return "01/01/2025"
        case _:
            return "Invalid code"


available_tools = [
    {"type": "retrieval"},
    {
        "type": "function",
        "function": {
            "name": "validate_promotional_code",
            "description": "Validate a promotional code based on the company's Discounts and Promotions policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The promotional code, in the format, COUPON_XX. For example: COUPON_ECO"
                    }
                },
                "required": ["code"]
            }
        }
    }
]

available_functions = {
    "validate_promotional_code": validate_promotional_code,
}
