# utils/parse_stm.py

import re

def parse_stm(content):
    data = {
        "order_number": None,
        "total_price": None,
        "order_date_time": None,
        "payment_method": None,
        "items": [],
        "total_amount": None,
        "vat_amount": None,
        "vat_summary": [],
        "change_due": None,
        "vat_number": None,
        "receipt_print_id": None
    }

    # Extract order number
    order_number = re.search(r"Order No: ([0-9]+)", content)
    if order_number:
        data["order_number"] = order_number.group(1)

    # Extract total price
    total_price = re.search(r"Total Price: ([0-9.]+ EUR)", content)
    if total_price:
        data["total_price"] = total_price.group(1)

    # Extract date and time
    date_time = re.search(r"Date/Time Ordered \(([0-9\-: ]+)\)", content)
    if date_time:
        data["order_date_time"] = date_time.group(1)

    # Extract payment method
    payment_method = re.search(r"Payment method \((.*?)\)", content)
    if payment_method:
        data["payment_method"] = payment_method.group(1)

    # Extract items
    items = re.findall(r"([0-9]+) - (.*?) // ([0-9.]+ EUR) // VAT: ([0-9.]+%) ([0-9.]+ EUR)", content)
    for item in items:
        item_data = {
            "quantity": item[0],
            "name": item[1],
            "price": item[2],
            "vat_rate": item[3],
            "vat_amount": item[4]
        }
        data["items"].append(item_data)

    # Extract total amount
    total_amount = re.search(r"Total amount: ([0-9.]+ EUR)", content)
    if total_amount:
        data["total_amount"] = total_amount.group(1)
    
    # Extract VAT amount
    vat_amount = re.search(r"VAT amount: ([0-9.]+ EUR)", content)
    if vat_amount:
        data["vat_amount"] = vat_amount.group(1)

    # Extract VAT summary
    vat_summary = re.findall(r"([0-9.]+%) - ([0-9.]+ EUR)", content)
    for vat in vat_summary:
        data["vat_summary"].append({
            "vat_rate": vat[0],
            "amount": vat[1]
        })

    # Extract change due
    change_due = re.search(r"Change due: ([0-9.]+ EUR)", content)
    if change_due:
        data["change_due"] = change_due.group(1)

    # Extract VAT number
    vat_number = re.search(r"Vat No: ([A-Z0-9]+)", content)
    if vat_number:
        data["vat_number"] = vat_number.group(1)
    
    # Extract receipt print ID
    receipt_print_id = re.search(r"Receipt print id: ([0-9]+)", content)
    if receipt_print_id:
        data["receipt_print_id"] = receipt_print_id.group(1)

    return data
