"""dupkey_scan -- fail when a gate's own rule table silently deletes one of its rules.

WHY THIS EXISTS (R83). appendix_identity.py defined "B: Exact capability table" twice in the
same EXEMPT dict. Python keeps the last binding and discards the first without a warning, so
the dash-footnote basis had not been in force since R82-INT. Nothing surfaced it: the file
imported cleanly, the tool ran, and it reported PASS.

This is a different failure from the other three the battery has produced. Those were gates
passing for a reason unrelated to the question asked, which at least leaves a reason to audit.
Here the rule was never in force at all, deleted by the language runtime at parse time, with
no symptom anywhere. A reviewer reading the source sees both entries and reasonably concludes
both apply.

WHY AST RATHER THAN LINTING. The obvious fix is `pylint --enable=duplicate-key`, which is one
line and covers every file. pylint is not in this environment, and adding a linter dependency
to a gate battery that currently has none is a worse trade than thirty lines of ast. This
checks the same property with the standard library, and it covers every tool at once rather
than needing an assertion added by hand to each new rule table.

WHAT IT CHECKS, in every tools/*.py:
  - dict literals with a repeated constant key (the appendix_identity defect);
  - set literals with a repeated constant member, which is the same defect for registries
    written as sets rather than mappings.

Non-constant keys are skipped: they cannot be compared without evaluating them, and no rule
table in this battery uses one.

Usage:
    python tools/dupkey_scan.py [dir]      dir defaults to the tools directory
Exit 1 on any duplicate.
"""
import ast
import collections
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def constants(nodes):
    return [n.value for n in nodes
            if isinstance(n, ast.Constant) and isinstance(n.value, (str, int))]


def duplicates(values):
    return sorted(v for v, c in collections.Counter(values).items() if c > 1)


def main():
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
    files = sorted(root.glob("*.py"))
    findings = []

    for f in files:
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError as exc:
            findings.append((f.name, getattr(exc, "lineno", 0), "UNPARSEABLE", [str(exc)]))
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                dup = duplicates(constants(node.keys))
                if dup:
                    findings.append((f.name, node.lineno, "dict key", dup))
            elif isinstance(node, ast.Set):
                dup = duplicates(constants(node.elts))
                if dup:
                    findings.append((f.name, node.lineno, "set member", dup))

    print("dupkey_scan: %d file(s) under %s" % (len(files), root))
    if not findings:
        print("\nPASS -- no rule is shadowed by a later duplicate")
        return 0
    for name, line, kind, dup in findings:
        print("  %s:%d  duplicate %s: %s" % (name, line, kind, ", ".join(map(repr, dup))))
        print("        the earlier binding is discarded at parse time and never takes effect")
    print("\nFAIL -- %d shadowed rule(s)" % len(findings))
    return 1


if __name__ == "__main__":
    sys.exit(main())
