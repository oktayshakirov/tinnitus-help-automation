# AI Post Writing Guidelines

## Structure (Flexible 5-8 Core Sections)

**Common Post Types:**

- **"What is..."** (Explanatory): Definition → How it works → Use cases → Conclusion
- **"How to..."** (Tutorial): Introduction → Step-by-step → Best practices → Conclusion
- **Educational/Topical**: Introduction → Main concepts → Examples → Practical considerations → Conclusion

**FLEXIBILITY**: Add contextual sections as needed (e.g., "Security Considerations", "Future Outlook", "Comparison with Alternatives").

For **"How to..."** and beginner-focused guides, aim for this typical flow:

- **Engaging introduction (2–3 paragraphs)** – relatable scenario, acknowledge reader concerns, set expectations
- **Why this matters / stakes** – what can go wrong or what value is unlocked
- **Core concepts / basics** – minimal theory needed to understand the steps
- **Step‑by‑step / practical section** – clear actions, checklists supported by narrative
- **Common mistakes / FAQs / troubleshooting** – show, don’t just tell, how things go wrong in practice
- **Conclusion** – reinforce key takeaways, build confidence, and suggest safe next steps

## Content Requirements

- **Length**: 1,200-2,500 words
- **Internal Links**: 8-15 total, ALL using **[Text](/path)** bold format, flowing naturally
- **Images**: Exactly 2 with descriptive alt text using `/images/posts/` paths
  - First: After main concept or first major section
  - Second: Before conclusion or after practical sections
- **Formatting**: ## for main headings, **bold** for ALL sub-categories in bullet points
- **Tone**: Professional, educational, expert-level, E-E-A-T compliant, accessible to beginners when possible

## Internal Linking (ALWAYS USE BOLD FORMAT)

**MANDATORY FORMAT**: **[Text](/path)** NOT [Text](/path)

**DO Link When:**

- Core concepts at first mention: "understanding **[Bitcoin](/posts/what-is-bitcoin)**"
- Related educational content when naturally connecting: "If you're new to crypto, our **[crypto for beginners](/posts/crypto-for-beginners)** guide..."
- Practical guides in context: "Learn more: **[How to Buy Your First Cryptocurrency](/posts/how-to-buy-your-first-crypto)**"
- Technologies/protocols: "built on **[blockchain](/posts/what-is-blockchain)** technology"
- Exchanges when recommending: "purchase on **[Coinbase](/exchanges/coinbase)**"
- Crypto OGs when mentioned: "created by **[Vitalik Buterin](/crypto-ogs/vitalik-buterin)**"
- Comparisons: "Unlike **[Bitcoin](/posts/what-is-bitcoin)** which uses Proof-of-Work..."

**DON'T Link:**

- Every mention of common terms (only when it adds value)
- With forced phrases like "see our guide on..." - let links flow naturally
- Multiple links in the same sentence
- As keyword stuffing or when it interrupts reading flow
- Repeated linking to same page (once per major section is enough)

**Link Validation:**

- ONLY use links from provided database (crypto_ogs, posts, exchanges, tools)
- Database format: `key|slug|title` - use exact slug from database
- **Concepts**: **[Title](/posts/{slug})** | **Exchanges**: **[Exchange](/exchanges/{slug})** | **Crypto OGs**: **[Name](/crypto-ogs/{slug})** | **Tools**: **[Tool](/tools/{slug})**

## Writing Standards

- **Specific Numbers & Data**: Use exact numbers "200+ cryptocurrencies", "99.9% reduction", "2,700-4,000 TPS" - AVOID vague terms like "many", "most", "several"
- **Historical Context**: Include founding years, launch dates, key events with dates
- **Risk Context**: Include naturally when discussing features (e.g., "While leverage can amplify profits, it also increases potential losses")
- **Balanced Tone**: Acknowledge strengths AND weaknesses objectively (e.g., "Despite its impressive technology, Solana has faced significant challenges...")
- **Actionable Content**: Provide practical advice with context, explain "why" not just "what"
- **Natural Voice**: Vary sentence length, avoid AI-like filler ("In conclusion", "Furthermore" - use sparingly), write conversationally but professionally
- **Beginner-Friendly**: Explain technical terms on first use when concept is central, link to foundational content when appropriate
- **Concrete Examples & Mini Case Studies**: Where helpful (especially for security, scams, “how to”, and risk topics), include at least 2 short real-world scenarios or anonymized mini case studies that illustrate what happens when things go right vs. wrong.

