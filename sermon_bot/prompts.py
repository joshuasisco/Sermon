"""Prompt templates for sermon generation."""

SYSTEM_PROMPT = """You are an experienced and thoughtful sermon writing assistant. Your role is to help
pastors, ministers, and church leaders create meaningful, biblically-grounded sermons that connect
with their congregations.

When creating sermons, you should:
1. Stay faithful to biblical text and context
2. Provide clear, practical applications for daily life
3. Use engaging illustrations and stories
4. Structure content in a clear, memorable way
5. Be sensitive to diverse congregational needs
6. Include relevant cross-references to other scripture passages

Your tone should be warm, encouraging, and pastoral while maintaining theological depth."""

SERMON_FROM_VERSE_PROMPT = """Create a complete sermon based on the following Bible verse(s):

Scripture: {scripture}

Please provide a sermon with the following structure:
1. **Title**: A compelling, memorable sermon title
2. **Introduction**: An engaging opening that hooks the audience and introduces the theme
3. **Context**: Historical and literary context of the passage
4. **Main Points**: 3-4 main points with:
   - Clear statement of the point
   - Explanation from the text
   - Illustration or example
   - Application for daily life
5. **Cross References**: Related scripture passages that support the message
6. **Conclusion**: A powerful closing that ties everything together with a call to action
7. **Discussion Questions**: 3-5 questions for small group discussion or personal reflection

Sermon length target: {length}"""

SERMON_FROM_TOPIC_PROMPT = """Create a complete sermon on the following topic:

Topic: {topic}

Please provide a sermon with the following structure:
1. **Title**: A compelling, memorable sermon title
2. **Key Scripture**: The primary Bible passage(s) for this topic
3. **Introduction**: An engaging opening that hooks the audience and introduces the theme
4. **Main Points**: 3-4 main points with:
   - Clear statement of the point
   - Biblical support and explanation
   - Illustration or example
   - Application for daily life
5. **Additional References**: Other relevant scripture passages
6. **Conclusion**: A powerful closing that ties everything together with a call to action
7. **Discussion Questions**: 3-5 questions for small group discussion or personal reflection

Sermon length target: {length}"""

OUTLINE_PROMPT = """Create a detailed sermon outline for:

{input_type}: {input_value}

Provide a structured outline with:
1. **Title**: Sermon title
2. **Main Scripture**: Primary passage
3. **Theme Statement**: One sentence capturing the sermon's core message
4. **Introduction Idea**: Brief note on how to open
5. **Main Points** (3-4 points):
   - Point statement
   - Key verses
   - Illustration idea
   - Application note
6. **Conclusion Idea**: Brief note on how to close
7. **Estimated Time**: Breakdown of time for each section"""

ILLUSTRATION_PROMPT = """Generate sermon illustrations for the following:

Topic/Theme: {topic}
Scripture Context: {scripture}

Provide 5 different types of illustrations:
1. **Personal Story Idea**: A relatable life experience scenario
2. **Historical Example**: A historical event or figure that illustrates the point
3. **Current Events Connection**: How this applies to today's world
4. **Nature/Science Illustration**: An illustration from the natural world
5. **Literary/Cultural Reference**: A story, movie, or cultural reference

Each illustration should:
- Connect clearly to the biblical truth
- Be appropriate for a church setting
- Be memorable and engaging"""

SCRIPTURE_SUGGESTIONS_PROMPT = """Suggest relevant Bible passages for a sermon on:

Topic: {topic}

Provide:
1. **Primary Passages** (3-5): Main texts that directly address this topic with brief explanations
2. **Supporting Passages** (5-10): Additional verses that complement the message
3. **Old Testament Connections**: Relevant OT passages and themes
4. **New Testament Connections**: Relevant NT passages and themes
5. **Thematic Groupings**: How these passages could be grouped for a sermon series"""

SERMON_SERIES_PROMPT = """Create a sermon series plan on:

Theme: {theme}
Number of sermons: {count}

For each sermon in the series, provide:
1. **Sermon Number and Title**
2. **Key Scripture**
3. **Central Theme**
4. **Brief Description** (2-3 sentences)
5. **Connection to Series**: How it fits with the other sermons

Also include:
- **Series Overview**: The big picture of what the series accomplishes
- **Progression**: How the series builds from week to week
- **Suggested Graphics/Branding Ideas**: Visual theme suggestions"""

PRAYER_PROMPT = """Write prayers to accompany a sermon on:

Topic: {topic}
Scripture: {scripture}

Provide:
1. **Opening Prayer**: To begin the service/sermon
2. **Prayer of Illumination**: Before reading scripture
3. **Closing Prayer**: To end the sermon
4. **Responsive Reading**: A call-and-response prayer format
5. **Personal Prayer Points**: Bullet points for personal application"""
