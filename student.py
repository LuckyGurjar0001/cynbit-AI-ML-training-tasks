import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simple Student Directory")
st.title(" Student Directory")

# Initialize session state with a DataFrame if it doesn't exist
if 'students_df' not in st.session_state:
    st.session_state.students_df = pd.DataFrame(columns=['Name', 'Email', 'Course', 'Score'])

# Add Student Form
with st.form("add_student"):
    st.header("Add New Student")
    
    # Input fields
    name = st.text_input("Name", key="name_input")
    email = st.text_input("Email", key="email_input")
    course = st.selectbox("Course", ["Math", "Science", "History", "English"], key="course_select")
    score = st.slider("Score", 0, 100, 70, key="score_slider")
    
    # Submit button
    submitted = st.form_submit_button("Add Student")
    
    if submitted:
        if name and email:  # Simple validation
            # Create new student as a dictionary
            new_student = {
                'Name': name,
                'Email': email,
                'Course': course,
                'Score': score
            }
            
            # Convert to DataFrame and append to existing data
            new_row = pd.DataFrame([new_student])
            st.session_state.students_df = pd.concat(
                [st.session_state.students_df, new_row], 
                ignore_index=True
            )
            st.success("Student added!")
        else:
            st.warning("Please fill name and email")

# Display and filter students
st.header("Current Students")

if st.session_state.students_df.empty:
    st.info("No students added yet. Use the form above to add some.")
else:
    # Show raw data
    st.subheader("All Students")
    st.dataframe(st.session_state.students_df)
    
    # Simple filters
    st.subheader("Filter Students")
    
    # Filter by course
    selected_course = st.selectbox(
        "Filter by course",
        ["All"] + list(st.session_state.students_df['Course'].unique())
    )
    
    # Filter by minimum score
    min_score = st.slider(
        "Minimum score", 
        min_value=0, 
        max_value=100,
        value=50
    )
    
    # Apply filters
    filtered_df = st.session_state.students_df.copy()
    if selected_course != "All":
        filtered_df = filtered_df[filtered_df['Course'] == selected_course]
    filtered_df = filtered_df[filtered_df['Score'] >= min_score]
    
    # Show filtered results
    st.write(f"Found {len(filtered_df)} students:")
    st.dataframe(filtered_df)
    
    # Show basic stats
    st.subheader("Statistics")
    st.write(f"Total students: {len(st.session_state.students_df)}")
    st.write(f"Average score: {st.session_state.students_df['Score'].mean():.1f}")