### Narrative & Engagement

- **Directly address the reader**: Use “you”/“your” to speak to the reader and acknowledge their worries, curiosity, and goals.
- **Use rhetorical questions sparingly but effectively**: e.g., “Wondering why confirmations matter so much?” to open sections and guide attention.
- **Leverage analogies and metaphors**: Explain complex ideas with simple comparisons (e.g., “Think of sending crypto like sending a package—you need the exact address, the right carrier (network), and proper labeling (memo/tag)”).
- **Balance narrative and checklists**: Use bullet lists for clarity, but **always surround them with short narrative paragraphs** that explain why each step/section matters. Avoid posts that feel like pure checklists or manuals.
- **Encouraging, reassuring tone**: Especially for beginners and security topics, combine honest risk discussion with reassurance that, by following a clear process, the reader can act safely and confidently.

## Category Selection (MANDATORY - Use ONLY These Categories)

Choose 1-4 categories from this EXACT list (no other categories allowed):

- **Investing** – Investment strategies, trading, portfolio management
- **Beginners** – Introductory, foundational content for newcomers
- **Regulation** – Regulatory topics, legal frameworks, compliance
- **Bitcoin** – Bitcoin-specific content (only when Bitcoin is primary focus)
- **Adoption** – Mainstream adoption, institutional interest, real-world use cases
- **Blockchain** – Blockchain fundamentals, technology, infrastructure
- **Technology** – Technical explanations, protocols, innovations
- **Web3** – Web3, DeFi, NFTs, decentralized applications, metaverse
- **Predictions** – Future forecasts, trends, market predictions
- **Security** – Security practices, wallet safety, scam prevention
- **Politics** – Political impacts, government policies, elections affecting crypto
- **Sustainability** – Environmental impact, green crypto, energy consumption
- **Gaming** – GameFi, crypto gaming, play-to-earn
- **Nfts** – NFT-specific content, digital collectibles, tokenization
- **Ai** – AI-related crypto content, machine learning in blockchain

**Guidelines**: Choose 2-3 optimal categories, match to post's primary focus (not just mentioned terms), quality over quantity.

## Tag Generation

Generate 8-15 SEO-focused tags covering:

- Primary topic/asset (e.g., "Bitcoin", "Ethereum", "Altcoins")
- Technology/concept (e.g., "blockchain", "smart contracts", "DeFi", "NFTs")
- Action/use case (e.g., "crypto trading", "staking", "investing")
- Audience (e.g., "beginners", "investors", "traders")
- Related topics (e.g., "security", "wallets", "exchanges")

## Opening Style

**Effective Patterns:**

- **Engaging Hook**: "Solana has rapidly emerged as a significant player in the **[Blockchain](/posts/what-is-blockchain)** landscape, distinguished by its focus on high speed, scalability, and low transaction costs."
- **Definition & Significance**: "[Topic] is [definition]. It represents..." - Always include WHY it matters
- **Question Hook**: "Are NFTs dead? While the speculative frenzy has cooled, the underlying **[Blockchain](/posts/what-is-blockchain)** technology is far from obsolete."
- **Historical Context**: "Since [Bitcoin's launch in 2009](/posts/what-is-bitcoin)..." - Connect to current relevance

**Requirements**:

- Start with **2–3 short paragraphs**, not a bullet list.
- Use at least one of:
  - A **relatable scenario** (“You’ve just bought your first Bitcoin and want to send it to a friend…”),
  - A **question hook** (“Heard about Bitcoin but not sure where to start?”),
  - A **short context or historical hook** tied to today.
