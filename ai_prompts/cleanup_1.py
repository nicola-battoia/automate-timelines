CLEANUP_TRANSCRIPT = """
You will be analyzing a long-form podcast interview transcript to extract the most valuable, interesting, and emotionally resonant segments. Your goal is to identify and preserve approximately 50% of the content while removing filler, repetitive content, and less interesting portions.

First, here is additional context about the podcast show, host, and guest:

<context>
{context}
</context>

Here is the full podcast transcript you will analyze:

<transcript>
{transcript}
</transcript>

The transcript follows this format:
- Timestamps in format HH:MM:SS,mmm --> HH:MM:SS,mmm
- Speaker names in brackets [Name]
- Spoken text following the speaker identification

Your task is to identify segments worth keeping based on these criteria:

KEEP segments that contain:
- Unique insights, stories, or perspectives
- Emotional moments (vulnerability, excitement, passion, humor)
- Key revelations or important information
- Memorable anecdotes or examples
- Moments of genuine connection between speakers
- Surprising or thought-provoking statements
- Practical advice or actionable takeaways
- Turning points in the conversation

REMOVE segments that contain:
- Filler words and phrases without substance
- Repetitive content or restating of previous points
- Overly long setup without payoff
- Small talk that doesn't lead anywhere meaningful
- Technical difficulties or off-topic tangents
- Excessive hedging or meandering thoughts
- Generic statements that could apply to any conversation

Before providing your selections, use the scratchpad to:
1. Read through the entire transcript
2. Identify the main themes and high-value moments
3. Note which sections are filler or low-value
4. Ensure your selections will result in approximately 50% of the original content

<scratchpad>
[Your analysis here]
</scratchpad>

Now provide your clip selections. Each selection should be output as a JSON object matching this structure:

{{
  "start": "HH:MM:SS,mmm",
  "end": "HH:MM:SS,mmm",
  "transcript_text": "The exact text from the transcript for this segment",
  "notes": "Brief explanation of why this segment is valuable"
}}

Guidelines for your output:
- Use the EXACT timestamp format from the transcript (HH:MM:SS,mmm)
- Include the complete transcript text for each selected segment, including speaker names
- Keep segments contiguous when possible (combine adjacent valuable moments)
- Your notes should be concise (1-2 sentences) explaining the value
- Aim for your total selected segments to represent approximately 50% of the original transcript length

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

Remember: Be selective and aim to cut approximately 50% of the content while preserving all the most valuable and interesting moments.
"""
