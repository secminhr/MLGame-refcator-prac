export FILE=profile.pstats

python -m cProfile -s cumtime -o $FILE \
-m mlgame \
-i ./games/Maze_Car/ml/ml_play_template.py \
-i ./games/Maze_Car/ml/ml_play_template.py \
-i ./games/Maze_Car/ml/ml_play_template.py \
-f 120 -1 \
./games/Maze_Car/ \
--game_type=MAZE --sound=off --time_to_play=450 --map=5

python -m gprof2dot -f pstats $FILE | dot -T png -o ${FILE}.png