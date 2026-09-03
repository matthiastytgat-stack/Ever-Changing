import { Client } from "pg";

const client = new Client({
  host: "localhost",
  port: 5432,
  database: "example_db",
  user: "postgres",
  password: "password",
});

// ❌ VULNERABLE: SQL Injection
// User input is concatenated directly into the query string.
// An attacker could pass: username = "' OR '1'='1" to bypass authentication,
// or "'; DROP TABLE users; --" to destroy data.
async function getUserVulnerable(username: string): Promise<void> {
  await client.connect();

  const query = "SELECT * FROM users WHERE username = '" + username + "'";
  //             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  //             VULNERABILITY: raw string concatenation — never do this!

  console.log("Executing query:", query);
  const result = await client.query(query);
  console.log("Result:", result.rows);

  await client.end();
}

// ✅ SAFE: Parameterised Query
// The database driver handles escaping; user input can never alter the SQL structure.
async function getUserSafe(username: string): Promise<void> {
  await client.connect();

  const query = "SELECT * FROM users WHERE username = $1";
  const values = [username];

  console.log("Executing query:", query, "with values:", values);
  const result = await client.query(query, values);
  console.log("Result:", result.rows);

  await client.end();
}

// --- Demo ---
const maliciousInput = "' OR '1'='1";

console.log("=== Vulnerable call ===");
getUserVulnerable(maliciousInput);
// Produces: SELECT * FROM users WHERE username = '' OR '1'='1'
// → returns every row in the table!

console.log("\n=== Safe call ===");
getUserSafe(maliciousInput);
// Produces: SELECT * FROM users WHERE username = $1  [values: ["' OR '1'='1"]]
// → returns nothing (no user with that literal username)
