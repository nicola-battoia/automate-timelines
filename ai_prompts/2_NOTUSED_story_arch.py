STORY_ARCH = """
You will be analyzing a podcast interview transcript to create a structured narrative for a 90-second trailer. Your goal is to identify the most compelling moments and organize them into a cohesive short-form story that will engage potential listeners.

Here is the transcript you will be analyzing:

<transcript>
{TRANSCRIPT}
</transcript>

The transcript is structured as a series of segments, where each segment contains:
- start: timestamp when the segment begins
- end: timestamp when the segment ends
- transcript_text: the dialogue between speakers
- notes: summary or key insights from that segment

Your task is to analyze this transcript and extract the following elements:

1. **Narrative**: Identify the overarching story or journey being discussed
2. **Key Points**: Find the main topics, themes, or arguments presented
3. **Lessons**: Extract actionable insights, wisdom, or takeaways
4. **Story Boundaries**: Identify compelling beginnings and endings of stories within the interview
5. **High-Retention Moments**: Find cliff-hangers, emotional revelations, surprising facts, or highly useful tips that would hook listeners

Use the scratchpad below to think through your analysis:

<scratchpad>
- Read through the entire transcript and identify the main narrative arc
- Note segments with high emotional content or surprising revelations
- Identify practical tips or wisdom that would resonate with listeners
- Look for natural story beginnings and climactic endings
- Consider which moments would create curiosity or suspense
- Think about how to structure these elements into a 90-second narrative flow
</scratchpad>

Now provide your analysis in the following structured format:

<analysis>

<narrative>
Describe the overarching narrative or journey in 2-3 sentences. What is the main story being told in this interview?
</narrative>

<key_points>
List 3-5 main topics or themes discussed, with their timestamps:
- [Point 1 with timestamp]
- [Point 2 with timestamp]
- etc.
</key_points>

<lessons>
List 2-4 key lessons or takeaways, with their timestamps:
- [Lesson 1 with timestamp]
- [Lesson 2 with timestamp]
- etc.
</lessons>

<story_moments>
Identify 2-3 complete story arcs with clear beginnings and endings:
- Story 1: [Beginning timestamp] to [End timestamp] - Brief description
- Story 2: [Beginning timestamp] to [End timestamp] - Brief description
- etc.
</story_moments>

<high_retention_moments>
List 4-6 moments with high engagement potential (emotional, surprising, or highly useful), with timestamps and why they're compelling:
- [Timestamp]: Description and reason for inclusion
- [Timestamp]: Description and reason for inclusion
- etc.
</high_retention_moments>

</analysis>
"""