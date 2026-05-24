# Password Cracker

A small timing-attack password cracker demo with CLI support and simple user management.

## Features

- Estimate password length using timing differences
- Recover passwords via sequential character timing analysis
- Add or update users and save the database to `password_cracker_db.json`
- Verify guesses with either normal or constant-time comparison
- Evaluate password strength and generate random passwords

## Usage

From the project root:

```bash
uv sync
uv run password-cracker list
uv run password-cracker estimate nathalie
uv run password-cracker crack nathalie --verbose
uv run password-cracker add alice "my secret"
uv run password-cracker check alice "my secret"
uv run password-cracker check alice "my secret" --constant-time
```

## Notes

- The timing attack functions rely on a comparison implementation that exits early on mismatch.
- `check_password_constant_time` can be used to demonstrate a safer password verification pattern.
