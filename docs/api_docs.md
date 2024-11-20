### Key Features in the `app.py`

1. **Search Query**:
   - Supports searching across `abstract`, `keywords`, and `author`.
   - Boosts `keywords` field for higher relevance in matching.

2. **Filters**:
   - Allows filtering by `year` using a query parameter (e.g., `?year=2023`).

3. **Sorting**:
   - Enables sorting by `year` in ascending or descending order (default: `desc`).

4. **Highlighting**:
   - Highlights matches in `abstract` and `keywords` fields for better readability.

5. **Environment Variables**:
   - Elasticsearch credentials are securely loaded from `.env`.

6. **Error Prevention**:
   - Handles empty search queries gracefully with a default value of `''`.

---

### Test Examples

#### Basic Search:
```bash
curl "http://127.0.0.1:5000/search?q=smart home"
```

#### Filter by Year:
```bash
curl "http://127.0.0.1:5000/search?q=smart home&year=2023"
```

#### Sort Results:
```bash
curl "http://127.0.0.1:5000/search?q=smart home&sort=asc"
```