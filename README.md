# Tryton Module Index

A grouping place for all third-party modules.

## How to contribute (Add modules)

### Submit a request adding the new module(s)

- Modules are always added to the end of the `src/assets/modules.json` file.
- - Required keys: `key`, `package_name`, `url`.
- - Optional keys: `tags`, `doc_url`.
- - Order always must be: `key`, `package_name`, `url`, `doc_url`, `tags`.

```diff
+    {
+      "key": "new_author/my_module",
+      "package_name": "trytond-my_module",
+      "url": "https://self-hosted-vcs.com/foo/my_module",
+      "tags": [
+        "new_tag"
+      ]
+    }
```

- If new authors or tags are added, they should be added in the `src/assets/authors.json` and `src/assets/tags.json` files. (Alphabetically sorted)

```diff
+    "new_author"
```

```diff
+    "new_tag"
```

- If VCS is self-hosted, the type must be added in `src/assets/vcs_types.json`.
For example:

```diff
+    "self-hosted-vcs.com": "gitlab"
```

- Make sure to:
- - `python api check new_author/my_module new_author/my_module2 ...` has been executed without any errors.
- - NOT modify `src/assets/modules-lock.json`.

## How to contribute (Improving the web or process)

```bash
# Fist start.
git clone <url>
cd tryton-module-index
npm i
npm run dev
```

Only and exclusively of the web, without adding new modules.
