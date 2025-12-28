from fastapi import HTTPException


def calculate_balance_denominations(balance_amount: float, denominations: list):
    """Calculate denomination breakup for returning exact balance amount."""

    if balance_amount == 0:
        return []

    denominations = sorted(
        denominations,
        key=lambda d: d["value"],
        reverse=True
    )

    result = []
    remaining_amount = balance_amount

    for denom in denominations:
        denom_value = denom["value"]
        denom_count = denom["count"]

        if remaining_amount <= 0:
            break

        max_needed = int(remaining_amount // denom_value)
        used = min(max_needed, denom_count)

        if used > 0:
            result.append({
                "value": denom_value,
                "count": used
            })
            remaining_amount -= used * denom_value

    if remaining_amount != 0:
        raise HTTPException(
            status_code=400,
            detail="Unable to return exact balance with available denominations"
        )

    return result
