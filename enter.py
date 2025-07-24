import streamlit as st
import time as t
# title : to give the main heading of our web page
st.title("welcome to cynbit technologies")
# header : give the heading of the page
st.header("traning of AI/ML")
# subheader : give the sub header means in header line
st.subheader("internship")
# warning : give warning if not do
st.warning("if you are not enter in meeting otherwise you leave from cynbit")
# write : write the simple text 
st.write("work with cynbit technologies to gain knowledge")
# write:
st.write(range(48))
#error:
st.error("error in your program")
#infot : to provide any information
st.info("this is information provide in cynbit")
# markdown : to mark your data with # accordint to size ! is bigger than other numbers are smaller
st.markdown("# cynbit technologies")
st.markdown("## cynbit technologies")
st.markdown("### cynbit technologies")
st.markdown(":moon:")
# text : normal message
st.text("works as inter student")
# caption 
st.caption("working in cynbit")
#latex : to write the mathematical expression
st.latex(r''' a+bx+cx^2''')
#widghts
st.checkbox("Login in cybit")
#button
st.button("Click there")
#radio : to chosse the gender 
st.radio("choose your gender",['Male','Female','other'])
# slider
st.select_slider("Rating the course",['bad','good','outstanding','Excellent'])
# slider
st.slider("enter your number " , 0,100)
# number input
st.number_input("chose the number",0,200)
# text_input
st.text_input("enter your name")
st.text_input("enter your email address")
# date_input
st.date_input("enter you date of birth")
# time_input
st.time_input("time are ongoing")
# text_area
st.text_area("welcome to cynbit.hello learners")
# file_uploader
st.file_uploader("upload your file/folder")
# color_picker
st.color_picker("color")
# progress : check your progress
st.progress(90)
# spinner
with st.spinner("just wait a sec"):
   t.sleep(3)
# ballon
st.balloons()
# sidebar
st.sidebar.title("welcome to cynbit techonolgies")
st.checkbox("sign up")
st.sidebar.text_input("enter your name")
st.sidebar.text_input("enter mail address")
st.sidebar.text_input("password")
st.sidebar.button("submit")
st.sidebar.radio("professional working experience",['fresher','experience','other'])

