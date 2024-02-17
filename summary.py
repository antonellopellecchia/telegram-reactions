import pandas as pd

def main():

    messages_df = pd.read_csv("messages.csv")
    reactions_df = pd.read_csv("reactions.csv")

    def print_chat(chat_df):
        chat = chat_df.chat.iloc[0]
        print("\nChat {}:".format(chat))

        def print_user(user_df):
            user = user_df.user.iloc[0]
            print("\n\tMessages by user {}:\n".format(user))

            for i,message in user_df.iterrows():
                reaction_df = reactions_df[(reactions_df.chat==chat)&(reactions_df.user==user)&(reactions_df.message==message.message)]
                print("\t\tMessage \"{}\" had {} reactions".format(message.text, len(reaction_df)))
                for j,reaction in reaction_df.iterrows():
                    print("\t\t\t{} reacted {}".format(reaction.user, reaction.emoji))

        chat_df.groupby("user").apply(print_user)

    messages_df.groupby("chat").apply(print_chat)

if __name__=="__main__":
    main()
