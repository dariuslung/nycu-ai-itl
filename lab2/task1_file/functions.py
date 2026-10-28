def find_duplicate_orders(orders):
    """Return order IDs that appear more than once in the list."""
    seen = {}
    duplicates = []

    for order in orders:
        order_id = order["id"]
        if order_id in seen:
            seen[order_id] += 1
        else:
            seen[order_id] = 1

    for order_id, count in seen.items():
        if count > 1:
            duplicates.append(order_id)

    return duplicates


def summarize_duplicates(orders):
    dupes = find_duplicate_orders(orders)
    if not dupes:
        return "No duplicate orders found."
    return f"Found {len(dupes)} duplicate order ID(s): {dupes}"