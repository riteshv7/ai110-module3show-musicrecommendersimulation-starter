"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
    },
    # Adversarial: sad mood but very high energy
    "Conflicted (sad but high energy)": {
        "favorite_genre": "folk",
        "favorite_mood": "sad",
        "target_energy": 0.9,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one profile."""
    print(f"\n=== {name} ===")
    print(f"Profile: {user_prefs}\n")
    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=k), start=1
    ):
        print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()