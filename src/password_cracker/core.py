import string
import timeit
import numpy as np

from password_cracker.db import check_password

ALLOWED_CHARS = string.ascii_lowercase + " "


def time_password(user: str, password: str, trials: int = 1000, repeat: int = 10) -> float:
    return np.min(
        timeit.repeat(
            stmt='check_password(user, password)',
            setup=f'user={user!r};password={password!r}',
            globals=globals(),
            number=trials,
            repeat=10,
        )
    )


def estimate_password_length(user: str, max_len: int = 32, trials: int = 1000, verbose: bool = False) -> int:
    sample_times = np.empty(max_len)
    for i in range(max_len):
        sample = "a" * i
        time = time_password(user, sample, trials)
        sample_times[i] = time

    best = int(np.argmax(sample_times))

    if verbose:
        # Normalize scores (z-score)
        mean = np.mean(sample_times)
        std = np.std(sample_times) + 1e-12
        z = (sample_times - mean) / std

        # Convert to confidence weights using softmax
        exp = np.exp(z - np.max(z))
        confidence = exp / np.sum(exp)

        top = np.argsort(-sample_times)[:5]

        print("------ Length Estimation Results -------")
        print(f"{'len':>4} | {'time':>9} | {'z-score':>7} | {'confidence':>10}")
        print("-" * 40)

        for i in top:
            time_ms = sample_times[i] * 1000  # convert seconds → ms
            print(f"{i:4d} | {time_ms:6.4f} ms | {z[i]:7.3f} | {confidence[i]:10.3%}")

        print("-" * 40)
        print(f"-> best guess is length {best} with {confidence[best]:.3%} confidence\n")

    return best


def crack_password(user: str, length: int, trials: int = 1000, verbose: bool = False) -> str:
    guess = "a" * length
    guess_time = time_password(user, guess, trials)
    sample_times = np.empty(len(ALLOWED_CHARS))

    while True:
        for position in range(length):
            for i, candidate_char in enumerate(ALLOWED_CHARS):
                sample = guess[:position] + candidate_char + guess[position + 1:]
                time = time_password(user, sample, trials)
                sample_times[i] = time
                
                if time > guess_time:
                    guess = sample
                    guess_time = time_password(user, guess, trials)

            if verbose:
                # Normalize scores (z-score)
                mean = np.mean(sample_times)
                std = np.std(sample_times) + 1e-12
                z = (sample_times - mean) / std

                # Convert to confidence weights using softmax
                exp = np.exp(z - np.max(z))
                confidence = exp / np.sum(exp)

                top = np.argsort(-sample_times)[:5]

                print(f"---- Character #{position} Estimation Results ----")
                print(f"{'char':>5} | {'time':>9} | {'z-score':>7} | {'confidence':>10}")
                print("-" * 41)

                for c in top:
                    time_ms = sample_times[c] * 1000  # convert seconds → ms
                    print(f"{ALLOWED_CHARS[c]!r:>5} | {time_ms:6.4f} ms | {z[c]:7.3f} | {confidence[c]:10.3%}")

                print("-" * 41)
                print(f"-> best guess is {ALLOWED_CHARS[top[0]]!r} with {confidence[top[0]]:.3%} confidence\n")
        
        if check_password(user, guess):
            return guess

        if verbose:
            print("best guess so far:", guess)

