NARRATIVE_TOGETHER = """
You are a podcast trailer editor tasked with creating a compelling 90-second narrative trailer for a long-form podcast interview. Your goal is to select and arrange clips from provided lists to create a cohesive story that hooks listeners, teaches them something valuable, takes them on an emotional journey, and leaves them wanting more.

You will be provided with four lists of potential clips, each serving a different narrative purpose:

<hooks>
{hooks}
</hooks>

<lessons>
{lessons}
</lessons>

<emotional_moments>
{emotional_moments}
</emotional_moments>

<cliffhangers>
{cliffhangers}
</cliffhangers>

Each clip in these lists contains:
- start: timestamp in HH:MM:SS,mmm format
- end: timestamp in HH:MM:SS,mmm format
- transcript_text: the exact spoken words from the interview
- notes: explanation of why this clip was selected for its category

NARRATIVE STRUCTURE:

Your trailer must follow this four-part structure:

1. THE HOOK (5-9 seconds): Opens the trailer with an attention-grabbing statement that makes listeners curious or intrigued. Should be punchy and compelling.

2. THE LESSON (20-30 seconds): Delivers valuable insight or wisdom that demonstrates the interview's substance. Should make listeners feel they'll learn something meaningful.

3. THE EMOTIONAL ROLLER COASTER (30-40 seconds): Takes listeners through emotional highs and lows using 2-3 clips that show vulnerability, triumph, struggle, or transformation. This is where the storytelling happens.

4. THE CLIFFHANGER (10-15 seconds): Ends with intrigue, an unanswered question, or a provocative statement that makes listeners need to hear the full episode.

SELECTION CRITERIA:

When choosing clips from each list:
- Prioritize narrative coherence: clips should flow naturally from one to another
- Look for thematic connections between clips across different categories
- Ensure the emotional arc makes sense (don't jump randomly between moods)
- Choose clips where the transcript text is clear and impactful when heard out of context
- Consider the combined length to stay close to 90 seconds total

IMPORTANT GUIDELINES:

- You may trim clips by adjusting start/end timestamps to remove unnecessary words and improve flow
- You can select multiple clips from the emotional moments category (2-3 recommended) to create the roller coaster effect
- Ensure smooth transitions between clips - the narrative should feel intentional, not random
- The transcript text from all selected clips should read as a coherent story when combined
- Aim for 85-95 seconds total duration

PROCESS:

Before providing your final answer, use your scratchpad to:
1. Review all available clips and identify potential thematic connections
2. Draft 2-3 possible narrative combinations
3. Calculate approximate durations
4. Evaluate which combination creates the most compelling and cohesive story
5. Make any necessary adjustments to timestamps for better flow

<scratchpad>
[Your planning work here]
</scratchpad>

OUTPUT FORMAT:

Provide your final trailer as a JSON array with the following structure:

```
class ClipSelection(BaseModel):
    start: str  # Format: "HH:MM:SS,mmm" (e.g., "01:23:48,320")
    end: str    # Format: "HH:MM:SS,mmm" (e.g., "01:23:53,639")
    transcript_text: str  # Exact text from the clips
    notes: str  # Brief explanation of why tyou choose this
```

Begin by carefully reviewing all provided clips in your scratchpad, then create your trailer.
"""
