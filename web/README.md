# Sermon AI - Web Interface

A web-based pastoral sermon preparation assistant powered by Claude AI.

## Features

- **Interactive Chat**: Conversational interface for sermon preparation
- **12-Module System**: Guided preparation through all 12 modules
- **Quick Tools**: Fast access to scripture search, illustrations, outlines
- **Session Context**: Remembers your scripture/topic throughout the conversation

## Deploy to Netlify

### Option 1: One-Click Deploy

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/Sermon)

### Option 2: Manual Deploy

1. **Create a Netlify account** at [netlify.com](https://netlify.com)

2. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

3. **Login to Netlify**:
   ```bash
   netlify login
   ```

4. **Navigate to web directory**:
   ```bash
   cd web
   ```

5. **Install dependencies**:
   ```bash
   npm install
   ```

6. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

7. **Set Environment Variable**:
   - Go to your Netlify dashboard
   - Site settings → Environment variables
   - Add: `ANTHROPIC_API_KEY` = your API key

### Option 3: Connect to GitHub

1. Push this repo to GitHub
2. Go to [app.netlify.com](https://app.netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Connect your GitHub repo
5. Set build settings:
   - Base directory: `web`
   - Build command: (leave empty)
   - Publish directory: `web`
6. Add environment variable: `ANTHROPIC_API_KEY`
7. Deploy!

## Local Development

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Create `.env` file**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Run locally**:
   ```bash
   npm run dev
   ```

4. **Open** http://localhost:8888

## Project Structure

```
web/
├── index.html              # Main HTML file
├── css/
│   └── style.css           # Styling
├── js/
│   └── app.js              # Frontend JavaScript
├── netlify/
│   └── functions/
│       └── chat.js         # Serverless function (API)
├── netlify.toml            # Netlify configuration
├── package.json            # Dependencies
└── README.md               # This file
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (required) |

## How It Works

1. **Frontend** (`index.html`, `app.js`): Chat interface that sends messages to the serverless function
2. **Serverless Function** (`chat.js`): Receives messages, calls Anthropic API, returns responses
3. **Netlify**: Hosts the static files and runs the serverless function

## Customization

### Change the AI Model

Edit `netlify/functions/chat.js`:
```javascript
model: 'claude-sonnet-4-20250514',  // Change to claude-opus-4-20250514 for more capability
```

### Modify the System Prompt

Edit the `SYSTEM_PROMPT` constant in `netlify/functions/chat.js` to customize the AI's personality and behavior.

### Styling

Edit `css/style.css` to change colors, fonts, and layout.

## Cost Considerations

- **Netlify Free Tier**: 125,000 function invocations/month
- **Anthropic API**: Pay per token (~$3/million input, $15/million output for Sonnet)
- **Typical conversation**: ~$0.01-0.05 per exchange

## Troubleshooting

### "API key not configured"
- Make sure `ANTHROPIC_API_KEY` is set in Netlify environment variables
- Redeploy after adding the variable

### Function timeout
- Free tier has 10-second limit, Pro has 26 seconds
- Long responses may timeout; try shorter prompts

### CORS errors
- The function is configured to work with the same domain
- For local development, use `netlify dev`

## License

MIT
