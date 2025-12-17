EMOTIONS_FINDER = """
You will be analyzing a podcast transcript to identify compelling emotional moments that could be used to create a ninety-second trailer with a storytelling arc. Your goal is to find clips that showcase emotional ups and downs, creating an "emotional roller coaster" effect.

Here is the podcast transcript you will be analyzing:

<transcript>
{transcript}
</transcript>

Your task is to identify and extract segments from this transcript that contain strong emotional moments. You are looking for:

**Emotional Ups (positive moments):**
- Exciting revelations or breakthroughs
- Moments of joy, laughter, or celebration
- Inspiring or uplifting statements
- Triumphant moments or victories
- Hopeful or optimistic expressions

**Emotional Downs (vulnerable/challenging moments):**
- Sad or melancholic reflections
- Vulnerable confessions or admissions
- Moments of struggle, difficulty, or pain
- Expressions of fear, anxiety, or worry
- Disappointing or challenging revelations

**Emotional Transitions:**
- Moments where the emotion shifts dramatically
- Surprising twists or revelations
- Reflective or contemplative moments that bridge different emotions

For each clip you identify, you should:
1. Select segments that are 10-30 seconds long when spoken (roughly 2-6 sentences)
2. Choose moments with clear, strong emotional content
3. Ensure the text is coherent and can stand somewhat independently
4. Aim for variety across different emotional tones
5. Look for moments with vivid language, personal stories, or powerful statements

Before providing your final output, use the scratchpad to think through your analysis:

<scratchpad>
- Read through the transcript and note timestamps where emotional shifts occur
- Identify the strongest emotional moments (both ups and downs)
- Consider how these moments could work together to create a narrative arc
- Ensure you have a good balance of different emotional tones
- Verify that each selected clip has clear start/end times and captures a complete thought
</scratchpad>

In the "notes" field, you must specify:
- The emotional tone (e.g., "Emotional Up - Joy", "Emotional Down - Vulnerability", "Transition - Reflective")
- Why this moment is compelling for the trailer
- How it might fit into a storytelling arc

Your final output should be a JSON array containing all selected clips, ordered by their appearance in the transcript. Aim to identify 8-15 strong clips that together could create a compelling emotional journey.

Now provide your selected clips in the following JSON format. Each clip should follow this exact structure:

Your output must follow this Pydantic data class structure:

```
class ClipSelection(BaseModel):
    start: str  # Format: "HH:MM:SS,mmm" (e.g., "01:23:48,320")
    end: str    # Format: "HH:MM:SS,mmm" (e.g., "01:23:53,639")
    transcript_text: str  # Exact text from the transcript
    notes: str  # Brief explanation
```

"""
