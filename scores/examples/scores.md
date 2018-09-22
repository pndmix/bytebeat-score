# ByteBeat Scores
| NAME | FORMULA | RATE[Hz] | TIME[sec] |
| :--- | :--- | :---: | :---: |
| [melody.wav](melody.wav) | t*((3+(1^t>>10&5))*(5+(3&t>>14)))>>(t>>8&3) | 8000 | 30 |
| [bass.wav](bass.wav) | (t*5)^t/30^t*7 | 8000 | 30 |
