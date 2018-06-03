import challenge

challenge_file = 'challenge/challenge.pt20.json'
results_file = "results/results20.txt"

challenge.index_songs_from_similar_playlist(challenge_file, results_file)
challenge.songs_popularity_file(results_file)
