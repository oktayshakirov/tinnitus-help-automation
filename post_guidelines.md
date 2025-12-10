# AI Post Writing Guidelines for Tinnitus Help

## Structure (Flexible 5-8 Core Sections)

**Common Post Types:**

- **"What is..."** (Explanatory): Definition → Symptoms → Causes → Diagnosis → Treatment/Management → Conclusion
- **"How to..."** (Tutorial): Introduction → Why it matters → Step-by-step strategies → Best practices → When to seek help → Conclusion
- **"Tinnitus and..."** (Relationship/Connection): Introduction → Connection explanation → Mechanisms → Management strategies → Conclusion
- **Question-based** (e.g., "Does tinnitus go away?"): Question → Answer overview → Types/context → Factors → Management → Conclusion

**FLEXIBILITY**: Add contextual sections as needed (e.g., "Research and Future Outlook", "Common Myths", "When to See a Doctor", "Risk Factors").

For **"How to..."** and beginner-focused guides, aim for this typical flow:

- **Engaging introduction (2–3 paragraphs)** – relatable scenario, acknowledge reader concerns, set expectations
- **Why this matters / stakes** – what can go wrong or what value is unlocked (presented as flowing paragraphs)
- **Core concepts / basics** – minimal theory needed to understand the steps (explained in narrative form with context)
- **Step‑by‑step / practical section** – clear actions presented as narrative walkthroughs, not numbered lists. If brief checklists are needed, embed them within paragraphs with context
- **Common mistakes / troubleshooting** – show, don't just tell, how things go wrong in practice (integrated into paragraphs, not as separate bullet lists)
- **Conclusion** – reinforce key takeaways, build confidence, and suggest safe next steps (2-3 paragraphs, not bullet points)

## Content Requirements

- **Length**: 1,200-2,500 words
- **Internal Links**: 8-15 total, flowing naturally throughout content
- **Images**: Exactly 2 with descriptive alt text using `/images/` paths
  - Cover image: Immediately after `<Blockquote>` (matches frontmatter `image` field)
  - Second: Before conclusion or after practical sections
- **Special Components**: `<Blockquote>` (2-3 sentence summary) → cover image → content → `<AdComponent />` (2-3 times) → conclusion

## Internal Linking (ALWAYS USE NATURAL FORMAT)

**MANDATORY FORMAT**: Links should flow naturally in sentences, NOT forced phrases like "see our guide on..."

**DO Link When:**

- Core concepts at first mention: "understanding **[tinnitus](/blog/what-is-tinnitus)**"
- Related educational content when naturally connecting: "If you're new to tinnitus management, our **[managing tinnitus](/blog/managing-tinnitus)** guide..."
- Practical guides in context: "Learn more: **[How Audiologists Diagnose and Treat Tinnitus](/blog/how-audiologists-diagnose-and-treat-tinnitus)**"
- Related conditions/topics: "linked to **[stress and anxiety](/blog/tinnitus-and-stress)**"
- Sound therapy resources: "explore our **[Zen sound library](/zen)**" or "try **[white noise](/zen/white-noise)**"
- Management strategies: "effective **[sound therapy](/blog/the-power-of-white-noise)**"
- When referencing specific sections: "common **[causes of tinnitus](/blog/what-is-tinnitus#what-causes-tinnitus-uncovering-the-roots)**"

**DON'T Link:**

- Every mention of common terms (only when it adds value)
- With forced phrases like "see our guide on..." - let links flow naturally
- Multiple links in the same sentence
- As keyword stuffing or when it interrupts reading flow
- Repeated linking to same page (once per major section is enough)

**Link Validation:**

- ONLY use links from provided database (blog posts, zen sounds)
- Database format: `key|slug|title` - use exact slug from database
- **Blog Posts**: **[Title](/blog/{slug})**
- **Zen Sounds**: **[Sound Name](/zen/{slug})**
- **App**: **[our app](/app)** or **[tinnitus relief app](/app)**

## Article Formatting & Structure

**CRITICAL: Prefer paragraphs over bullet lists** (bullets ONLY for quick reference like comparison tables)

- Convert nested/numbered lists into narrative paragraphs with **bold** category headers (e.g., **Vascular causes**, **Pressure-related factors**)
- Group related info into cohesive paragraphs with transitions
- Start sections with context before technical details
- Integrate action items into prose, not standalone bullets

**Example**: ❌ "• Hypertension: optimize blood pressure" → ✅ "If hypertension is the culprit, optimizing blood pressure, cholesterol, and lifestyle changes can help."

