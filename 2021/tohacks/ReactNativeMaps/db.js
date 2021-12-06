const MONGODB_URI = "mongodb+srv://tohacks:tohacks@cluster0-4nfpn.gcp.mongodb.net/test?retryWrites=true&w=majority";

const mongoose = require("mongoose");
mongoose.set('useFindAndModify', false);
const URI = process.env.MONGODB_URI || MONGODB_URI;

mongoose.connect(URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false
});

// Make sure MongoDB is running
mongoose.Promise = global.Promise;

const { Restaurant } = require("./models/restaurants");

module.exports = { Restaurant };