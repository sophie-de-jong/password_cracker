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
python -m password_cracker list
python -m password_cracker estimate nathalie
python -m password_cracker crack nathalie --verbose
python -m password_cracker add alice "my secret"
python -m password_cracker check alice "my secret"
python -m password_cracker check alice "my secret" --constant-time
python -m password_cracker strength "my secret"
python -m password_cracker generate 12
```

## Notes

- The timing attack functions rely on a comparison implementation that exits early on mismatch.
- `check_password_constant_time` can be used to demonstrate a safer password verification pattern.

## Tests

Run the test suite with the source directory on `PYTHONPATH`:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```
