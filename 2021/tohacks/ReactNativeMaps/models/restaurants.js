
const mongoose = require("mongoose");

let restaurantSchema = new mongoose.Schema({
    name: String,
    tags: String,
    phone: String,
    lat: Float32Array,
    long: Float32Array,
    curbside: Boolean,
    mobile_order: Boolean,
    delivery: Boolean,
});

restaurantSchema.set("toJSON", { virtuals: true });

const Restaurant = mongoose.model("Restaurant", restaurantSchema, "Restaurants");

module.exports = { Restaurant };