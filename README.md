# AI-Powered Video Timeline Automation

Shorts and reels are a necessary evil of our age. You have an amazing 2 hours long podcast, great. But if you want more people than your aunt to see it, you need a dopamine kicker teaser. 
Now, going from those 2 hours to 150 seconds is a pain in the ass. 

But hey, it's 2025. The year of AI magically solve our life problems. 
So, everyone is selling you the magic pill "1 long video, 10 viral clips. Create 10x faster."

I tried those and I don't like them. 

They kind of work, get you some 60% there. But when you try to finish that 40% it becomes a nightmare. 

In this project, I'll show you how you can delete the boring part to AI: find good clips. And then you take control, import it directly to Davinci Resolve and do your magic there. 

High quality videos, full control, fast e free. 

If you're up for it, let's get going

## Main steps

1. Starting point: transcript of your long form video with timestamps
2. Call to an AI model to select the clips for a 120s video *fully custom prompt*
3. Create a .otio timeline you can import in your editing SW directly.

## What you need to do

### inputs to change in `1-long-short.py``

1. Paste your OPENAI_API_KEY in .env
2. Place the transcription file of the video in `transcripts`
3. Set the name in `TRANSCRIPT_FILE_NAME`
4. Write the context of your long form video in `CONTEXT` (optional)
5. Set the frames per second of the video you're using in `FPS`
6. Set the paths of the videos you're using in `MEDIA_PATHS`. Can be as many as you want.
7. Write the name of the timeline in `TIMELINE_FILENAME`

# Building blocks

# AI calls 
folder `examples`

## Simple call to an AI model
-check `load-api-checks.py```

## Structured output
- check `0-structured-ouput.py`` and `0.2-structured-ouput-gemini.py``

### data models

how they work 
- check `data_models.py``

## orchestrator

# create timeline from timestamps

## convert the timestamps to fps

the transcript has hh:mm:ss,mmm. convert it to fps. 

Need a list of clips with starting frames and end frames

- check `utils.py`

## create timeline

with otio library it create the timeline that links the media sources. 





