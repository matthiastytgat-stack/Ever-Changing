/**
 * inefficientCode.ts
 * A collection of common TypeScript anti-patterns and inefficiencies.
 * Intended for code quality tooling tests.
 */


// ── 1. Using 'any' everywhere (defeats TypeScript's purpose) ─────────────────
function processPayload(data: any): any {
  return data.value * data.rate;   // no type safety; use a proper interface
}


// ── 2. Non-null assertions without justification ──────────────────────────────
function getUsername(user: { name?: string }): string {
  return user.name!;               // crashes at runtime if name is undefined
}


// ── 3. Type assertions instead of type guards ─────────────────────────────────
interface Cat { meow(): void; }
interface Dog { bark(): void; }

function makeSound(animal: Cat | Dog): void {
  (animal as Cat).meow();          // assumes Cat; crashes if it's actually a Dog
}


// ── 4. Ignoring Promise rejections (no try/catch or .catch) ──────────────────
async function loadUser(id: number): Promise<void> {
  const res = await fetch(`/api/users/${id}`);   // unhandled rejection on network error
  console.log(await res.json());
}


// ── 5. Enums with string values duplicated in logic ──────────────────────────
const STATUS_ACTIVE   = "active";
const STATUS_INACTIVE = "inactive";
const STATUS_PENDING  = "pending";
// use: enum Status { Active = "active", Inactive = "inactive", Pending = "pending" }


// ── 6. Object spread for deep clone (only shallow) ───────────────────────────
function cloneOrder(order: { items: string[]; total: number }) {
  const copy = { ...order };
  copy.items.push("extra");        // mutates the original's items array
  return copy;
}


// ── 7. Returning union types that callers must narrow constantly ───────────────
function divide(a: number, b: number): number | null | undefined {
  if (b === 0) return null;
  if (isNaN(a) || isNaN(b)) return undefined;
  return a / b;                    // callers need three branches every time
}


// ── 8. Interface with only optional fields (everything unknown) ───────────────
interface Config {
  host?: string;
  port?: number;
  timeout?: number;
  retries?: number;               // all optional → no guarantees; use Required<> where needed
}


// ── 9. Compiling RegExp inside a function called in a loop ───────────────────
function countMatches(items: string[], pattern: string): number {
  return items.filter(i => new RegExp(pattern).test(i)).length;  // recompiles each .test()
}


// ── 10. async/await inside Array.forEach ─────────────────────────────────────
async function processAll(ids: number[]): Promise<void> {
  ids.forEach(async id => {
    await fetch(`/api/${id}`);     // forEach doesn't await; all fire concurrently uncontrolled
  });
}


// ── 11. Hardcoded secrets ─────────────────────────────────────────────────────
const API_KEY    = "sk-prod-abc123";
const DB_PASS    = "hunter2";      // use process.env / secrets manager


// ── 12. Mutating function parameters ─────────────────────────────────────────
function applyTax(order: { total: number }, rate: number): { total: number } {
  order.total *= 1 + rate;         // mutates caller's object; return a new one
  return order;
}


// ── 13. Using == instead of === ───────────────────────────────────────────────
function isZero(val: number): boolean {
  return val == 0;                 // coerces; always use ===
}


// ── 14. Index signature with 'any' value type ────────────────────────────────
interface DataStore {
  [key: string]: any;              // any value possible; use generics or mapped types
}


// ── 15. Catching Error but re-throwing as unknown type ───────────────────────
function safeParse(json: string): unknown {
  try {
    return JSON.parse(json);
  } catch (e) {
    throw new Error(e as any);     // wraps original info poorly; just rethrow or check instanceof
  }
}


// ── 16. Boolean flag parameters (boolean trap) ───────────────────────────────
function render(component: string, visible: boolean, animated: boolean, cached: boolean) {
  // callers: render("Modal", true, false, true) — unreadable; use an options object
}


// ── 17. Deeply nested optional chaining without fallback ─────────────────────
function getCity(user?: { address?: { city?: string } }): string {
  return user?.address?.city as string;   // returns undefined silently; add ?? "Unknown"
}


// ── 18. Large switch on string literals (should be a lookup table) ────────────
function getLabel(status: string): string {
  switch (status) {
    case "active":   return "Active";
    case "inactive": return "Inactive";
    case "pending":  return "Pending";
    case "archived": return "Archived";
    case "deleted":  return "Deleted";
    default:         return "Unknown";    // use: const LABELS: Record<string, string> = { ... }
  }
}


// ── 19. console.log with sensitive data ──────────────────────────────────────
function login(username: string, password: string): boolean {
  console.log(`Login attempt: ${username} / ${password}`);   // logs plaintext password
  return username === "admin";
}


// ── 20. Re-exporting everything with 'export *' ───────────────────────────────
// In a barrel file:
// export * from "./orders";
// export * from "./users";
// export * from "./products";
// breaks tree-shaking and leaks internal symbols


// ── 21. No readonly on constructor-injected dependencies ──────────────────────
class OrderService {
  private db: DataStore;
  constructor(db: DataStore) {
    this.db = db;                  // should be: private readonly db: DataStore
  }
}


// ── 22. Catching and ignoring errors silently ────────────────────────────────
async function sendEmail(to: string, body: string): Promise<void> {
  try {
    await fetch("/api/email", { method: "POST", body: JSON.stringify({ to, body }) });
  } catch {
    // silent — caller has no idea the email failed
  }
}


// ── 23. Type widening via explicit annotation ─────────────────────────────────
const ROLES: string[] = ["admin", "editor", "viewer"];  // widened to string[]
// use: const ROLES = ["admin", "editor", "viewer"] as const


// ── 24. Array.find result used without undefined check ───────────────────────
function getProduct(id: number, products: { id: number; name: string }[]): string {
  return products.find(p => p.id === id)!.name;   // ! hides possible undefined
}


// ── 25. Overloaded function returning different shapes ────────────────────────
function fetch_data(id: number): { data: string } | { error: string } | null {
  if (id < 0) return null;
  if (id === 0) return { error: "invalid" };
  return { data: "ok" };           // three different shapes; callers need complex narrowing
}
