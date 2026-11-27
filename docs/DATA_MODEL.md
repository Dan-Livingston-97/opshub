# OpsHub data model

OpsHub models a fictional wholesale distributor that sells products to business customers. An entity is a type of thing the business tracks. Each record represents one instance of that entity.

## Core entities

| Entity | What one record represents | Example |
| --- | --- | --- |
| Customer | One business that buys from the distributor | Northstar Retail |
| Order | One purchase placed by a customer | A purchase from Northstar Retail |
| Order line | One product entry within an order, with the quantity purchased | 10 cases of packing tape on an order |
| Product | One item the distributor sells | Packing tape, sold by the case |

## Relationships

- Each order belongs to one customer. A customer can place multiple orders.
- Each order contains one or more order lines. Each line belongs to one order.
- Each order line refers to one product. A product can appear on many order lines.

For example, if Northstar Retail buys 10 cases of packing tape and five bundles of shipping cartons in one purchase, that purchase uses one customer record, one order record, and two order lines. A later order can refer to the same customer and products.

The initial model focuses on customer orders. Supplier relationships and shipment records are deferred until their reporting needs are defined.

## Record structures

A primary key uniquely identifies a record in its own table. A foreign key refers to a primary key in another table. For example, two orders can have different `order_id` values and share the same `customer_id`.

| Entity | Field | Type | Purpose |
| --- | --- | --- | --- |
| Customer | `customer_id` | Integer | Primary key. Stays the same if the business changes its name. |
| Customer | `customer_name` | Text | Business name displayed in the dashboard. |
| Order | `order_id` | Integer | Primary key and display identifier, such as `1001`. |
| Order | `customer_id` | Integer | Foreign key to the customer who placed the order. |
| Order | `order_date` | Date | Date the order was placed. |
| Order | `promised_ship_date` | Date | Date the distributor plans to ship the order. |
| Order | `shipped_date` | Date, optional | Actual ship date. Blank until the order ships. |
| Order | `status` | Text | Order status shown in the dashboard. The prototype uses `Processing`, `Shipped`, and `Delayed`. |
| Order line | `order_line_id` | Integer | Primary key for an individual line. |
| Order line | `order_id` | Integer | Foreign key to the order containing this line. |
| Order line | `product_id` | Integer | Foreign key to the product being purchased. |
| Order line | `quantity` | Integer | Number of selling units purchased. |
| Order line | `unit_price_cents` | Integer | Price per selling unit at the time of purchase, in US cents. |
| Product | `product_id` | Integer | Primary key for the product. |
| Product | `product_name` | Text | Display name, such as Packing Tape. |
| Product | `selling_unit` | Text | Unit used to count the product, such as case or bundle. |

Use `YYYY-MM-DD` for dates in CSV files. Store prices in whole cents so totals can be calculated exactly with integer arithmetic. Calculate each line's value as `quantity × unit_price_cents` and add the lines to get the order value.

One order-level ship date assumes the order ships together. This model covers order value before taxes and shipping fees.

## Synthetic dataset

The CSVs in [`data/`](../data/) represent a snapshot as of November 20, 2026. The data includes repeat customers, single-product and multi-product orders, and shipments that went out after the promised date.

| File | Records |
| --- | ---: |
| [`customers.csv`](../data/customers.csv) | 8 |
| [`products.csv`](../data/products.csv) | 6 |
| [`orders.csv`](../data/orders.csv) | 44 |
| [`order_lines.csv`](../data/order_lines.csv) | 84 |

To follow an example, find order `1001` in `orders.csv`. Look up its `customer_id` in `customers.csv`, filter `order_lines.csv` by `order_id`, and use each line's `product_id` to find its name in `products.csv`. Multiply each line's quantity by its unit price in cents and add the results to get the order total.

The Streamlit prototype still displays its original five sample orders. The CSVs are ready for the Week 3 SQLite import.

## Business rules

- Every order belongs to an existing customer and has at least one order line. Every order line belongs to an existing order and refers to an existing product.
- The promised and actual ship dates must be on or after the order date. Orders and actual shipments in the snapshot must be dated on or before the reporting date. The promised ship date may be in the future.
- Each line has a positive whole-number quantity and unit price in cents. The order value is the sum of each line's quantity multiplied by its purchase-time price. Taxes and shipping fees are outside this calculation.

| Status | Rule as of the reporting date |
| --- | --- |
| `Processing` | The actual ship date is blank and the promised ship date is today or later. |
| `Delayed` | The actual ship date is blank and the promised ship date has passed. |
| `Shipped` | The order has an actual ship date on or before the reporting date. |

A shipment is late when its actual ship date falls after its promised ship date. Shipping on the promised date counts as on time. Order `1003` was promised for October 14 and shipped on October 16, so it has status `Shipped` and counts as a late shipment.
