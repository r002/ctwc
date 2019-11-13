# ctwc
This repo holds all coding projects related to the CTWC (Classic Tetris World Championships).  To start, I've uploaded the "CTWC Video Analyzer" project.

## Resources
Here is the YouTube link to all CTWC videos:  
https://www.youtube.com/channel/UC-8BAEcWSEs4-KQp1ULVnaQ/videos

Here is the Twitch link to CTWC's stream:  
https://www.twitch.tv/classictetris/videos/all

## Analyzer
To run the CTWC Video Analyzer:
```
C:\code\ctwc>python -m analyzer.runner
```

## Tasks
- Parse the score from a frame.
- Parse the next piece that's about to be dropped.
- Parse if a line clear is a single/double/triple/Tetris.


## Extra Notes
ROI = image[y1:y2, x1:x2]

In Part01, the first game starts at 2:12 (132,000 ms)
