import challenge

challenge_file = 'challenge/challenge.pt8.notracks.json'
results_file = "results/results8.notracks.txt"

challenge.index_songs_from_similar_playlist(challenge_file, results_file)
challenge.songs_popularity_file(results_file)
