# Change Log

The format is modified from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

### [10.4.1] - 2023.11.10
**新增**
* 在初始資料，新增一個背景圖層。

### [10.3.1] - 2023.09.22
**新增**
* 新增 list 型態的遊戲參數。

### [10.2.9] - 2023.05.11
**更新**
* 修正 error_type 顯示資訊

### [10.2.1] - 2023.02.24
**新增**
* 增加`-r` `-p`參數，讓使用者匯出json格式的畫面資訊，可指定單一檔案幀數與存放位置。
* 增加暫停的功能，遊戲執行過程中，可以按下 `P` 暫停遊戲。


### [10.1.1] - 2023.02.07
**新增**
* 增加`-o`參數，讓使用者開啟匯出圖片功能，並存至指定資料夾。

### [10.0.3] - 2022.10.13
**修復**
* 修復在伺服器上運作，WS會提前中斷的問題。

### [10.0.2] - 2022.09.13
**修復**
* 修復拖曳視窗，會產生warning的問題

### [10.0.1] - 2022.09.05
**修復**
* 修復WS 的連線問題

### [10.0.0] - 2022.08.22
**新增**
* MLPlay 初始化資訊新增遊戲參數
* 新增文件


### [9.5.3] - 2022.08.02
**更新**
* 更新專案架構 
* 建立pypi 
* 更新指令格式
* 更新MLPlay 初始化資訊


### [9.3.5] - 2022.04.18
**新增**
* 新增 game_progress 欄位: `toggle_with_bias` 

### [9.3.4] - 2022.04.18
**修復**
* 修正 easy_game 的 `main.py`

### [9.3.3] - 2022.04.14

**新增**
* 在 `view_model.py` 中 新增 `create_scene_progress_data` 

**變更**
* `get_scene_progress_data` 須回傳 `frame`

### [9.3.2] - 2022.04.12
**修復**
* 改善 MLGame 繪圖機制

### [9.3.1] - 2022.04.08
**變更**
* MLGame會將鍵盤事件(英文字母、數字、方向鍵)，傳送給 AI Client。


### [9.2.3] - 2022.02.13
**修復**
* 修復遊戲AI沒有回傳 `RESET` 會無法停止的錯誤


### [9.2.2-beta] - 2022.02.09
**變更**
* 更新 easy_game中的積木設定檔案

### [9.2.1-beta] - 2022.01.24
**變更**

* 改變啟動遊戲指令中，遊戲的參數格式
  * old: `python MLGame.py -i ml_play_template.py easy_game 1200 15 10 FF9800`
  * now: `python MLGame.py -i ml_play_template.py easy_game  --score 10 --color FF9800 --time_to_play 1200 --total_point 15`

**新增**
* 新增縮放功能 遊戲畫面中可以使用 `I` `J` `K` `L` `U` `O` `H` 來控制畫面
* 遊戲重新啟動，遊戲畫面會重置。
* 新增中文英文 變更文件


### [9.0.7-beta] - 2021.07.23
**Changed**

* Change the function name and data format in each game.

**Added**
* Add Interface `PaiaGame` every game should implement this interface to run on PAIA. 
* Add decorator to validate data format.
* Add view.py in MLGame to draw scene of game.
* Add two game in submodule.



### [Beta 8.0.1] - 2020.10.05

**Changed**

* The recorded game progress for the inactivated ml client will be an empty list.

### [Beta 8.0] - 2020.09.29

**Added**

* Add `"record_format_version"` field to the log file

**Changed**

* Change the data structure received from or sent to the game class: use a dict to store the information of each ml client. For example, the game has two players and defines the name of them as `"ml_1P"` and `"ml_2P"` in the `config.py`.
  * The scene information returned from `get_player_scene_info()` will be:
    ```
    {
        "ml_1P": scene_info_for_ml_1P,
        "ml_2P": scene_info_for_ml_2P
    }
    ```
  * The command sent to the `update()` will be:
    ```
    {
        "ml_1P": command_sent_from_ml_1P,
        "ml_2P": command_sent_from_ml_2P
    }
    ```
  * And the command returned from `get_keyboard_command()` should also be:
    ```
    {
        "ml_1P": command_for_ml_1P,
        "ml_2P": command_for_ml_2P
    }
    ```
* Record the scene information and command individually for each ml client in the log file
* Update the version of built-in games
  * arkanoid: 1.0 -> 1.1
  * pingpong: 1.1 -> 1.2
  * snake: 1.0 -> 1.1

### [Beta 7.2] - 2020.08.23

**Fixed**

* The game could not be closed when running non-python client

**Changed**

* `-i/--input-script` supports specifying the file in the subdirectory
  * For example, `-i foo/ml_play.py` means the file is at `games/<game_name>/ml/foo/ml_play.py`

**Removed**

* Remove `--input-module` flag

### [Beta 7.1.3] - 2020.06.20

**Fixed**

* Handle the exception of `SystemExit`
* Handle the situation of reseting the ml executor before the game ends
  * The game executor will ignore the ready command.

**Changed**

* Optimize the checking of the received object from either side

### [Beta 7.1.2] - 2020.06.19

**Fixed**

* Use wrong value to chack frame delay

**Changed**

* Modify the game "snake" for the game development tutorial
  * The `ml_play_template.py` of the game "snake" contains simple rule-based algorithm.

### [Beta 7.1.1] - 2020.06.15

**Changed**

* ML process doesn't send the command only when the returned value of `MLPlay.update()` is `None`.

### [Beta 7.1] - 2020.06.01

**Fixed**

* Handle the exception of `BrokenPipeError`

**Added**

* Add "dynamic_ml_clients" to the "GAME_SETUP" of the game config

