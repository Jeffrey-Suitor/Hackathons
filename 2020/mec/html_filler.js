// Require the various libraries
const QRReader = require('qrcode-reader');
const fs = require('fs');
const jimp = require('jimp');

results = run().catch(error => console.error(error.stack)); // Run the function defined below


// Create an async function meant to be called by browser
async function run() {

  // Read the image
  const img = await jimp.read(fs.readFileSync('./sanpellegrino.png'));

  // Create a new QRReader object
  const qr = new QRReader();

  // qrcode-reader's API doesn't support promises, so wrap it
  const value = await new Promise((resolve, reject) => {
    qr.callback = (err, v) => err != null ? reject(err) : resolve(v);
    qr.decode(img.bitmap);
  });


  // Result of QR code
  console.log(value.result);

  var i;
  var dict = {}
  results = value.result.toString() // Convert to string to assure type
  results_list = results.split("\n") // Split along new lines

  console.log(results_list) // Log the new list of rows

  for (i = 0; i < results_list.length; i++) {
    current_entry = results_list[i]
    key_and_values = current_entry.split(":") // Format of data is category: info
    dict[key_and_values[0]] = key_and_values[1] // Create the appropriate dicitonary key and values
  }

  // Create string of current date
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();
  today = mm + '/' + dd + '/' + yyyy;

  // Add todays date to the dict and log the dict
  dict['date_scanned'] = today
  console.log(dict)

  // Fill out the document with the appropriate info gathered from the item qr_code
  document.getElementById('Exp_Date').value = dict['expiration_date']
  document.getElementById('Description').value = dict['description']
  document.getElementById('Shipment_Date').value = dict['date_of_shipment']
  document.getElementById('Supplier').value = dict['supplier']
  document.getElementById('Quantity').value = dict['quantity']
  document.getElementById('Item_Name').value = dict['item_name']
  document.getElementById('Flavour').value = dict['flavour']
  document.getElementById('Date_Scanned').value = dict['date_scanned']
}