**AVOID**: Long nested lists, lists without context, technical jargon without explanation, abrupt shifts, dry list-heavy sections  
**PREFER**: Flowing paragraphs, context before details, smooth transitions, engaging readable prose

## Writing Standards

**Voice & Tone**: Conversational, accessible, empathetic. Use "you"/"your" to address readers directly. Acknowledge challenges while maintaining hope. Professional but warm. Use active voice, vary sentence length, avoid AI filler ("In conclusion", "Furthermore" - use sparingly).

**Content Quality**: Use exact numbers ("millions worldwide", "15-20%") not vague terms. Acknowledge evidence limitations ("some research suggests", "may help"). Include risk context naturally ("Always consult your healthcare provider..."). Explain "why" not just "what". Explain technical terms in context on first use, add brief context before introducing concepts.

**Engagement**: Use rhetorical questions sparingly to open sections. Leverage analogies for complex ideas. When lists/tables are needed, surround with narrative paragraphs explaining context. Combine honest challenges with reassurance that strategies can help. Validate reader's struggle.

## Tags Selection (MANDATORY - Use ONLY These Tags)

Choose 1-4 tags from this EXACT list (no other tags allowed):

basics, history, lifestyle, management, meditation, neuroscience, nutrition, psychology, research, society, sounds, technology

## Opening Style

Start with **2–3 paragraphs** (not bullets). Use at least one: relatable scenario, question hook, or context tied to tinnitus. Acknowledge reader's concerns, state what they'll learn and why it matters. Include ONE natural internal link. Avoid dense medical definitions—lead with connection, then explain.

**Required**: `<Blockquote>` (2-3 sentence summary) → cover image (matches frontmatter `image` field) → content

## Conclusion Style

MUST end with `## <Highlighter>Conclusion: [Phrase]</Highlighter>` or `## <Highlighter>Conclusion</Highlighter>`. Write **2–3 paragraphs** (not bullets): summarize takeaways in plain language, restate why it matters, reinforce hope/confidence that strategies can help. Suggest 1–2 practical next steps with natural internal links. End encouragingly.

## Frontmatter Requirements

**Title Formats:**

- "What is [Topic]?" or "What is [Topic]? A Comprehensive Guide"
- "How to [Action]" or "[Topic] and [Related Topic]"
- "Understanding [Topic]" or "[Topic] Explained"
- "[Topic]: [Subtitle]" for descriptive posts
- Question format for analytical posts (e.g., "Does Tinnitus Go Away?")

**Description (CRITICAL - EXACTLY 150-160 characters):**

- VERY SPECIFIC with unique differentiators (NOT generic)
- Formula: [Topic name] + [Key features/benefits] + [What readers learn] + [Audience optional]
- ❌ BAD: "Learn about tinnitus and how to manage it"
- ✅ GOOD: "Understand tinnitus — the perception of sound without an external source. Learn about symptoms, causes and treatments."
- ❌ BAD: "Stress management for tinnitus explained"
- ✅ GOOD: "Learn how stress can aggravate tinnitus and discover effective stress management techniques to alleviate its impact."

**Image**: `/images/{descriptive-name}.jpg` or `.png` (use descriptive, relevant image names)

**Tags**: Array of 1-4 relevant keywords (see Tag Generation section above)

**Date**: Use format 'Month DD, YYYY' (e.g., 'July 13, 2023')

**Featured** (Optional): Set to `true` for important/popular posts

## Special Formatting Requirements

**Headings**: `## <Highlighter>Section Title</Highlighter>` (always prefix with `##`)

**Components**:

- `<Blockquote>`: 2-3 sentence summary after frontmatter
- `<Image>`: `src="/images/image-name.jpg"` with descriptive alt text
- `<AdComponent />`: 2-3 times (after first section, midway, before conclusion)

**Bold**: Key terms on first mention, main category headers in paragraphs (NOT list items), table subheadings

**Tables**: Markdown format for comparisons (use **bold** for subheadings)

## Content Restrictions

**DO NOT**: References/bibliographies, external links (use internal from database only), closing "related articles" sections, cure promises, medical advice (always recommend consulting professionals), FAQ sections (answer naturally in content), excessive bullet lists

**DO**: "When to seek help" sections, healthcare disclaimers, research limitation acknowledgments, encouragement balanced with realism

## Final JSON Output (REQUIRED)

After writing the post, provide JSON:

```json
{
  "tags": ["tinnitus", "anxiety", "meditation"],
  "description": "Learn how stress can aggravate tinnitus and discover effective stress management techniques to alleviate its impact."
}
```

**Requirements:**

- **Tags**: Use the Tags from Tags Selection
- **Description**: EXACTLY 150-160 characters, SPECIFIC with unique differentiator
