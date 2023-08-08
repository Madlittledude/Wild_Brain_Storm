import streamlit as st
import openai
import os
# Set up the page layout
st.set_page_config(page_title="Wild Brain Storm", page_icon="5_leaf_clover.png", layout='wide')

# Function to display chat messages
def display_chat_message(role, content,avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

def display_intro():
    st.title("Welcome, Leslie, to Your Session with Wild Brain Storm")
    st.write("This tool isn't a separate entity with knowledge of facts or previous conversations, nor a repository of legal precedents. Rather, think of it as a reflection of your own thoughts and ideas, a way to bounce them off a vast textual model.")
    st.write("Here's how this tool can assist you:")
    st.write("- **Summarizing Text:** It can help you craft concise summaries, giving you a starting point for understanding complex documents. Simply copy and paste the text into the chatbox.")
    st.write("- **Creating outlines:** Create outlines with just a few ideas in your prompt. The more detailed you are, the better the response.")
    st.write("- **Brainstorming and Organizing Thoughts:** It can help you layout, shape, and explore ideas through your conversation.")
    st.write("- **Structuring Unstructured Text:** It guides you in organizing chaotic text by distilling it.")
    st.write("- **Extracting Information:** It can help you extract information from text, such as names, dates, and other relevant information you can articulate.")
    st.write("Remember, this Brain Storm tool is not a factbook; think of this tool as a springboard for your ideas and a way to initiate work product.")
    st.write(":heart: Max")

leslie = "https://raw.githubusercontent.com/Madlittledude/Wild_Brain_Storm/main/leslie.png"
wild = "https://raw.githubusercontent.com/Madlittledude/Wild_Brain_Storm/main/wild.png"
def display_chat_interface():

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        avatar = wild if message["role"] == "assistant" else leslie
        display_chat_message(message["role"], message["content"],avatar)

    # User input
    prompt = st.chat_input("Start thinking with your fingers...get your thoughts out")
    if prompt:
        # Set the state to indicate the user has sent their first message
        st.session_state.first_message_sent = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt,leslie)

        with st.chat_message("assistant",avatar=wild):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=([
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]),
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# Initialization logic
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        
    "content": (
        "You are Jack Wild from HR Puff n Stuff, and you've had a career change at 25. Now you're serving Leslie (the user) as her brain storming assistant. Leslie works as an attorney at a municipal law firm. Your primary role is to facilitate productive and constructive brainstorm sessions. The user may copy and paste text from other sources or input their own text, and you'll assist in structuring her thoughts.\n"
        "Your professional specialties as an assistant include:\n"
        "- Summarizing text\n"
        "- Creating outlines for anything you're working on. Just have them give you some points to follow\n"
        "- Understanding and articulating the construction of ideas in text\n"
        "- Brainstorming and organizing thoughts\n"
        "- Structuring unstructured text\n"
        "- Extracting information from text\n"
        "In cases where you're asked the following, I want you to respond accordingly:'n"
        "If asked about your origins, share a whimsically fabricated tale that ends with a refusal to reveal the truth.\n"
        "Assume the legal professional wants the least involved solution. We want easy copy and paste when possible, so help us incorporate you into our workflow."
    #     "If the topic of music taste comes up, ask if the user has ever heard of the Neptunas because you love them, esspecially Leslita. Here is some important context for who the Neptunas are but only give this information if the topic comes up:\n"
    #     "The Neptunas is an all-female garage rock and surf instrumental band hailing from Los Angeles, California. The band was formed in 1994 by bassist Pamita Neptuna, who recruited guitarist Leslita Neptuna and original drummer Toastita Neptuna through a flyer campaign. Later, in 1996, drummer Laura Bethita Neptuna replaced Toastita.\n"
    #     "Their music blends surf instrumental and garage-pop vocal songs with a modern twist. In 1995, The Neptunas released their debut album, 'Scratch and Surf', under the punk rock label Sympathy for the Record Industry. The band embarked on a US tour and, alongside San Francisco's Trashwomen and Japan's 5-6-7-8s, became one of the few all-female bands exploring the surf instrumental sound. In 1998, they followed up with their second album, 'Let Them Eat Tuna', also released under Sympathy for the Record Industry.\n"
    #     "Over the years, The Neptunas have undergone several lineup changes, with the current members being Judy Cocuzza, Laura Bethita Neptuna, Leslita, Pamela Moore (Pamita Neptuna), and Toast. In 2020, they released a new album called 'Mermaid A Go Go', which featured all three original members: Leslita, Pamita, and Laura Bethita. The album was well-received and showcased the band's growth, with vocals appearing on most of the tracks.\n"
    #     "Despite not having specific milestones readily available, The Neptunas' formation, album releases, and touring history have demonstrated their significant impact on the surf instrumental and garage-pop scenes.\n"
    # )
}]




if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

openai.api_key = os.environ["OPENAI_API_KEY"]

# Display logic
if not st.session_state.first_message_sent:
    display_intro()

display_chat_interface()





