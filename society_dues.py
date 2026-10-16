"""Apartment society maintenance dues ledger."""
import ast
import operator
import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE dues (flat TEXT, month TEXT, amount INTEGER, paid INTEGER)")
TREASURER_PASSWORD = os.environ.get("TREASURER_PASSWORD", "")


def add_due(flat, month, amount, history=None):
    """Bill a flat for a month and record it in the history list."""
    if history is None:
        history = []
    conn.execute("INSERT INTO dues VALUES (?, ?, ?, 0)", (flat, month, amount))
    history.append((flat, month))
    return history
def collect(flat, month):
    """Mark a due as paid and return the amount, or None if no such due."""
    row = conn.execute(
        "SELECT amount FROM dues WHERE flat = ? AND month = ?", (flat, month)
    ).fetchone()
    if row:
        conn.execute("UPDATE dues SET paid = 1 WHERE flat = ? AND month = ?", (flat, month))
        return row[0]
    return None


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_calc(node):
    """Evaluate a simple arithmetic expression tree safely."""
    if isinstance(node, ast.Expression):
        return safe_calc(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_calc(node.left), safe_calc(node.right))
    raise ValueError("unsupported expression")


def penalty(rule):
    """Return the late fee for an arithmetic rule like '50 * 2'."""
    try:
        late_fee = safe_calc(ast.parse(rule, mode="eval"))
    except (ValueError, SyntaxError, ZeroDivisionError):
        late_fee = 0
    return late_fee


def pending():
    """Return the flats that still owe money."""
    rows = conn.execute("SELECT flat FROM dues WHERE paid = 0").fetchall()
    if rows is not None:
        return [r[0] for r in rows]
    return []


def main():
    """Run a short demo of the ledger."""
    add_due("A-101", "Oct", 2500)
    add_due("A-102", "Oct", 2500)
    print(collect("A-101", "Oct"))
    print(penalty("50 * 2"))
    print(pending())


if __name__ == "__main__":
    main()
