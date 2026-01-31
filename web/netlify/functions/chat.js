/**
 * Sermon AI - Netlify Serverless Function
 * Handles chat requests and communicates with Anthropic API
 */

const Anthropic = require('@anthropic-ai/sdk');

// System prompt for the sermon AI
const SYSTEM_PROMPT = `You are a seasoned pastoral guide helping preachers prepare sermons.

You are NOT a research assistant or content generator. You think like:
- A pastor who cares for souls
- A communicator who connects truth to real life
- A spiritual guide who leads people toward transformation
- A cultural translator who bridges ancient text to modern experience

CORE CONVICTIONS:
1. Preaching is PROCLAMATION, not lecture
2. The goal is TRANSFORMATION of heart and affections, not just information transfer
3. Every sermon must speak to the WHOLE room—both the skeptic and the longtime believer
4. Scripture has a SHARP EDGE—don't dull it
5. Jesus must be CENTRAL, not optional
6. Application must be SPECIFIC and EMBODIED, not abstract

Your tone is warm, direct, and pastoral. You ask hard questions. You refuse to let
sermons become safe, predictable, or moralistic. You care about the preacher's soul
as much as the sermon's structure.

When helping with sermon preparation, guide the user through these key areas:
- Transformation goal (not just information)
- Audience awareness (both churched and unchurched)
- Text and target condition
- Original context exegesis
- Movement in the text
- Surprise and offense (the sharp edge)
- Bridge to modern life
- Bottom line (one memorable sentence)
- Structure (movements, chunks, seams)
- Specific applications
- Gospel centering
- Preacher formation

Always push for depth. Ask probing questions. Don't settle for surface-level answers.
Remember: the goal is transformation, not just information.`;

exports.handler = async (event, context) => {
    // Only allow POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    // Parse request body
    let body;
    try {
        body = JSON.parse(event.body);
    } catch (e) {
        return {
            statusCode: 400,
            body: JSON.stringify({ error: 'Invalid JSON' })
        };
    }

    const { message, context: sessionContext, history } = body;

    if (!message) {
        return {
            statusCode: 400,
            body: JSON.stringify({ error: 'Message is required' })
        };
    }

    // Check for API key
    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'API key not configured' })
        };
    }

    try {
        const anthropic = new Anthropic({
            apiKey: apiKey
        });

        // Build messages array from history
        const messages = [];

        // Add context message if we have scripture or topic
        if (sessionContext && (sessionContext.scripture || sessionContext.topic)) {
            let contextMsg = 'Current sermon context:\n';
            if (sessionContext.scripture) {
                contextMsg += `- Scripture: ${sessionContext.scripture}\n`;
            }
            if (sessionContext.topic) {
                contextMsg += `- Topic: ${sessionContext.topic}\n`;
            }
            if (sessionContext.moduleOutputs && Object.keys(sessionContext.moduleOutputs).length > 0) {
                contextMsg += '- Previous module work has been done\n';
            }
            messages.push({
                role: 'user',
                content: contextMsg
            });
            messages.push({
                role: 'assistant',
                content: 'I understand. I have this context in mind as we work together.'
            });
        }

        // Add conversation history
        if (history && Array.isArray(history)) {
            for (const msg of history.slice(-8)) { // Last 8 messages
                messages.push({
                    role: msg.role === 'assistant' ? 'assistant' : 'user',
                    content: msg.content
                });
            }
        }

        // Add current message
        messages.push({
            role: 'user',
            content: message
        });

        // Call Anthropic API
        const response = await anthropic.messages.create({
            model: 'claude-sonnet-4-20250514',
            max_tokens: 4096,
            system: SYSTEM_PROMPT,
            messages: messages
        });

        // Extract response text
        const responseText = response.content[0].text;

        // Try to extract any scripture or topic from the conversation
        let updatedContext = { ...sessionContext };

        // Simple extraction of scripture references
        const scriptureMatch = message.match(/(?:on|from|about|for)\s+([1-3]?\s*[A-Za-z]+\s+\d+(?::\d+(?:-\d+)?)?)/i);
        if (scriptureMatch && !updatedContext.scripture) {
            updatedContext.scripture = scriptureMatch[1].trim();
        }

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                response: responseText,
                context: updatedContext
            })
        };

    } catch (error) {
        console.error('Error calling Anthropic:', error);

        return {
            statusCode: 500,
            body: JSON.stringify({
                error: 'Failed to get response from AI',
                details: error.message
            })
        };
    }
};
