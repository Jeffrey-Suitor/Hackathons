var QRCode = require('qrcode') // Require the qrcode node module

dict = {} // Create an empty dictionary named dict

// Get all values from the document form
dict['item_name'] = document.getElementById("Item_name")
dict['item_number'] = document.getElementById("Item_Number")
dict['data_scanned'] = document.getElementById("Date_Scanned")
dict['description'] = document.getElementById("Description")
dict['flavour'] = document.getElementById("Flavour")
dict['quantity'] = document.getElementById("Quantity")
dict['exp_date'] = document.getElementById("Exp_Date")
dict['supplier'] = document.getElementById("Supplier")
dict['shipment_date'] = document.getElementById("Shipment_Date")
dict['concerns'] = document.getElementById("Concerns")

// Create a new string with all the data to be used by the qr code
new_string = ""
for (var key in dict) {
    if (dict.hasOwnProperty(key)) {
        new_string = new_string + " " + key + ": " + dict[key] + "\n"
    }
}

console.log(new_string) // Log the new string

// Create the new qr_code and display in terminal
QRCode.toString(new_string, {type:'terminal'}, function (err, url) {
  console.log(url)
});
