## Permissions & Groups Setup

This app uses Django's built-in permission and group system.

### Custom Permissions (on Book model)
- `can_view`: View list/detail of books
- `can_create`: Create new books
- `can_edit`: Edit existing books
- `can_delete`: Delete books

### Groups & Access
- **Viewers**: `can_view`
- **Editors**: `can_view`, `can_create`, `can_edit`
- **Admins**: All permissions

### Usage
Permissions are enforced in `views.py` using `@permission_required`.

To test:
- Create users in Django admin
- Assign them to groups
- Try accessing restricted views to confirm access control