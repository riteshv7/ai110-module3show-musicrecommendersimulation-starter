# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a user's favorite genre, favorite mood, and target energy level. It returns a top 5 list and a short reason for each song.

It assumes the user has one favorite genre, one favorite mood, and one energy level they want. It is built for classroom exploration, not for real users.

**Not intended for:**
- Real music apps or real listeners
- Making decisions about artists, such as who gets promoted
- Users with mixed or changing tastes
- Any setting where fairness to artists or genres matters

---

## 3. How the Model Works

The system looks at every song one at a time and gives it points:

- **+2.0 points** if the song's genre matches the user's favorite genre
- **+1.0 point** if the song's mood matches the user's favorite mood
- **Up to +1.0 point for energy.** The closer the song's energy is to the user's target, the more points it gets. A perfect match gives 1.0. A song far away gives close to 0.

The maximum score is 4.0. After every song has a score, the system sorts them from highest to lowest and shows the top 5. Each result also lists its reasons, such as "genre match (+2.0)", so you can see why it ranked where it did.

Genre and mood must match exactly. "Folk" matches "folk" and nothing else. Energy is the only feature that works on a sliding scale.

**Changes from the starter:** I wrote the loading, scoring, and ranking code. I also made the scoring return reasons along with the score.

---

## 4. Data

- **18 songs** in `data/songs.csv`
- The starter file had 10 songs. I added 8 more using an AI assistant, each with a new genre and a new mood.
- **15 genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, r&b, metal, edm, reggae, folk
- **14 moods:** happy, chill, intense, relaxed, moody, focused, confident, serene, nostalgic, romantic, aggressive, euphoric, laid-back, melancholic
- Most genres have only one song. Lofi has the most (3), and pop has 2.
- Each song also has tempo, valence, danceability, and acousticness, but **the scoring does not use them**.
- Missing: lyrics, language, artist popularity, release year, and anything about how people actually listen (skips, replays, playlists).

---

## 5. Strengths

- It works well for users whose taste fits cleanly into one genre, one mood, and one energy level. The Chill Lofi profile returned all three lofi songs first, with Library Rain scoring a perfect 4.00.
- The Deep Intense Rock profile put Storm Runner first, which is the only rock song, and it matched on genre, mood, and energy.
- It is easy to explain. Every score comes with reasons, so I can say exactly why a song ranked where it did.
- Energy closeness works as intended. It rewards songs on either side of the target, not just higher or lower ones.

---

## 6. Limitations and Bias

The system gives genre a lot of power. A genre match is worth 2.0 points, which is twice a mood match. I found this with my adversarial profile, a folk fan who wants "sad" music at energy 0.9. The top result was Hollow Pines, a quiet folk song with energy 0.30. It scored 2.40 only because of its genre, even though the user asked for high energy. When I halved the genre weight and doubled the energy weight, Hollow Pines dropped out of the top 5, which shows how much the genre weight controlled the result.

Other problems I found:
- **Nothing in the catalog has the mood "sad".** The system cannot tell that "melancholic" or "moody" is close to "sad", so that part of the profile never scored for anyone.
- **After the genre and mood matches, energy decides everything.** Most songs in positions 2 to 5 are explained only by "energy closeness", so those lists are really "songs with similar energy".
- **Gym Hero appears for many people.** It shows up for the High-Energy Pop, Deep Intense Rock, and conflicted profiles. It is a high-energy pop song with an "intense" mood, so it picks up points from several different users.
- **The catalog is tiny.** Most genres have a single song, so fans of those genres get one good match and then a list of unrelated songs.
- **Unused features.** Valence, danceability, acousticness, and tempo are in the data but not in the score. The `UserProfile` even has a `likes_acoustic` field that nothing uses.
- **One taste per user.** A person who likes both lofi and rock cannot be described by this profile.

---

## 7. Evaluation

**Profiles tested:**
1. High-Energy Pop (pop, happy, energy 0.9)
2. Chill Lofi (lofi, chill, energy 0.35)
3. Deep Intense Rock (rock, intense, energy 0.92)
4. Conflicted (folk, sad, energy 0.9). This one is adversarial.

