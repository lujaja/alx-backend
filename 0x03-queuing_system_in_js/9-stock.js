const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

// Data setup
const listProducts = [
    { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
    { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
    { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
    { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

// Data access function
function getItemById(id) {
    return listProducts.find(product => product.itemId === parseInt(id));
}

// Redis client setup
const client = redis.createClient();
const asyncGet = promisify(client.get).bind(client);
const asyncSet = promisify(client.set).bind(client);

// Reserve stock functions
async function reserveStockById(itemId, stock) {
    await asyncSet(`item.${itemId}`, stock.toString());
}

async function getCurrentReservedStockById(itemId) {
    const reservedStock = await asyncGet(`item.${itemId}`);
    return parseInt(reservedStock) || 0;
}

// Express setup
const app = express();
const PORT = 1245;

// Middleware to parse JSON
app.use(express.json());

// Route to list all products
app.get('/list_products', (req, res) => {
    res.json(listProducts.map(product => ({
        itemId: product.itemId,
        itemName: product.itemName,
        price: product.price,
        initialAvailableQuantity: product.initialAvailableQuantity
    })));
});

// Route to get product details by itemId
app.get('/list_products/:itemId', async (req, res) => {
    const { itemId } = req.params;
    const product = getItemById(itemId);
    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const currentReserved = await getCurrentReservedStockById(itemId);
    const currentQuantity = product.initialAvailableQuantity - currentReserved;

    res.json({
        itemId: product.itemId,
        itemName: product.itemName,
        price: product.price,
        initialAvailableQuantity: product.initialAvailableQuantity,
        currentQuantity: currentQuantity
    });
});

// Route to reserve a product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
    const { itemId } = req.params;
    const product = getItemById(itemId);
    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const currentReserved = await getCurrentReservedStockById(itemId);
    if (currentReserved >= product.initialAvailableQuantity) {
        return res.json({ status: 'Not enough stock available', itemId: product.itemId });
    }

    await reserveStockById(itemId, currentReserved + 1);
    res.json({ status: 'Reservation confirmed', itemId: product.itemId });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
