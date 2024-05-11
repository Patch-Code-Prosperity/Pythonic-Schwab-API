<p align="center"><img width="50%" src="https://github.com/Patch-Code-Prosperity/Pythonic-Schwab-API/assets/31261577/a8f48499-fac4-400a-afe1-72f0dadf9631"></p>

# Pythonic-Schwab-API
This is an unofficial Python wrapper for accessing the individual [Schwab API](), designed for developers who require a straightforward and efficient method to interact with financial data and trading operations.

You will need a [Schwab developer account](https://beta-developer.schwab.com/) before you can use this wrapper.

For community support and discussions, join our [Pythonic Schwab API Discord group](https://discord.gg/6XMYKEFr).

## Quick Setup
1. **Create a Schwab Developer App**: Register a new application with a callback URL set to "https://127.0.0.1". Ensure the app status changes to "Ready for use", as "Approved - Pending" status means it has not yet been approved.
2. **Enable Thinkorswim (TOS)**: This is necessary for order placements and other critical API functionalities.
3. **Install Python**: This wrapper requires Python version 3.11 or higher.
4. **Install Dependencies**: Run `pip install -r requirements.txt`.
5. **Configure Environment**: Populate your `.env` file with your `APP_KEY` and `APP_SECRET`.
6. **Run the Program**: Start by executing `main.py`.

## Capabilities
- **API Authentication**: Utilizes OAuth for secure access `schwab-api.initialize()`.
- **Comprehensive API Function Coverage**: Includes ready-to-use functions for all API endpoints `schwab-api.perform_request()`.
- **Automatic Token Management**: Handles access token renewals `schwab-api.update_tokens_automatically()`.
- **Real-Time Data Streaming**: Facilitates streaming via websockets `schwab-api.stream.start_manual()`.
- **Automated Stream Management**: Automates the start and stop of data streams `schwab-api.stream.start_automatically()`.

## Additional Features (TBD)
- **Refresh Token Automation**: Pending Schwab's API enhancements.
- **Custom Stream Handlers**: Pending implementation for user-defined data handling.

## Usage and Design
This Python client simplifies interactions with the Schwab API by providing a user-friendly, organized, and automated interface. The design focuses on clear structure and maintainability.

### Project Structure
- **`main.py`**: Serves as the entry point of the application, and includes usage examples.
- **`.env`**: Stores sensitive credentials like the API key and secret.
- **`tokens.json`**: Maintains API tokens and their expiration metadata.

### Modules
- **`schwab-api.py`**: Manages API interactions, token lifecycle, and request handling.
- **`stream.py`**: Handles web socket connections for live data feeds.
- **`terminal.py`**: Enhances terminal output with color-coded messages and supports additional terminal operations.

## Special Thanks
Credit to [Tyler Bowers](https://github.com/tylerebowers) for inspiring this work. This is a blatant rip-off of his work formatted in a more pythonic way. We started as a fork but felt this would likely end up going in a whole different direction as far as our intended purpose and scope. Thank you, Tyler, for your work. We will continue to steal his work and publish it as our own and hope he does the same if it is ever advantageous for him to return the favor.

## License (MIT)
This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be responsible for any claim, damages, or other liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.
