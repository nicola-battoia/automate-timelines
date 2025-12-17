CLIFFHANGER_FINDER = """
You will be analyzing a podcast transcript to identify compelling cliffhanger moments that can be used in a podcast trailer. Your goal is to find segments that create curiosity and motivate listeners to watch the full episode.

Here is the podcast transcript to analyze:

<transcript>
{transcript}
</transcript>

A great cliffhanger moment has one or more of these qualities:
- Poses an intriguing question that isn't immediately answered
- Teases a surprising revelation or counterintuitive insight without fully revealing it
- Introduces a dramatic story or anecdote at a moment of tension or uncertainty
- Hints at valuable information, strategies, or secrets that will be explained later
- Creates a "wait, what?" moment that makes the listener want to know more
- Presents a bold or controversial statement that demands further context
- Sets up a transformation, result, or outcome without explaining how it happened

As you analyze the transcript, look for moments where the guest or host:
- Begins telling a compelling story but hasn't reached the resolution
- Makes a surprising claim that needs explanation
- Asks a thought-provoking question
- Alludes to an important lesson or insight without fully explaining it
- Describes a problem or challenge before revealing the solution
- Shares the beginning of a transformation or journey

Avoid selecting moments that:
- Fully answer the question or complete the thought
- Are too vague or lack context to be intriguing
- Require too much prior knowledge to understand
- Are purely informational without emotional or curiosity-driven appeal

For each cliffhanger you identify, you will output it in the following JSON format:

```
class ClipSelection(BaseModel):
    start: str  # Format: "HH:MM:SS,mmm" (e.g., "01:23:48,320")
    end: str    # Format: "HH:MM:SS,mmm" (e.g., "01:23:53,639")
    transcript_text: str  # Exact text from the transcript
    notes: str  # Brief explanation of why this works as a cliffhanger
```

In your notes field, specifically explain:
- What question or curiosity this moment creates
- Why a listener would want to hear more
- What makes this an effective trailer ending

Find as many strong cliffhanger moments as you can throughout the transcript. These will be used to end the podcast trailer, so prioritize moments with maximum curiosity-driving power. Aim to identify at least 10 cliffhangers if the transcript is substantial enough.

Output each cliffhanger as a separate JSON object. Begin your response with your cliffhanger findings immediately.
"""
