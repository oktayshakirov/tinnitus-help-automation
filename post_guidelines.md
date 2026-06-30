# Tinnitus Help — Post Writing Guidelines

Write a comprehensive, SEO-optimized, E-E-A-T blog post. Output ONLY the Markdown body (no frontmatter — it is generated separately), followed by the required JSON block.

## Structure
Pick the natural flow for the topic (5–8 sections):
- **"What is…"**: Definition → Symptoms → Causes → Diagnosis → Management → Conclusion
- **"How to…"**: Intro → Why it matters → Steps → Common mistakes → When to seek help → Conclusion
- **"X and Tinnitus"**: Intro → Connection → Mechanisms → Management → Conclusion
- **Question**: Question → Short answer → Factors → Management → Conclusion

Add contextual sections as useful (Myths, Risk Factors, When to See a Doctor, Sample Day).

## Length & components
- **1,200–2,500 words.**
- `<Blockquote>` right after the start: 2–3 sentence summary.
- `<Highlighter>Section Title</Highlighter>` for every main heading.
- `<AdComponent />` 2–3 times (after a major section, mid-post, before conclusion).
- Exactly **2 `<Image>`** (see Images).
- Markdown tables for comparisons/data. **Bold** key terms on first mention.
- End with a `<Highlighter>Conclusion…</Highlighter>` section (2–3 paragraphs, encouraging, 1–2 natural next-step links).

## Internal linking (STRICT)
- **8–15 links total. Link each page AT MOST ONCE. Never repeat a link or force one** — link only where it genuinely helps the reader.
- Natural, in-sentence format: `**[managing tinnitus](/blog/managing-tinnitus)**`. Never "see our guide on…".
- Use ONLY slugs from the provided databases. Format: blog → `/blog/{slug}`, zen → `/zen/{slug}`, app → `/app`.
- Distribute across the post; max one link per sentence.
- Good targets: core concepts (what-is-tinnitus, brain/neural), related conditions (stress, sleep, anxiety), management (managing-tinnitus, white-noise, CBT), sound therapy (zen sounds), the app for tracking.

## Images (use the real archive)
Insert exactly **2** `<Image>` in the body — one after the first main section, one before the conclusion. Choose filenames **ONLY from the Available Body Images list below** (do NOT invent names). Pick images that fit the section's topic.
Format: `<Image src="/images/FILENAME.jpg" alt="Descriptive, tinnitus-relevant alt text." />`
The main (frontmatter) image is chosen manually later — ignore it.

**Available Body Images:** airpods, airpods-2, alcohol-smoking, anxiety, anxiety-girl, apple-hearing-test, astronaut, audiologist, bird, brain-research, bull, cardiologist, cat, cbd-oil, cbd-oil-woman, celebrity, celebrity2, crowd, daily-routines, depressed-man, digital-art, digital-devices, doctor, drinking-water, evening-routine, fire, fruits, future-technology, gamer, genetics, girl-with-headphones, girl-with-headphones2, happy, happy-girl, headphones, headphones-2, health-app, health-app-2, healthy-diet, jaw-female, jungle, leopard, live-music-show, meditation, megaphone-noise, morning-routine, mother-daughter, musician, neck-tension, neurons, relaxing-woman, research, screaming-man, seasonal-tinnitus, seasonal-tinnitus-2, silence, sleeping-kid, sleeping-woman, stress-tinnitus-man, stress-tinnitus-woman, stressometer, therapy, therapy-2, tinnitus-arts, tinnitus-digital-age, tinnitus-history, tinnitus-history2, tinnitus-military-veterans, tinnitus-military-veterans2, tinnitus-myths-reality, tinnitus-pandemic, tinnitus-pandemic2, tinnitus-wildlife, traveling, van-gogh, van-gogh-starry-night, waterfall-man, woman-and-sunflowers, working-out-female, working-out-male, yoga-dog, young-listening-music, young-tinnitus, zen-nature, zen-white

## Writing standards
- Open with 2–3 short paragraphs (no bullet list): a relatable scenario or question hook, acknowledge the reader's situation, state what they'll learn. Include one natural link.
- Address the reader as "you". Empathetic, hopeful, realistic, expert but accessible. Vary sentence length; avoid filler ("In conclusion", "Furthermore").
- Use specific numbers when available ("15–20% of adults") over vague terms. Acknowledge limited evidence honestly ("some research suggests", "may help").
- Recommend consulting professionals for medical decisions; include a "When to seek help" angle for medical topics. No cure promises.
- Balance narrative with lists/tables — always wrap lists in explanatory prose.

## Do NOT include
External links, a References/Further-reading/bibliography section, or any closing "related articles" list (links go inline). No frontmatter, no `featured` flag.

## Final JSON (after the post)
```json
{
  "tags": ["nutrition", "management", "research"],
  "description": "150–160 char description, specific with a unique differentiator (not generic)."
}
```
- **tags: exactly 2–3**, lowercase, ONLY from: `basics, management, research, psychology, nutrition, meditation, sounds`.
- **description: exactly 150–160 characters.**
