HOOK_FINDER = """
You will be analyzing a podcast interview transcript to identify powerful, emotional, or compelling phrases that would work as opening hooks for a trailer. Your goal is to find moments where the guest shares something unexpected, controversial, deeply emotional, or reveals a personal struggle or realization.

Here is the transcript to analyze:

<transcript>
{transcript}
</transcript>

Good trailer hooks have these characteristics:
- Unexpected takes or perspectives on familiar topics
- Controversial truths or bold statements
- Deeply emotional or vulnerable moments
- Personal struggles or challenges shared openly
- Profound realizations or lessons learned
- Surprising revelations or confessions
- Powerful declarations or commitments

Important constraints:
- Each clip must be between 5 to 9 seconds long when spoken aloud
- The clip should be a complete thought or phrase that makes sense on its own
- You can make cuts within the transcript to extract just the powerful moment
- Focus on what the GUEST says, not the interviewer

Your output must follow this Pydantic data class structure:

```
class ClipSelection(BaseModel):
    start: str  # Format: "HH:MM:SS,mmm" (e.g., "01:23:48,320")
    end: str    # Format: "HH:MM:SS,mmm" (e.g., "01:23:53,639")
    transcript_text: str  # Exact text from the transcript
    notes: str  # Brief explanation of why this works as a hook
```

Here is an example of a good selection:

{{
  "start": "01:21:32,954",
  "end": "01:21:40,000",
  "transcript_text": "[Hwei]I used to think that my existence is to be of use by others, is to lose my shapes and forms and then putting myself down to the dust.",
  "notes": "Deeply vulnerable admission about past self-worth issues - emotionally powerful and relatable struggle"
}}

Before providing your final output, use a scratchpad to work through the transcript:

<scratchpad>
- Read through the entire transcript carefully
- Identify moments of high emotional intensity, vulnerability, controversy, or surprise
- For each potential clip, estimate if it's 5-9 seconds when spoken
- Note the exact start and end timestamps
- Verify the text is compelling enough to hook a viewer
- Ensure each clip can stand alone and make sense out of context
</scratchpad>

After your analysis, provide your final answer with all the clips you've identified. Format each clip as a JSON object following the Pydantic structure shown above. Include as many strong clips as you can find - aim to identify at least 5-10 powerful moments if the transcript contains them.

Write your complete output inside <clips> tags, with each clip as a separate JSON object.
"""
