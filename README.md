
# Pythonic-Schwab-API
This is an unofficial Python wrapper for accessing the Schwab API, designed for developers who require a straightforward and efficient method to interact with financial data and trading operations.

Before you can use this wrapper, ensure you have a Schwab developer account, which you can obtain [here](https://beta-developer.schwab.com/).

For community support and discussions, join our [Discord group](https://discord.gg/m7SSjr9rs9).

## Quick Setup
1. **Create a Schwab Developer App**: Register a new application with a callback URL set to "https://127.0.0.1". Ensure the app status changes to "Ready for use", as "Approved - Pending" status may not function correctly.
2. **Enable Thinkorswim (TOS)**: This is necessary for order placements and other critical API functionalities.
3. **Install Python**: This wrapper requires Python version 3.11 or higher.
4. **Install Dependencies**: Run `pip install requests python-dotenv websockets`.
5. **Configure Environment**: Populate your `.ENV` file with your `APP_KEY` and `APP_SECRET`.
6. **Run the Program**: Start by executing `main.py`.

## Capabilities
- **API Authentication**: Utilizes OAuth for secure access (`api.initialize()`).
- **Comprehensive API Function Coverage**: Includes ready-to-use functions for all API endpoints (`api.perform_request()`).
- **Automatic Token Management**: Handles access token renewals (`api.update_tokens_automatically()`).
- **Real-Time Data Streaming**: Facilitates streaming via websockets (`stream.start_manual()`).
- **Automated Stream Management**: Automates the start and stop of data streams (`stream.start_automatically()`).

## Additional Features (TBD)
- **Refresh Token Automation**: Pending Schwab's API enhancements.
- **Custom Stream Handlers**: Pending implementation for user-defined data handling.

## Usage and Design
This Python client simplifies interactions with the TD/Schwab API by providing a user-friendly, organized, and automated interface. The design focuses on clear structure and maintainability.

### Project Structure
- **`main.py`**: Serves as the entry point of the application, includes usage examples.
- **`.ENV`**: Stores sensitive credentials like the API key and secret.
- **`tokens.json`**: Maintains API tokens and their expiration metadata.

### Modules
- **`api.py`**: Manages API interactions, token lifecycle, and request handling.
- **`stream.py`**: Handles websocket connections for live data feeds.
- **`terminal.py`**: Enhances terminal output with color-coded messages and supports additional terminal operations.

## License (MIT)
This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be responsible for any claim, damages, or other liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.
