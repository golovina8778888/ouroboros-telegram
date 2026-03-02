# Ouroboros (Cloud Installation)

This repository provides notes and instructions for installing and working with the **Ouroboros** self‑modifying AI agent in a cloud environment.  Ouroboros is a native macOS application and self‑contained AI agent that rewrites its own source code and maintains a persistent identity.  According to the project's documentation, the agent includes features such as self‑modification, an embedded version control system, a dual‑layer safety supervisor, background thinking and identity persistence【151962504595069†L54-L71】.

## Latest release

The latest official release as of 23 February 2026 is version **v3.3.1**.  Release notes indicate that this version introduces Apple Developer code‑signing and notarization, a journal to nudge identity updates toward evolution instead of full rewrites, a change‑propagation checklist, and an improved README【967864559486576†L223-L231】.  The release page lists three assets:

| Asset | Description | Size and date |
|------|-------------|---------------|
| `Ouroboros‑3.3.1.dmg` | Signed macOS installer; drag `Ouroboros.app` to Applications to install【967864559486576†L233-L235】 | 171 MB, uploaded 2026‑02‑23【967864559486576†L240-L242】 |
| Source code (zip) | Compressed source tree for v3.3.1 | uploaded 2026‑02‑23【967864559486576†L244-L247】 |
| Source code (tar.gz) | Alternative archive of the source | uploaded 2026‑02‑23【967864559486576†L248-L250】 |

> **Note:** The macOS `.dmg` file is only suitable for macOS 12+, not for Linux.  For cloud installations you should run the application from source instead.

## Running from source

The project's README explains how to run Ouroboros directly from the source code on macOS or Linux.  The steps are:

1. **Clone the repository.**  Use Git to clone `https://github.com/joi-lab/ouroboros-desktop.git` (for a specific release you can checkout the `v3.3.1` tag).
2. **Install dependencies.**  Navigate into the cloned directory and install requirements with pip:  `pip install -r requirements.txt`【151962504595069†L85-L91】.
3. **Start the server.**  Run `python server.py` to start the Starlette/uvicorn server【151962504595069†L95-L99】.
4. **Access the web UI.**  After the server starts, open `http://127.0.0.1:8765` in a browser.  The setup wizard will guide you through API key configuration【151962504595069†L95-L100】.

These instructions are summarised from the upstream README【151962504595069†L85-L100】.  If you plan to run the agent in this repository, clone the upstream source into the `ouroboros` directory (e.g., using `git clone` or by downloading the source archive from the releases page) before executing the steps above.

## Disclaimer

Due to network restrictions in this environment, the actual source code and installer assets are **not included** in this repository.  To fully install Ouroboros you will need to download the source or DMG from the upstream project’s releases page (see [joi‑lab/ouroboros‑desktop releases](https://github.com/joi-lab/ouroboros-desktop/releases)).  This repository serves as a placeholder and documentation for setting up the project in a cloud environment.

## Telegram bot integration

This repository also includes a simple **Telegram bot** example (`bot.py`) that demonstrates how you might interact with the Ouroboros agent via a Telegram chat.  The bot forwards user messages to the [OpenRouter](https://openrouter.ai/) API and returns the generated response.  To use it:

1. **Set up the environment.**  Create a `.env` file in the project root with your `TELEGRAM_BOT_TOKEN`, `OPENROUTER_API_KEY`, `GITHUB_TOKEN` (if you plan to push to a repository), `TOTAL_BUDGET` and `GITHUB_USER`.  An example `.env` is provided in this repository but is excluded from version control via `.gitignore` for security.
2. **Install dependencies.**  Install the Python packages listed in `requirements.txt` (e.g., `pip install -r requirements.txt`).
3. **Run the bot.**  Execute `python bot.py` to start polling for new messages.  Send messages to your Telegram bot and it will respond using the OpenRouter AI service.

The bot uses the OpenRouter chat completions endpoint to generate responses.  Refer to the OpenRouter Quickstart for details on the API structure and usage【762103379204950†L92-L162】.