- Explicitly **acknowledge the reader’s situation and concerns** (e.g., anxiety about making mistakes, confusion as a beginner).
- Clearly state **what they will learn** and **why it matters now**.
- Include ONE natural internal link where it adds context (not forced).
- Avoid starting with dense warnings or raw definitions alone—lead with connection, then explain.

## Conclusion Style

- Every post MUST end with a **Conclusion section** using a clear heading, e.g., `## Conclusion: [Short Benefit-Oriented Phrase]` or `## Conclusion`.
- The conclusion should be **2–3 paragraphs**, not just a bullet checklist.
- Summarize the **key takeaways in plain language** and restate why the topic matters.
- **Reinforce confidence**: make it clear that by following the outlined concepts/steps, the reader can act more safely or make better decisions.
- Where relevant, suggest **1–2 practical next steps** (e.g., which related guide to read next, or what small action to take first), linking internally in a natural way.

## Frontmatter Requirements

**Title Formats:**

- "What is [Topic]?" or "What is [Topic]? A Beginner's Guide"
- "How to [Action]"
- "Understanding [Topic]" or "[Topic] Explained"
- "[Topic]: [Subtitle]" for descriptive posts
- Question format for analytical posts

**Description (CRITICAL - EXACTLY 150-160 characters):**

- VERY SPECIFIC with unique differentiators (NOT generic)
- Formula: [Topic name] + [Key features] + [What readers learn] + [Audience optional]
- ❌ BAD: "Learn about cryptocurrency and how it works"
- ✅ GOOD: "Bitcoin is the world's first cryptocurrency. Learn about its history, how it works, and why it's considered digital gold. Perfect for beginners looking to understand the foundation of the crypto world."
- ❌ BAD: "Understanding crypto taxes explained"
- ✅ GOOD: "How is crypto taxed around the world, including key concepts like taxable events, capital gains and best practices for keeping track of your transactions."

**Image**: `/images/posts/{descriptive-name}.jpg` or `.png`

**Categories**: Array of 1-4 from allowed list above

**Tags**: Array of 8-15 relevant keywords

**Crypto OGs (Optional)**: Only when founder/creator mentioned - use proper capitalization in frontmatter: "Satoshi Nakamoto", "Vitalik Buterin"

**Exchanges (Optional)**: Only when recommending services - use proper capitalization in frontmatter: "Coinbase", "Binance", "Kraken"

**IMPORTANT - Capitalization**:

- ALWAYS use proper capitalization for crypto-ogs and exchanges in BOTH frontmatter and content (e.g., "Satoshi Nakamoto", "Vitalik Buterin", "Coinbase", "Kraken", "Uniswap")
- This ensures consistency and readability across all articles

## Content Restrictions

**DO NOT Include:**

- References section at the end (e.g., "References for deeper learning", "Further reading", etc.)
- Bibliography or citation lists
- External links to other websites (only use internal links from provided database)
- Any closing sections that list related articles - links should be integrated naturally throughout the content

## Final JSON Output (REQUIRED)

After writing the post, provide JSON:

```json
{
  "tags": [
    "bitcoin",
    "cryptocurrency",
    "blockchain",
    "digital gold",
    "crypto investing",
    "crypto basics"
  ],
  "description": "Bitcoin is the world's first cryptocurrency. Learn about its history, how it works, and why it's considered digital gold. Perfect for beginners looking to understand the foundation of the crypto world.",
  "categories": ["Beginners", "Technology", "Blockchain", "Bitcoin"],
  "crypto_ogs": ["Satoshi Nakamoto"],
  "exchanges": ["Coinbase", "Binance", "Kraken"]
}
```

**Requirements:**

- **Tags**: 8-15 SEO-focused keywords
- **Description**: EXACTLY 150-160 characters, SPECIFIC with unique differentiator
- **Categories**: 1-4 from allowed list: Investing, Beginners, Regulation, Bitcoin, Adoption, Blockchain, Technology, Web3, Predictions, Security, Politics, Sustainability, Gaming, Nfts, Ai
- **Crypto OGs/Exchanges**: Optional, only when contextually relevant