I also ran the original pop / happy / 0.8 profile as a sample. The full outputs are in the README.

**What I looked for:** whether the top song matched what I would pick by hand, whether different profiles gave different lists, and whether the reasons made sense.

**Experiment:** I changed the weights to genre 1.0, mood 1.0, energy 2.0 (the maximum stayed 4.0). The pop, lofi, and rock profiles kept the same top songs, but the gaps between songs got smaller. The conflicted profile changed the most: Hollow Pines fell out of the top 5, and high-energy songs like Storm Runner took over. That is more accurate for the energy the user asked for, but all five results now match only on energy, so genre and mood are ignored for that user. The change did not fix the problem, it just moved the bias.

**What surprised me:** how much one weight controlled the results, and that a folk song with the wrong energy could win for someone who wanted high energy.

**Why Gym Hero keeps showing up for "Happy Pop" fans:** Gym Hero is a pop song, so it gets the genre points. Its energy (0.93) is also almost exactly what a high-energy pop fan wants, so it gets nearly full energy points. The system never checks that its mood is "intense" instead of "happy", because a mood miss only costs the 1.0 mood bonus, not a penalty.

**Profile comparisons:**

- **High-Energy Pop vs Chill Lofi:** The two lists share no songs. Pop gets loud, fast songs like Sunrise City and Gym Hero. Lofi gets quiet songs like Library Rain and Midnight Coding. This makes sense because the energy targets (0.9 and 0.35) sit at opposite ends and the genres and moods differ too.
- **High-Energy Pop vs Deep Intense Rock:** Four of the five songs are the same (Sunrise City, Gym Hero, Storm Runner, Neon Pulse Drop). The energy targets are almost the same (0.9 and 0.92), so most of the list is decided by energy. The main differences are the first place (Sunrise City vs Storm Runner) and that rock brings in Iron Cathedral, a metal song, while pop brings in Rooftop Lights, a happy indie pop song.
- **High-Energy Pop vs Conflicted:** Both want energy 0.9, so they share Storm Runner, Gym Hero, and Neon Pulse Drop. Pop leads with Sunrise City because it matches genre and mood. The conflicted profile leads with Hollow Pines because it matches folk, even though its energy is low.
- **Chill Lofi vs Deep Intense Rock:** No shared songs. This is the clearest contrast. Lofi picks quiet, acoustic songs and rock picks loud, intense ones. It shows that the system can tell the two tastes apart, which is what my earlier AI critique said I needed to check.
- **Chill Lofi vs Conflicted:** No shared songs. Lofi looks for low energy and the conflicted profile wants high energy, so the lists point in opposite directions.
- **Deep Intense Rock vs Conflicted:** Four of the five songs are the same (Storm Runner, Gym Hero, Neon Pulse Drop, Iron Cathedral). The energy targets are close, so energy dominates. The conflicted profile differs only because Hollow Pines gets in on the folk match, and the rock profile gives a mood bonus to Gym Hero.

---

## 8. Future Work

- **Use more features.** Add valence and acousticness (and finally use `likes_acoustic`) so that rock and lofi are separated by more than energy alone.
- **Treat similar moods as close.** Group moods like sad, melancholic, and moody so that near-misses still earn partial points.
- **Add a diversity rule.** Penalize songs from an artist or genre that is already in the top results, so lists are not full of near-duplicates.
- **Support mixed tastes.** Let a profile list several genres or moods with different weights.
- **Add more songs.** A larger catalog would give each genre more than one or two options.

---

## 9. Personal Reflection

Building this showed me that a recommender is just a set of choices about what matters. My scoring rule is simple (points for genre, mood, and energy closeness), yet it produced lists that felt sensible. But when I tested an adversarial profile, a quiet folk song ranked first for someone who wanted high-energy music, because the genre weight was too strong. Changing the weights fixed that case but made the system ignore genre and mood for that user, so the bias moved instead of disappearing.

Bias can show up in small ways: a tiny catalog where most genres have one song, features the score never uses, and exact-match rules that can't tell "sad" from "melancholic." Real systems with millions of songs and users would hide these problems more, not remove them. See `model_card.md` for the full details.