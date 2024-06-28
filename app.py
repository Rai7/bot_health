import streamlit as st

def main():
    st.sidebar.title("Navigation")
    options = ["Home", "Analyze Image"]
    choice = st.sidebar.radio("Go to", options)
    
    if choice == "Home":
        from home import home
        home()
    elif choice == "Analyze Image":
        from analyze import analyze
        analyze()

if __name__ == "__main__":
    main()
