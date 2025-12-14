"""Prompt templates used across the workflow."""

ORCHESTRATOR_PROMPT = """
You will analyze a podcast transcript to identify and extract 3-4 compelling segments that can be used to create a 2-minute teaser introduction for the episode. Your goal is to select segments that will hook listeners and motivate them to listen to the full episode.

## Input Materials

First, here is additional context about the podcast show, host, and guest:

<context>
{context}
</context>

Here is the full podcast transcript you will analyze:

<transcript>
{transcript}
</transcript>

The transcript follows this format:
- Each segment begins with a line containing two timestamps: start time --> end time (format: HH:MM:SS,mmm)
- The speaker's name appears in square brackets on the same line as the timestamps
- The spoken text appears on the following line(s)

Example:
```
00:00:16,640 --> 00:00:18,820 [John]
and I really look forward to our good

00:00:18,860 --> 00:00:19,900 [John]
conversation today.
```

## Your Task

Select 3-4 specific segments from the transcript that will work best as teaser content for a 2-minute podcast introduction. The combined duration of your selected segments should total approximately 120 seconds or less.

## What Makes a Great Teaser Segment

Select segments that accomplish one or more of these goals:

1. **Hook listeners immediately** - Surprising, intriguing, or dramatic statements that grab attention
2. **Create cliffhangers** - Incomplete thoughts, questions raised without answers, stories that build tension
3. **Showcase compelling content** - Revelations, insights, emotional moments, demonstrations of expertise, unique perspectives
4. **Generate curiosity** - Statements that make listeners want to know more

## Selection Criteria

Prioritize segments with these qualities:
- Surprising revelations or unexpected insights
- Emotional or dramatic moments
- Statements that raise intriguing questions without providing complete answers
- Moments that demonstrate the guest's unique expertise or perspective
- Story beginnings that create suspense
- Controversial or thought-provoking statements

## Analysis Process

Before providing your final output, work through your analysis in <segment_analysis> tags. In this section:

1. **Parse the transcript format**: Confirm you understand the timestamp format (HH:MM:SS,mmm) and speaker labels so you can accurately extract segments

2. **Scan for potential segments**: Go through the transcript and identify potential teaser segments. For each one, write out:
   - The start timestamp
   - The end timestamp
   - The exact text verbatim from the transcript
   
   It's OK for this section to be quite long - take your time to identify all promising candidates.

3. **Evaluate each candidate**: For each potential segment you identified, systematically assess it against the four main criteria. Be explicit:
   - Does it hook listeners immediately? (Answer yes or no, then explain why)
   - Does it create cliffhangers? (Answer yes or no, then explain why)
   - Does it showcase compelling content? (Answer yes or no, then explain why)
   - Does it generate curiosity? (Answer yes or no, then explain why)

4. **Calculate durations**: For each promising segment, calculate the duration in seconds. Show your work:
   - Convert start timestamp to total seconds
   - Convert end timestamp to total seconds
   - Subtract to get duration
   - Example: 00:01:30,000 = (0*3600) + (1*60) + 30 = 90 seconds

5. **Consider combinations**: Think about how different segments might work together as a cohesive teaser that flows well and creates a compelling narrative arc

6. **Verify total timing**: Add up the durations of your candidate segments step-by-step, showing the math (e.g., "Segment 1: 25 seconds + Segment 2: 18 seconds + Segment 3: 32 seconds = 75 seconds total"). Ensure the total is approximately 120 seconds or less

7. **Make final selection**: Choose your final 3-4 segments that work best together, meet the timing constraint, and maximize teaser impact

Take your time with this analysis section - it's important to thoroughly review the entire transcript and show your reasoning.

## Output Format

After completing your analysis, provide your final selection as a JSON array. Each object in the array should represent one selected segment with these exact fields:

- `start`: Start timestamp in 'HH:MM:SS,mmm' format (e.g., "01:23:48,320")
- `end`: End timestamp in 'HH:MM:SS,mmm' format (e.g., "01:23:53,639")
- `transcript_text`: The exact text from the transcript for this segment
- `notes`: A brief explanation of why you selected this segment

Output your final selection in <clips> tags in this format

# ClipsList
## ClipSelection 1
    - "start": "HH:MM:SS,mmm",
    - "end": "HH:MM:SS,mmm",
    - "transcript_text": "exact text from transcript",
    - "notes": "brief explanation of teaser value"
## ClipSelection 2
    - "start": "HH:MM:SS,mmm",
    - "end": "HH:MM:SS,mmm",
    - "transcript_text": "exact text from transcript",
    - "notes": "brief explanation of teaser value"
]
```

Include 3-4 objects in your response depending on how many segments best fit within the 2-minute constraint while maximizing teaser impact.

## Important Reminders

- Extract timestamps and text exactly as they appear in the transcript
- Ensure your selected segments combine to approximately 120 seconds or less
- Your JSON output should contain only your final selections, not any of the analysis work
- Make sure your JSON is valid and properly formatted
"""
