# 🎵 Music Recommender Simulation

## Project Summary

This project is a small content-based music recommender. It loads a catalog of 18 songs from a CSV file, compares each song to a user's taste profile (favorite genre, favorite mood, and target energy), and gives every song a score. The songs with the highest scores are returned as recommendations, along with plain-language reasons for each score. I tested it with four user profiles, including one adversarial profile, to see where the scoring works well and where it breaks down.

---

## How The System Works

Real platforms like Spotify and YouTube combine two ideas. Collaborative
filtering recommends songs based on what similar users liked, skipped, or
added to playlists. Content-based filtering recommends songs whose attributes
(genre, mood, energy, tempo) match what a user already likes. My version uses
only content-based filtering. It scores every song in the catalog against a
user's taste profile and ranks the highest scores first. It prioritizes genre
first, then mood, then how close a song's energy is to the user's target.

**Song features:** genre, mood, energy, tempo_bpm, valence, danceability, acousticness

**UserProfile features:** favorite_genre, favorite_mood, target_energy

### User Profile
```python
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
}
```

### Algorithm Recipe
- +2.0 points for a genre match
- +1.0 point for a mood match
- Up to +1.0 point for energy closeness: 1 - abs(song_energy - target_energy)
- Maximum score: 4.0

### Expected Bias
This system may over-prioritize genre. A great song that matches the
user's mood and energy but has a different genre can't beat a genre match
with a poor mood fit. With only 18 songs, some genres have just one song,
so users who like those genres get very little variety.

AI critique of my profile: a pop/happy/0.8 profile mostly tests energy,
since rock and lofi songs match neither genre nor mood. I will test extra
profiles (rock/intense/0.9 and lofi/chill/0.35) in Phase 4 to check that
the system can tell them apart.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the starter tests with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output for the default pop / happy / 0.8 energy profile:

```
Loading songs from data/songs.csv...

Top recommendations:

Sunrise City - Score: 3.98
Because: genre match (+2.0); mood match (+1.0); energy closeness (+0.98)

Gym Hero - Score: 2.87
Because: genre match (+2.0); energy closeness (+0.87)

Rooftop Lights - Score: 1.96
Because: mood match (+1.0); energy closeness (+0.96)

Concrete Crown - Score: 0.98
Because: energy closeness (+0.98)

Night Drive Loop - Score: 0.95
Because: energy closeness (+0.95)
```

---

## Profile Outputs (Phase 4)

### High-Energy Pop
```
Profile: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.9}

1. Sunrise City by Neon Echo - Score: 3.92
   Because: genre match (+2.0); mood match (+1.0); energy closeness (+0.92)
2. Gym Hero by Max Pulse - Score: 2.97
   Because: genre match (+2.0); energy closeness (+0.97)
3. Rooftop Lights by Indigo Parade - Score: 1.86
   Because: mood match (+1.0); energy closeness (+0.86)
4. Storm Runner by Voltline - Score: 0.99
   Because: energy closeness (+0.99)
5. Neon Pulse Drop by Circuit Saint - Score: 0.96
   Because: energy closeness (+0.96)
```

### Chill Lofi
```
Profile: {'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.35}

1. Library Rain by Paper Lanterns - Score: 4.00
   Because: genre match (+2.0); mood match (+1.0); energy closeness (+1.00)
2. Midnight Coding by LoRoom - Score: 3.93
   Because: genre match (+2.0); mood match (+1.0); energy closeness (+0.93)
3. Focus Flow by LoRoom - Score: 2.95
   Because: genre match (+2.0); energy closeness (+0.95)
4. Spacewalk Thoughts by Orbit Bloom - Score: 1.93
   Because: mood match (+1.0); energy closeness (+0.93)
5. Coffee Shop Stories by Slow Stereo - Score: 0.98
   Because: energy closeness (+0.98)
```

### Deep Intense Rock
```
Profile: {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.92}

1. Storm Runner by Voltline - Score: 3.99
   Because: genre match (+2.0); mood match (+1.0); energy closeness (+0.99)
2. Gym Hero by Max Pulse - Score: 1.99
   Because: mood match (+1.0); energy closeness (+0.99)
3. Neon Pulse Drop by Circuit Saint - Score: 0.98
   Because: energy closeness (+0.98)
4. Iron Cathedral by Black Obelisk - Score: 0.95
   Because: energy closeness (+0.95)
5. Sunrise City by Neon Echo - Score: 0.90
   Because: energy closeness (+0.90)
```

### Conflicted (sad but high energy) - adversarial
```
Profile: {'favorite_genre': 'folk', 'favorite_mood': 'sad', 'target_energy': 0.9}

1. Hollow Pines by Wren & Willow - Score: 2.40
   Because: genre match (+2.0); energy closeness (+0.40)
2. Storm Runner by Voltline - Score: 0.99
   Because: energy closeness (+0.99)
3. Gym Hero by Max Pulse - Score: 0.97
   Because: energy closeness (+0.97)
4. Neon Pulse Drop by Circuit Saint - Score: 0.96
   Because: energy closeness (+0.96)
5. Iron Cathedral by Black Obelisk - Score: 0.93
   Because: energy closeness (+0.93)
```

---

## Experiments You Tried

**Weight shift: genre 2.0 → 1.0, energy 1.0 → 2.0 (max score still 4.0).**

- **Pop, Lofi, Rock profiles:** the same songs stayed on top. Matching songs were already strong on energy too, so the top results did not change. Gaps between songs got smaller (e.g. Gym Hero for the rock profile went from 1.99 to 2.98, closer to Storm Runner at 3.98).
- **Conflicted profile (folk, sad, energy 0.9):** this changed the most. Before, Hollow Pines (folk, energy 0.30) ranked first with 2.40 just for matching the genre. After the shift it dropped out of the top 5, and high-energy songs like Storm Runner took over.
- **More accurate or just different?** More accurate for the conflicted profile, because the results now fit the energy the user asked for. But all five results match only on energy, so the system now ignores genre and mood for this user. Weight shifts trade one bias for another.

Final weights kept in the code: (state which one you left in, see below).

---

## Limitations and Risks

- **Genre dominates the ranking.** A genre match is worth 2.0 points, so a same-genre song with poor energy can beat a better-fitting song from another genre. In the adversarial profile, Hollow Pines (folk, energy 0.30) ranks first with a score of 2.40 even though the user wanted energy 0.9. It wins only because it matches the genre.
- **After the genre match, energy decides everything.** In the second through fifth spots, almost every song is explained only by "energy closeness", so the list becomes a list of songs with similar energy, not similar taste. The adversarial profile shows this clearly: positions 2-5 are rock, pop, EDM and metal songs.
- **Mood must match exactly.** No song has the mood "sad", so that part of the profile never scores. The system does not know that "melancholic" or "moody" is close to "sad".
- **Gym Hero shows up for very different users.** It appears for High-Energy Pop (rank 2), Deep Intense Rock (rank 2), and the adversarial profile (rank 3), because it is high in energy and its mood is "intense".
- **Tiny catalog.** With 18 songs, some genres have only one song, so those users get very little variety. There is also only one rock song.
- **Unused features.** valence, danceability, acousticness and tempo are in the data but not in the score.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

*(TODO: write 1 to 2 paragraphs in your own words.)*

- What did you learn about how recommenders turn data into predictions?
- Where could bias or unfairness show up in systems like this?