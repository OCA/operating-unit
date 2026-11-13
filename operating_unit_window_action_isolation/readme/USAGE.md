Configure operating units and assign a default operating unit to users.

Example:

- User A → Default Operating Unit = OU-A
- User B → Default Operating Unit = OU-B

When a window action targets a model containing an `operating_unit_id` field, the action domain is automatically extended.

For User A:

```python
[('operating_unit_id', 'in', [False, OU_A_ID])]
```

For User B:

```python
[('operating_unit_id', 'in', [False, OU_B_ID])]
```

As a result:

- User A sees records belonging to OU-A and records without an operating unit.
- User B sees records belonging to OU-B and records without an operating unit.
- Users without a default operating unit are not affected.
- The superuser is not affected.