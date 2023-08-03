import csv

def generate_form_html(entries):
    form_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shipment Price Prediction</title>
    </head>
    <body>
        <h1>Shipment Price Prediction</h1>
        <form action="/predict_shipment_price" method="post">
    """

    for entry in entries:
        form_html += f"""
            <label for="line_item_quantity">Line Item Quantity:</label>
            <input type="text" id="line_item_quantity" name="line_item_quantity" value="{entry['Line_Item_Quantity']}" required><br>

            <label for="pack_price">Pack Price:</label>
            <input type="text" id="pack_price" name="pack_price" value="{entry['Pack_Price']}" required><br>

            <label for="unit_price">Unit Price:</label>
            <input type="text" id="unit_price" name="unit_price" value="{entry['Unit_Price']}" required><br>

            <label for="weight_kilograms">Weight (Kilograms):</label>
            <input type="text" id="weight_kilograms" name="weight_kilograms" value="{entry['Weight_Kilograms']}" required><br>

            <label for="brand">Brand:</label>
            <input type="text" id="brand" name="brand" value="{entry['Brand']}" required><br>

            <label for="dosage_form">Dosage Form:</label>
            <input type="text" id="dosage_form" name="dosage_form" value="{entry['Dosage_Form']}" required><br>

            <label for="country">Country:</label>
            <input type="text" id="country" name="country" value="{entry['Country']}" required><br>

            <label for="dosage">Dosage:</label>
            <input type="text" id="dosage" name="dosage" value="{entry['Dosage']}" required><br>

            <label for="item_description">Item Description:</label>
            <input type="text" id="item_description" name="item_description" value="{entry['Item_Description']}" required><br>

            <label for="po_so">PO/SO:</label>
            <input type="text" id="po_so" name="po_so" value="{entry['PO_SO']}" required><br>

            <hr>
        """

    form_html += """
            <input type="submit" value="Predict Shipment Price">
        </form>
    </body>
    </html>
    """

    return form_html

def read_csv(filename):
    entries = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entries.append(row)
    return entries

if __name__ == "__main__":
    entries = read_csv("artifacts/train.csv")
    form_html = generate_form_html(entries)
    with open("form.html", "w") as form_file:
        form_file.write(form_html)