### [Beta 7.0.1] - 2020.05.29

This update is compatible with Beta 7.0.

**Fixed**

* Hang when the game exits on Linux

**Added**

* Add `errno.py` to define the exit code of errors
* Handle the exception occurred in manual mode

**Changed**

* Change the exit code of errors

### [Beta 7.0] - 2020.05.27

**Added**

* Use executors to control the execution loop
  * The game and the ml script only need to provide "class" for the executor to invoke (like an interface).
  * The game doesn't need to provide manual and ml version. Just one game class.
  * Replace `ml_loop()` with `MLPlay` class in ml script
* Add commnuication manager
  * The manager for the ml process has a queue for storing the object received. If the queue has more than 15 objects, the oldest object will be dropped.

**Changed**

* Change the format of the recording game progress
* Replace `PROCESSES` with `GAME_SETUP` in `config.py` of the game to setup the game and the ml scripts
* Rename `GameConfig` to `ExecutionCommand`
* Simplfy the `communication` package into a module

**Removed**

* Remove `record.py` and ml version of the game in the game directory

### [Beta 6.1] - 2020.05.06

**Changed**

* Pingpong - version 1.1
  * Shorten the ball speed increasing interval
  * Randomly set the initial position of the blocker, and speed up the moving speed of it

### [Beta 6.0] - 2020.04.28

**Added**

* Add `-l` and `--list` flag for listing available games
* Use `config.py` in games to set up the game parameters and the game execution
* Use `argparse` for generating and handling game parameters
  * List game parameters of a game by using `python MLGame.py <game> -h`
* Exit with non-zero value when an error occurred

**Changed**

* The game execution flags must be specified before the game name, including `-i/--input-script/--input-module` flags
* `-i/--input-script/--input-module` flags carry one script or one module at a time.
  * Specify these flags multiple times for multiple scripts or modules, such as `-i script_1P -i script_2P`.
* Games: Use dictionary objects as communication objects between game and ml processes for flexibility
  * The record file only contains dictionay objects and built-in types, therefore, it can be read outside the `mlgame` directory.
* `mlgame.gamedev.recorder.RecorderHelper` only accepts dictionary object.
* Code refactoring

**Removed**

* Games
  * Remove `main.py` (replaced by `config.py`)
  * Remove `communication.py`
    * For the ml script, use `mlgame.communication.ml` module to communicate with the game process. See `ml_play_template.py` for the example.
* Remove `CommandReceiver` from the `mlgame.communication.game`
  * The game has to validate the command recevied by itself.

### [Beta 5.0.1] - 2020.03.06

**Fixed**

* Fix typo in the README of the arkanoid
* Arkanoid: Add additional checking condition for the ball bouncing

### [Beta 5.0] - 2020.03.03

**Added**

* Arkanoid and Pingpong:
  * The serving position and direction of the ball can be decided
  * Add difficulties for different mechanisms
  * Add ball slicing mechanism
* Arkanoid: Add hard bricks
* Pingpong: Add blocker

**Changed**

* Update the python from 3.5 to 3.6: For the `auto()` of the custom `Enum`
* Optimize the output of the error message
* Refactor the game classes: Extract the drawing and recording functions
* Add prefix to the filename of the record files
* Physics: Optimize the ball bouncing algorithm

### [Beta 4.1] - 2019.11.06

**Added**

* New game - Snake
* Add README to the game Arkanoid and Pingpong

**Changed**

* Update pygame from 1.9.4 to 1.9.6
* Arkanoid and Pingpong (Follow the structure of the game Snake):
  * Move `SceneInfo` to the `gamecore.py`
  * Rename `GameInstruction` to `GameCommand`
* Arkanoid: Add `command` member to `SceneInfo`
  * Trying to load the record files generated before beta 4.1 will get `AttributeError: 'SceneInfo' object has no attribute 'command'` error.
* Code refactoring

### [Beta 4.0] - 2019.08.30

**Added**

* `mlgame` - MLGame development API
* `--input-module` flag for specifying the absolute importing path of user modules

**Changed**

* Use 4 spaces instead of tab
* Support one shot mode in the manual mode
* Fit the existing games to the new API
* Move the directory of game to "games" directory
* Arkanoid: Wait for the ml process before start new round
* Arkanoid: Change the communication API

### [Beta 3.2] - 2019.07.30

**Changed**

* Pingpong: Exchange the 1P and 2P side
* Code refactoring

### [Beta 3.1] - 2019.05.28

**Changed**

* Pingpong: Set the height of the platform from 10 to 30
* Optimize the collision detection algorithm

### [Beta 3.0] - 2019.05.22

**Added**

* 2P game "pingpong"

**Changed**

* Optimize the call stack message of ml process
* Use `argparse` instead of `optparse`

### [Beta 2.2.2] - 2019.04.15

**Fixed**

* The game doesn't wait for the ready command

### [Beta 2.2.1] - 2019.04.12

**Fixed**

* The game hangs when the exception occurred before `ml_ready()`

**Changed**

* Some code refactoring and optimization

### [Beta 2.2] - 2019.04.01

**Added**

* `-i` and `--input-script` for specifying the custom ml script

### [Beta 2.1.1] - 2019.03.21

**Added**

* Print the whole call stack when the exception occurred

### [Beta 2.1] - 2019.03.18

**Fixed**

* Quit the game automatically when an exception occurred

**Added**

* `-1` and `--one-shot` for the one shot mode in ml mode
* Version message

### [Beta 2.0] - 2019.02.27

**Changed**

* Use function call instead of class instance to invoke use code
* Optimize the collision detection algorithm
* Increase the difficulty of the game "arkanoid"

**Added**

* `-r` and `--record` to record the game progress
