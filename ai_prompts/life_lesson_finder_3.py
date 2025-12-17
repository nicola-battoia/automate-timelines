LIFE_LESSON_FINDER = """
You are tasked with analyzing a podcast transcript and your goal is to find segments that contain actionable life lessons, practical tips, memorable quotes, or valuable insights that would make a listener think "Wow, I didn't know that" or "That's really useful for my life."

Here is the podcast transcript to analyze:

<transcript>
{transcript}
</transcript>

Your task is to identify clips that would win the trust of potential listeners by showcasing the most helpful and juicy information from the podcast. Look for segments that contain:

- **Actionable quotes or mental models**: Wisdom the guest or host shares about getting through tough moments, making decisions, or approaching life challenges
- **Practical tools and techniques**: Specific methods, frameworks, or strategies that listeners can immediately apply
- **Problem-cost-solution examples**: Clear explanations where the guest identifies a problem, explains what it costs people, and provides a concrete solution
- **Expert tips and insights**: Valuable information that demonstrates expertise and provides genuine value
- **Memorable one-liners**: Quotable moments that people would want to share with others

**What to look for:**
- Concise, self-contained segments (suitable for 90-second clips)
- Moments where the guest is teaching or giving away valuable information
- Content that feels like a "free gift" of knowledge to the listener
- Insights that are specific and actionable, not vague or generic

**What to avoid:**
- Long backstory or biographical information without lessons
- Vague platitudes without actionable content
- Inside jokes or references that require full episode context
- Promotional content or advertisements

Before providing your final selections, use the scratchpad below to think through potential clips:

<scratchpad>
- Review the transcript and note timestamps where valuable lessons appear
- Evaluate each potential clip: Is it actionable? Is it memorable? Would it make someone want to listen to the full episode?
- Consider whether each segment is self-contained enough for a trailer
- Prioritize the most impactful and valuable moments
</scratchpad>

Now provide your selected clips in the following format. Each clip should be a separate JSON object with this exact structure:

{{
  "start": "01:21:32,954",
  "end": "01:21:40,000",
  "transcript_text": "[Hwei]I used to think that my existence is to be of use by others, is to lose my shapes and forms and then putting myself down to the dust.",
  "notes": "Deeply vulnerable admission about past self-worth issues - emotionally powerful and relatable struggle"
}}

Present your selections inside <clips> tags, with each clip as a properly formatted JSON object. Include as many clips you can find, depending on how much valuable content is present in the transcript.
"""
