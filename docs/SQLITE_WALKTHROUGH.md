# Week 3 SQLite walkthrough

SQLite runs inside the program using it. The `sqlite3` command-line tool lets you run SQL directly, and Python's built-in `sqlite3` module lets OpsHub run SQL from application code.

## Step 1 — Run a query

In your terminal, open an in-memory database:

```sh
sqlite3 :memory:
```

At the `sqlite>` prompt, enter:

```sql
SELECT 'OpsHub' AS project, 10 * 4250 AS line_total_cents;
```

The default output is `OpsHub|42500`. `SELECT` returns values and `AS` names each result column. The example calculates the line total for 10 units at 4,250 cents each, or $425.00.

Type `.quit` to return to the terminal. The in-memory database disappears as soon as the session closes. In Step 2, we'll use a database file so the OpsHub tables persist between sessions.

## Step 2 — Create the tables

From the OpsHub repository root, open a new database file. If `db.sqlite3` already contains your Week 3 work, continue at Step 4 to run the practice queries against it.

```sh
sqlite3 db.sqlite3
```

At the `sqlite>` prompt, run the saved [table definitions](../sql/schema.sql):

```text
PRAGMA foreign_keys = ON;
.read sql/schema.sql
.tables
```

`.tables` should list `customers`, `order_lines`, `orders`, and `products`. Foreign key enforcement applies to the current session, so enable it again if you reopen SQLite before importing.

## Step 3 — Import the synthetic data

Run these commands once against the empty tables. Load customers and products first so their IDs exist when orders and order lines refer to them. `--skip 1` skips each CSV header.

```text
PRAGMA foreign_keys = ON;
.import --csv --skip 1 data/customers.csv customers
.import --csv --skip 1 data/products.csv products
.import --csv --skip 1 data/orders.csv orders
.import --csv --skip 1 data/order_lines.csv order_lines
UPDATE orders SET shipped_date = NULL WHERE shipped_date = '';
```

The `UPDATE` represents blank ship dates as SQL `NULL`. Check the import:

```sql
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM order_lines;
PRAGMA foreign_key_check;
```

Expect counts of `8`, `6`, `44`, and `84`, in that order. `foreign_key_check` should return no rows.

## Step 4 — Run the practice queries

From the `sqlite>` prompt, run:

```text
.read sql/practice_queries.sql
```

The [practice queries](../sql/practice_queries.sql) list eight overdue orders, show those orders again with customer names, and return `14400` cents ($144.00) for order `1001`.
