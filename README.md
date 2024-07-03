# Whatsapp Chat Analyser

A Streamlit app for analyzing WhatsApp chat exports. Upload your chat file to get insights into overall and user-specific activity.
Features include total messages, words, media, and links shared, message timelines, activity maps, user activity rankings, word clouds, and common words and emojis.

## Features

- **Overall Analysis**: Get a summary of the entire chat.
- **User-Specific Analysis**: Select a group member to see their activity.
- **Message Statistics**: Total messages, words, media, and links shared.
- **Timelines**: Line graphs showing message trends over time.
- **Activity Maps**: Bar graphs of active months and days.
- **User Rankings**: Most active users and their activity percentages.
- **Word Cloud**: Visualization of the most common words.
- **Emoji Analysis**: Most frequently used emojis.
- **Many More Features**: Constantly adding more insights and visualizations.


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/RatnapalHacker/whatsapp-chat-analyzer.git
    cd whatsapp-chat-analyzer
    ```

2. Create a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Export your WhatsApp chat:
   - Open WhatsApp and go to the chat you want to analyze.
   - Tap on the chat menu and select "Export Chat".
   - Choose "Without Media" for faster processing.
   - Save the file to your device.

2. Open the app:
   - Follow the installation steps to run the app locally.

3. Upload your chat file:
   - Click on the "Browse files" button and select the exported chat file.

4. View the analysis:
   - Explore overall chat statistics and user-specific insights using the sidebar.

## Live App

You can access the deployed app here [whatsapp chat analyzer](https://wachatanalyzer.streamlit.app/).

## Meta

Ratnapal Shende - [Linkedin](https://in.linkedin.com/in/ratnapalshende) - Ratnapalshende2001@gmail.com

Distributed under the Apache 2.0 license. See ``LICENSE`` for more information.

[https://github.com/RatnapalHacker](https://github.com/RatnapalHacker)
## Contribution

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```

3. Make your changes.
4. Commit your changes:
    ```bash
    git commit -m "Add feature description"
    ```

5. Push to the branch:
    ```bash
    git push origin feature-name
    ```

6. Open a pull request on GitHub.

## Future Enhancements

- **Sentiment Analysis**: Show the overall mood of the chat or individual users.
- **Message Heatmap**: Visualize message frequency by hour and day of the week.
- **Advanced Filtering**: Filter messages by keywords or date ranges.
- **Interaction Network**: Visualize user interactions with a network graph.
- **Data Export**: Export analyzed data to CSV or Excel.
- **Text Summarization**: Summarize chat conversations.
- **User Mentions**: Highlight user mentions.

## License

[Apache License 2.0](LICENSE)
