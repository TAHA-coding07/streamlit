import streamlit as st
import datetime


st.set_page_config(
    page_title="Library Issue Portal",
    page_icon="📚",
    layout="centered"
)


st.title("📚 Library Issue Portal")
st.markdown("Welcome! Please fill out the form below to borrow a book. Fields marked with **\*** are mandatory.")
st.divider() # Creates a clean visual separation line


with st.form("book_issue_form"):
    
    st.subheader("Student & Book Details")
    # Added 'help' parameter for hover tooltips
    student_name = st.text_input("Student Name *", placeholder="e.g., Jane Doe", help="Enter your full registered name.")
    book_title = st.text_input("Book Title *", placeholder="e.g., Introduction to Python", help="Enter the exact title of the book.")
    
    st.write("") # Adds vertical breathing room
    
    st.subheader("Timeline Details")
    col1, col2 = st.columns(2)
    
    with col1:
        issue_date = st.date_input("Issue Date", value=datetime.date.today())
    
    with col2:
        default_return = datetime.date.today() + datetime.timedelta(days=7)
        return_date = st.date_input("Expected Return Date", value=default_return, help="Standard borrowing period is 7 days.")
        
    st.write("") 
    
   
    agree_to_terms = st.checkbox("I agree to return the book in good condition and pay any late fees. *")
    
    
    submitted = st.form_submit_button("Issue Book", type="primary", use_container_width=True)



if submitted:
    # 1. Check for empty fields (strip() removes accidental spacebar presses)
    if not student_name.strip() or not book_title.strip():
        st.error("🚨 Please fill in both your name and the book title.")
        
    # 2. Check for impossible dates
    elif return_date < issue_date:
        st.error("🚨 Invalid Date! The return date cannot be before the issue date.")
        
    # 3. Check for terms agreement
    elif not agree_to_terms:
        st.warning("⚠️ You must agree to the terms and conditions to proceed.")
        
    # 4. Success State
    else:
        st.success(f"✅ Success! **{book_title}** has been issued to **{student_name}**.")
        st.info(f"📅 Your return due date is **{return_date.strftime('%B %d, %Y')}**.")
        st.balloons() 