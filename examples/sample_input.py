def calculate_discount(items: list) -> float:
    """Calculate total discount for a shopping cart
    
    Args:
        items: List of (price, quantity) tuples
    Returns:
        float: Total discount amount
    """
    if not items:
        return 0.0
        
    total = sum(price * qty for price, qty in items)
    
    if total > 100:
        return total * 0.1
    return 0.0